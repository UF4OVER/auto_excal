from cx_Freeze import setup, Executable

"""
import json
import os
import re
import time
import sys
import pyautogui

from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTranslator, QPoint
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QLineEdit, QAbstractItemView, QVBoxLayout, QLabel, \
    QHBoxLayout, QFileDialog

from setting_interface import SettingInterface
from config import cfg
from new import Ui_Form
from openpyxl.reader.excel import load_workbook
from pynput import mouse

from qfluentwidgets import setThemeColor, Dialog, Flyout, InfoBarIcon, \
    FlyoutAnimationType, PrimaryPushButton, LineEdit, TransparentPushButton, ToolTipFilter, \
    ToolTipPosition, FluentTranslator, isDarkTheme

from qframelesswindow import StandardTitleBar, AcrylicWindow, FramelessWindow
"""

zlib_dll_path = "E:\\python\\file_asa\\auto_excal\\zlib.dll"
resource_path = "E:\\python\\auto_excal_new\\flu\\resource"

build_exe_options = {
    "packages": [
        "json",
        "pyautogui",
        "time",
        "sys",
        "os",
        "re",
        "new",
        "openpyxl.reader.excel",
        "pynput",
        "qfluentwidgets",
        "qframelesswindow",

        "PyQt5.QtCore",
        "PyQt5.QtGui",
        "PyQt5.QtWidgets",
    ],
    "include_files": [
        ("icon.ico", "icon.ico"),
        (zlib_dll_path, "zlib.dll"),
        (resource_path, "resource"),
    ],
    "excludes": [("scipy"),
                 ("scipy.libs"),
                 ("numpy"),
                 ("numpy.libs"),
                 ("PIL"),
                 ("setuptools"),
                 ("email")]
}

base = "Win32GUI"

setup(
    name="原神",
    version="3.1.0",
    description="AUTO-INPUT",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            script="main.py",
            base=base,
            icon="icon.ico"
        )
    ]
)
