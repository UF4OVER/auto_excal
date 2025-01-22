# -*- coding: utf-8 -*-

#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

# -------------------------------
#  @Project : siui
#  @Time    : 2025 - 01-22 22:16
#  @FileName: page_updatepage.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------
import os

import requests
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QTableWidget, QFileDialog, QTableWidgetItem, QAbstractItemView
from openpyxl.reader.excel import load_workbook
from siui.components import SiLabel, SiTitledWidgetGroup, SiLongPressButton, SiOptionCardLinear, SiDenseHContainer, \
    SiDenseVContainer, SiOptionCardPlane, SiPushButton
from siui.components.button import SiSwitchRefactor, SiPushButtonRefactor, SiProgressPushButton
from siui.components.editbox import SiLineEdit
from siui.components.page import SiPage
from siui.components.spinbox.spinbox import SiIntSpinBox
from siui.core import SiGlobal, SiColor, Si
from parts.event.send_message import show_message
from PyQt5.QtCore import Qt
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


class UpDatePage(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPadding(64)
        self.setScrollMaximumWidth(1000)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("更新")  # 设置标题

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
            group.addTitle("文件夹")
            self.choose_btu = SiLongPressButton(self)
            self.choose_btu.resize(128, 32)
            self.choose_btu.setHint("长按选择文件夹")
            self.choose_btu.attachment().setText("选择文件夹")

            boswer_filter = SiOptionCardLinear(self)
            boswer_filter.setTitle("新版本所在文件夹", "选择文件夹来储存新版本")
            boswer_filter.load(SiGlobal.siui.iconpack.get("ic_fluent_folder_add_filled"))
            boswer_filter.addWidget(self.choose_btu)

            group.addWidget(boswer_filter)

        with self.titled_widgets_group as group:
            group.addTitle("检查更新")
            self.check_btu = SiProgressPushButton(self)
            self.check_btu.resize(128, 32)
            self.check_btu.setText("检查新版本")
            self.check_btu.clicked.connect(self.get_file_content)

            boswer_filter = SiOptionCardLinear(self)
            boswer_filter.setTitle("检查更新", "检测是否发布了新版本")
            boswer_filter.load(SiGlobal.siui.iconpack.get("ic_fluent_cloud_checkmark_filled"))
            boswer_filter.addWidget(self.check_btu)

            group.addWidget(boswer_filter)




