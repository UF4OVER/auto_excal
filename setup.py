import sys
from cx_Freeze import setup, Executable
from PyQt5.QtCore import QLibraryInfo

qml_dir = QLibraryInfo.location(QLibraryInfo.Qml2ImportsPath)
print(qml_dir)

resource_path = "E:\\python\\upper_computer\\config"
# 定义构建选项
# 添加依赖包
build_exe_options = {
    "packages": [
    "PyQt5.QtCore",
    "PyQt5.QtGui",
    "PyQt5.QtWidgets",
    "siui",
    "qfluentwidgets",
    "icons",
    "patrs",
    "network",
    "sys",
    "openpyxl",
    "ui",
    "json",
    "DrissionPage"
    ],
    "include_files": [
        (resource_path, "config"),
        (qml_dir, "qml")
    ],
    "excludes": [
    ]
}

# 设置 GUI 基础
base = "Win32GUI"
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name='my_apps',
    version='1.0.0',
    url='https://github.com/UF4OVER',
    license='MIT',
    author='UF4',
    author_email='uf4hp@foxmail.com',
    description='app',
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            script="start.py",
            base=base
            # icon="icon.ico"
        )
    ]
)