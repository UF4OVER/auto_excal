import sys
from cx_Freeze import setup, Executable


"""
#import json
#import pyautogui
#from qt_material import apply_stylesheet
#from PyQt5.QtCore import pyqtSignal
#from PyQt5.QtGui import QColor, QTextCharFormat
#from openpyxl.reader.excel import load_workbook
import main_window as m
import small_window as s
#from PyQt5.QtWidgets import QApplication,QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox, \
    QInputDialog, QLineEdit
#import threading
#import time
#from pynput import mouse"""


# 定义构建选项
build_exe_options = {
    "packages": [
        "threading", "time", "pyautogui", "pynput",
        "PyQt5.QtCore", "PyQt5.QtGui", "PyQt5.QtWidgets",
        "openpyxl", "json", "qt_material", "sys"
    ],
    "include_files": [
        ("icon.ico")
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
    version="2.2.0",
    description="AUTO-INPUT",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "main.py",
            target_name="原神",
            base=base,
            icon="icon.ico"
        )
    ]
)
