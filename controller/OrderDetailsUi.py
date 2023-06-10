from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import *

from ui.widget.ItemCustomWidget import ItemCustomWidget
from ui.orderDetails import Ui_orderDetails
from common.utils import *


class OrderDetailsUi(QWidget, Ui_orderDetails):

    def __init__(self, parent=None):
        super(OrderDetailsUi, self).__init__(parent)
        self.setupUi(self)
        self.globelck = ''
        self.globelOrdNo = 0


    def showTips(self, text):
        QMessageBox.information(self, '提示', text, QMessageBox.Close)

    def showErrorTips(self, text):
        QMessageBox.warning(self, '警告', text, QMessageBox.Close)

    def setCk(self, ck):
        self.globelck = ck

    def setOrdNo(self, ordNo):
        self.globelOrdNo = ordNo

    def initOrderDetaild(self):
        if self.globelck == '' or self.globelOrdNo == 0:
            self.showErrorTips('cookie或订单号为空，无法查询订单')
            return

        orders = getOrderDetaild(self.globelck, self.globelOrdNo)
        if orders['outNo'] == None:
            self.showErrorTips('没有查到订单信息！')
            return

        outNo = orders['outNo']
        statusShow = orders['statusShow']
        skuName = orders['skuName']
        recipientName = orders['addressInfo']['recipientName']
        recipientPhone = orders['addressInfo']['recipientPhone']
        recipientAddress = orders['addressInfo']['recipientAddress']



        self.skuNameBox.setText(skuName)
        self.orderNoBox.setText(outNo)
        self.statusBox.setText(statusShow)
        self.addressBox.setText(f'{recipientName} {recipientPhone} {recipientAddress}')


        if orders['expressInfo'] != None:
            expressNo = orders['expressInfo']['expressNo']
            expressName = orders['expressInfo']['expressName']
            trace = orders['expressInfo']['trace']
            self.wuLiuNameBox.setText(f'{expressName}:')
            self.wuLiuNoBox.setText(expressNo)
            self.wuLiuBoxModel = QStandardItemModel(self)
            self.wuLiuListBox.setModel(self.wuLiuBoxModel)
            for it in trace:
                timeStamp = it['time']
                ten_timeArray = time.localtime(timeStamp)
                timestr = time.strftime("%Y-%m-%d %H:%M:%S", ten_timeArray)
                statusShow = it['statusShow']
                content = it['content']
                if statusShow == None:
                    statusShow = ''
                if timestr == None:
                    timestr = ''
                if content == None:
                    content = ''

                item = QStandardItem()
                item.setCheckable(False)
                self.wuLiuBoxModel.appendRow(item)
                index = self.wuLiuBoxModel.indexFromItem(item)
                widget = ItemCustomWidget(timestr, statusShow, content)
                item.setSizeHint(widget.sizeHint())
                self.wuLiuListBox.setIndexWidget(index, widget)



