from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant
from database import *


class FtpListModel(QAbstractTableModel):
    logData = []# type:list[FtpAccess]

    def __init__(self, parent=None):
        super().__init__()
        with db_session:
            logs = FtpAccess.select(lambda l:l.sniff_session.current_session==True)[:]
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
