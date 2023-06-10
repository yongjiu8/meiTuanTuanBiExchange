import threading

import pyperclip
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import *

from ui.widget.ItemCustomWidget import ItemCustomWidget
from ui.Loading import Loading
from controller.OrderUi import OrderUi
from ui.widget.ProductCustomWidget import ProductCustomWidget

from PyQt5.QtGui import QStandardItemModel, QStandardItem, QCursor
from qt_material import apply_stylesheet

from ui.main import Ui_MainWindow
from common.utils import *


class TuanBi(QMainWindow, Ui_MainWindow):
    initCkSignal = pyqtSignal(list)
    initAddressSignal = pyqtSignal(list)
    initProductsSignal = pyqtSignal(list)
    initImgSignal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(TuanBi, self).__init__(parent)
        self.setupUi(self)
        self.loading = Loading()

        self.globelck = ''
        self.globelAddressDatas = []
        self.globelAddressIndex = 0
        self.globelSearchAddressDatas = []
        self.globelSearchAddressIndex = 0
        self.globelProductsDatas = []
        self.globelProductsIndex = 0
        self.ckSortIsDesc = True
        self.blanceCount = 0
        self.cksCount = 0

        self.importckbtn.clicked.connect(self.openckTxt)
        self.ckListBox.clicked.connect(self.ckListClicked)
        self.addressListBox.clicked.connect(self.addressListClicked)
        self.searchAddressBtn.clicked.connect(self.searchAddressClick)
        self.searchAddressListBox.clicked.connect(self.searchAddressListClicked)
        self.addAddressBtn.clicked.connect(self.addAddressClick)
        self.productsListBox.clicked.connect(self.productsListClicked)
        self.submitBtn.clicked.connect(self.submitBtnClicked)
        self.orderBtn.clicked.connect(self.orderBtnClicked)
        self.ckSortBtn.clicked.connect(self.sortCkListDesc)

        self.initCkSignal.connect(self.initCkBox)
        self.initAddressSignal.connect(self.initAddressBox)
        self.initProductsSignal.connect(self.initProductsBox)
        self.initImgSignal.connect(self.updateProductBoxImg)

    def showTips(self, text):
        QMessageBox.information(self, '提示', text, QMessageBox.Close)

    def showErrorTips(self, text):
        QMessageBox.warning(self, '警告', text, QMessageBox.Close)

    def showLoading(self):
        self.loading = Loading()
        self.loading.setWindowModality(Qt.ApplicationModal)
        self.loading.show()

    def closeLoading(self):
        if self.loading != None:
            self.loading.hide()

    def openckTxt(self):
        fname, ftype = QFileDialog.getOpenFileName(self, '导入美团ck', './', 'Txt (*.txt)')
        printf(fname)
        if ftype == 'Txt (*.txt)':
            self.cks = execCkDatas(fname)
            printf(self.cks)
            self.showLoading()
            self.cksCount = 0
            self.blanceCount = 0
            threading.Thread(target=getTuanBiBlance, args=(self.initCkSignal, self.cks)).start()

            # 获取一个有效的ck加载商品
            for ck in self.cks:
                if checkCkStatus(ck):
                    threading.Thread(target=getProducts, args=(self.initProductsSignal, ck)).start()
                    break
        else:
            self.showErrorTips('文件选择有误')

    def initCkBox(self, datas):
        self.cksCount = len(datas)
        self.ckCountLabel.setText(str(self.cksCount))
        self.cksModel = QStandardItemModel(self)
        self.ckListBox.setModel(self.cksModel)
        for data in datas:
            item = QStandardItem()
            item.setCheckable(True)
            item.setCheckState(Qt.Unchecked)
            self.cksModel.appendRow(item)
            index = self.cksModel.indexFromItem(item)

            widget = ItemCustomWidget(data['name'], data['blance'], data['ck'])
            item.setSizeHint(widget.sizeHint())
            self.ckListBox.setIndexWidget(index, widget)
            self.blanceCount += int(data['blance'].replace("小团币", '').replace("个", ''))

        if self.cksModel.rowCount() > 0:
            seIndex = self.cksModel.index(0, 0)
            self.globelck = self.ckListBox.indexWidget(seIndex).children()[5].text()
            self.cksModel.itemFromIndex(seIndex).setCheckState(Qt.Checked)
            self.ckListBox.setCurrentIndex(seIndex)
            threading.Thread(target=getAddressList, args=(self.initAddressSignal, self.globelck)).start()
            self.blanceCountLabel.setText(str(self.blanceCount))

    def sortCkListDesc(self):
        model = self.ckListBox.model()

        if model:
            datas = []
            for i in range(model.rowCount()):
                item = self.ckListBox.indexWidget(model.index(i, 0))
                blance = item.children()[3].text()
                datas.append({
                    "item": item,
                    "blance": int(blance.replace("小团币", '').replace("个", ''))
                })

            datas = sorted(datas, key=lambda it: it['blance'], reverse=self.ckSortIsDesc)

            self.cksModel = QStandardItemModel(self)
            self.ckListBox.setModel(self.cksModel)
            for i in range(len(datas)):
                widget = ItemCustomWidget(datas[i]['item'].children()[1].text(), datas[i]['item'].children()[3].text(), datas[i]['item'].children()[5].text())
                item = QStandardItem()
                item.setCheckable(True)
                item.setCheckState(Qt.Unchecked)
                self.cksModel.appendRow(item)
                index = self.cksModel.indexFromItem(item)
                item.setSizeHint(widget.sizeHint())
                self.ckListBox.setIndexWidget(index, widget)

            if self.cksModel.rowCount() > 0:
                seIndex = self.cksModel.index(0, 0)
                self.globelck = self.ckListBox.indexWidget(seIndex).children()[5].text()
                self.cksModel.itemFromIndex(seIndex).setCheckState(Qt.Checked)
                self.ckListBox.setCurrentIndex(seIndex)
                threading.Thread(target=getAddressList, args=(self.initAddressSignal, self.globelck)).start()
                self.ckSortIsDesc = not self.ckSortIsDesc

    def ckListClicked(self):
        index = self.ckListBox.currentIndex()
        for i in range(self.cksModel.rowCount()):
            item = self.cksModel.item(i)
            if item.index() == index:
                item.setCheckState(Qt.Checked)
                widget = self.ckListBox.indexWidget(item.index())
                self.globelck = widget.children()[5].text()
                self.showLoading()
                threading.Thread(target=getAddressList, args=(self.initAddressSignal, self.globelck)).start()
            else:
                if item.checkState() == Qt.Checked:
                    item.setCheckState(Qt.Unchecked)

    def initAddressBox(self, datas):
        self.addressModel = QStandardItemModel(self)
        self.addressListBox.setModel(self.addressModel)
        self.globelAddressDatas = datas
        for addressItem in self.globelAddressDatas:
            recipient_name = addressItem['recipient_name']
            address_name = addressItem['address_name']
            phone = addressItem['phone']
            house_number = addressItem['house_number']
            address_admin_list = addressItem['address_admin_list']
            preAddress = ''
            for it in address_admin_list:
                preAddress = preAddress + it['name']

            addressStr = preAddress + address_name + house_number

            item = QStandardItem()
            item.setCheckable(True)
            item.setCheckState(Qt.Unchecked)
            self.addressModel.appendRow(item)
            index = self.addressModel.indexFromItem(item)
            widget = ItemCustomWidget(recipient_name, phone, addressStr)
            item.setSizeHint(widget.sizeHint())
            self.addressListBox.setIndexWidget(index, widget)
            widget.setContextMenuPolicy(Qt.CustomContextMenu)
            widget.customContextMenuRequested[QtCore.QPoint].connect(self.showAddressBoxRightMenu)

        seIndex = self.addressModel.index(0, 0)
        self.globelAddressIndex = 0
        if self.addressModel.rowCount() > 0:
            self.addressModel.itemFromIndex(seIndex).setCheckState(Qt.Checked)
            self.addressListBox.setCurrentIndex(seIndex)

        self.closeLoading()

    def addressListClicked(self):
        index = self.addressListBox.currentIndex()
        for i in range(self.addressModel.rowCount()):
            item = self.addressModel.item(i)
            if item.index() == index:
                item.setCheckState(Qt.Checked)
                self.globelAddressIndex = item.row()
            else:
                if item.checkState() == Qt.Checked:
                    item.setCheckState(Qt.Unchecked)

    def showAddressBoxRightMenu(self):
        menus = QMenu(self.addressListBox)

        copyAction = QAction(self)
        copyAction.setText('复制')
        copyAction.triggered.connect(self.addressRightMenuCopy)
        removeAction = QAction(self)
        removeAction.setText('删除地址')
        removeAction.triggered.connect(self.addressRightMenuRemoveClick)
        menus.addAction(copyAction)
        menus.addAction(removeAction)
        menus.exec_(QCursor.pos())

    def addressRightMenuRemoveClick(self):
        index = self.addressListBox.currentIndex()
        row = self.addressModel.itemFromIndex(index).row()
        address_view_id = self.globelAddressDatas[row]['address_view_id']
        self.showLoading()
        delAddress(self.globelck, address_view_id)
        threading.Thread(target=getAddressList, args=(self.initAddressSignal, self.globelck)).start()

    def addressRightMenuCopy(self):
        index = self.addressListBox.currentIndex()
        row = self.addressModel.itemFromIndex(index).row()
        item = self.addressModel.item(row)
        widget = self.addressListBox.indexWidget(item.index())
        widgets = widget.children()
        copyStr = widgets[1].text() + widgets[2].text() + widgets[3].text() + widgets[4].text() + widgets[5].text()
        pyperclip.copy(copyStr)
        self.showTips('复制成功')

    def searchAddressClick(self):
        city = self.addressCityEdit.toPlainText()
        keyword = self.searchAddressEdit.toPlainText()
        if city == '' or keyword == '':
            self.showErrorTips('城市或关键字不能为空哦！')
            return
        if self.globelck == '':
            self.showErrorTips('Cookie为空或没有导入选择！')
            return
        self.initSearchAddressBox()

    def initSearchAddressBox(self):
        city = self.addressCityEdit.toPlainText()
        keyword = self.searchAddressEdit.toPlainText()
        self.searchAddressModel = QStandardItemModel(self)
        self.searchAddressListBox.setModel(self.searchAddressModel)
        self.globelSearchAddressDatas = searchAddress(self.globelck, city, keyword)
        for addressItem in self.globelSearchAddressDatas:
            name = addressItem['name']
            address = addressItem['address']

            item = QStandardItem()
            item.setCheckable(True)
            item.setCheckState(Qt.Unchecked)
            self.searchAddressModel.appendRow(item)
            index = self.searchAddressModel.indexFromItem(item)
            widget = ItemCustomWidget(name, address, '')
            item.setSizeHint(widget.sizeHint())
            self.searchAddressListBox.setIndexWidget(index, widget)

        seIndex = self.searchAddressModel.index(0, 0)
        self.globelSearchAddressIndex = 0
        if self.searchAddressModel.rowCount() > 0:
            self.searchAddressModel.itemFromIndex(seIndex).setCheckState(Qt.Checked)
            self.searchAddressListBox.setCurrentIndex(seIndex)

    def searchAddressListClicked(self):
        index = self.searchAddressListBox.currentIndex()
        for i in range(self.searchAddressModel.rowCount()):
            item = self.searchAddressModel.item(i)
            if item.index() == index:
                item.setCheckState(Qt.Checked)
                self.globelSearchAddressIndex = item.row()
            else:
                if item.checkState() == Qt.Checked:
                    item.setCheckState(Qt.Unchecked)

    def addAddressClick(self):
        detailedAddress = self.detailedAddressEdit.toPlainText()
        name = self.detailedNameEdit.toPlainText()
        phone = self.detailedPhoneEdit.toPlainText()
        if detailedAddress == '' or name == '' or phone == '':
            self.showErrorTips('详细地址或收货人或收货手机号不能为空哦！')
            return

        self.showLoading()
        addAddress(self.globelck, self.globelSearchAddressDatas[self.globelSearchAddressIndex], name, phone,
                   detailedAddress)
        threading.Thread(target=getAddressList, args=(self.initAddressSignal, self.globelck)).start()

    def initProductsBox(self, datas):
        self.productsBoxModel = QStandardItemModel(self)
        self.productsListBox.setModel(self.productsBoxModel)
        self.globelProductsDatas = datas
        for pitem in self.globelProductsDatas:
            for key in pitem.keys():
                item = pitem[key]
                if '10031' not in item.keys():
                    self.globelProductsDatas.remove(pitem)

        for pitem in self.globelProductsDatas:
            for key in pitem.keys():
                item = pitem[key]
                imgurl = item['10009']
                descs = item['10029']
                name = item['10002']
                balance = '需要团币' + str(json.loads(descs)[0]['ruleDetail'][0]['count']) + '个'

                item = QStandardItem()
                item.setCheckable(True)
                item.setCheckState(Qt.Unchecked)
                self.productsBoxModel.appendRow(item)
                index = self.productsBoxModel.indexFromItem(item)
                widget = ProductCustomWidget(name, balance, b'')
                item.setSizeHint(widget.sizeHint())
                # 异步加载图片
                data = {
                    "index": index,
                    "name": name,
                    "balance": balance,
                    "imgUrl": imgurl
                }
                threading.Thread(target=getImg, args=(self.initImgSignal, data)).start()

                self.productsListBox.setIndexWidget(index, widget)

        seIndex = self.productsBoxModel.index(0, 0)
        self.globelProductsIndex = 0
        if self.productsBoxModel.rowCount() > 0:
            self.productsBoxModel.itemFromIndex(seIndex).setCheckState(Qt.Checked)
            self.productsListBox.setCurrentIndex(seIndex)

    def updateProductBoxImg(self, datas):
        index = datas['index']
        name = datas['name']
        balance = datas['balance']
        img = datas['img']
        self.productsListBox.setIndexWidget(index, ProductCustomWidget(name, balance, img))

    def productsListClicked(self):
        index = self.productsListBox.currentIndex()
        for i in range(self.productsBoxModel.rowCount()):
            item = self.productsBoxModel.item(i)
            if item.index() == index:
                item.setCheckState(Qt.Checked)
                self.globelProductsIndex = item.row()
            else:
                if item.checkState() == Qt.Checked:
                    item.setCheckState(Qt.Unchecked)

    def submitBtnClicked(self):
        if len(self.globelProductsDatas) == 0 or len(self.globelAddressDatas) == 0:
            self.showErrorTips('请选择商品和地址后在提交兑换！')
            return

        isOk, outNo = submitOrderV2(self.globelck, self.globelAddressDatas[self.globelAddressIndex],
                                    self.globelProductsDatas[self.globelProductsIndex])
        if isOk:
            self.showTips(f'恭喜兑换成功！订单号：{outNo}')
        else:
            self.showErrorTips('兑换失败！小团币不足或其他问题')

    def orderBtnClicked(self):
        orderui = OrderUi(self)
        orderui.setCk(self.globelck)
        orderui.initOrder()
        orderui.setWindowModality(Qt.ApplicationModal)
        orderui.show()


if __name__ == '__main__':
    try:
        signal2 = QtCore.pyqtSignal(str)
        app = QtWidgets.QApplication(sys.argv)
        apply_stylesheet(app, theme='light_blue.xml')
        tuanBi = TuanBi()
        tuanBi.show()
        sys.exit(app.exec_())
    except Exception as e:
        tuanBi.showErrorTips(f'错误：{e}')
        tuanBi.closeLoading()
