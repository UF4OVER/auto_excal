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
from PyQt5.QtCore import Qt, pyqtSignal
from siui.components.page import SiPage
from siui.components.titled_widget_group import SiTitledWidgetGroup
from siui.components.widgets import (
    SiPixLabel,
)
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

    def login_button_container(self):
        with self.titled_widgets_group as g:
            login_button_container = SiDenseContainer(self)

            huawei_logom_pixlabel = PixButton(self)
            huawei_logom_pixlabel.setFixedSize(100, 100)
            huawei_logom_pixlabel.setBorderRadius(5)
            huawei_logom_pixlabel.load(f"{PIC_PATH}\\login_pix\\huawei.png")
            huawei_logom_pixlabel.clilked.connect(lambda: self.huawei_login())

            github_logom_pixlabel = PixButton(self)
            github_logom_pixlabel.setFixedSize(100, 100)
            github_logom_pixlabel.setBorderRadius(5)
            github_logom_pixlabel.load(f"{PIC_PATH}\\login_pix\\github.jpg")
            github_logom_pixlabel.clilked.connect(lambda: self.github_login())

            login_button_container.addWidget(huawei_logom_pixlabel)
            login_button_container.addWidget(github_logom_pixlabel)
            login_button_container.adjustSize()

            g.addWidget(login_button_container)

    def huawei_login(self):
        from parts.event.login import LoginHuawei
        login = LoginHuawei()
        login.run()

    def github_login(self):
        from parts.event.login import LoginGithub
        login = LoginGithub()
        login.run()


class PixButton(SiPixLabel):
    clilked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, ev):
        self.clilked.emit()
