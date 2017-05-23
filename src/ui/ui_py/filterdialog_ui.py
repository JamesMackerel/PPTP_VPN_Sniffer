# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui_files/filterdialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FilterDialog(object):
    def setupUi(self, FilterDialog):
        FilterDialog.setObjectName("FilterDialog")
        FilterDialog.resize(734, 452)
        self.verticalLayout = QtWidgets.QVBoxLayout(FilterDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addFilterButton = QtWidgets.QPushButton(FilterDialog)
        self.addFilterButton.setObjectName("addFilterButton")
        self.horizontalLayout.addWidget(self.addFilterButton)
        self.deleteButton = QtWidgets.QPushButton(FilterDialog)
        self.deleteButton.setObjectName("deleteButton")
        self.horizontalLayout.addWidget(self.deleteButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.filterTalbeView = QtWidgets.QTableView(FilterDialog)
        self.filterTalbeView.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.filterTalbeView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.filterTalbeView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.filterTalbeView.setObjectName("filterTalbeView")
        self.verticalLayout.addWidget(self.filterTalbeView)

        self.retranslateUi(FilterDialog)
        QtCore.QMetaObject.connectSlotsByName(FilterDialog)

    def retranslateUi(self, FilterDialog):
        _translate = QtCore.QCoreApplication.translate
        FilterDialog.setWindowTitle(_translate("FilterDialog", "Filters"))
        self.addFilterButton.setText(_translate("FilterDialog", "Add Filter"))
        self.deleteButton.setText(_translate("FilterDialog", "Delete"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FilterDialog = QtWidgets.QDialog()
    ui = Ui_FilterDialog()
    ui.setupUi(FilterDialog)
    FilterDialog.show()
    sys.exit(app.exec_())

