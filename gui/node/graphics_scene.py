import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from core.config import *


class QDMGraphicsScene(QGraphicsScene):
    def __init__(self, scene, parent=None):
        super().__init__(parent)

        self.scene = scene

        # settings
        self.gridSize = 20
        self.gridSquares = 5

        '''self._color_background = QColor("#EEEEEE")
        self._color_light = QColor("#FAFAFA")
        self._color_dark = QColor("#F5F5F5")'''
        if CONF["THEME"] == "WHITE":
            self._color_background = QColor("#F5F5F5")  # F1F1F1
            self._color_light = QColor("#F1F1F1")  # black : 323232
            self._color_dark = QColor("#F1F1F1")  # white : AAAFBA
        else:
            self._color_background = QColor("#262626")  # F1F1F1
            self._color_light = QColor("#323232")  # black : 323232
            self._color_dark = QColor("#323232")  # white : AAAFBA

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(1)

        self.setBackgroundBrush(self._color_background)

    def setGrScene(self, width, height):
        self.setSceneRect(-width // 2, -height // 2, width, height)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        # here we create our grid
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.gridSize)
        first_top = top - (top % self.gridSize)

        # compute all lines to be drawn
        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.gridSize):
            if (x % (self.gridSize * self.gridSquares) != 0):
                lines_light.append(QLine(x, top, x, bottom))
            else:
                lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.gridSize):
            if y % (self.gridSize * self.gridSquares) != 0:
                lines_light.append(QLine(left, y, right, y))
            else:
                lines_dark.append(QLine(left, y, right, y))

        # draw the lines
        painter.setPen(self._pen_light)
        painter.drawLines(*lines_light)

        painter.setPen(self._pen_dark)
        painter.drawLines(*lines_dark)
