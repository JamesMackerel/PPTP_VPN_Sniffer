import smtplib
import configparser
from email.mime.text import MIMEText


class EmailSender:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('../config.ini')
        self.email_config = config['email']

    def send(self, content):
        msg = MIMEText(content, 'html')
        msg['subject'] = 'message from VPN server'
        msg['from'] = self.email_config['account']
        msg['to'] = self.email_config['address']

        sender = smtplib.SMTP(self.email_config['smtp'], 25)
        sender.login(self.email_config['account'], self.email_config['password'])
        sender.sendmail(self.email_config['account'], self.email_config['address'], msg.as_string())

if __name__=='__main__':
    sender = EmailSender()
    sender.send('hellow')