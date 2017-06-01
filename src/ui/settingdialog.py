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

        if 'i18n' in config['DEFAULT']:
            self.i18nComboBox.setCurrentIndex(self.i18nComboBox.findText(config['DEFAULT']['i18n']))
        else:
            self.i18nComboBox.setCurrentIndex(0)

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

        self.i18nChanged = False

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        config = ConfigParser()
        config['DEFAULT']['interface'] = self.interfaceComboBox.currentData()
        config['DEFAULT']['i18n'] = self.i18nComboBox.currentText()

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

        if self.i18nChanged:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(self, self.tr('i18n Changed'), self.tr(
                'Please restart the application to apply the internationalization setting.'), QMessageBox.Ok)

    @pyqtSlot(int)
    def on_i18nComboBox_currentIndexChanged(self, index: int):
        self.i18nChanged = True
