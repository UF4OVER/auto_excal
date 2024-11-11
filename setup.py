import sys
from cx_Freeze import setup, Executable

# 定义构建选项
# 添加依赖包
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
# 默认为 None
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# 设置项目信息
# 添加作者信息
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
