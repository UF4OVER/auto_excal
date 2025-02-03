# -*- coding: utf-8 -*-
#  Copyright (c) 2025 UF4OVER
#   All rights reserved.
# -------------------------------
#  @Project : zip.py
#  @Time    : 2025 - 02-01 12:09
#  @FileName: test1.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------

import os

def get_local_username():
    try:
        username = os.getlogin()
        print(f"本地账户名: {username}")
    except Exception as e:
        print(f"无法获取本地账户名: {e}")

if __name__ == "__main__":
    get_local_username()
