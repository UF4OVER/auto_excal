# -*- coding: utf-8 -*-
# -------------------------------
#  @Project : siui_refactor
#  @Time    : 2025 - 06-21 21:44
#  @FileName: init_edge.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------
import config.CONFIG as F
from DrissionPage import ChromiumOptions
PATH_CONFIG = F.CONFIG_PATH

try:
    broswer_address = F.READ_CONFIG("chromium_options", "address")
    browser_path = F.READ_CONFIG("chromium_options", "browser_path")

except Exception as e:
    print(f"config.ini 配置文件读取失败: {e}")
    browser_path = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    broswer_address = "127.0.0.1:9222"
finally:
    print("*" * 20 + "broswer" + "*" * 20)
    print(f"浏览器路径:{browser_path}")
    print(f"浏览器地址:{broswer_address}")
    print("*" * 20 + "finish" + "*" * 20)

co = ChromiumOptions()
co.set_browser_path(browser_path)
co.set_address(broswer_address)