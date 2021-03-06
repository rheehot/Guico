from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from core.config import *
from core import script_variables


class AttributesTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super(AttributesTableWidget, self).__init__(parent)

        self.setColumnCount(2)
        self.setRowCount(MAX_VAR)
        self.setHorizontalHeaderLabels(["변수명", "값"])

        # self.setItem(0, 0, QTableWidgetItem("name"))
        # self.setItem(0, 1, QTableWidgetItem("value"))

        # print(QTableWidgetItem(self.item(0,0)).text())

    def buildVariablesGlobals(self, vars: dict):
        script_variables.globals = vars
        _ = 0

        for k, v in vars.items():
            self.setItem(_, 0, QTableWidgetItem(k))
            self.setItem(_, 1, QTableWidgetItem(v))
            _ += 1

    def getGlobals(self) -> dict:
        global_s = {}
        for i in range(MAX_VAR):
            if QTableWidgetItem(self.item(i, 0)).text() != "":
                global_s[
                    QTableWidgetItem(self.item(i, 0)).text().replace(" ", "_")
                ] = QTableWidgetItem(self.item(i, 1)).text()
        script_variables.globals = global_s

        return global_s

    def focusOutEvent(self, *args, **kwargs):
        super().focusOutEvent(*args, **kwargs)
        self.buildVariablesGlobals(self.getGlobals())
