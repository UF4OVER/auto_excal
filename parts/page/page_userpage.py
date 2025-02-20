# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QBoxLayout

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

#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

PIC_PATH = F.PNG_PATH
from PyQt5.QtCore import Qt
from siui.components.page import SiPage
from siui.components.titled_widget_group import SiTitledWidgetGroup
from siui.components.container import SiDenseContainer
from siui.core import Si, SiGlobal

class User(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPadding(64)
        self.setScrollMaximumWidth(1000)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("个人主页")  # 设置标题

        # 创建控件组
        self.titled_widgets_group = SiTitledWidgetGroup(self)
        self.titled_widgets_group.setSiliconWidgetFlag(Si.EnableAnimationSignals)

        self.login_button_container()

        SiGlobal.siui.reloadStyleSheetRecursively(self)

        # 添加页脚的空白以增加美观性
        self.titled_widgets_group.addPlaceholder(64)
        # 设置控件组为页面对象
        self.setAttachment(self.titled_widgets_group)

    def setup_login(self):
        self.base_container = SiDenseContainer(self, QBoxLayout.TopToBottom)



    def setup_user(self):
        pass
    # todo
