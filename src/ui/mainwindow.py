from collections import deque
from configparser import ConfigParser
import logging

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore
from PyQt5.QtCore import QVariant, Qt
from PyQt5.QtWidgets import QMainWindow

import sniffer
from config import config_file_name
from database import *
from .settingdialog import SettingDialog
from .ui_py.mainwindow_ui import Ui_MainWindow


class FtpListModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        self.logData = []  # type:list[FtpAccess]
        super().__init__()

    def columnCount(self, *args, **kwargs):
        return 6

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.logData)

    def headerData(self, p_int, Qt_Orientation, int_role=None):
        headers = ['id', 'User', 'Host', 'Command', 'Command Arg', 'Timestamp']
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
                return self.logData[row].user.username
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


class HttpTableModel(QtCore.QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.logData = []  # type:list[HttpAccess]

    def columnCount(self, *args, **kwargs):
        return 4

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.logData)

    def headerData(self, p_int, Qt_Orientation, int_role=None):
        headers = ['id', 'User', 'Host', 'Method', 'Timestamp']
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
                return self.logData[row].user.username
            elif col == 2:
                return self.logData[row].host
            elif col == 3:
                return self.logData[row].method
            elif col == 4:
                return str(self.logData[row].timestamp)

    def add_log(self, log_id):
        log = HttpAccess[log_id]
        self.logData.append(log)
        self.layoutChanged.emit()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.setWindowState(QtCore.Qt.WindowMaximized)
        self.tabView.setCurrentIndex(0)

        self.user_login_check_timer = QtCore.QTimer()
        self.user_login_check_timer.timeout.connect(self.sniffer_message_handler)
        self.update_traffic_update_timer = QtCore.QTimer()
        self.update_traffic_update_timer.timeout.connect(self.updateTrafficDiagram)

        config = ConfigParser()
        config.read(config_file_name)
        self.sniffer_process = sniffer.Sniffer(
            config['DEFAULT']['interface'] if 'interface' in config['DEFAULT'] else None)
        self.sniff_started = False

        self.graphicsView.setBackground('w')
        # self.graphicsView.set
        # traffic diagram data
        self.trafficData = deque(np.zeros(100, dtype='f'), 100)
        self.trafficPlot = self.graphicsView.addPlot()
        self.trafficPlot.setLabel('bottom', 'Traffic Diagram')
        self.trafficPlot.setClipToView(True)
        self.trafficPlot.setRange(yRange=[0, 1000])
        self.trafficPlot.setRange(xRange=[0, 60])
        self.trafficPlot.hideButtons()
        # self.trafficPlot.setLimits(yMax=1000)
        self.trafficPlotCurve = self.trafficPlot.plot()
        self.trafficPtr = 0

        pen = pg.mkPen(color=(0, 0, 0), width=1)
        self.trafficPlot.getAxis('bottom').setPen(pen)
        self.trafficPlot.getAxis('left').setLabel(text='KB/s')
        self.trafficPlot.getAxis('left').setPen(pen)

        self.ftpLogModel = FtpListModel()
        self.ftpTableView.setModel(self.ftpLogModel)
        self.ftpTableView.hideColumn(0)
        self.ftpTableView.resizeColumnsToContents()

        self.httpLogModel = HttpTableModel()
        self.httpTableView.setModel(self.httpLogModel)
        self.httpTableView.hideColumn(0)
        self.ftpTableView.resizeColumnsToContents()

        with db_session:
            with db_session:
                sessions = SniffSession.select(lambda s: s.current_session == True)[:]
                for s in sessions:
                    s.current_session = False

    @QtCore.pyqtSlot()
    def on_settingButton_clicked(self):
        settingDialog = SettingDialog()
        settingDialog.exec_()

    @QtCore.pyqtSlot()
    def on_startSnifferButton_clicked(self):
        if self.sniff_started:
            self.sniffer_process.stop()
            self.startSnifferButton.setText("Start Sniffer")
            self.sniff_started = False
            with db_session:
                session = SniffSession.get(current_session=True)
                session.current_session = False
            self.ftpLogModel = FtpListModel()
            self.ftpTableView.setModel(self.ftpLogModel)
            self.httpLogModel = HttpTableModel()
            self.httpTableView.setModel(self.httpLogModel)

            self.user_login_check_timer.stop()
            self.update_traffic_update_timer.stop()
            self.userListWidget.clear()
        else:
            self.sniffer_process.start()
            self.sniff_started = True
            with db_session:
                SniffSession(timestamp=datetime.now(), current_session=True)
            self.startSnifferButton.setText("Stop Sniffer")
            self.user_login_check_timer.start(1000)
            self.update_traffic_update_timer.start(1000)

    @QtCore.pyqtSlot()
    def on_searchLogButton_clicked(self):
        from .managelogdialog import LogManageDialog
        dialog = LogManageDialog()
        dialog.exec_()

    @QtCore.pyqtSlot()
    @db_session
    def sniffer_message_handler(self):
        while not self.sniffer_process.data_queue.empty():
            msg = self.sniffer_process.data_queue.get()
            print(msg)
            try:
                if msg['type'] == 'user_login':
                    self.userListWidget.addItem(msg['user'].name)
                elif msg['type'] == 'user_logout':
                    items_to_delete = self.userListWidget.findItems(msg['user'].name, QtCore.Qt.MatchExactly)
                    if len(items_to_delete) > 0:
                        for item in items_to_delete:
                            logging.debug('removing: %s' % item.text())
                            self.userListWidget.takeItem(self.userListWidget.row(item))

                elif msg['type'] == 'ftp_log':
                    with db_session:
                        log = FtpAccess(host=msg['host'], action=msg['action'], content=msg['content'],
                                        timestamp=msg['timestamp'], sniff_session=SniffSession.get(current_session=True),
                                        user=User[msg['uid']])
                        commit()
                    self.ftpLogModel.add_log(log.id)
                elif msg['type'] == 'http_log':
                    with db_session:
                        log = HttpAccess(host=msg['host'], method=msg['method'], timestamp=msg['timestamp'],
                                         sniff_session=SniffSession.get(current_session=True), user=User[msg['uid']])
                        commit()
                    self.httpLogModel.add_log(log.id)
            except KeyError:
                print(msg)

    @QtCore.pyqtSlot()
    def on_emailWarningButton_clicked(self):
        from .warninghostsdialog import WarningHostsDialog
        WarningHostsDialog().exec_()

    def updateTrafficDiagram(self):
        self.trafficData.append(self.sniffer_process.data['traffic_per_second'] / 1024)
        self.sniffer_process.data["traffic_per_second"] = 0
        self.trafficPlotCurve.setData(np.array(self.trafficData))

    @QtCore.pyqtSlot()
    def on_loginLogPushButton_clicked(self):
        from .userloginlogdialog import UserLoginLogDialog
        UserLoginLogDialog().exec_()

    def closeEvent(self, event):
        if self.sniff_started:
            self.sniffer_process.stop()
            self.sniffer_process.worker.join()
