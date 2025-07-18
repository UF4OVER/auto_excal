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
import json
import os
import time

from DrissionPage._base.chromium import Chromium
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QBoxLayout, QTableWidget, QAbstractItemView, QFileDialog, QTableWidgetItem
from openpyxl.reader.excel import load_workbook

from siui.components import SiDenseHContainer, SiDenseVContainer, SiTitledWidgetGroup, SiOptionCardLinear, \
    SiOptionCardPlane, SiLabel, SiLongPressButton
from siui.components.button import (
    SiPushButtonRefactor,
    SiSwitchRefactor,
)
from siui.components.container import SiDenseContainer
from siui.components.editbox import SiLineEdit
from siui.components.page import SiPage
from siui.core import SiGlobal

from config import Settings
from parts.component.ShowMessage import show_message
from parts.component.qss import TabelQss
from parts.event.parser import delete_data_for_table_widget, import_file_for_table_widget, \
    reload_data_for_new_table_widget


def limit_for_table(func):
    """
    装饰器：判断self.sheet 是否 有效，有效的话执行func函数
    """

    def wrapper(self):
        if self.sheet:
            return func(self)
        else:
            print("无效，无法执行操作")
            show_message(4, "错误", "康康表格是否有问题？？？", "ic_fluent_error_circle_regular")
            return None

    return wrapper
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
            self.duplicate_filter_btu.setChecked(False)
            self.duplicate_filter_btu.clicked.connect(self.update_flag)

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

        with self.titled_widgets_group as group:
            table_widget_height = 900
            table_widget_width = 500

            new_table_widget_height = 700
            new_table_widget_width = 500
            group.addTitle("表格数据")

            auto_input_widget_box = SiOptionCardPlane(self)
            auto_input_widget_box.adjustSize()
            auto_input_widget_box.setTitle("原始表格数据")
            auto_input_widget_box.body().setFixedSize(table_widget_height + 40, table_widget_width + 40)
            auto_input_widget_box.footer().setFixedHeight(40)

            self.table_widget = QTableWidget(self)
            self.table_widget.setStyleSheet(TabelQss)
            self.table_widget.setFixedSize(table_widget_height, table_widget_width)

            self.clear_data_btu = SiLongPressButton(self)
            self.clear_data_btu.resize(80, 32)
            self.clear_data_btu.attachment().setText("清除数据")
            self.clear_data_btu.longPressed.connect(lambda:
                                                    delete_data_for_table_widget(
                                                        self.table_widget,
                                                        self.new_table_widget))

            choose_file_btu = SiPushButtonRefactor(self)
            choose_file_btu.setText("选择文件")
            choose_file_btu.clicked.connect(lambda: import_file_for_table_widget(self.table_widget))

            auto_input_widget_box.header().addWidget(choose_file_btu, "right")
            auto_input_widget_box.body().addWidget(self.table_widget)
            auto_input_widget_box.footer().addWidget(Label(self, "使用表格数据时，请确保表格数据与输入框对应"))
            auto_input_widget_box.footer().addWidget(self.clear_data_btu, "right")

            new_input_widget_box = SiOptionCardPlane(self)
            new_input_widget_box.adjustSize()
            new_input_widget_box.setTitle("自定义表格数据")
            new_input_widget_box.body().setFixedSize(new_table_widget_height + 40, new_table_widget_width + 70)
            new_input_widget_box.footer().setFixedHeight(40)

            reload_the_data_btu = SiPushButtonRefactor(self)
            reload_the_data_btu.setText("加载数据")
            reload_the_data_btu.clicked.connect(lambda:
                                                reload_data_for_new_table_widget(
                                                    self.new_table_widget, self.table_widget,
                                                    self.choose_switch,
                                                    self.start_input, self.finish_input,
                                                    self.start_input1, self.finish_input1,
                                                    self.start_input2, self.finish_input2))

            new_input_widget_box.header().addWidget(reload_the_data_btu, "right")

            self.new_table_widget = QTableWidget(self)
            self.new_table_widget.setStyleSheet(TabelQss)
            self.new_table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.new_table_widget.setFixedSize(int(new_table_widget_height * 0.7), new_table_widget_width)
            # 设置第一列的宽度为100，第二行为200，第三行为80
            self.new_table_widget.setColumnWidth(0, 100)
            self.new_table_widget.setColumnWidth(1, 300)
            self.new_table_widget.setColumnWidth(2, 100)

            # 此容器左侧用于放置表格数据，右侧放置按钮
            operate_the_container_h = SiDenseHContainer(self)
            # 此容器用于放置表格数据
            vertical_container_for_tabular_data = SiDenseVContainer(self)
            vertical_container_for_tabular_data.addWidget(self.new_table_widget)
            # 此容器用于放置按钮
            btu_container_for_vertical_container = SiDenseVContainer(self)

            self.open_web_btu = SiPushButtonRefactor(self)
            self.open_web_btu.setText("打开浏览器")
            self.open_web_btu.setFixedSize(128, 32)
            # self.open_web_btu.clicked.connect(self.open_broswer)

            self.start_btu = SiPushButtonRefactor(self)
            self.start_btu.setText("开始")
            self.start_btu.setFixedSize(128, 32)
            # self.start_btu.clicked.connect(self.start_main_loop_in_thread)

            self.stop_btu = SiPushButtonRefactor(self)
            self.stop_btu.setText("停止")
            self.stop_btu.setFixedSize(128, 32)
            # self.stop_btu.clicked.connect(self.stop_main_loop_in_thread)

            self.delete_btu = SiPushButtonRefactor(self)
            self.delete_btu.setText("删除")
            self.delete_btu.setFixedSize(210, 32)
            # self.delete_btu.clicked.connect(self.del_data_for_new_table)

            self.insert_btu = SiPushButtonRefactor(self)
            self.insert_btu.setText("插入")
            self.insert_btu.setFixedSize(210, 32)
            # self.insert_btu.clicked.connect(self.insert_data_for_new_table)
            # insert data
            self.data1_input = SiLineEdit(self)
            self.data1_input.setTitleWidth(50)
            self.data1_input.setTitle("姓名")
            self.data1_input.setText("何平")
            self.data1_input.resize(210, 32)

            self.data2_input = SiLineEdit(self)
            self.data2_input.setTitleWidth(50)
            self.data2_input.setTitle("学号")
            self.data2_input.setText("2023303010311")
            self.data2_input.resize(210, 32)

            self.data3_input = SiLineEdit(self)
            # self.data3_input.setLabelWidth(100)
            self.data3_input.setTitle("分数")
            self.data3_input.setTitleWidth(50)
            self.data3_input.setText("3")
            self.data3_input.resize(210, 32)

            btu_container_for_vertical_container.addWidget(self.data1_input)
            btu_container_for_vertical_container.addWidget(self.data2_input)
            btu_container_for_vertical_container.addWidget(self.data3_input)
            btu_container_for_vertical_container.addWidget(self.insert_btu)
            btu_container_for_vertical_container.addWidget(self.delete_btu)

            temp_h = SiDenseHContainer(self)

            temp_h.addWidget(self.open_web_btu)
            temp_h.addWidget(self.start_btu)
            temp_h.addWidget(self.stop_btu)

            vertical_container_for_tabular_data.addWidget(temp_h)

            operate_the_container_h.addWidget(vertical_container_for_tabular_data)
            operate_the_container_h.addWidget(btu_container_for_vertical_container)

            new_input_widget_box.body().addWidget(operate_the_container_h)
            new_input_widget_box.footer().addWidget(Label(self, "使用表格数据时，请确保表格数据与输入框对应"))

            group.addWidget(auto_input_widget_box)
            group.addWidget(new_input_widget_box)

            # 调整父部件大小
            auto_input_widget_box.adjustSize()
            new_input_widget_box.adjustSize()
            group.adjustSize()
            self.adjustSize()
    def update_flag(self):
        Settings.duplicate_filter = self.duplicate_filter_btu.isChecked()
