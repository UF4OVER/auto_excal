# -*- coding: utf-8 -*-
#  Copyright (c) 2025 UF4OVER
#   All rights reserved.
import configparser
import requests
from parts.event.send_message import show_message
import config.CONFIG

PATH_CONFIG = config.CONFIG.CONFIG_PATH

config = configparser.ConfigParser()

config.read(PATH_CONFIG,encoding='utf-8')

config = config["version"]
VERSION = config["version"]
URL = config["url"]


def get_file_content():
    try:
        response = requests.get(URL)
        response.raise_for_status()  # 检查请求是否成功
        content = response.text

        if content == VERSION:
            show_message(1, "版本更新", f"当前版本已是最新版本{VERSION}", "ic_fluent_globe_error_filled")
            print(F"当前版本已是最新版本{VERSION}")
            return False
        if content != VERSION:
            show_message(3, "版本更新", f"发现了最新版本{content}", "ic_fluent_globe_arrow_up_filled")
            print(F"发现了最新版本{content}")
            return True

    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}")
        show_message(1, "请求出错", f"请求出错: {e}", "ic_fluent_globe_error_filled")
        return False
