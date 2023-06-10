from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QLineEdit, QPushButton, QLabel


class ItemCustomWidget(QWidget):

    def __init__(self, name, balance, ck, *args, **kwargs):
        super(ItemCustomWidget, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QLabel(name.strip(), self))
        layout.addWidget(QLabel("----", self))
        layout.addWidget(QLabel(balance.strip(), self))
        layout.addWidget(QLabel("----", self))
        layout.addWidget(QLabel(ck.strip(), self))


    def sizeHint(self):
        # 决定item的高度
        return QSize(200, 40)