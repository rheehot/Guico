import logging

from pyqode.python.widgets import PyCodeEdit

logging.basicConfig(level=logging.ERROR)

from pyqode.python.backend import server

from core.config import *

logging.basicConfig()

AUTO_GENERATED = (f"# AUTO GENERATED BY {NAME.upper()}.\n"
                  "# AT {by_class}, {when}\n"
                  "# DO NOT EDIT THIS FILE.\n\n")


class SpriteScriptEditor(PyCodeEdit):

    def __init__(self, parent=None):
        super(SpriteScriptEditor, self).__init__(parent)
        self.backend.start(server.__file__)

        self.setWindowTitle(f"{NAME} {self.__class__.__name__}")

    def showEvent(self, event):
        self.setWindowTitle(f"{NAME} {self.__class__.__name__} - {CONF['FILE_PATH']} [{CONF['CLASS_PATH']}]")
        super().showEvent(event)

    def focusOutEvent(self, event):
        if CONF["CLASS_PATH"] is not None:
            self.save()
        super().focusOutEvent(event)

    def focusInEvent(self, event):

        super().focusInEvent(event)

    def save(self):
        with open(CONF["CLASS_PATH"], "w", encoding="utf8") as _cf:
            if f"# AUTO GENERATED BY {NAME.upper()}." not in self.toPlainText().split("\n"):
                _cf.write(AUTO_GENERATED.format(by_class=self.__class__.__name__, when="UNKNOWN"))
            _cf.write(self.toPlainText())

    def load(self):
        if not os.path.isfile(CONF["CLASS_PATH"]):
            open(CONF["CLASS_PATH"], "w", encoding="utf8")
        self.setPlainText(open(CONF["CLASS_PATH"], "r", encoding="utf8").read())
