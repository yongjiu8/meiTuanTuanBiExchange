# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'order.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_orderMain(object):
    def setupUi(self, orderMain):
        orderMain.setObjectName("orderMain")
        orderMain.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("logo.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        orderMain.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(orderMain)
        self.centralwidget.setObjectName("centralwidget")
        self.orderListBox = QtWidgets.QListView(self.centralwidget)
        self.orderListBox.setGeometry(QtCore.QRect(5, 11, 781, 541))
        self.orderListBox.setObjectName("orderListBox")
        orderMain.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(orderMain)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        orderMain.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(orderMain)
        self.statusbar.setObjectName("statusbar")
        orderMain.setStatusBar(self.statusbar)

        self.retranslateUi(orderMain)
        QtCore.QMetaObject.connectSlotsByName(orderMain)

    def retranslateUi(self, orderMain):
        _translate = QtCore.QCoreApplication.translate
        orderMain.setWindowTitle(_translate("orderMain", "订单"))
