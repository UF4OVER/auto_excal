#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

from cx_Freeze import setup, Executable

pic_path = "E:\\python\\auto_excal_new\\siui\\pic"
build_exe_options = {
    "packages": [
        "PyQt5.QtCore",
        "PyQt5.QtGui",
        "PyQt5.QtWidgets",
        "siui",
        "icons",
        "parts",
        "config",
        "openpyxl",
        "ui",
        "DrissionPage",
        "mutagen.mp3",
        "music",
        "pycaw",
        "wmi",
        "comtypes",
        "pic"
    ],
    "include_files": [
    ],
    "excludes": [
        "scipy",
        "scipy.libs",
        "matplotlib",
        "backports",        # 通常用于兼容旧版 Python，如果您运行的是现代 Python 版本（如 3.8+），可以移除。
        "PIL",
        "lib2to3",
        "cryptography",
        "setuptools",
        "tkinter",          # 排除 tkinter 以减小体积
        "unittest",         # 排除测试模块
        "email",            # 排除 email 模块
        "pydoc",            # 排除文档模块
    ],
    # "zip_include_packages": ["*"],
    # #
    # "zip_exclude_packages": ["siui",
    #                          "ui",
    #                          "icons",
    #                          "config",
    #                          "music"
    #                          ]
}

# 设置 GUI 基础
base = "Win32GUI"

setup(
    name='Wedding Invitation',
    version='1.1.3.3',
    url='https://github.com/UF4OVER',
    license='MIT',
    author='UF4',
    author_email='uf4hp@foxmail.com',
    description='Wedding Invitation 系列',
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            script="start.py",
            target_name="Wedding Invitation",
            base=base,
            icon="pic/logo.ico"
        )
    ]
)
