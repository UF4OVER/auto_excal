# -*- coding: utf-8 -*-

#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

# ------------------------------
#  @Project : upper_computer
#  @Time    : 2024 - 12-22 14:55
#  @FileName: CONFIG.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 3.10
# -------------------------------
import enum
import os

from sys_std_io import setup_logging

setup_logging(False)


class CONFIG(enum.Enum):
    PATH_CONFIG: str = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
        ), 'config.ini')

    PATH_PNG: str = os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        ), "pic")

    PATH_MUSIC: str = os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        ), "music")


CONFIG_PATH: str = CONFIG.PATH_CONFIG.value
PNG_PATH: str = CONFIG.PATH_PNG.value
MUSIC_PATH: str = CONFIG.PATH_MUSIC.value

print(f"全局配置文件路径:{CONFIG_PATH}")
print(f"全局图片文件路径:{PNG_PATH}")
print(f"全局音乐文件路径:{MUSIC_PATH}")
