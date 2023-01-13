import requests
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QLineEdit, QPushButton, QLabel


class ProductCustomWidget(QWidget):

    def __init__(self, name, balance, imgurl, *args, **kwargs):
        super(ProductCustomWidget, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        res = requests.get(imgurl)
        img = QImage.fromData(res.content)

        l1 = QLabel(self)
        l1.resize(50, 80)
        l1.setScaledContents(True)
        l1.setPixmap(QPixmap.fromImage(img).scaled(50, 80))


        layout.addWidget(l1)
        layout.addWidget(QLabel("", self))
        layout.addWidget(QLabel(name, self))
        layout.addWidget(QLabel("", self))
        layout.addWidget(QLabel(balance, self))


    def sizeHint(self):
        # 决定item的高度
        return QSize(200, 80)