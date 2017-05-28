from datetime import datetime
from multiprocessing import Process, Queue, Manager, Value

import pyshark

from database import *
import logging
import threading
from typing import List, Dict, Tuple


class LogInUser:
    def __init__(self, call_id, identifier, name, ip):
        self.name = name
        self.call_id = call_id
        self.identifier = identifier
        self.status = 0
        self.ip = ip
        self.local_ip = None
        self.capture_session = None  # type:UserSniffer
        self.server_call_id = None


class PacketParser:
    @staticmethod
    def parse(p):
        supported_protocol = ['HTTP']
        if str(p.highest_layer) not in supported_protocol:
            return None

        res = {}

        if str(p.highest_layer) == 'HTTP':
            if 'request_method' in p.http.field_names:
                try:
                    host = str(p.http.host)
                    time_now = datetime.now()
                    method = str(p.http.request_method)

                    res['type'] = 'http_log'
                    res['host'] = host
                    res['timestamp'] = time_now
                    res['method'] = method
                    return res
                except AttributeError:
                    print(p)

        if 'FTP' in p.highest_layer:
            try:
                if 'request_command' in p.ftp.field_names:
                    host = str(p.ip.dst)
                    if str(p.ftp.request_command) == 'USER':  # this is a login request
                        action = 0
                        content = str(p.ftp.request_arg)
                    if str(p.ftp.request_command) == 'RETR':
                        action = 1
                        content = str(p.ftp.request_arg)

                    res['type'] = 'ftp_log'
                    res['host'] = host
                    res['action'] = action
                    res['content'] = content
                    res['timestamp'] = datetime.now()
                    return res

            except AttributeError:
                logging.info('skip ftp data packets')
                return


class UserSniffer(threading.Thread):
    def __init__(self, user: LogInUser, data_queue: Queue):
        super().__init__()
        self.user = user
        with db_session:
            self.user_id = User.get(username=self.user.name).id
        from utils import get_net_interfaces
        interfaces = get_net_interfaces()
        for i in interfaces:
            if i[1] == user.local_ip:
                self.interface = i[0]
                user.capture_session = self

        self.q = data_queue
        self.exit_flag = False

    def run(self):
        self.do_sniff()

    def do_sniff(self):
        from configparser import ConfigParser
        config = ConfigParser()
        config.read('config.ini')
        interface = config['DEFAULT']['interface']
        cap = pyshark.LiveRingCapture(interface=interface, bpf_filter='not udp and ip')
        for p in cap:
            res = PacketParser.parse(p)
            # if there is a parse result, put it into the queue with it's user id
            if res is not None:
                res['uid'] = self.user_id
                self.q.put(res)
                print('in :' + str(res))
            if self.exit_flag:
                return


class PptpUserLogger(object):
    def __init__(self):
        self.log_in_user = []
        self.user_login_handler = []
        self.user_logout_handler = []
        self.users = {}  # type:Dict[str, LogInUser]

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
                logging.info("%s's server_call_id is %d" % (user.name, user.server_call_id))

                # for f in self.user_login_handler:
                #     f(user)

        elif packet.highest_layer == "IPCP":
            if packet.ipcp.ppp_code.hex_value == 2:  # it's a config ack! S->C
                # find our user and populate its ip address!
                try:
                    user = [u for u in self.log_in_user if u.server_call_id == packet.gre.key_call_id.hex_value][0]
                except IndexError:
                    return

                user.local_ip = str(packet.ipcp.opt_ip_address)
                self.users[str(packet.ipcp.opt_ip_address)] = user
                logging.info("%s's local ip is %s" % (user.name, user.local_ip))
                for f in self.user_login_handler:
                    f(user)

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
                    f(user)

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
        self.exit_flag = Value('B')
        self.exit_flag.value = False

        self.user_manager = PptpUserLogger()
        self.user_manager.add_user_logged_in_handler(self.send_user_login)
        self.user_manager.add_user_logged_out_handler(self.send_user_logout)
        self.user_manager.add_user_logged_in_handler(self.sniff_user)
        self.user_manager.add_user_logged_out_handler(self.stop_sniff_user)

    def start(self):
        self.data['total_traffic'] = 0
        self.data['traffic_per_second'] = 0
        self.worker = Process(target=self.do_sniff, args=(self.data_queue, self.data, self.exit_flag,))
        self.worker.start()

    def stop(self):
        self.worker.terminate()
        # self.exit_flag = True

    def do_sniff(self, data_queue, data: dict, exit_flag: Value):
        capture = pyshark.LiveRingCapture(interface=self.interface, bpf_filter='ip and not udp')
        for p in capture:
            self.do_parse(p)
            self.data['total_traffic'] += p.length.hex_value
            self.data['traffic_per_second'] += p.length.hex_value
            if exit_flag.value:
                print('exit')
                print(self.user_manager.users)
                return

    def do_parse(self, packet):
        if 'UDP' in str(packet.layers):
            return

        # if this packet is a MSCHAPV2 Response
        if packet.highest_layer == "CHAP" or packet.highest_layer == "IPCP" or packet.highest_layer == "LCP":
            self.user_manager.process(packet)
            return

    def send_user_login(self, user: LogInUser):
        self.data_queue.put({'type': 'user_login', 'user': user})
        # write to database
        with db_session:
            user_logged_in = User.get(username=user.name)
            if user_logged_in is None:
                user_logged_in = User(username=user.name)
                commit()
            LoginLog(timestamp=datetime.now(), user=user_logged_in, ip=user.ip,
                     sniff_session=SniffSession.get(current_session=True))

    def send_user_logout(self, user: LogInUser):
        self.data_queue.put({'type': 'user_logout', 'user': user})

    def sniff_user(self, user: LogInUser):
        sniffer = UserSniffer(user, self.data_queue)
        sniffer.start()

    @staticmethod
    def stop_sniff_user(user: LogInUser):
        user.capture_session.exit_flag = True
