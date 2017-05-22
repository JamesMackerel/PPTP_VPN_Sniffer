from .userinfo_ui import Ui_userInfoWidget

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget
from database import *


class UserInfoWidget(Ui_userInfoWidget, QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setupUi(self)

        self.usernameLabel.setText(username)

        with db_session:
            # get last log in log
            try:
                loginlog = User.get(username=username).login_logs.order_by(lambda l:desc(l.timestamp))[:][1]
            except IndexError:
                self.lastLoginLabel.setText('No record')
            else:
                self.lastLoginLabel.setText(str(loginlog.timestamp))

    def add_http(self, log: dict):
        print(log)

    def add_ftp(self, log:dict):
        print(log)
