from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QColor

from database import *
from .ui_py.managelogdialog_ui import *

from typing import List


class HttpTableModel(QAbstractTableModel):
    headers = ['id', 'User', 'Host', 'URI', 'Method', 'Timestamp']

    def __init__(self, s):
        super().__init__()

        self.logData = []
        with db_session:
            logs = s.http_accesses.select()[:]
            for l in logs:
                self.logData.append(l)

    def columnCount(self, *args, **kwargs):
        return len(self.headers)

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.logData)

    def headerData(self, p_int, Qt_Orientation, int_role=None):
        if int_role == Qt.DisplayRole and Qt_Orientation == Qt.Horizontal:
            return self.headers[p_int]

        return QVariant()

    @db_session
    def data(self, QModelIndex, int_role=None):
        # return super().data(QModelIndex, int_role)
        if int_role == Qt.DisplayRole:
            row = QModelIndex.row()
            col = QModelIndex.column()

            if col == 0:
                return self.logData[row].id
            elif col == 1:
                return User[self.logData[row].user.id].username
            elif col == 2:
                return self.logData[row].host
            elif col == 3:
                return self.logData[row].uri
            elif col == 4:
                return self.logData[row].method
            elif col == 5:
                return str(self.logData[row].timestamp.strftime('%b-%d-%y %H:%M:%S'))

        if int_role == Qt.BackgroundColorRole:
            col = QModelIndex.column()
            if col != 2 and col != 4:
                return

            d = self.logData[QModelIndex.row()]
            warning_hosts = EmailWarning.select()[:]

            for host in warning_hosts:
                if d.host == host.host and d.method == host.method:
                    return QColor(Qt.red)

    def add_log(self, log_id):
        log = HttpAccess[log_id]
        self.logData.append(log)
        self.layoutChanged.emit()

    def clear(self):
        self.logData = []
        self.layoutChanged.emit()

    @db_session
    def new_select(self, s, *args):
        self.logData = []
        if s is None:
            return
        if len(args) == 0:
            logs = s.http_accesses.select()[:]
            for l in logs:
                self.logData.append(l)
        else:
            logs = select(l for l in HttpAccess if l.user == args[0], )
            for l in logs:
                self.logData.append(l)

        self.layoutChanged.emit()

    @db_session
    def delete_log(self, index: int):
        self.beginRemoveRows(QModelIndex(), index, index)

        HttpAccess[self.logData[index].id].delete()
        del self.logData[index]

        self.endRemoveRows()


class FtpListModel(QAbstractTableModel):
    headers = ['id', 'User', 'Host', 'Command', 'Command Arg', 'Timestamp']

    def __init__(self, s):
        super().__init__()
        self.logData = []  # type:list[FtpAccess]
        with db_session:
            logs = s.ftp_accesses.select()[:]
            for l in logs:
                self.logData.append(l)

    def columnCount(self, *args, **kwargs):
        return len(self.headers)

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.logData)

    def headerData(self, p_int, Qt_Orientation, int_role=None):
        if int_role == Qt.DisplayRole and Qt_Orientation == Qt.Horizontal:
            return self.headers[p_int]

        return QVariant()

    @db_session
    def data(self, QModelIndex, int_role=None):
        if int_role == Qt.DisplayRole:
            row = QModelIndex.row()
            col = QModelIndex.column()

            if col == 0:
                return self.logData[row].id
            elif col == 1:
                return User[self.logData[row].user.id].username
            elif col == 2:
                return self.logData[row].host
            elif col == 3:
                action = self.logData[row].action
                if action == 0:
                    return 'USER'
                elif action == 1:
                    return 'RETR'
            elif col == 4:
                return self.logData[row].content
            elif col == 5:
                return str(self.logData[row].timestamp)

    def add_log(self, log_id):
        log = FtpAccess[log_id]
        self.logData.append(log)
        self.layoutChanged.emit()

    def clear(self):
        self.logData = []
        self.layoutChanged.emit()

    def new_select(self, s):
        self.logData = []
        with db_session:
            logs = s.ftp_accesses.select()[:]
            for l in logs:
                self.logData.append(l)
        self.layoutChanged.emit()

    @db_session
    def delete_log(self, index: int):
        # del self.logData[index]
        # self.layoutChanged.emit()
        self.beginRemoveRows(QModelIndex(), index, index)

        FtpAccess[self.logData[index].id].delete()
        del self.logData[index]

        self.endRemoveRows()


class LogManageDialog(Ui_WarningHostsDialog, QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.sessions = []  # type:List[SniffSession]

        with db_session:
            sessions = SniffSession.select()[:]
            for s in sessions:
                self.sessionListWidget.addItem(str(s.timestamp.strftime('%b-%d-%y %H:%M')))
                self.sessions.append(s)
            users = User.select()[:]
            self.userComboBox.addItem("", None)
            for u in users:
                self.userComboBox.addItem(u.username, u)

        self.setWindowState(Qt.WindowMaximized)
        # self.userComboBox.currentIndexChanged.connect(self.on_userComboBox_currentIndexChanged);

    @pyqtSlot(int)
    def on_sessionListWidget_currentRowChanged(self, index: int):
        session = self.sessions[index]

        try:
            self.ftpModel.new_select(session)
            self.httpModel.new_select(session)
            # self.ftpTableView.resizeColumnsToContents()
            # self.httpTableView.resizeColumnsToContents()
        except AttributeError:
            self.ftpModel = FtpListModel(session)
            self.httpModel = HttpTableModel(session)
            self.ftpTableView.setModel(self.ftpModel)
            self.httpTableView.setModel(self.httpModel)

        self.httpTableView.hideColumn(0)
        # self.httpTableView.resizeColumnsToContents()
        self.ftpTableView.hideColumn(0)
        # self.ftpTableView.resizeColumnsToContents()

    @pyqtSlot()
    @db_session
    def on_deleteSessionButton_clicked(self):
        index = self.sessionListWidget.currentIndex().row()
        self.sessionListWidget.takeItem(index)
        session_to_delete = self.sessions[index]
        SniffSession[session_to_delete.id].delete()
        del self.sessions[index]

    @pyqtSlot()
    @db_session
    def on_deleteFtpButton_clicked(self):
        index = self.ftpTableView.currentIndex().row()
        self.ftpTableView.model().delete_log(index)

    @pyqtSlot()
    @db_session
    def on_deleteHttpButton_clicked(self):
        index = self.httpTableView.currentIndex().row()
        self.httpTableView.model().delete_log(index)

    @pyqtSlot(int)
    @db_session
    def on_userComboBox_currentIndexChanged(self, index):
        if self.userComboBox.currentText() == "":
            return
        if self.httpTableView.model() is None or self.ftpTableView.model() is None:
            return
        session = self.sessions[self.sessionListWidget.currentIndex().row()]

        self.httpTableView.model().new_select(session, self.userComboBox.currentData())
