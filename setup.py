# -*- coding: utf-8 -*-
# -------------------------------
#  @Project : flu_new
#  @Time    : 2025 - 02-14 15:25
#  @FileName: setup.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------
#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

VERSION_A = "1.1.5"

from cx_Freeze import setup, Executable


resource_path = "resource"

build_exe_options = {
    "packages":
        [
            "PyQt5.QtWidgets",
            "PyQt5.QtCore",
            "PyQt5.QtGui",
            "PyQt5.QtMultimedia",
            "config",
            "page",
        ],
    "include_files":
        [
            (resource_path, "resource")
        ],
    "excludes":
        [
            "scipy",
            "numpy",
            "matplotlib",
            "pandas",
            "sklearn",
            "tensorflow",
            "pillow",
            "opencv-python",
            "pyqtgraph",
            "pyqt5-sip",
            "PIL",
            "tkinter"
        ],
    "optimize": 2
    # "zip_include_packages": ["*"],
    #
    # "zip_exclude_packages": []
}

# 设置 GUI 基础
base = "Win32GUI"

setup(
    name='test',
    version=VERSION_A,
    url='https://github.com/UF4OVER',
    license='MIT',
    author='UF4',
    author_email='uf4hp@foxmail.com',
    description='sa',
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            script="main.py",
            target_name="auto",
            base=base,
            # icon=".ico"
        )
    ]
)