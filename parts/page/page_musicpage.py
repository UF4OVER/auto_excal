#  Copyright (c) 2025 UF4OVER
#   All rights reserved.
import os
import shutil

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QApplication
from siui.components import SiTitledWidgetGroup, SiMasonryContainer
from siui.components.button import (
    SiPushButtonRefactor,
)
from siui.components.page import SiPage
from siui.components.widgets import (
    SiDenseHContainer,
    SiSimpleButton,
    SiLineEdit)
from siui.core import Si, SiGlobal
from typing_extensions import Union

import config.CONFIG
from parts.component.MusicPresenter import SiMusicDisplayer, MusicManager

PATH_MUSIC = config.CONFIG.MUSIC_PATH


class search_box(SiLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.button = SiSimpleButton(self)
        self.button.resize(24, 24)
        self.button.attachment().setSvgSize(16, 16)
        self.button.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_search_filled"))
        self.button.clicked.connect(self.llll)
        self.container().setSpacing(0)
        self.container().addPlaceholder(8, "right")
        self.container().addWidget(self.button, "right")

    def llll(self):
        self.lineEdit().setText("嘿嘿嘿~ ~ ~，这功能我还没写呢:)")

    def setText(self, txt: str):
        self.lineEdit().setText(txt)


class PageMusicPage(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPadding(64)
        self.setScrollMaximumWidth(1100)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("音乐")  # 设置标题

        # 创建控件组
        self.line_edit_with_button = search_box(self)
        self.line_edit_with_button.resize(512, 32)
        self.line_edit_with_button.setText("点击右侧按钮搜索")

        self.add_music_btu = SiPushButtonRefactor(self)
        self.add_music_btu.setFixedSize(512, 32)
        self.add_music_btu.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_add_circle_regular"))
        self.add_music_btu.setText("添加音乐")
        self.add_music_btu.clicked.connect(self.AddMusic)
        self.add_music_btu.setToolTip("只能添加.mp3格式的音乐")
        self.add_music_btu.adjustSize()

        self.titled_widgets_group = SiTitledWidgetGroup(self)
        self.titled_widgets_group.setSiliconWidgetFlag(Si.EnableAnimationSignals)

        self.scroll_container = SiDenseHContainer(self.titled_widgets_group)
        self.scroll_container.addWidget(self.line_edit_with_button)
        self.scroll_container.addWidget(self.add_music_btu)
        self.scroll_container.adjustSize()

        self.titled_widgets_group.addWidget(self.scroll_container)

        self.setupUi()

        SiGlobal.siui.reloadStyleSheetRecursively(self)
        self.titled_widgets_group.adjustSize()
        # 添加页脚的空白以增加美观性
        self.titled_widgets_group.addPlaceholder(64)
        self.setAttachment(self.titled_widgets_group)

    def setupUi(self):
        self.players = MusicManager()
        with self.titled_widgets_group as group:
            self.displayer_container = SiMasonryContainer(self)
            self.displayer_container.setColumns(2)
            self.displayer_container.setColumnWidth(512)
            self.displayer_container.setFixedWidth(512 + 512 + 16)
            self.displayer_container.setSpacing(horizontal=16, vertical=16)

            mp3_files = []
            for root, dirs, files in os.walk(PATH_MUSIC):
                for file in files:
                    if file.lower().endswith('.mp3'):
                        mp3_files.append(os.path.join(root, file))

            for i, mp3_path in enumerate(mp3_files):
                displayer = SiMusicDisplayer(self)
                displayer.resize(512, 128)
                displayer.loadMusic(mp3_path)  # noqa: E501
                self.displayer_container.addWidget(displayer)
                self.players.add_music_displayer(displayer)
            group.addWidget(self.displayer_container)
            group.adjustSize()

    def AddMusic(self):
        AddMusic_path, _ = QFileDialog.getOpenFileName(self, "选择音乐文件", "", "*.mp3")
        if AddMusic_path:
            try:
                # 确保目标目录存在
                if not os.path.exists(PATH_MUSIC):
                    os.makedirs(PATH_MUSIC)
                # 复制文件
                shutil.copy(AddMusic_path, PATH_MUSIC)
                print(f"{AddMusic_path}::: successfully copied to :::{PATH_MUSIC}")
                # 重新加载界面
                # self.displayer_container.arrangeWidgets()
                self.displayer_container.adjustSize()
                # 强制刷新界面
                self.adjustSize()
            except IOError as e:
                print(f"无法复制文件: {str(e)}")
            except Exception as e:
                print(f"复制文件时发生错误: {str(e)}")
        else:
            print("未选择文件")

    def showEvent(self, a0):
        super().showEvent(a0)
