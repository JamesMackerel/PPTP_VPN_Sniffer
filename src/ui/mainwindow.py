from .mainwindow_ui import Ui_MainWindow
from .ftpListViewModel import *
from .httpTableViewModel import *

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore
from configparser import ConfigParser
import logging
import numpy as np
from collections import deque

from .settingdialog import SettingDialog
from .userinfo import UserInfoWidget
import sniffer
from config import config_file_name

from database import *


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.setWindowState(QtCore.Qt.WindowMaximized)
        self.tabView.setCurrentIndex(0)

        with db_session:
            sessions = SniffSession.select(lambda s:s.current_session==True)[:]
            for s in sessions:
                s.current_session = False

        self.user_login_check_timer = QtCore.QTimer()
        self.user_login_check_timer.timeout.connect(self.sniffer_message_handler)
        self.update_traffic_update_timer = QtCore.QTimer()
        self.update_traffic_update_timer.timeout.connect(self.updateTrafficDiagram)

        config = ConfigParser()
        config.read(config_file_name)
        self.sniffer_process = sniffer.Sniffer(
            config['DEFAULT']['interface'] if 'interface' in config['DEFAULT'] else None)
        self.sniff_started = False

        # traffic diagram data
        self.trafficData = deque(np.zeros(100, dtype='f'), 100)
        self.trafficPlot = self.graphicsView.addPlot()
        self.trafficPlot.setClipToView(True)
        self.trafficPlot.setRange(yRange=[0, 1000])
        # self.trafficPlot.setLimits(yMax=1000)
        self.trafficPlotCurve = self.trafficPlot.plot()
        self.trafficPtr = 0

        self.ftpLogModel = FtpListModel()
        self.ftpTableView.setModel(self.ftpLogModel)
        self.ftpTableView.hideColumn(0)
        self.ftpTableView.resizeColumnsToContents()

        self.httpLogModel = HttpTableModel()
        self.httpTableView.setModel(self.httpLogModel)
        self.httpTableView.hideColumn(0)
        self.ftpTableView.resizeColumnsToContents()

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
            if msg['type'] == 'user_login':
                self.userListWidget.addItem(msg['username'])

            elif msg['type'] == 'user_logout':
                items_to_delete = self.userListWidget.findItems(msg['username'], QtCore.Qt.MatchExactly)
                if len(items_to_delete) > 0:
                    for item in items_to_delete:
                        logging.debug('removing: %s' % item.text())
                        self.userListWidget.takeItem(self.userListWidget.row(item))
            elif msg['type'] == 'ftp_log':
                self.ftpLogModel.add_log(msg['data'])
                # username = User[msg['data']['user']].username
                # self.userInfoWidgets[username].add_ftp(msg['data'])
            elif msg['type'] == 'http_log':
                self.httpLogModel.add_log(msg['data'])
                # username = User[msg['data']['user']].username
                # self.userInfoWidgets[username].add_http(msg['data'])

    def updateTrafficDiagram(self):
        self.trafficData.append(self.sniffer_process.data['traffic_per_second']/1024)
        self.sniffer_process.data["traffic_per_second"] = 0
        self.trafficPlotCurve.setData(np.array(self.trafficData))

    def closeEvent(self, event):
        if self.sniff_started:
            self.sniffer_process.stop()

    # @QtCore.pyqtSlot()
    # def on_userListWidget_itemSelectionChanged(self):
    #     current_item = self.userListWidget.currentItem()
    #
    #     username = current_item.text()
    #     logging.debug('Displaying user: ' + username)
    #     # hide the graphics view and show the associate user's info view
    #     self.graphicsView.hide()
    #     if self.currentShownUserInfoWidget is not None:
    #         self.currentShownUserInfoWidget.hide()
    #     self.userInfoWidgets[username].show()
    #     self.currentShownUserInfoWidget = self.userInfoWidgets[username]

    # @QtCore.pyqtSlot()
    # def on_backPushButton_clicked(self):
    #     self.currentShownUserInfoWidget.hide()
    #     self.currentShownUserInfoWidget = None
    #     self.graphicsView.show()
