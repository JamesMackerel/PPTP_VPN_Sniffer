from multiprocessing import Process, Queue, Manager
import pyshark
import logging
from database import *
from pony.orm.serialization import to_dict
from datetime import datetime


class LogInUser:
    def __init__(self, call_id, identifier, name, ip):
        self.name = name
        self.call_id = call_id
        self.identifier = identifier
        self.status = 0
        self.ip = ip


class PptpUserLogger(object):
    def __init__(self):
        self.log_in_user = []
        self.user_login_handler = []
        self.user_logout_handler = []
        self.users = {}

    def process(self, packet):
        if packet.highest_layer == "CHAP":
            if packet.chap.Code.hex_value == 2:  # client response, remember the user C->S
                print(packet.chap.field_names)
                self.log_in_user.append(
                    LogInUser(packet.gre.key_call_id.hex_value, packet.chap.identifier.hex_value,
                              str(packet.chap.name), str(packet.ip.src)))
                logging.info(str(packet.chap.name) + ' tried to log in.')
            elif packet.chap.Code.hex_value == 3:  # log in succeed, change the one's status to Success(1) S->C
                user = [u for u in self.log_in_user if u.identifier == packet.chap.identifier.hex_value][0]
                user.status = 1
                user.server_call_id = packet.gre.key_call_id.hex_value
                logging.info(user.name + '  logged in successfully.')
                # user.ip = str(packet.ip.src)
                self.users[user.ip] = user
                logging.info("%s's ip is %s" % (user.name, user.ip))

                for f in self.user_login_handler:
                    f(user.name)

        # elif packet.highest_layer == "IPCP":
        #     if packet.ipcp.ppp_code.hex_value == 2:  # it's a config ack! S->C
        #         # find our user and populate its ip address!
        #         try:
        #             user = [u for u in self.log_in_user if u.server_call_id == packet.gre.key_call_id.hex_value][0]
        #         except IndexError:
        #             return
        #
        #         user.ip = str(packet.ipcp.opt_ip_address)
        #         self.users[str(packet.ipcp.opt_ip_address)] = user
        #         user.status = 2
        #         logging.info("%s's ip is %s" % (user.name, user.ip))
        #         for f in self.user_login_handler:
        #             f(user.name)
        elif packet.highest_layer == "LCP":
            if packet.lcp.ppp_code.hex_value == 6:  # user terminates the data S->C
                try:
                    user = [u for u in self.log_in_user if u.server_call_id == packet.gre.key_call_id.hex_value][0]
                except IndexError:
                    return
                username = user.name
                self.log_in_user.remove(user)
                del self.users[str(user.ip)]
                logging.info("%s disconnected" % user.name)
                for f in self.user_logout_handler:
                    f(username)

    def add_user_logged_in_handler(self, handler):
        self.user_login_handler.append(handler)

    def add_user_logged_out_handler(self, handler):
        self.user_logout_handler.append(handler)


class Sniffer(object):
    def __init__(self, interface: str):
        self.interface = interface
        self.data_queue = Queue()
        manager = Manager()
        self.data = manager.dict()

        self.user_manager = PptpUserLogger()
        self.user_manager.add_user_logged_in_handler(self.send_user_login)
        self.user_manager.add_user_logged_out_handler(self.send_user_logout)

    def start(self):
        self.data['total_traffic'] = 0
        self.data['traffic_per_second'] = 0
        self.worker = Process(target=self.do_sniff, args=(self.data_queue, self.data,))
        self.worker.start()

    def stop(self):
        self.worker.terminate()

    def do_sniff(self, data_queue, data: dict):
        capture = pyshark.LiveCapture(self.interface)
        for p in capture:
            self.do_parse(p)
            self.data['total_traffic'] += p.length.hex_value
            self.data['traffic_per_second'] += p.length.hex_value

    def do_parse(self, packet):
        # if 'HTTP' in str(packet.layers):
        #     if 'host' in packet.http.field_names:
        #         if 'www.freebuf.com' in str(packet.http.host):
        #             print('hello')

        if "IPV6" in str(packet.layers):
            return

        if 'UDP' in str(packet.layers):
            return

        # if this packet is a MSCHAPV2 Response
        if packet.highest_layer == "CHAP" or packet.highest_layer == "IPCP" or packet.highest_layer == "LCP":
            self.user_manager.process(packet)
            return

        if str(packet.highest_layer) == 'HTTP':
            if 'request_method' in packet.http.field_names:
                try:
                    host = str(packet.http.host)
                    time_now = datetime.now()
                    method = str(packet.http.request_method)
                    with db_session:
                        session = SniffSession.get(current_session=True)
                        log = HttpAccess(host=host, timestamp=time_now, method=method, sniff_session=session)
                        commit()
                        self.data_queue.put({'type': 'http_log', 'data': log.id})
                    return
                except AttributeError:
                    print(packet)

        if 'FTP' in packet.highest_layer:
            try:
                if 'request_command' in packet.ftp.field_names:
                    host = str(packet.ip.dst)
                    if str(packet.ftp.request_command) == 'USER':  # this is a login request
                        action = 0
                        content = str(packet.ftp.request_arg)
                        with db_session:
                            session = SniffSession.get(current_session=True)
                            log = FtpAccess(host=host, action=action, content=content,
                                            timestamp=datetime.now(), sniff_session=session)
                            commit()
                            self.data_queue.put({'type': 'ftp_log', 'data': log.id})
                        return
                    if str(packet.ftp.request_command) == 'RETR':
                        action = 1
                        content = str(packet.ftp.request_arg)
                        with db_session:
                            session = SniffSession.get(current_session=True)
                            log = FtpAccess(host=host, action=action, content=content,
                                            timestamp=datetime.now(), sniff_session=session)
                            commit()
                            self.data_queue.put({'type': 'ftp_log', 'data': log.id})
                        return
            except AttributeError:
                logging.info('skip ftp data packets')
                return

    def send_user_login(self, user: str):
        self.data_queue.put({'type': 'user_login', 'username': user})
        # write to database
        with db_session:
            user_logged_in = User.get(username=user)
            if user_logged_in is None:
                user_logged_in = User(username=user)
                commit()
            LoginLog(timestamp=datetime.now(), user=user_logged_in)

    def send_user_logout(self, user: str):
        self.data_queue.put({'type': 'user_logout', 'username': user})
