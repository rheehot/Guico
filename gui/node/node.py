import sys

from gui.node.graphics_node import QDMGraphicsNode
from gui.node.content_widget import QDMNodeContentWidget
from gui.node.socket import *
from contents.node_ui import *

DEBUG = False


class Node(Serializable):
    def __init__(
        self,
        scene,
        title="Undefined Node",
        inputs=None,
        outputs=None,
        types="Undefined Type",
    ):
        super().__init__()

        if outputs is None:
            outputs = []
        if inputs is None:
            inputs = []

        self._title = title
        self.scene = scene
        # self.type = types
        # print(self.type)
        self.type = types

        try:
            ui_info = NODE_UI[self.type]
        except KeyError:
            # print("Nonexistent leaf")
            sys.exit(1)

        try:
            title, self.bg, self.width, self.height = (
                ui_info[0],
                ui_info[1],
                ui_info[2],
                ui_info[3],
            )
        except IndexError:
            self.width, self.height = 180, 100
            title, self.bg = ui_info[0], ui_info[1]

        # 잎 유형별 정리..
        if self.bg == "#4CAF50":
            inputs = []  # 잎 유형이 이벤트일 경우 input socket 을 제거

        self.content: QDMNodeContentWidget = QDMNodeContentWidget(self, self.type)
        self.grNode = QDMGraphicsNode(
            self, title_background=self.bg, w=self.width, h=self.height
        )
        self.title = title

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.socket_spacing = 30

        # create socket for inputs and outputs
        self.inputs = []
        self.outputs = []
        counter = 0
        for item in inputs:
            socket = Socket(
                node=self, index=counter, position=LEFT_TOP, socket_type=item
            )
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            socket = Socket(
                node=self, index=counter, position=RIGHT_TOP, socket_type=item
            )
            counter += 1
            self.outputs.append(socket)

    def __str__(self):
        return "<Node %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    @property
    def pos(self):
        return self.grNode.pos()  # QPoint

    def setPos(self, x, y):
        self.grNode.setPos(x, y)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.grNode.title = self._title

    def getSocketPosition(self, index, position):
        x = 0 if (position in (LEFT_TOP, LEFT_BOTTOM)) else self.grNode.width

        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            # start from bottom
            y = (
                self.grNode.height
                - self.grNode.edge_size
                - self.grNode._padding
                - index * self.socket_spacing
            )
        else:
            # start from top
            y = (
                self.grNode.title_height
                + self.grNode._padding
                + self.grNode.edge_size
                + index * self.socket_spacing
            )

        return [x, y]

    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.updatePositions()

    def remove(self):
        if DEBUG:
            print("> Removing Node", self)
        if DEBUG:
            print(" - remove all edges from sockets")
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                if DEBUG:
                    print("    - removing from socket:", socket, "edge:", socket.edge)
                socket.edge.remove()
        if DEBUG:
            print(" - remove grNode")
        self.scene.grScene.removeItem(self.grNode)
        self.grNode = None
        if DEBUG:
            print(" - remove node from the scene")
        self.scene.removeNode(self)
        if DEBUG:
            print(" - everything was done.")

    def serialize(self):
        inputs, outputs = [], []
        for socket in self.inputs:
            inputs.append(socket.serialize())
        for socket in self.outputs:
            outputs.append(socket.serialize())
        return OrderedDict(
            [
                ("id", self.id),
                ("title", self.title),
                ("type", self.type),
                ("pos_x", self.grNode.scenePos().x()),
                ("pos_y", self.grNode.scenePos().y()),
                ("inputs", inputs),
                ("outputs", outputs),
                ("content", self.content.serialize()),
            ]
        )

    def deserialize(self, data, hash_map={}, restore_id=True):
        if restore_id:
            self.id = data["id"]
            hash_map[data["id"]] = self

        self.setPos(data["pos_x"], data["pos_y"])
        self.title = data["title"]

        self.content.deserialize(data["content"])

        data["inputs"].sort(
            key=lambda socket: socket["index"] + socket["position"] * 10000
        )
        data["outputs"].sort(
            key=lambda socket: socket["index"] + socket["position"] * 10000
        )

        self.inputs = []
        for socket_data in data["inputs"]:
            new_socket = Socket(
                node=self,
                index=socket_data["index"],
                position=socket_data["position"],
                socket_type=socket_data["socket_type"],
            )
            new_socket.deserialize(socket_data, hash_map, restore_id)
            self.inputs.append(new_socket)

        self.outputs = []
        for socket_data in data["outputs"]:
            new_socket = Socket(
                node=self,
                index=socket_data["index"],
                position=socket_data["position"],
                socket_type=socket_data["socket_type"],
            )
            new_socket.deserialize(socket_data, hash_map, restore_id)
            self.outputs.append(new_socket)

        return True
