# -*- coding: utf-8 -*-
# -------------------------------
#  @Project : 11.py
#  @Time    : 2025 - 02-08 15:50
#  @FileName: setup模板.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------


VERSION_A = "V1.1.5"

from cx_Freeze import setup, Executable

build_exe_options = {
    "packages":
        [
        ],
    "include_files":
        [
        ],
    "excludes":
        [
        ],
    "optimize": 2
    # "zip_include_packages": ["*"],
    #
    # "zip_exclude_packages": []
}

# 设置 GUI 基础
base = "Win32GUI"

setup(
    name='',
    version=VERSION_A,
    url='https://github.com/UF4OVER',
    license='MIT',
    author='UF4',
    author_email='uf4hp@foxmail.com',
    description='',
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            script=".py",
            target_name="",
            base=base,
            icon=".ico"
        )
    ]
)