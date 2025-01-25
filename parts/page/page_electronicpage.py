# -*- coding: utf-8 -*-

#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

# -------------------------------
#  @Project : siui
#  @Time    : 2025 - 01-25 15:06
#  @FileName: page_electronicpage.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------s
from siui.core import Si, SiColor, SiGlobal

from siui.components.widgets import (
    SiCheckBox,
    SiDenseHContainer,
    SiDraggableLabel,
    SiIconLabel,
    SiLabel,
    SiLongPressButton,
    SiPixLabel,
    SiPushButton,
    SiRadioButton,
    SiSimpleButton,
    SiSwitch,
    SiToggleButton,
)
from PyQt5.QtCore import Qt
from siui.components.combobox import SiComboBox
from siui.components.editbox import SiDoubleSpinBox
from siui.components.option_card import SiOptionCardPlane
from siui.components.page import SiPage
from siui.components.titled_widget_group import SiTitledWidgetGroup
from siui.components.widgets import (
    SiDenseHContainer,
)
from siui.components.button import (SiSwitchRefactor,
                                    SiPushButtonRefactor)

from siui.core import Si, SiGlobal
import config.CONFIG as F
from event.send_message import show_message


class PageElectronicComputing(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.E6: list = []
        self.E12: list = []
        self.E24: list = []
        self.E48: list = []
        self.E96: list = []
        self.E192: list = []
        self.EEE: list = []
        self.r1_r2: float = 0
        self.read_res_nominal_resistance()

        self.setPadding(64)
        self.setScrollMaximumWidth(1000)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("电子计算")  # 设置标题

        # 创建控件组
        self.titled_widgets_group = SiTitledWidgetGroup(self)
        self.titled_widgets_group.setSiliconWidgetFlag(Si.EnableAnimationSignals)

        SiGlobal.siui.reloadStyleSheetRecursively(self)
        self.setupUi()
        # 添加页脚的空白以增加美观性
        self.titled_widgets_group.addPlaceholder(64)
        # 设置控件组为页面对象
        self.setAttachment(self.titled_widgets_group)

    def setupUi(self):
        with self.titled_widgets_group as g:
            g.addTitle("电子计算")
            resistors_tab = SiOptionCardPlane(self)
            resistors_tab.setTitle("FB电压计算")

            widget_h = SiDenseHContainer(self)

            self.reference_voltage = SiDoubleSpinBox(self)
            self.reference_voltage.setTitle("参考电压")
            self.reference_voltage.setSingleStep(0.1)
            self.reference_voltage.setValue(1)
            self.reference_voltage.setFixedSize(150, 60)
            self.reference_voltage.adjustSize()

            self.target_voltage = SiDoubleSpinBox(self)
            self.target_voltage.setTitle("目标电压")
            self.target_voltage.setSingleStep(0.1)
            self.target_voltage.setValue(13)
            self.target_voltage.setFixedSize(150, 60)
            self.target_voltage.adjustSize()

            self.resistance_select = SiComboBox(self)
            self.resistance_select.resize(128, 40)
            self.resistance_select.addOption("E6 ±20%")
            self.resistance_select.addOption("E12 ±10%")
            self.resistance_select.addOption("E24 ±5%")
            self.resistance_select.addOption("E48 ±2%")
            self.resistance_select.addOption("E96 ±1%")
            self.resistance_select.addOption("E192 ±0.5%")
            self.resistance_select.menu().setShowIcon(False)
            self.resistance_select.menu().setIndex(2)
            self.resistance_select.moveTo(330, 21)

            self.r1_label = SiLabel(self)
            self.r1_label.setText("R上:")
            self.r1_label.setTextColor(self.getColor(SiColor.TEXT_B))
            self.r1_label.moveTo(500, 30)

            self.r2_label = SiLabel(self)
            self.r2_label.setText("R下:")
            self.r2_label.setTextColor(self.getColor(SiColor.TEXT_B))
            self.r2_label.moveTo(600, 30)

            self.r1_result = SiLabel(self)
            self.r1_result.setText("0.0")
            self.r1_result.setFixedWidth(40)
            self.r1_result.setTextColor(self.getColor(SiColor.TEXT_B))
            self.r1_result.moveTo(540, 30)

            self.r2_result = SiLabel(self)
            self.r2_result.setText("0.0")
            self.r2_result.setFixedWidth(40)
            self.r2_result.setTextColor(self.getColor(SiColor.TEXT_B))
            self.r2_result.moveTo(640, 30)

            self.deviation_label = SiLabel(self)
            self.deviation_label.setText("误差:")
            self.deviation_label.setTextColor(self.getColor(SiColor.TEXT_B))
            self.deviation_label.moveTo(700, 30)

            self.deviation_result = SiLabel(self)
            self.deviation_result.setText("0.0 %")
            self.deviation_result.setTextColor(self.getColor(SiColor.TEXT_B))
            self.deviation_result.setFixedWidth(70)
            self.deviation_result.moveTo(740, 30)

            widget_h.addWidget(self.reference_voltage)
            widget_h.addWidget(self.target_voltage)
            widget_h.addWidget(self.resistance_select)
            widget_h.addWidget(self.r1_label)
            widget_h.addWidget(self.r2_label)
            widget_h.addWidget(self.r1_result)
            widget_h.addWidget(self.r2_result)
            widget_h.addWidget(self.deviation_label)
            widget_h.addWidget(self.deviation_result)

            calculate_btu = SiPushButtonRefactor(self)
            calculate_btu.resize(100, 32)
            calculate_btu.setText("计算")
            calculate_btu.clicked.connect(
                lambda: self.calculate_r1_r2(self.target_voltage.value(), self.reference_voltage.value()))

            resistors_tab.header().addWidget(calculate_btu, "right")
            resistors_tab.body().addWidget(widget_h)
            resistors_tab.body().addPlaceholder(12)

            resistors_tab.adjustSize()

            g.addWidget(resistors_tab)

    def calculate_r1_r2(self, vout: float = 0, vref: float = 0):
        print("-"*70)
        # VOUT = 0.8 × (1 + (R1 ÷ R2))
        if vref == 0 or vref <= 0:
            show_message(1, "错误", "参考电压不正确哦", "ic_fluent_wrench_settings_filled")
            return

        self.r1_r2 = round((vout / vref) - 1, 3)
        print(f"比例系数：{self.r1_r2}")

        match self.resistance_select.value():
            case "E6 ±20%":
                self.EEE = self.E6
                print("E6 ±20%")
            case "E12 ±10%":
                self.EEE = self.E12
                print("E12 ±10%")
            case "E24 ±5%":
                self.EEE = self.E24
                print("E24 ±5%")
            case "E48 ±2%":
                self.EEE = self.E48
                print("E48 ±2%")
            case "E96 ±1%":
                self.EEE = self.E96
                print("E96 ±1%")
            case "E192 ±0.5%":
                self.EEE = self.E192
                print("E192 ±0.5%")
            case _:
                self.EEE = self.E24
                print("E24 ±5%")

        res = []
        err = []
        rat = []
        for r1 in self.EEE:
            for r2 in self.EEE:
                ratio = round(float(r1) / float(r2), 3)
                error = round(abs(ratio - self.r1_r2), 3)

                res.append((r1, r2))
                rat.append(ratio)
                err.append(error)
        # print(f"RES: {res}")
        # print(f"RAT: {rat}")
        # print(f"ERR: {err}")

        min_index, min_value = min(enumerate(err), key=lambda x: x[1])
        self.r1_result.setText(str(res[min_index][0]))
        self.r2_result.setText(str(res[min_index][1]))
        self.deviation_result.setText(str(round(min_value * 100, 2)) + " %")
        print(f"最小误差: {min_value}, 对应的 R1, R2: {res[min_index]}")
        print("-"*70)

    def read_res_nominal_resistance(self):
        self.E6 = list(map(float, F.READ_CONFIG("resistance", "E6").split(",")))
        self.E12 = list(map(float, F.READ_CONFIG("resistance", "E12").split(",")))
        self.E24 = list(map(float, F.READ_CONFIG("resistance", "E24").split(",")))
        self.E48 = list(map(float, F.READ_CONFIG("resistance", "E48").split(",")))
        self.E96 = list(map(float, F.READ_CONFIG("resistance", "E96").split(",")))
        self.E192 = list(map(float, F.READ_CONFIG("resistance", "E192").split(",")))

        # print(f"E6: {self.E6}")
