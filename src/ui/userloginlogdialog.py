from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog

from database import *
from .ui_py.userloginlogdialog_ui import *


class LoginLogModel(QAbstractTableModel):
    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return 3

    def headerData(self, p_int, Qt_Orientation, int_role=None):
        headers = [
            'ID',
            'Timestamp',
            'IP'
        ]
        if int_role == Qt.DisplayRole and Qt_Orientation == Qt.Horizontal:
            return headers[p_int]

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.dataList)

    def data(self, QModelIndex, int_role=None):
        if int_role == Qt.DisplayRole:
            row = QModelIndex.row()
            col = QModelIndex.column()
            d = self.dataList[row]

            if col == 0:
                return d.id
            elif col == 1:
                return str(d.timestamp.strftime('%b-%d-%y %H:%M:%S'))
            elif col == 2:
                return d.ip

        return QVariant()

    def __init__(self, username):
        super().__init__()

        self.dataList = []  # type:list[LoginLog]

        with db_session:
            user = User.get(username=username)
            logs = user.login_logs.select()[:]
            for log in logs:
                self.dataList.append(log)

    @db_session
    def removeLog(self, row):
        self.beginRemoveRows(QModelIndex(), row, row)

        LoginLog[self.dataList[row].id].delete()
        commit()
        del self.dataList[row]

        self.endRemoveRows()


class UserLoginLogDialog(QDialog, Ui_loginLogDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        with db_session:
            users = User.select()[:]
            for u in users:
                self.userListWidget.addItem(u.username)

    @pyqtSlot()
    def on_userListWidget_itemSelectionChanged(self):
        if self.userListWidget.currentItem() is None: # all users has been deleted
            return
        username = self.userListWidget.currentItem().text()
        self.logTableView.setModel(LoginLogModel(username))
        self.logTableView.resizeColumnsToContents()
        self.logTableView.hideColumn(0)

    @pyqtSlot()
    def on_deleteLogPushButton_clicked(self):
        self.logTableView.model().removeLog(self.logTableView.currentIndex().row())

    @pyqtSlot()
    @db_session
    def on_deleteUserPushButton_clicked(self):
        username = self.userListWidget.currentItem().text()
        User.get(username=username).delete()
        self.userListWidget.takeItem(self.userListWidget.currentIndex().row())
        # items_to_delete = self.userListWidget.findItems(username, QtCore.Qt.MatchExactly)
        # if len(items_to_delete) > 0:
        #     for item in items_to_delete:
        #         logging.debug('removing: %s' % item.text())
        #         self.userListWidget.takeItem(self.userListWidget.row(item))
