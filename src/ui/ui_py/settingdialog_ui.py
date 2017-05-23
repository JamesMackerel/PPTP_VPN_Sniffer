# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui_files/settingdialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SettingDialog(object):
    def setupUi(self, SettingDialog):
        SettingDialog.setObjectName("SettingDialog")
        SettingDialog.resize(929, 545)
        self.verticalLayout = QtWidgets.QVBoxLayout(SettingDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setObjectName("formLayout_3")
        self.label = QtWidgets.QLabel(SettingDialog)
        self.label.setObjectName("label")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.interfaceComboBox = QtWidgets.QComboBox(SettingDialog)
        self.interfaceComboBox.setObjectName("interfaceComboBox")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.interfaceComboBox)
        self.verticalLayout_2.addLayout(self.formLayout_3)
        self.groupBox = QtWidgets.QGroupBox(SettingDialog)
        self.groupBox.setObjectName("groupBox")
        self.formLayout_4 = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.emailAddress = QtWidgets.QLineEdit(self.groupBox)
        self.emailAddress.setWhatsThis("")
        self.emailAddress.setObjectName("emailAddress")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.emailAddress)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.emailAccount = QtWidgets.QLineEdit(self.groupBox)
        self.emailAccount.setObjectName("emailAccount")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.emailAccount)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.emailPassword = QtWidgets.QLineEdit(self.groupBox)
        self.emailPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.emailPassword.setObjectName("emailPassword")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.emailPassword)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.popServer = QtWidgets.QLineEdit(self.groupBox)
        self.popServer.setObjectName("popServer")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.popServer)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.formLayout_4.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.smtpServer = QtWidgets.QLineEdit(self.groupBox)
        self.smtpServer.setObjectName("smtpServer")
        self.formLayout_4.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.smtpServer)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.formLayout_4.setItem(5, QtWidgets.QFormLayout.LabelRole, spacerItem)
        self.useSsl = QtWidgets.QCheckBox(self.groupBox)
        self.useSsl.setObjectName("useSsl")
        self.formLayout_4.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.useSsl)
        self.verticalLayout_2.addWidget(self.groupBox)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(SettingDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SettingDialog)
        self.buttonBox.accepted.connect(SettingDialog.accept)
        self.buttonBox.rejected.connect(SettingDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingDialog)

    def retranslateUi(self, SettingDialog):
        _translate = QtCore.QCoreApplication.translate
        SettingDialog.setWindowTitle(_translate("SettingDialog", "Settings"))
        self.label.setText(_translate("SettingDialog", "Interface:"))
        self.groupBox.setTitle(_translate("SettingDialog", "Email Infomation"))
        self.label_2.setText(_translate("SettingDialog", "Email:"))
        self.emailAddress.setToolTip(_translate("SettingDialog", "Email to receive information."))
        self.label_6.setText(_translate("SettingDialog", "Email Account:"))
        self.label_3.setText(_translate("SettingDialog", "Email Password:"))
        self.label_4.setText(_translate("SettingDialog", "POP Server:"))
        self.popServer.setToolTip(_translate("SettingDialog", "server_domain:port"))
        self.label_5.setText(_translate("SettingDialog", "SMTP Server:"))
        self.smtpServer.setToolTip(_translate("SettingDialog", "server_domain:port"))
        self.useSsl.setText(_translate("SettingDialog", "Use SSL"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SettingDialog = QtWidgets.QDialog()
    ui = Ui_SettingDialog()
    ui.setupUi(SettingDialog)
    SettingDialog.show()
    sys.exit(app.exec_())

