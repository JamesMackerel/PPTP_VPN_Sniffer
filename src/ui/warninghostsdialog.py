from .ui_py.warninghostsdialog_ui import *
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import *
from database import *


class RuleTableModle(QAbstractTableModel):
    def __init__(self):
        super().__init__()

        self.dataList = [] # type:list[EmailWarning]

        with db_session:
            query_result = EmailWarning.select()[:]
            for res in query_result:
                self.dataList.append(res)

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.dataList)

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return 3

    def data(self, QModelIndex, int_role=None):
        if int_role == Qt.DisplayRole:
            row = QModelIndex.row()
            col = QModelIndex.column()
            res = [
                self.dataList[row].id,
                self.dataList[row].host,
                self.dataList[row].method
            ]
            return res[col]
        return QVariant()

    def headerData(self, p_int, Qt_Orientation, int_role=None):
        headers = [
            'id',
            'Host',
            'Method'
        ]
        if int_role==Qt.DisplayRole and Qt_Orientation==Qt.Horizontal:
            return headers[p_int]

        return QVariant()

    @db_session
    def removeRule(self, row:int):
        self.beginRemoveRows(QModelIndex(), row, row)

        EmailWarning[self.dataList[row].id].delete()
        commit()
        del self.dataList[row]

        self.endRemoveRows()

    @db_session
    def addRule(self, rule):
        self.beginInsertRows(QModelIndex(), len(self.dataList)-1, len(self.dataList)-1)

        r = EmailWarning(host=rule['host'], method=rule['method'])
        self.dataList.append(r)

        self.endInsertRows()


class WarningHostsDialog(QDialog, Ui_warningHostDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.tableModel = RuleTableModle()
        self.tableView.setModel(self.tableModel)
        # self.tableView.hideColumn(0)
        self.tableView.resizeColumnsToContents()

    @pyqtSlot()
    def on_addPushButton_clicked(self):
        from .addruledialog import AddRuleDialog
        rule = AddRuleDialog.get_rule()
        if rule is None: return

        self.tableView.model().addRule(rule)

    @pyqtSlot()
    def on_deletePushButton_clicked(self):
        self.tableModel.removeRule(self.tableView.currentIndex().row())