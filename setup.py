import os
import sys
from cx_Freeze import setup, Executable


zlib_dll_path = "E:\\python\\file_asa\\auto_excal\\zlib.dll"

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
        ("icon.ico", "icon.ico"),
        (zlib_dll_path, "zlib.dll"),
    ],
    "excludes": []
}

base = "Win32GUI"

setup(
    name="原神",
    version="2.5.0",
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
