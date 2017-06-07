import smtplib
import requests
import configparser
import logging
from database import *
from typing import *
from datetime import datetime
from email.mime.text import MIMEText
from PyQt5.QtCore import QTimer
from utils import  RepeatTimer


class EmailSender:
    _instance = None  # type: EmailSender

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.email_config = config['email']
        self.warning_list = {}  # type: Dict[str, str]

        # set email warning pool
        self.warning_pool = {}  # type: Dict[str, datetime]

        with db_session:
            warning_items = EmailWarning.select()[:]
            for w in warning_items:
                self.warning_list[w.host] = w.method

        # self.timer = QTimer()
        # self.timer.timeout.connect(self.clean_warning_pool)
        # self.timer.start(5)
        self.timer = RepeatTimer(self.clean_warning_pool, 5)
        self.timer.setDaemon(True)
        self.timer.start()

    def send(self, content):
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['subject'] = 'message from VPN server'
        # msg['from'] = self.email_config['account']
        msg['to'] = self.email_config['address']
        msg['from'] = self.email_config['account']

        print(self.email_config['password'])

        email_sender = smtplib.SMTP()
        email_sender.connect(self.email_config['smtp'], 587)
        email_sender.starttls()
        email_sender.login(self.email_config['account'], self.email_config['password'])
        email_sender.sendmail(self.email_config['account'], [self.email_config['address']], msg.as_string())
        email_sender.close()

        # res = requests.post(
        #     "https://api.mailgun.net/v3/spade.world/messages",
        #     auth=("api", "key-e6bc7da23e355f40265cf97dd8fed44a"),
        #     data={"from": "VPN test <postmaster@spade.world>",
        #           "to": self.email_config['address'],
        #           "subject": "A dangerous host is visited.",
        #           "text": content})
        #
        # print(res)
        # print(res.text)

    def process(self, msg: Dict):
        try:
            if msg['type'] != 'http_log':
                return
        except KeyError:
            # is not a msg
            return

        # a email has been sent recently
        if msg['host'] in self.warning_pool.keys():
            return

        try:
            if self.warning_list[msg['host']] == msg['method']:
                logging.info('sending email.')

                username = User[msg['uid']].username
                self.send(username + ' sent request to host which you consider dangerous. \nHost: ' + msg[
                    'host'] + '\n Method: ' + msg['method'] + '\n Timestamp:'+ str(msg['timestamp']))
                self.warning_pool[msg['host']] = datetime.now()
        except KeyError:
            # host does not exist in dangerous list
            return

    def clean_warning_pool(self):
        now = datetime.now()
        # remove those hosts which has now been accessed in 30 seconds
        self.warning_pool = dict(filter(lambda x: (now - x[1]).seconds > 30, self.warning_pool.items()))

    def __del__(self):
        print('stop')
        self.timer.stop()


if __name__ == '__main__':
    import os
    os.chdir('../')
    sender = EmailSender()
    sender.send('hello world')
    del sender
