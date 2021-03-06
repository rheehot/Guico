import datetime
import json
import signal
import subprocess
import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from core.execute import Execute, execute_manager
from gui.node.editor_widget import NodeEditorWidget
import build_tools
from core.config import *
from core import actions
from gui.widgets import customized
from gui.widgets.script_widget import ScriptWidget, TabScriptWidget
from gui.widgets.attr_widget import AttributesTableWidget
from contents.create_widgets.window_new import define_parent_window
from gui.widgets.pos_widget import *
from gui import dialogs
from gui.widgets.sprite_class_edit import SpriteScriptEditor


class MainForm(QMainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        self.setWindowTitle(f"{TEAM} {NAME} {VERSION}")

        if hasattr(Qt, "AA_EnableHighDpiScaling"):
            QApplication.instance().setAttribute(Qt.AA_EnableHighDpiScaling, True)

        if hasattr(Qt, "AA_UseHighDpiPixmaps"):
            QApplication.instance().setAttribute(Qt.AA_UseHighDpiPixmaps, True)

        self.pos_widget = None
        self.dock_pos = None

        self.log = QPlainTextEdit(self)
        self.log.setReadOnly(True)
        self.dock_log = QDockWidget("Log", self)
        self.dock_log.setWidget(self.log)
        self.dock_log.hide()

        actions.initialize(self)
        build_tools.initialize(self)
        dialogs.initialize(self)
        customized.initialize(self)

        self.create_menu()
        # self.status_mouse_pos = QLabel("Unknown Mouse Pos")
        # self.statusBar().addPermanentWidget(self.status_mouse_pos)

        self.editor = NodeEditorWidget(self)
        self.editor.scene.addHasBeenModifiedListener(
            lambda: self.signal_change_editor()
        )
        self.editor.view.scenePosChanged.connect(actions.on_scene_pos_changed)

        # self.dock_editor = QDockWidget("편집 환경", self)
        # self.dock_editor.setWidget(self.editor)
        self.setCentralWidget(self.editor)

        self.leaf_widget = TabScriptWidget(self)
        self.leaf_widget.setMaximumWidth(250)

        self.dock_leaf = QDockWidget("스크립트", self)
        self.dock_leaf.setWidget(self.leaf_widget)
        self.dock_leaf.setFeatures(
            QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable
        )

        self.attribute_widget = AttributesTableWidget()
        self.dock_attribute = QDockWidget("Attributes", self)
        self.dock_attribute.setWidget(self.attribute_widget)
        self.dock_attribute.showMaximized()
        self.dock_attribute.setFeatures(
            QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable
        )

        self.script_editor = SpriteScriptEditor(self)
        self.dock_script = QDockWidget("스프라이트 클래스 편집기", self)
        self.dock_script.setWidget(self.script_editor)
        self.dock_script.setFloating(True)
        self.dock_script.resize(640, 480)
        self.dock_script.hide()

        # self.addDockWidget(Qt.RightDockWidgetArea, self.dock_editor)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock_log)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_attribute)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_leaf)
        self.tabifyDockWidget(self.dock_leaf, self.dock_attribute)
        self.dock_leaf.raise_()
        self.setDockOptions(
            QMainWindow.AllowNestedDocks
            | QMainWindow.AnimatedDocks
            | QMainWindow.AllowTabbedDocks
        )

        self.set_pos_widget()
        self.dock_pos.hide()

        self.showMaximized()
        self.log.appendPlainText(
            f"{str(datetime.datetime.now()).split('.')[0]} 에 {NAME} 초기화 성공"
        )
        # self.showFullScreen()

    def set_pos_widget(self):
        self.pos_widget = View(640, 480, self)
        self.pos_widget.view.scenePosChanged.connect(self.pos_widget_pos_change)
        self.dock_pos = QDockWidget("Emulate Window", self)
        self.dock_pos.setWidget(self.pos_widget)
        define_parent_window(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_pos)

    def reset_pos_widget(self, x, y):
        self.dock_pos.hide()
        self.pos_widget = View(int(x), int(y), self)
        self.pos_widget.view.scenePosChanged.connect(self.pos_widget_pos_change)
        self.dock_pos = QDockWidget("Emulate Window", self)
        self.dock_pos.setWidget(self.pos_widget)
        define_parent_window(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_pos)
        if int(x) > 800 or int(y) > 600:
            self.dock_pos.setFloating(True)
        else:
            self.dock_pos.setFloating(False)
        self.dock_pos.show()

    def create_menu(self):
        menu_bar: QMenu = self.menuBar()
        # menu_bar.setFont(QFont("맑은 고딕", 9))

        menu_file = menu_bar.addMenu("파일(&F)")
        menu_file.addAction(actions.file_new())
        menu_file.addAction(actions.file_open())
        menu_file.addAction(actions.file_save())
        menu_file.addAction(actions.file_save_as())
        menu_file.addSeparator()
        menu_file.addAction(actions.file_save_as_image())
        menu_file.addSeparator()
        menu_file.addAction(
            QAction(
                f"{NAME} 종료(&X)",
                self,
                shortcut="Alt+F4",
                triggered=lambda: self.close(),
            )
        )
        menu_edit = menu_bar.addMenu("편집(&E)")
        menu_edit.addAction(actions.undo())
        menu_edit.addAction(actions.redo())
        menu_edit.addSeparator()
        menu_edit.addAction(actions.cut())
        menu_edit.addAction(actions.copy())
        menu_edit.addAction(actions.paste())
        menu_edit.addAction(actions.delete())
        menu_edit.addSeparator()
        menu_view = menu_bar.addMenu("보기(&V)")
        menu_view.addAction(
            QAction(
                "출력 창 보이기(&O)",
                self,
                shortcut="Alt+1",
                triggered=lambda: self.dock_log.show(),
            )
        )
        menu_view.addAction(
            QAction(
                "스프라이트 클래스 편집기",
                self,
                shortcut="Alt+2",
                triggered=lambda: self.dock_script.show(),
            )
        )
        menu_view.addAction(
            QAction(
                "윈도우 에뮬레이팅 보기(&W)",
                self,
                shortcut="F10",
                triggered=self._showEmulateWindow,
                checkable=True,
                checked=False,
            )
        )
        menu_view.addSeparator()
        menu_view.addAction(
            QAction(
                "전체 화면으로 보기(&S)",
                self,
                shortcut="F11",
                triggered=self._showFullScreen,
                checkable=True,
            )
        )
        if USE_PLUGINS:
            self.create_plugins_menu(menu_bar.addMenu("확장 기능(&P)"))
        menu_run = menu_bar.addMenu("실행(&R)")
        menu_run.addAction(actions.run_as_python())
        menu_run.addAction(actions.compile_to_python())
        menu_run.addAction(actions.run_as_python__dev())
        menu_run.addSeparator()
        menu_run.addAction(actions.packaging())
        menu_help = menu_bar.addMenu("도움말(&H)")
        menu_help.addAction(actions.license_dialog())
        menu_help.addAction(QAction("&Qt 에 대해서...", self, triggered=qApp.aboutQt))
        menu_help.addSeparator()
        menu_help.addAction(
            QAction(
                f"{NAME} 정보(&A)",
                self,
                triggered=lambda: QMessageBox.about(
                    None,
                    f"{NAME} 정보",
                    "Copyright 2018 {TEAM}\n{NAME} {EDITION}\nBuild {VERSION}".format(
                        TEAM=TEAM, NAME=NAME, EDITION=EDITION, VERSION=VERSION
                    ),
                ),
            )
        )
        # menu_edit.addAction(actions.new_leaf())

    def create_plugins_menu(self, _):
        if RELEASE:
            sys.path.append(os.path.join(os.path.dirname(os.getcwd()), PLUGIN_DIR))
            # noinspection PyUnresolvedReferences
            import plugin
        else:
            sys.path.append(os.path.join(os.getcwd(), PLUGIN_DIR))
            from plugins import plugin
        for module in plugin.__modules__:
            dock = QDockWidget(plugin.__description__[module], self)
            dock.setWidget(__import__(module).main(self, CONF))
            _.addAction(
                QAction(
                    plugin.__description__[module],
                    self,
                    triggered=lambda: self.show_pluginWidget(dock),
                )
            )
            dock.hide()

    def show_pluginWidget(self, w):
        w.setFloating(True)
        w.resize(640, 480)
        self.addDockWidget(Qt.RightDockWidgetArea, w)
        w.show()

    def signal_change_editor(self, changed=True):
        CONF["MODIFIED"] = True if changed else False

        if execute_manager.is_process_running() and changed:
            if (
                QMessageBox.warning(
                    None,
                    "Your program is running",
                    "이 스크립트가 아직 실행 중 입니다." "실행 중인 프로세스를 끝내고 수정을 계속하시겠습니까?",
                    QMessageBox.Yes | QMessageBox.No,
                )
                == QMessageBox.No
            ):
                CONF["MODIFIED"] = False
            else:
                # https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true/4791612#4791612
                execute_manager.process: subprocess.Popen
                subprocess.Popen(f"taskkill /F /PID {execute_manager.process.pid} /T")
        # print(self.focusWidget())

        self.renewal()

    def pos_widget_pos_change(self, x, y):
        self.pos_widget.pos_label.setText("{},{}".format(x * 2, y * 2))

    def renewal(self):
        if not CONF["MODIFIED"]:
            self.setWindowTitle(
                f"{TEAM} {NAME} {VERSION} [{CONF['FILE_PATH']}]"
                if CONF["FILE_PATH"] is not None
                else f"{TEAM} {NAME} {VERSION} - 빈 파일"
            )
        elif CONF["MODIFIED"]:
            self.setWindowTitle(
                f"{TEAM} {NAME} {VERSION} [{CONF['FILE_PATH']}]*"
                if CONF["FILE_PATH"] is not None
                else f"{TEAM} {NAME} {VERSION} - 제목 없음*"
            )

    def _showFullScreen(self, checked):
        self.showFullScreen() if checked else self.showNormal()

    def _showEmulateWindow(self, checked):
        if self.dock_pos.isHidden():
            self.dock_pos.show()
            return

        self.dock_pos.show() if checked else self.dock_pos.hide()

    def is_modified(self) -> bool:
        return self.editor.scene.has_been_modified

    def maybe_save(self):
        if not (self.is_modified() or CONF["MODIFIED"]):
            return True

        res = QMessageBox.warning(
            None,
            f"{NAME} - 현재 파일이 변경됨",
            f"현재 파일 ["
            f"{CONF['FILE_PATH'] if CONF['FILE_PATH'] is not None else '제목 없음'}"
            f"]이 수정되었습니다.\n"
            f"변경 사항을 저장하시겠습니까?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
        )

        if res == QMessageBox.Save:
            self.save()
            return True
        elif res == QMessageBox.Cancel:
            return False

        return True

    def save(self):
        if CONF["FILE_PATH"] is None:
            _name, _filter = QFileDialog.getSaveFileName(
                None, f"{NAME} - 저장", "", FILE_TYPES
            )
            if _name == "":
                return False
            CONF["FILE_PATH"] = _name
            CONF["SOURCE_PATH"] = os.path.join(
                "/".join(list(CONF["FILE_PATH"].split("/")[:-1])),
                (CONF["FILE_PATH"].split("/")[-1].split(".")[0] + ".py"),
            )
            CONF["CLASS_PATH"] = os.path.join(
                "/".join(list(CONF["FILE_PATH"].split("/")[:-1])),
                (CONF["FILE_PATH"].split("/")[-1].split(".")[0] + ".class"),
            )
        if os.path.isfile(CONF["FILE_PATH"]):
            _backup = open(CONF["FILE_PATH"], "r", encoding="utf8").read()
        else:
            _backup = None
        try:
            with open(CONF["FILE_PATH"], "w") as file:
                file.write(json.dumps(self.editor.scene.serialize(), indent=4))
            with open(CONF["FILE_PATH"], "a") as file:
                file.write(
                    f"Below are the variables.{json.dumps(self.attribute_widget.getGlobals(), indent=4)}"
                )
            self.editor.scene.has_been_modified = False
        except:
            with open(CONF["FILE_PATH"], "w") as file:
                if _backup is not None:
                    file.write(_backup)
            del _backup
            QMessageBox.critical(None, "저장 실패!", "죄송ㅠ")
        else:
            self.signal_change_editor(False)
            self.renewal()

    def save_as(self):
        _name, _filter = QFileDialog.getSaveFileName(
            None, f"{NAME} - 저장", "", FILE_TYPES
        )
        if _name == "":
            return False
        CONF["FILE_PATH"] = _name
        CONF["SOURCE_PATH"] = os.path.join(
            "/".join(list(CONF["FILE_PATH"].split("/")[:-1])),
            (CONF["FILE_PATH"].split("/")[-1].split(".")[0] + ".py"),
        )
        CONF["CLASS_PATH"] = os.path.join(
            "/".join(list(CONF["FILE_PATH"].split("/")[:-1])),
            (CONF["FILE_PATH"].split("/")[-1].split(".")[0] + ".class"),
        )

        self.script_editor.save()

        self.save()

    def load(self):
        _name, _filter = QFileDialog.getOpenFileName(
            None, f"{NAME} - 열기", "", FILE_TYPES
        )
        if _name == "":
            return
        if os.path.isfile(_name):
            CONF["FILE_PATH"] = _name
            CONF["SOURCE_PATH"] = os.path.join(
                "/".join(list(CONF["FILE_PATH"].split("/")[:-1])),
                (CONF["FILE_PATH"].split("/")[-1].split(".")[0] + ".py"),
            )
            CONF["CLASS_PATH"] = os.path.join(
                "/".join(list(CONF["FILE_PATH"].split("/")[:-1])),
                (CONF["FILE_PATH"].split("/")[-1].split(".")[0] + ".class"),
            ).replace("\\", "/")
            data = open(_name).read()
            self.editor.scene.load(
                json.loads(data.split("Below are the variables.")[0], encoding="utf-8")
            )
            self.script_editor.load()
            self.signal_change_editor(False)
            self.renewal()

            self.attribute_widget.buildVariablesGlobals(
                json.loads(data.split("Below are the variables.")[1], encoding="utf-8")
            )

            self.dock_script.setWindowTitle(
                f"{NAME} {self.script_editor.__class__.__name__} - {CONF['FILE_PATH'] } [{CONF['CLASS_PATH']}]"
            )

    def closeEvent(self, event):
        if self.maybe_save():
            self.deleteLater()
            if execute_manager.is_process_running():
                subprocess.Popen(f"taskkill /F /PID {execute_manager.process.pid} /T")
            event.accept()
        else:
            event.ignore()
