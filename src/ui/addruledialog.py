from .ui_py.addruledialog_ui import *
from .warninghostsdialog import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class AddRuleDialog(Ui_addRuleDialog, QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    @staticmethod
    def get_rule():
        dialog = AddRuleDialog()
        if dialog.exec_() == QDialog.Accepted:
            host = dialog.hostLineEdit.text()
            method = dialog.methodLineEdit.text()
            return {'host': host, 'method': method}
        return None
