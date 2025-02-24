# -*- coding: utf-8 -*-

#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

# -------------------------------
#  @Project : 11.py
#  @Time    : 2025 - 02-20 15:40
#  @FileName: QuickActions.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------
import config.CONFIG as F

PIC_PATH = F.PNG_PATH
from siui.components.container import SiDenseContainer
from siui.components.button import (
    SiFlatButton,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from siui.core import SiGlobal
from siui.components import SiLabel, SiWidget


class DCHContainer(SiDenseContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.background = SiLabel(self)
        # self.background.setFixedStyleSheet("border-radius: 15px; background-color: #ffffff")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.background.resize(event.size())


class quick_action(SiWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_container = DCHContainer(self)
        self.base_container.resize(200, 32)
        self.w = SiGlobal.siui.windows["MAIN_WINDOW"].width()
        self.h = SiGlobal.siui.windows["MAIN_WINDOW"].height()

        self.setup_btu()

        self.login_info = SiLabel(self)
        self.login_info.resize(120, 28)
        self.login_info.setText("未登录用户")
        self.login_info.setHint("后续可提供登录方式\r\n"
                                "HUAWEI和GitHub")
        self.login_info.setStyleSheet("color: #1ff1f1")
        self.login_info.setFont(QFont("Microsoft YaHei", 8))
        self.base_container.addWidget(self.login_info, Qt.RightEdge)

    def setup_btu(self):
        self.flat_button = SiFlatButton(self)
        self.flat_button.resize(60, 28)
        self.flat_button.setText("ini")
        self.flat_button.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_wrench_settings_filled"))
        self.flat_button.adjustSize()

        self.base_container.addWidget(self.flat_button, Qt.RightEdge)

    def btu(self):
        return self.flat_button

    def set_login_info(self, text):
        self.login_info.setText(text)
        self.login_info.adjustSize()
