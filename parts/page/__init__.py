# -*- coding: utf-8 -*-

#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

# -------------------------------
#  @Project : siui
#  @Time    : 2025 - 01-22 15:40
#  @FileName: __init__.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------

# 注册页面
from .page_aboutpage import About
from .page_autoexcalpage import Autoexcal
from .page_homepage import Homepage
from .page_musicpage import PageMusicPage
from .page_settingpage import PageSettingPage
from .page_userpage import User

SettingPage = PageSettingPage
AutoFormPage = Autoexcal
MusicPage = PageMusicPage
HomePage = Homepage
UserPage = User
AboutPage = About
