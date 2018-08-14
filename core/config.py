import os

NAME = "Guico"
AUTHOR = "tdh8316@naver.com"
TEAM = "TakturStudio"
VERSION = "0.5c1 빌드 183"
OPEN_SOURCE_LICENSE = open(r".\docs\LICENSE.txt", "r", encoding="utf-8").read()
TMP_PATH = os.path.join(os.path.expanduser("~"), f".{NAME}")
PREF_FILE = os.path.join(TMP_PATH, ".pref")

FILE_TYPES = f"{NAME} script files (*.gvs);;" \
             "모든 파일 (*.*)"

CONF = {
    "FILE_PATH": None,
    "SOURCE_PATH": None,
    "MODIFIED": False,
    "MOUSE_X": int(),
    "MOUSE_Y": int()
}

INDEX = None

RELEASE = False
