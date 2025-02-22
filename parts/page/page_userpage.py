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

import config.CONFIG as F

PIC_PATH = F.PNG_PATH

from PyQt5.QtCore import Qt

from siui.components.page import SiPage
from siui.core import SiGlobal
from siui.components.container import SiDenseContainer

from parts.component import LoginToPortlet


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
