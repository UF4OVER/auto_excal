# -*- coding: utf-8 -*-
# -------------------------------
#  @Project : upper_computer
#  @Time    : 2025 - 01-16 16:18
#  @FileName: page_3dviewer.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------
import os

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from siui.components import SiPixLabel
from siui.components.option_card import SiOptionCardLinear
from siui.components.page import SiPage
from siui.components.titled_widget_group import SiTitledWidgetGroup
from siui.components.widgets import (
    SiDenseHContainer,
    SiDenseVContainer,
    SiLabel,
    SiPushButton,
)
from siui.core import GlobalFont, Si, SiColor, SiGlobal
from siui.gui import SiFont


class Q3DV(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPadding(64)
        self.setScrollMaximumWidth(1000)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("3D VIEWER")  # 设置标题

        # 创建控件组
        self.titled_widgets_group = SiTitledWidgetGroup(self)
        self.titled_widgets_group.setSiliconWidgetFlag(Si.EnableAnimationSignals)

        SiGlobal.siui.reloadStyleSheetRecursively(self)

        self.setup_widgets()
        # 添加页脚的空白以增加美观性
        self.titled_widgets_group.addPlaceholder(64)
        # 设置控件组为页面对象
        self.setAttachment(self.titled_widgets_group)


    def setup_widgets(self):
        with self.titled_widgets_group as group:
            group.addTitle("3D VIEWER")
        
            # 添加浏览器窗口
            self.browser = QWebEngineView()
            self.browser.setUrl(QUrl("https://vpn.neepu.edu.cn/portal/#!/login"))  # 设置加载的3D模型文件路径
            self.browser.resize(800, 600)
            vertical_vessel = SiDenseVContainer()
            vertical_vessel.addWidget(self.browser)
            vertical_vessel.setSpacing(64)
            group.addWidget(vertical_vessel)

