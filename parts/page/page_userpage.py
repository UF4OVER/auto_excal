# -*- coding: utf-8 -*-

#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

# -------------------------------
#  @Project : zip.py
#  @Time    : 2025 - 01-31 12:08
#  @FileName: page_userpage.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact :
#  @Python  :
# -------------------------------


from PyQt5.QtCore import Qt

from siui.components.page import SiPage
from siui.core import SiGlobal
from siui.components.container import SiDenseContainer

from parts.component import LoginToPortlet
from parts.event.login import LoginGithub, LoginHuawei

import config.CONFIG as F

PIC_PATH = F.PNG_PATH


class User(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPadding(64)
        self.setScrollMaximumWidth(1000)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("个人主页")  # 设置标题

        # 创建控件组
        self.titled_widgets_group = SiDenseContainer(self)

        self.setup_login()

        SiGlobal.siui.reloadStyleSheetRecursively(self)
        self.setAttachment(self.titled_widgets_group)

    def setup_login(self):
        self.login_widget = LoginToPortlet(self)
        self.titled_widgets_group.addWidget(self.login_widget, Qt.LeftEdge)

        # 注册LoginToPortlet类的点击事件
        self.login_widget.huawei_login_start_ed.connect(self.huawei_login)
        self.login_widget.github_login_start_ed.connect(self.github_login)

    def huawei_login(self):
        print("华为登录")
        self.huawei_login_thread = LoginHuawei(self)
        self.huawei_login_thread.start()

    def github_login(self):
        print("github登录")
        self.github_login_thread = LoginGithub(self)
        self.github_login_thread.start()
