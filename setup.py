import sys
from cx_Freeze import setup, Executable
# cx_Freeze配置
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

base = "Win32GUI"


setup(
    name="原神",
    version="2.4.6",
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
