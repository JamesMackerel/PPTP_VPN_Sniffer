from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant
from database import *
import logging


class HttpTableModel(QAbstractTableModel):
    logData = None

    def __init__(self):
        super().__init__()

        with db_session:
            self.logData = HttpAccess.select(lambda l: l.sniff_session.current_session == True)[:]

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

