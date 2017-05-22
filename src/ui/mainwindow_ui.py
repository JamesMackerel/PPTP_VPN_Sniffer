# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(990, 618)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.emailWarningButton = QtWidgets.QPushButton(self.centralWidget)
        self.emailWarningButton.setObjectName("emailWarningButton")
        self.horizontalLayout.addWidget(self.emailWarningButton)
        self.searchLogButton = QtWidgets.QPushButton(self.centralWidget)
        self.searchLogButton.setObjectName("searchLogButton")
        self.horizontalLayout.addWidget(self.searchLogButton)
        self.settingButton = QtWidgets.QPushButton(self.centralWidget)
        self.settingButton.setObjectName("settingButton")
        self.horizontalLayout.addWidget(self.settingButton, 0, QtCore.Qt.AlignRight)
        self.startSnifferButton = QtWidgets.QPushButton(self.centralWidget)
        self.startSnifferButton.setObjectName("startSnifferButton")
        self.horizontalLayout.addWidget(self.startSnifferButton, 0, QtCore.Qt.AlignRight)
        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.tabView = QtWidgets.QTabWidget(self.centralWidget)
        self.tabView.setObjectName("tabView")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.graphicsView = GraphicsLayoutWidget(self.tab)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout_3.addWidget(self.graphicsView)
        self.userListWidget = QtWidgets.QListWidget(self.tab)
        self.userListWidget.setMaximumSize(QtCore.QSize(200, 16777215))
        self.userListWidget.setObjectName("userListWidget")
        self.horizontalLayout_3.addWidget(self.userListWidget)
        self.tabView.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab_2)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ftpTableView = QtWidgets.QTableView(self.tab_2)
        self.ftpTableView.setObjectName("ftpTableView")
        self.horizontalLayout_2.addWidget(self.ftpTableView)
        self.tabView.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.tab_3)
        self.horizontalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.httpTableView = QtWidgets.QTableView(self.tab_3)
        self.httpTableView.setObjectName("httpTableView")
        self.horizontalLayout_4.addWidget(self.httpTableView)
        self.tabView.addTab(self.tab_3, "")
        self.gridLayout_2.addWidget(self.tabView, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        self.tabView.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "VPN Data Sniffer"))
        self.emailWarningButton.setText(_translate("MainWindow", "Email warning"))
        self.searchLogButton.setText(_translate("MainWindow", "Manage Log"))
        self.settingButton.setText(_translate("MainWindow", "Setting"))
        self.startSnifferButton.setText(_translate("MainWindow", "Start Sniffing"))
        self.tabView.setTabText(self.tabView.indexOf(self.tab), _translate("MainWindow", "Statistics"))
        self.tabView.setTabText(self.tabView.indexOf(self.tab_2), _translate("MainWindow", "FTP Log"))
        self.tabView.setTabText(self.tabView.indexOf(self.tab_3), _translate("MainWindow", "HTTP Log"))

from pyqtgraph import GraphicsLayoutWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

