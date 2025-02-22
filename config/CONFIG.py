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
from datetime import datetime
from enum import Enum
from pathlib import Path
import configparser
import pytz

BASE_DIR = Path(__file__).resolve().parent.parent
print(f"配置路径: {BASE_DIR}")
CONFIG_PATH: Path = BASE_DIR / "config" / "config.ini"
print(f"配置文件路径: {CONFIG_PATH}")


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
else:
    print("时间未更新")

TODAY = today


class CONFIG(Enum):
    PATH_LOGIN_PIC: Path = BASE_DIR / "pic" / "login_pix"
    PATH_PNG: Path = BASE_DIR / "pic" / "res"
    PATH_MUSIC: Path = BASE_DIR / "music"
    PATH_HTML: Path = BASE_DIR / "parts" / "html"
    PATH_USER_INFO: Path = BASE_DIR / "config" / "user_info"
    VERSION: str = READ_CONFIG("version", "version")
    AUTHOR: str = READ_CONFIG("version", "author")

PIC_LOGIN_PATH: Path = CONFIG.PATH_LOGIN_PIC.value
PNG_PATH: Path = CONFIG.PATH_PNG.value
MUSIC_PATH: Path = CONFIG.PATH_MUSIC.value
HTML_PATH: Path = CONFIG.PATH_HTML.value
USER_INFO_PATH: Path = CONFIG.PATH_USER_INFO.value
VERSION: str = CONFIG.VERSION.value
AUTHOR: str = CONFIG.AUTHOR.value
print("-"*20 + "info" + "-"*20)
print(f"全局版本: {VERSION}")
print(f"全局作者: {AUTHOR}")
print("-"*20 + "file" + "-"*20)
print(f"全局图片文件路径: {PNG_PATH}")
print(f"全局音乐文件路径: {MUSIC_PATH}")
print(f"全局HTML文件路径: {HTML_PATH}")
print(f"全局用户文件路径: {USER_INFO_PATH}")
print("-"*20 + "start" + "-"*20)


