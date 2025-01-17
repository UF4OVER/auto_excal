#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

import os
import time

from PyQt5.QtCore import Qt
from siui.components import SiPixLabel, Si
from siui.components.page import SiPage
from siui.components.titled_widget_group import SiTitledWidgetGroup
from siui.components.widgets import (
    SiDenseHContainer,
    SiDenseVContainer,
    SiLabel,
)
from siui.core import GlobalFont, SiColor, SiGlobal
from siui.gui import SiFont

from parts.themed_option_card import ThemedOptionCardPlane
from task import TaskCardLinear, Task


class Homepage(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 滚动区域
        self.scroll_container = SiTitledWidgetGroup(self)
        # 整个顶部
        self.head_area = SiLabel(self)
        self.head_area.setFixedHeight(450)
        # 创建背景底图和渐变
        self.background_image = SiPixLabel(self.head_area)
        self.background_image.setFixedSize(1366, 300)
        self.background_image.setBorderRadius(6)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.background_image.load("./pic/ccc.jpg")

        self.background_fading_transition = SiLabel(self.head_area)
        self.background_fading_transition.setGeometry(0, 100, 0, 200)
        self.background_fading_transition.setStyleSheet(
            """
            background-color: qlineargradient(x1:0, y1:1, x2:0, y2:0, stop:0 {}, stop:1 {})
            """.format(SiGlobal.siui.colors["INTERFACE_BG_B"],
                       SiColor.trans(SiGlobal.siui.colors["INTERFACE_BG_B"], 0))
        )
        # 创建背景底图和渐变
        self.title = SiLabel(self.head_area)
        self.title.setGeometry(64, 0, 500, 128)
        self.title.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.title.setText("Wedding Invitation")
        self.title.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_A"]))
        self.title.setFont(SiFont.tokenized(GlobalFont.XL_MEDIUM))

        self.subtitle = SiLabel(self.head_area)
        self.subtitle.setGeometry(64, 72, 500, 48)
        self.subtitle.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.subtitle.setText("A powerful and artistic UI library based on PyQt5")
        self.subtitle.setStyleSheet("color: {}".format(SiColor.trans(SiGlobal.siui.colors["TEXT_A"], 0.9)))
        self.subtitle.setFont(SiFont.tokenized(GlobalFont.S_MEDIUM))

        self.container_for_cards = SiDenseHContainer(self.head_area)
        self.container_for_cards.move(0, 130)
        self.container_for_cards.setFixedHeight(310)
        self.container_for_cards.setAlignment(Qt.AlignCenter)
        self.container_for_cards.setSpacing(32)
        # 添加卡片
        self.option_card_project = ThemedOptionCardPlane(self)
        self.option_card_project.setTitle("GitHub Repo")
        self.option_card_project.setFixedSize(218, 270)
        self.option_card_project.setThemeColor("#855198")
        self.option_card_project.setDescription(
            "connect to my github\r\n"
            "home page.you can click\r\n"
            "btu to mypage")
        self.option_card_project.setURL("https://github.com/UF4OVER/auto_excal")

        self.option_card_example = ThemedOptionCardPlane(self)
        self.option_card_example.setTitle("Bilibili")
        self.option_card_example.setFixedSize(218, 270)
        self.option_card_example.setThemeColor("#FB7299")
        self.option_card_example.setDescription(
            "connect to my bilibili\r\n"
            "home page.you can click\r\n"
            "btu to mypage .")  # noqa: E501
        self.option_card_example.setURL("https://space.bilibili.com/1000215778?spm_id_from=333.1007.0.0")
        # 添加到水平容器
        self.container_for_cards.addPlaceholder(64 - 32)
        self.container_for_cards.addWidget(self.option_card_project)
        self.container_for_cards.addWidget(self.option_card_example)

        # 添加到滚动区域容器
        self.scroll_container.addWidget(self.head_area)

        self.body_area = SiLabel(self)
        self.body_area.setSiliconWidgetFlag(Si.EnableAnimationSignals)
        self.body_area.resized.connect(lambda _: self.scroll_container.adjustSize())

        # 下面的 titledWidgetGroups
        self.titled_widget_group = SiTitledWidgetGroup(self.body_area)
        self.titled_widget_group.setSiliconWidgetFlag(Si.EnableAnimationSignals)
        self.titled_widget_group.resized.connect(lambda size: self.body_area.setFixedHeight(size[1]))
        self.titled_widget_group.move(64, 0)

        # 开始搭建界面
        # 控件的线性选项卡

        self.titled_widget_group.setSpacing(16)
        self.titled_widget_group.addTitle("说明")
        self.titled_widget_group.addWidget(WidgetsPanel(self))

        self.titled_widget_group.addPlaceholder(64)

        # 添加到滚动区域容器
        self.body_area.setFixedHeight(self.titled_widget_group.height())
        self.scroll_container.addWidget(self.body_area)

        # 添加到页面

        self.setAttachment(self.scroll_container)
        self.scroll_container.adjustSize()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w = event.size().width()
        self.body_area.setFixedWidth(w)
        self.background_image.setFixedWidth(w)
        self.titled_widget_group.setFixedWidth(min(w - 128, 900))
        self.background_fading_transition.setFixedWidth(w)


class WidgetsPanel(SiDenseVContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setAdjustWidgetsSize(True)
        self.setSpacing(12)

        container_h_a = SiDenseVContainer(self)
        container_h_a.setSpacing(12)

        self.test_task_card = TaskCardLinear(
            Task("语言详情", "全局语言：python，基本框架：PyQt5，UI框架：siui", "环境开发详情","IDE:Pycharm 24.1.6(pro)，python：3.10，siui：1.0.1",time.time(), self.getColor(SiColor.PROGRESS_BAR_COMPLETING)),
            parent=self)
        self.test_task_card.resize(SiGlobal.siui.windows["MAIN_WINDOW"].height(), 80)

        self.test_task_card2 = TaskCardLinear(
            Task("架构详情", "parts：页面组件，config：注册文件，pic：全局图片", "应用组成架构","parts：页面代码，config：配置文件，pic：页面图片",time.time(), self.getColor(SiColor.PROGRESS_BAR_PROCESSING)),
            parent=self)
        self.test_task_card2.resize(SiGlobal.siui.windows["MAIN_WINDOW"].height(), 80)

        container_h_a.addWidget(self.test_task_card)
        container_h_a.addWidget(self.test_task_card2)
        # 添加两个水平容器到自己
        self.addWidget(container_h_a)

    def resizeEvent(self, event):
        super().resizeEvent(event)
