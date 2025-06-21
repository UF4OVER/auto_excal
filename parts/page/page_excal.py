# -*- coding: utf-8 -*-
# -------------------------------
#  @Project : siui_refactor
#  @Time    : 2025 - 06-21 21:42
#  @FileName: page_excal.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------
#  Copyright (c) 2025 UF4OVER
#   All rights reserved.
import random
from contextlib import contextmanager

from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QBoxLayout, QButtonGroup, QWidget, QTableWidget

from siui.components import SiDenseHContainer, SiDenseVContainer, SiTitledWidgetGroup
from siui.components.button import (
    SiFlatButton,
    SiFlatButtonWithIndicator,
    SiLongPressButtonRefactor,
    SiProgressPushButton,
    SiPushButtonRefactor,
    SiRadioButtonR,
    SiRadioButtonWithAvatar,
    SiRadioButtonWithDescription,
    SiSwitchRefactor,
    SiToggleButtonRefactor,
)
from siui.components.chart import SiTrendChart
from siui.components.container import SiDenseContainer, SiTriSectionPanelCard, SiTriSectionRowCard
from siui.components.editbox import SiCapsuleEdit, SiDoubleSpinBox, SiLineEdit, SiSpinBox
from siui.components.label import SiLinearIndicator, SiLinearPartitionIndicator
from siui.components.page import SiPage
from siui.components.slider_ import SiCoordinatePicker2D, SiCoordinatePicker3D, SiSlider
from siui.core import SiGlobal
from siui.gui import SiFont


class Excal(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPadding(64)
        self.setScrollMaximumWidth(1000)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("重构")

        # 创建控件组
        self.titled_widgets_group = SiTitledWidgetGroup(self)
        self.titled_widgets_group.setSpacing(32)
        self.titled_widgets_group.setAdjustWidgetsSize(True)  # 禁用调整宽度
        with self.titled_widgets_group as group:
            group.addTitle("编辑表格")

            self.first_table_widget = QTableWidget(self)
        # 添加页脚的空白以增加美观性
        self.titled_widgets_group.addPlaceholder(64)

        # 设置控件组为页面对象
        self.setAttachment(self.titled_widgets_group)
