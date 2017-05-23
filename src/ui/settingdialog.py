from .ui_py.settingdialog_ui import Ui_SettingDialog

from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot
from configparser import ConfigParser

from utils import get_net_interfaces


class SettingDialog(QDialog, Ui_SettingDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.label_4.hide();
        self.popServer.hide();
        self.useSsl.hide();

        config = ConfigParser()
        config.read('config.ini')

        # populate the interface selection
        interfaces = get_net_interfaces()
        for i in interfaces:
            self.interfaceComboBox.addItem("name:" + i[0] + '  addr:' + i[1] + '  netmask:' + i[2], i[0])

        # set interface selection
        defaultInterfaceIndex = self.interfaceComboBox.findData(
            config['DEFAULT']['interface']) if 'interface' in config['DEFAULT'] else -1
        if defaultInterfaceIndex != -1:
            self.interfaceComboBox.setCurrentIndex(defaultInterfaceIndex)

        # set email texts
        if 'email' in config:
            email = config['email']
            self.emailAddress.setText(email['address'])
            self.emailAccount.setText(email['account'])
            self.emailPassword.setText(email['password'])
            self.popServer.setText(email['pop'])
            self.smtpServer.setText(email['smtp'])
            if 'ssl' in email:
                self.useSsl.setChecked(bool(email['ssl']));

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        config = ConfigParser()
        config['DEFAULT']['interface'] = self.interfaceComboBox.currentData()

        config['email'] = {
            'address': self.emailAddress.text(),
            'account': self.emailAccount.text(),
            'password': self.emailPassword.text(),
            'pop': self.popServer.text(),
            'smtp': self.smtpServer.text(),
            'ssl': self.useSsl.isChecked()
        }

        with open('config.ini', 'w') as config_file:
            config.write(config_file)
