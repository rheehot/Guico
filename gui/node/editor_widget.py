from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from compiler.default import *
from gui.node.scene import Scene
from gui.node.node import Node
from gui.node.edge import Edge, EDGE_TYPE_BEZIER
from gui.node.graphics_view import QDMGraphicsView

from core import actions


class NodeEditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        actions.set_editor(self)

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # crate graphics scene
        self.scene = Scene()
        # self.grScene = self.scene.grScene

        self.addNodes()
        self.add_default_node()

        # create graphics view
        self.view = QDMGraphicsView(self.scene.grScene, self)
        self.layout.addWidget(self.view)

    def addNodes(self):
        node1 = Node(self.scene, "", inputs=[0,], outputs=[1], types=DRAW_TEXT)
        #node2 = Node(self.scene, "", inputs=[0,], outputs=[1])
        node3 = Node(self.scene, "", inputs=[0,], outputs=[1])
        node1.setPos(-350, -250)
        #node2.setPos(-75, 0)
        node3.setPos(200, -150)

    def add_default_node(self):
        Node(self.scene, "진입점", inputs=[], outputs=[1], types=ENTRY_POINT)

    def addDebugContent(self):
        greenBrush = QBrush(Qt.green)
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(2)

        rect = self.grScene.addRect(-100, -100, 80, 100, outlinePen, greenBrush)
        rect.setFlag(QGraphicsItem.ItemIsMovable)

        text = self.grScene.addText("This is my Awesome text!", QFont("Ubuntu"))
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))

        widget1 = QPushButton("Hello World")
        proxy1 = self.grScene.addWidget(widget1)
        proxy1.setFlag(QGraphicsItem.ItemIsMovable)
        proxy1.setPos(0, 30)

        widget2 = QTextEdit()
        proxy2 = self.grScene.addWidget(widget2)
        proxy2.setFlag(QGraphicsItem.ItemIsSelectable)
        proxy2.setPos(0, 60)

        line = self.grScene.addLine(-200, -200, 400, -100, outlinePen)
        line.setFlag(QGraphicsItem.ItemIsMovable)
        line.setFlag(QGraphicsItem.ItemIsSelectable)
