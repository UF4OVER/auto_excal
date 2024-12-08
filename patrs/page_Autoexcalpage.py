from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from siui.components import SiPixLabel
from siui.components.button import SiSwitchRefactor
from siui.components.option_card import SiOptionCardLinear, SiOptionCardPlane
from siui.components.page import SiPage
from siui.components.slider import SiSliderH
from siui.components.titled_widget_group import SiTitledWidgetGroup
from siui.components.widgets import (
    SiDenseHContainer,
    SiDenseVContainer,
    SiLabel,
    SiLineEdit,
    SiLongPressButton,
    SiPushButton,
    SiSimpleButton,
    SiSwitch,
)
from siui.core import GlobalFont, Si, SiColor, SiGlobal, SiQuickEffect, GlobalFontSize
from siui.gui import SiFont
from siui.components.spinbox.spinbox import SiIntSpinBox
from patrs.themed_option_card import ThemedOptionCardPlane


class Label(SiLabel):
    def __init__(self, parent, text):
        super().__init__(parent)

        self.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(32)

        # self.setFixedStyleSheet("border-radius: 4px")
        self.setText(text)
        self.adjustSize()
        self.resize(self.width() + 24, self.height())

    def reloadStyleSheet(self):
        self.setStyleSheet(f"color: {self.getColor(SiColor.TEXT_B)};")
        # f"background-color: {self.getColor(SiColor.INTERFACE_BG_D)}")


class Autoexcal(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPadding(64)
        self.setScrollMaximumWidth(1000)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("AUTOEXCAL")

        # 创建控件组
        self.titled_widgets_group = SiTitledWidgetGroup(self)
        self.titled_widgets_group.setSiliconWidgetFlag(Si.EnableAnimationSignals)

        # 密堆积容器
        with self.titled_widgets_group as group:
            group.addTitle("设置")
            choose_switch = SiSwitchRefactor(self)

            self.custom_data_selection = SiOptionCardLinear(self)
            self.custom_data_selection.setTitle("自定义数据", "启用以自定义选择需要的数据")
            self.custom_data_selection.load(SiGlobal.siui.iconpack.get("ic_fluent_signature_filled"))
            self.custom_data_selection.addWidget(choose_switch)

            choose_boswer_btu = SiLongPressButton(self)
            choose_boswer_btu.resize(128, 32)
            choose_boswer_btu.setHint("长按选择文件夹")
            choose_boswer_btu.attachment().setText("选择文件夹")

            choose_boswer_sw = SiSwitchRefactor(self)

            self.boswer_filter = SiOptionCardLinear(self)
            self.boswer_filter.setTitle("浏览器所在文件夹", "启用以自定义选择浏览器")
            self.boswer_filter.load(SiGlobal.siui.iconpack.get("ic_fluent_folder_add_filled"))
            self.boswer_filter.addWidget(choose_boswer_sw)
            self.boswer_filter.addWidget(choose_boswer_btu)

            self.port_int_spin_box = SiIntSpinBox(self)
            self.port_int_spin_box.resize(128, 32)
            self.port_int_spin_box.setMaximum(65535)
            self.port_int_spin_box.setMinimum(1024)
            self.port_int_spin_box.setValue(9002)

            choose_port_sw = SiSwitchRefactor(self)

            self.choose_port_card = SiOptionCardLinear(self)
            self.choose_port_card.setTitle("端口号", "启用以自定义端口号")
            self.choose_port_card.load(SiGlobal.siui.iconpack.get("ic_fluent_plug_connected_filled"))
            self.choose_port_card.addWidget(choose_port_sw)
            self.choose_port_card.addWidget(self.port_int_spin_box)

        group.addWidget(self.custom_data_selection)
        group.addWidget(self.boswer_filter)
        group.addWidget(self.choose_port_card)

        with self.titled_widgets_group as group:
            group.addTitle("功能")


        # 添加页脚的空白以增加美观性
        self.titled_widgets_group.addPlaceholder(64)

        # 设置控件组为页面对象
        self.setAttachment(self.titled_widgets_group)
