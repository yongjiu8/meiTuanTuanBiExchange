from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QMovie

import resources.images
class Loading(QWidget):
    def __init__(self):
        super(Loading, self).__init__()
        self.label = QLabel("", self)
        self.label.setContentsMargins(0, 0, 0, 0)
        self.setFixedSize(150, 150)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint)
        self.movie = QMovie(":images/ld.gif")
        self.movie.setScaledSize(QSize(150, 150))
        self.label.setMovie(self.movie)
        self.movie.start()