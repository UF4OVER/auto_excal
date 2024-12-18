# -*- coding: utf-8 -*-
# -------------------------------

#  @Project : upper_computer
#  @Time    : 2024 - 12-18 19:43
#  @FileName: page_esp32.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 3.10

# -------------------------------

import os

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

from parts.themed_option_card import ThemedOptionCardPlane
from i2c.uart_to_i2c import UartToI2c


class I2C_page(SiPage):
    class Autoexcal(SiPage):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.setPadding(64)
            self.setScrollMaximumWidth(1000)
            self.setScrollAlignment(Qt.AlignLeft)
            self.setTitle("I2C设备")  # 设置标题

            # 创建控件组
            self.titled_widgets_group = SiTitledWidgetGroup(self)
            self.titled_widgets_group.setSiliconWidgetFlag(Si.EnableAnimationSignals)

            SiGlobal.siui.reloadStyleSheetRecursively(self)

            # 添加页脚的空白以增加美观性
            self.titled_widgets_group.addPlaceholder(64)
            # 设置控件组为页面对象
            self.setAttachment(self.titled_widgets_group)
