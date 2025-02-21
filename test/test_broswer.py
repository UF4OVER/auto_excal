# -*- coding: utf-8 -*-

#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

from DrissionPage import ChromiumOptions, Chromium
# co = ChromiumOptions(read_file=True, ini_path=r"E:\Add_score\auto_excal-siui\config\config.ini")
# 接管9333端口的浏览器，如该端口空闲，启动一个浏览器
browser = Chromium(9333)
# browser = Chromium('127.0.0.1:9333')


# 导入 ChromiumOptions
# from DrissionPage import Chromium, ChromiumOptions
#
# # 创建浏览器配置对象，指定浏览器路径
# co = ChromiumOptions().set_browser_path(r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')
# # 用该配置创建页面对象
# browser = Chromium(addr_or_opts=co)