import sys
from cx_Freeze import setup, Executable

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
    "parts",
    "network",
    "sys",
    "openpyxl",
    "ui",
    "json",
    "DrissionPage"
    ],
    "include_files": [
        (resource_path, "config"),

    ],
    "excludes": [
    "scipy",
    "scipy.libs",
    "lxml",
    "PIL",
    "setuptools",

    "sqlite3.dll",
    "tcl86t.dll",
    "tk86k.dll",
    "libcrypto-3-x64.dll",
    "libssl-3-x64.dll",


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