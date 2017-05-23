# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui_files/userinfo.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_userInfoWidget(object):
    def setupUi(self, userInfoWidget):
        userInfoWidget.setObjectName("userInfoWidget")
        userInfoWidget.resize(610, 408)
        self.gridLayout_2 = QtWidgets.QGridLayout(userInfoWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(userInfoWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(userInfoWidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.lastLoginLabel = QtWidgets.QLabel(self.groupBox)
        self.lastLoginLabel.setObjectName("lastLoginLabel")
        self.gridLayout.addWidget(self.lastLoginLabel, 1, 1, 1, 1)
        self.trafficLabel = QtWidgets.QLabel(self.groupBox)
        self.trafficLabel.setObjectName("trafficLabel")
        self.gridLayout.addWidget(self.trafficLabel, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.usernameLabel = QtWidgets.QLabel(self.groupBox)
        self.usernameLabel.setObjectName("usernameLabel")
        self.gridLayout.addWidget(self.usernameLabel, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 1, 0, 1, 1)
        self.httpListWidget = QtWidgets.QListWidget(userInfoWidget)
        self.httpListWidget.setObjectName("httpListWidget")
        self.gridLayout_2.addWidget(self.httpListWidget, 1, 1, 3, 1)
        self.label_3 = QtWidgets.QLabel(userInfoWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.ftpListWidget = QtWidgets.QListWidget(userInfoWidget)
        self.ftpListWidget.setObjectName("ftpListWidget")
        self.gridLayout_2.addWidget(self.ftpListWidget, 3, 0, 1, 1)

        self.retranslateUi(userInfoWidget)
        QtCore.QMetaObject.connectSlotsByName(userInfoWidget)

    def retranslateUi(self, userInfoWidget):
        _translate = QtCore.QCoreApplication.translate
        userInfoWidget.setWindowTitle(_translate("userInfoWidget", "Form"))
        self.label_2.setText(_translate("userInfoWidget", "HTTP log:"))
        self.groupBox.setTitle(_translate("userInfoWidget", "User Info"))
        self.label_4.setText(_translate("userInfoWidget", "Last login:"))
        self.label_5.setText(_translate("userInfoWidget", "Traffic:"))
        self.lastLoginLabel.setText(_translate("userInfoWidget", "TextLabel"))
        self.trafficLabel.setText(_translate("userInfoWidget", "TextLabel"))
        self.label.setText(_translate("userInfoWidget", "Username:"))
        self.usernameLabel.setText(_translate("userInfoWidget", "TextLabel"))
        self.label_3.setText(_translate("userInfoWidget", "FTP log:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    userInfoWidget = QtWidgets.QWidget()
    ui = Ui_userInfoWidget()
    ui.setupUi(userInfoWidget)
    userInfoWidget.show()
    sys.exit(app.exec_())

