#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

VERSION_A = "1.1.5"

from cx_Freeze import setup, Executable
import config.CONFIG as F
from setuptools import setup

F.WRITE_CONFIG("version", "version", VERSION_A)
upx_exe_path = r"E:\python\auto_excal_new\siui\upx.exe"

# 设置 GUI 基础
base = "Win32GUI"


def build_exe_cx_freeze():
    build_exe_options = {
        "packages":
            [
                "PyQt5.QtCore",
                "PyQt5.QtGui",
                "PyQt5.QtWidgets",
                "PyQt5.QtMultimedia",
                "PyQt5.QtNetwork",
                "siui",
                "parts",
                "config",
                "openpyxl",
                "DrissionPage",
                "mutagen.mp3",
                "music",
                "pycaw",
                "wmi",
                "comtypes",
                "pic"
            ],
        "include_files":
            [
                upx_exe_path
            ],
        "excludes":
            [
                "scipy",
                "scipy.libs",
                "matplotlib",
                "backports",
                "PIL",
                "lib2to3",
                "cryptography",
                "setuptools",
                "tkinter",
                "unittest",
                "email",
                "pydoc",
            ],
        "optimize": 2
    }

    setup(
        name='Wedding Invitation',
        version=VERSION_A,
        url='https://github.com/UF4OVER',
        license='MIT',
        author='UF4',
        author_email='uf4hp@foxmail.com',
        description='Loot Hearts 系列',
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



if __name__ == '__main__':
    build_exe_cx_freeze()
