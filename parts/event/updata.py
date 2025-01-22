# -*- coding: utf-8 -*-
import requests

from parts.event.send_message import show_message

#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

# -------------------------------
#  @Project : siui
#  @Time    : 2025 - 01-22 22:53
#  @FileName: updata.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------
import config.CONFIG

PATH_CONFIG = config.CONFIG.CONFIG_PATH


def get_file_content():
    url = "https://raw.githubusercontent.com/UF4OVER/auto_excal/siui/version"
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        content = response.text
        print("文件内容:")
        print(content)
        return content
    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}")
        show_message(1, "请求出错", f"请求出错: {e}", "ic_fluent_globe_error_filled")
        return ""
