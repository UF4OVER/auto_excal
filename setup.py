#  Copyright (c) 2025. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

import sys
from cx_Freeze import setup, Executable

pic_path = "E:\\python\\auto_excal_new\\siui\\pic"
# 定义构建选项
# 添加依赖包
build_exe_options = {
    "packages": [
    "PyQt5.QtCore",
    "PyQt5.QtGui",
    "PyQt5.QtWidgets",
    "siui",
    "icons",
    "parts",
    "sys",
    "os",
    "config",
    "openpyxl",
    "ui",
    "json",
    "DrissionPage"
    ],
    "include_files": [
        (pic_path, "pic"),
    ],
    "excludes": [
    "scipy",
    "scipy.libs",
    "setuptools",
    ]
}

# 设置 GUI 基础
base = "Win32GUI"
# if sys.platform == "win32":
#     base = "Win32GUI"
# base = None

setup(
    name='Wedding Invitation',
    version='1.0.1',
    url='https://github.com/UF4OVER',
    license='MIT',
    author='UF4',
    author_email='uf4hp@foxmail.com',
    description='app',
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            script="start.py",
            base=base,
            icon="pic/圆角-default_256x256.ico"
        )
    ]
)