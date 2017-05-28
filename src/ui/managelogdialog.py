from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog

from database import *
from .ui_py.managelogdialog_ui import *


class HttpTableModel(QAbstractTableModel):
    logData = []

    def __init__(self, s):
        super().__init__()

        with db_session:
            logs = s.http_accesses.select()[:]
            for l in logs:
                self.logData.append(l)

    def columnCount(self, *args, **kwargs):
        return 4

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.logData)

    def headerData(self, p_int, Qt_Orientation, int_role=None):
        headers = ['id', 'Host', 'Method', 'Timestamp']
        if int_role == Qt.DisplayRole and Qt_Orientation == Qt.Horizontal:
            return headers[p_int]

        return QVariant()

    def data(self, QModelIndex, int_role=None):
        # return super().data(QModelIndex, int_role)
        if int_role == Qt.DisplayRole:
            row = QModelIndex.row()
            col = QModelIndex.column()

            if col == 0:
                return self.logData[row].id
            elif col == 1:
                return self.logData[row].host
            elif col == 2:
                return self.logData[row].method
            elif col == 3:
                return str(self.logData[row].timestamp)

    def add_log(self, log_id):
        log = HttpAccess[log_id]
        self.logData.append(log)
        self.layoutChanged.emit()

    def clear(self):
        self.logData = []
        self.layoutChanged.emit()

    def new_select(self, s):
        self.logData = []
        with db_session:
            logs = s.http_accesses.select()[:]
            for l in logs:
                self.logData.append(l)
        self.layoutChanged.emit()



class FtpListModel(QAbstractTableModel):
    logData = []  # type:list[FtpAccess]

    def __init__(self, s):
        super().__init__()
        with db_session:
            logs = s.ftp_accesses.select()[:]
            for l in logs:
                self.logData.append(l)

    def columnCount(self, *args, **kwargs):
        return 5

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.logData)

    def headerData(self, p_int, Qt_Orientation, int_role=None):
        headers = ['id', 'Host', 'Command', 'Command Arg', 'Timestamp']
        if int_role == Qt.DisplayRole and Qt_Orientation == Qt.Horizontal:
            return headers[p_int]

        return QVariant()

    def data(self, QModelIndex, int_role=None):
        # return super().data(QModelIndex, int_role)
        if int_role == Qt.DisplayRole:
            row = QModelIndex.row()
            col = QModelIndex.column()

            if col == 0:
                return self.logData[row].id
            elif col == 1:
                return self.logData[row].host
            elif col == 2:
                action = self.logData[row].action
                if action == 0:
                    return 'USER'
                elif action == 1:
                    return 'RETR'
            elif col == 3:
                return self.logData[row].content
            elif col == 4:
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

    def delete_log(self, index:int):
        del self.logData[index]
        self.layoutChanged.emit()


class LogManageDialog(Ui_WarningHostsDialog, QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        with db_session:
            sessions = SniffSession.select()[:]
            for s in sessions:
                self.comboBox.addItem(str(s.timestamp), s)

        self.httpTableView.hideColumn(0)
        self.ftpTableView.hideColumn(0)

    @pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self, index):
        session = self.comboBox.currentData()

        try:
            self.ftpModel.new_select(session)
            self.httpModel.new_select(session)
            self.ftpTableView.resizeColumnsToContents()
            self.httpTableView.resizeColumnsToContents()
        except AttributeError:
            self.ftpModel = FtpListModel(session)
            self.httpModel = HttpTableModel(session)
            self.ftpTableView.setModel(self.ftpModel)
            self.httpTableView.setModel(self.httpModel)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        index = self.ftpTableView.currentIndex().row()
        self.ftpModel.delete_log(index)
