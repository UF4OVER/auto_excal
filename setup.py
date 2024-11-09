import sys
from cx_Freeze import setup, Executable


"""
import json
import pyautogui
import main_window as m
import small_window as s
import threading
import time
import sys

from qt_material import apply_stylesheet
from openpyxl.reader.excel import load_workbook
from pynput import mouse

from PyQt5.QtCore 
from PyQt5.QtGui 
from PyQt5.QtWidgets """


# 定义构建选项
build_exe_options = {
    "packages": [
        "json",
        "pyautogui",
        "threading",
        "time",
        "sys",
        "os",
        "re",

        "qt_material",
        "openpyxl",
        "pynput",

        "PyQt5.QtCore",
        "PyQt5.QtGui",
        "PyQt5.QtWidgets",
    ],
    "include_files": [
        ("icon.ico", "icon.ico")
    ],
    "excludes": []
}

# 设置 GUI 基础
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# 设置项目信息
setup(
    name="原神",
    version="2.4.5",
    description="AUTO-INPUT",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "main.py",
            base=base,
            icon="icon.ico"
        )
    ]
)
