# -*- coding: utf-8 -*-
import configparser
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
from datetime import datetime
import pytz


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


def READ_CONFIG(cls: str, name: str) -> str | int | bool | list:
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH, encoding='utf-8')
    return config.get(cls, name)


def WRITE_CONFIG(cls: str, name: str, value: str | int | bool | list):
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH, encoding='utf-8')
    config.set(cls, name, value)
    with open(CONFIG_PATH, 'w', encoding='utf-8') as configfile:
        config.write(configfile)


utc_now = datetime.utcnow()
eastern = pytz.timezone('Asia/Shanghai')
today = utc_now.replace(tzinfo=pytz.utc).astimezone(eastern).strftime("%Y-%m-%d")


if READ_CONFIG("date", "time") != today:
    WRITE_CONFIG('date', 'time', today)
    WRITE_CONFIG("Email", "email_send", "True")
else:
    print("时间未更新")

