
import time

import PySide6

from main import Main, main
from random import randint
import NonExistentModule
from PySide6.QtWidgets import QApplication, QSplashScreen, QProgressBar
from PySide6.QtGui import QMovie, QPixmap, QPainter
from PySide6.QtCore import QSize

from main import Main, main
from random import randint

class MovieSplashScreen(QSplashScreen):
    my_size = QSize(600, 600)

    def __init__(path_to_gif: str)
        self.movie = QMovie(path_to_gif)
        self.movie.jumpToFrame(0)
        pixmap = QPixmap(self.my_size)
        QSplashScreen.__init__(self, pixmap)
        self.movie.frameChanged.connect(self.repaint)

    def showEvent(event: PySide6.QtGui.QShowEvent) -> None:
        while True:
            self.movie.start()

    def hideEvent(event: PySide6.QtGui.QHideEvent) -> None:
        self.movie.stop()

    def paintEvent(event: PySide6.QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        pixmap = self.movie.currentPixmap()
        pixmap = pixmap.scaled(self.my_size)
        painter.drawPixmap(0, 0, pixmap)


