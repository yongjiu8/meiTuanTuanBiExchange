from PyQt5.QtGui import QStandardItem, QStandardItemModel, QCursor
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from ui.widget.OrderCustomWidget import OrderCustomWidget
from controller.OrderDetailsUi import OrderDetailsUi
from ui.order import Ui_orderMain
from common.utils import *


class OrderUi(QMainWindow, Ui_orderMain):

    def __init__(self, parent=None):
        super(OrderUi, self).__init__(parent)
        self.setupUi(self)
        self.globelck = ''
        self.globelOrders = 0



    def showTips(self, text):
        QMessageBox.information(self, '提示', text, QMessageBox.Close)

    def showErrorTips(self, text):
        QMessageBox.warning(self, '警告', text, QMessageBox.Close)

    def setCk(self, ck):
        self.globelck = ck

    def initOrder(self):
        if self.globelck == '':
            self.showErrorTips('未选择账号，无法查询订单')
            return

        self.globelOrders = getOrderList(self.globelck)
        if len(self.globelOrders) == 0:
            self.showErrorTips('没有查到订单！')

        self.orderBoxModel = QStandardItemModel(self)
        self.orderListBox.setModel(self.orderBoxModel)
        for order in self.globelOrders:
            outNo = order['outNo']
            statusShow = order['statusShow']
            skuImgUrl = order['skuImgUrl']
            skuName = order['skuName']

            item = QStandardItem()
            item.setCheckable(False)
            self.orderBoxModel.appendRow(item)
            index = self.orderBoxModel.indexFromItem(item)
            widget = OrderCustomWidget(outNo, skuName, statusShow, skuImgUrl)
            item.setSizeHint(widget.sizeHint())
            self.orderListBox.setIndexWidget(index, widget)

            widget.setContextMenuPolicy(Qt.CustomContextMenu)
            widget.customContextMenuRequested[QtCore.QPoint].connect(self.showOrderBoxRightMenu)

    def showOrderBoxRightMenu(self):
        menus = QMenu(self.orderListBox)

        copyAction = QAction(self)
        copyAction.setText('查看订单详细信息')
        copyAction.triggered.connect(self.openOrderDetaild)
        menus.addAction(copyAction)
        menus.exec_(QCursor.pos())

    def openOrderDetaild(self):
        index = self.orderListBox.currentIndex()
        index = self.orderBoxModel.itemFromIndex(index).row()
        ordNO = self.globelOrders[index]['outNo']
        orderDetailsUi = OrderDetailsUi(self)
        orderDetailsUi.setCk(self.globelck)
        orderDetailsUi.setOrdNo(ordNO)
        orderDetailsUi.initOrderDetaild()
        orderDetailsUi.setWindowModality(Qt.ApplicationModal)
        orderDetailsUi.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        orderDetailsUi.show()






