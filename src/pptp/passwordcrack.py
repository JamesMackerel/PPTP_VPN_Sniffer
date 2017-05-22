import logging

import pyshark


class ChapSessionInfo(object):
    username = b''
    authenticator_challenge = b''
    peer_challenge = b''
    nt_response = b''
    password = None

    @staticmethod
    def find_sessions(capture):
        chap_packets = [p for p in capture if p.highest_layer == "CHAP"]

        logging.info("Searching for users in the traffic...")
        identifiers = [int(p.chap.Identifier) for p in chap_packets]
        identifiers = list(set(identifiers)) # remove duplicate

        sessions = []
        for i in identifiers:
            session = ChapSessionInfo()
            success = False
            for p in chap_packets:
                if int(p.chap.Identifier) != i:
                    continue

                if int(p.chap.Code) == 1: #Challenge
                    session.authenticator_challenge = p.chap.Value.binary_value

                if p.chap.Code.int_value == 2: #Response
                    session.username = p.chap.Name.binary_value
                    session.peer_challenge = p.chap.Value.binary_value[0:16]
                    session.nt_response = p.chap.Value.binary_value[24:48]

                if p.chap.Code.int_value == 3: #Success founded!
                    success = True
            if success:
                logging.info("find user %s" % session.username.decode())
                sessions.append(session)
            else:
                logging.info("ignored user %s who failed logging in" % session.username.decode())

            return sessions


def find_users(capture_file: str):
    capture = pyshark.FileCapture(capture_file)
    users = [str(p.chap.Name) for p in capture if p.highest_layer == "CHAP" and int(p.chap.Code) == 2]
    return tuple(users)

if __name__ == '__main__':
    capture = pyshark.FileCapture('test_data/connect.pcapng')
    sessions = ChapSessionInfo.find_sessions(capture)
    print()
