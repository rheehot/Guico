from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from core.config import *


class QDMGraphicsNode(QGraphicsItem):
    def __init__(self, node, parent=None, title_background="#498DEB", w=180, h=180):
        super().__init__(parent)
        self.node = node
        self.content = self.node.content

        self._title_color = Qt.white
        self._title_font = QFont("나눔바른펜", 15)

        self.width = w
        self.height = h
        self.edge_size = 6.9
        self.title_height = 30
        self._padding = 5.0

        if CONF["THEME"] == "WHITE":
            self._pen_default = QPen(QColor("#FFFFFF"))  # 테두리 white : 000000
            self._pen_selected = QPen(QColor("#FFFFA637"))
            self._brush_background = QBrush(QColor("#CFD6E5"))
        else:
            self._pen_default = QPen(QColor("#000000"))  # 테두리 white : 000000
            self._pen_selected = QPen(QColor("#FFFFA637"))
            self._brush_background = QBrush(QColor("#2D2D30"))

        self._brush_title = QBrush(QColor(title_background))
        # white : CFD6E5 / black : 2D2D30

        # init title
        self.initTitle()
        self.title = self.node.title

        # init sockets
        self.initSockets()

        # init content
        self.initContent()

        self.initUI()
        self.wasMoved = False

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

        # optimize me! just update the selected nodes
        for node in self.scene().scene.nodes:
            if node.grNode.isSelected():
                node.updateConnectedEdges()
        self.wasMoved = True

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

        if self.wasMoved:
            self.wasMoved = False
            self.node.scene.history.storeHistory("Node moved", setModified=True)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height).normalized()

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def initTitle(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.node = self.node
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self._padding, 0)
        self.title_item.setTextWidth(self.width * self._padding)

    def initContent(self):
        self.grContent = QGraphicsProxyWidget(self)
        self.content.setGeometry(
            self.edge_size,
            self.title_height + self.edge_size,
            self.width - 2 * self.edge_size,
            self.height - 2 * self.edge_size - self.title_height,
        )
        self.grContent.setWidget(self.content)

    def initSockets(self):
        pass

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(
            0, 0, self.width, self.title_height, self.edge_size, self.edge_size
        )
        path_title.addRect(
            0, self.title_height - self.edge_size, self.edge_size, self.edge_size
        )
        path_title.addRect(
            self.width - self.edge_size,
            self.title_height - self.edge_size,
            self.edge_size,
            self.edge_size,
        )
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(
            0,
            self.title_height,
            self.width,
            self.height - self.title_height,
            self.edge_size,
            self.edge_size,
        )
        path_content.addRect(0, self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(
            self.width - self.edge_size,
            self.title_height,
            self.edge_size,
            self.edge_size,
        )
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())

        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(
            0, 0, self.width, self.height, self.edge_size, self.edge_size
        )
        painter.setPen(
            self._pen_default if not self.isSelected() else self._pen_selected
        )
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())
