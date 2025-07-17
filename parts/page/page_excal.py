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

from siui.components import SiDenseHContainer, SiDenseVContainer, SiTitledWidgetGroup, SiOptionCardLinear, \
    SiOptionCardPlane, SiLabel
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

class Label(SiLabel):
    def __init__(self, parent, text):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(32)

        self.setText(text)
        self.adjustSize()
        self.resize(self.width() + 24, self.height())

class ExcalPage(SiPage):
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

        self._init_constant()
        self._init_widgets()

        # 添加页脚的空白以增加美观性
        self.titled_widgets_group.addPlaceholder(64)
        # 设置控件组为页面对象
        self.setAttachment(self.titled_widgets_group)
    def _init_constant(self):
        """常量的初始化"""
        self.choose_switch_flag = False

    def _init_widgets(self):
        """控件的初始化"""
        with self.titled_widgets_group as group:
            group.addTitle("设置")
            self.duplicate_filter_btu = SiSwitchRefactor(self)  # todo : 添加去重按钮
            duplicate_filter_card = SiOptionCardLinear(self)
            duplicate_filter_card.setTitle("去重", "启用以数据去重")
            duplicate_filter_card.load(SiGlobal.siui.iconpack.get("ic_fluent_poll_off_filled"))
            duplicate_filter_card.addWidget(self.duplicate_filter_btu)

        group.addWidget(duplicate_filter_card)

        with self.titled_widgets_group as group:
            self.choose_switch = SiSwitchRefactor(self)  # todo : 添加选择窗口

            data_stream_container = SiDenseContainer(self, QBoxLayout.LeftToRight)
            data_stream_container_v1 = SiDenseContainer(self, QBoxLayout.TopToBottom)
            data_stream_container_v2 = SiDenseContainer(self, QBoxLayout.TopToBottom)

            self.start_input = SiLineEdit(self)
            self.start_input.setTitleWidth(100)
            self.start_input.setTitle("姓名起始")
            self.start_input.setText("(9,5)")
            self.start_input.setFixedSize(350, 32)

            self.finish_input = SiLineEdit(self)
            self.finish_input.setTitleWidth(100)
            self.finish_input.setTitle("姓名结束")
            self.finish_input.setText("(200,5)")
            self.finish_input.setFixedSize(350, 32)

            self.start_input1 = SiLineEdit(self)
            self.start_input1.setTitleWidth(100)
            self.start_input1.setTitle("学号起始")
            self.start_input1.setText("(9,6)")
            self.start_input1.setFixedSize(350, 32)

            self.finish_input1 = SiLineEdit(self)
            self.finish_input1.setTitleWidth(100)
            self.finish_input1.setTitle("学号结束")
            self.finish_input1.setText("(200,6)")
            self.finish_input1.setFixedSize(350, 32)

            self.start_input2 = SiLineEdit(self)
            self.start_input2.setTitleWidth(100)
            self.start_input2.setTitle("分数起始")
            self.start_input2.setText("(9,7)")
            self.start_input2.setFixedSize(350, 32)

            self.finish_input2 = SiLineEdit(self)
            self.finish_input2.setTitleWidth(100)
            self.finish_input2.setTitle("分数结束")
            self.finish_input2.setText("(200,7)")
            self.finish_input2.setFixedSize(350, 32)

            data_stream_container_v1.addWidget(self.start_input)
            data_stream_container_v2.addWidget(self.finish_input)
            data_stream_container_v1.addWidget(self.start_input1)
            data_stream_container_v2.addWidget(self.finish_input1)
            data_stream_container_v1.addWidget(self.start_input2)
            data_stream_container_v2.addWidget(self.finish_input2)

            data_stream_container_v1.adjustSize()
            data_stream_container_v2.adjustSize()

            data_stream_container.addWidget(data_stream_container_v1)
            data_stream_container.addWidget(data_stream_container_v2)

            data_stream_container.adjustSize()

            info_ = Label(self, "启用以自定义添加数据，若不启用，则使用默认设置(一般情况下不建议启用)")

            customize_the_input_box = SiOptionCardPlane(self)
            customize_the_input_box.setTitle("自定义输入框")
            customize_the_input_box.header().addWidget(self.choose_switch, "right")
            customize_the_input_box.body().addWidget(data_stream_container)
            customize_the_input_box.footer().addWidget(info_)
            customize_the_input_box.footer().setFixedHeight(40)

            customize_the_input_box.body().addPlaceholder(20)
            customize_the_input_box.body().adjustSize()

            customize_the_input_box.adjustSize()

            customize_the_input_box.body().setEnabled(False)
            customize_the_input_box.footer().setEnabled(False)

            self.choose_switch.toggled.connect(lambda checked: customize_the_input_box.body().setEnabled(checked))
            self.choose_switch.toggled.connect(lambda checked: customize_the_input_box.footer().setEnabled(checked))

            self.choose_switch.toggled.connect(self.finish_input2.notifyInvalidInput)
            self.choose_switch.toggled.connect(self.finish_input1.notifyInvalidInput)
            self.choose_switch.toggled.connect(self.finish_input.notifyInvalidInput)
            self.choose_switch.toggled.connect(self.start_input.notifyInvalidInput)
            self.choose_switch.toggled.connect(self.start_input2.notifyInvalidInput)
            self.choose_switch.toggled.connect(self.start_input1.notifyInvalidInput)

            group.addWidget(customize_the_input_box)