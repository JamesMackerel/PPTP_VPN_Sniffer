# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui_files/managelogdialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WarningHostsDialog(object):
    def setupUi(self, WarningHostsDialog):
        WarningHostsDialog.setObjectName("WarningHostsDialog")
        WarningHostsDialog.resize(1077, 539)
        self.verticalLayout = QtWidgets.QVBoxLayout(WarningHostsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboBox = QtWidgets.QComboBox(WarningHostsDialog)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout.addWidget(self.comboBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ftpTableView = QtWidgets.QTableView(WarningHostsDialog)
        self.ftpTableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.ftpTableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.ftpTableView.setObjectName("ftpTableView")
        self.horizontalLayout.addWidget(self.ftpTableView)
        self.httpTableView = QtWidgets.QTableView(WarningHostsDialog)
        self.httpTableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.httpTableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.httpTableView.setObjectName("httpTableView")
        self.horizontalLayout.addWidget(self.httpTableView)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pushButton = QtWidgets.QPushButton(WarningHostsDialog)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(WarningHostsDialog)
        QtCore.QMetaObject.connectSlotsByName(WarningHostsDialog)

    def retranslateUi(self, WarningHostsDialog):
        _translate = QtCore.QCoreApplication.translate
        WarningHostsDialog.setWindowTitle(_translate("WarningHostsDialog", "Manage Logs"))
        self.pushButton.setText(_translate("WarningHostsDialog", "Delete"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WarningHostsDialog = QtWidgets.QDialog()
    ui = Ui_WarningHostsDialog()
    ui.setupUi(WarningHostsDialog)
    WarningHostsDialog.show()
    sys.exit(app.exec_())

