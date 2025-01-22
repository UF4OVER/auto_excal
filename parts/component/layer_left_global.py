#  Copyright (c) 2025 UF4OVER
#   All rights reserved.
from PyQt5.QtCore import Qt
from siui.components import SiLabel, SiTitledWidgetGroup
from siui.components.combobox import SiComboBox
from siui.components.slider.slider import SiSliderH
from siui.core import SiColor
from siui.core import SiGlobal
from siui.templates.application.components.layer.global_drawer import SiLayerDrawer
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import wmi

# 获取系统的音频设备
devices = AudioUtilities.GetAllDevices()

device = AudioUtilities.GetSpeakers()
interface = device.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None
)
volume = interface.QueryInterface(IAudioEndpointVolume)


def set_brightness(brightness_level):  # 屏幕亮度设置
    # 限制亮度在 0 到 100 之间
    brightness_level = max(0, min(100, brightness_level))

    wmi_instance = wmi.WMI(namespace='root\\WMI')
    brightness_methods = wmi_instance.WmiMonitorBrightnessMethods()[0]
    brightness_methods.WmiSetBrightness(brightness_level, 0)  # 第二个参数是时间，0 表示立即生效


def get_current_brightness() -> int:
    wmi_instance = wmi.WMI(namespace='root\\WMI')
    brightness = wmi_instance.WmiMonitorBrightness()[0]
    return int(brightness.CurrentBrightness)


print(f"当前屏幕亮度: {get_current_brightness()}%")


def get_current_volume() -> int:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None
    )
    volume = interface.QueryInterface(IAudioEndpointVolume)
    # 获取当前音量（比例值）
    current_volume = volume.GetMasterVolumeLevelScalar()
    print(f"当前系统音量: {current_volume * 100}%")
    # 转换为百分比
    return int(round(current_volume * 100, 2))


# print(f"当前系统音量: {get_current_volume()}%")


class LayerLeftGlobalDrawer(SiLayerDrawer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.drawer.move(-self.drawer.width(), 0)

        self.drawer_widget_group = SiTitledWidgetGroup(self)
        self.drawer_widget_group.setSpacing(8)

        self.drawer_page.setPadding(48)
        self.drawer_page.setTitle("全局左侧抽屉")
        self.drawer_page.title.setContentsMargins(32, 0, 0, 0)
        self.drawer_page.setScrollAlignment(Qt.AlignLeft)

        with self.drawer_widget_group as group:
            group.addTitle("音量设置")

            self.text_label = SiLabel(self)
            self.text_label.setTextColor(self.getColor(SiColor.TEXT_D))
            self.text_label.setWordWrap(True)
            self.text_label.setText("用来设置设备音量")
            self.text_label.setFixedHeight(64)

            group.addWidget(self.text_label)

        with self.drawer_widget_group as group:
            group.addTitle("声音")

            self.label_output_device = SiLabel(self)
            self.label_output_device.setTextColor(self.getColor(SiColor.TEXT_C))
            self.label_output_device.setText("输出设备")

            self.output_device = SiComboBox(self)
            self.output_device.resize(128, 32)
            self.output_device.addOption("默认设备")
            self.output_device.menu().setShowIcon(False)

            self.label_slider_1 = SiLabel(self)
            self.label_slider_1.setTextColor(self.getColor(SiColor.TEXT_C))
            self.label_slider_1.setText("系统音量")

            self.slider_1 = SiSliderH(self)
            self.slider_1.resize(0, 16)
            self.slider_1.setMinimum(0)
            self.slider_1.setMaximum(100)
            self.slider_1.setValue(get_current_volume(), move_to=False)
            self.slider_1.valueChanged.connect(
                lambda: volume.SetMasterVolumeLevelScalar(self.slider_1.value() / 100, None))

            self.label_slider_2 = SiLabel(self)
            self.label_slider_2.setTextColor(self.getColor(SiColor.TEXT_C))
            self.label_slider_2.setText("屏幕亮度")

            self.slider_2 = SiSliderH(self)
            self.slider_2.resize(0, 16)
            self.slider_2.setMinimum(0)
            self.slider_2.setMaximum(100)
            self.slider_2.setValue(get_current_brightness(), move_to=False)
            self.slider_2.setValue(100, move_to=False)
            self.slider_2.valueChanged.connect(lambda: set_brightness(self.slider_2.value()))

            group.addWidget(self.label_output_device)
            group.addWidget(self.output_device)
            group.addPlaceholder(8)
            group.addWidget(self.label_slider_1)
            group.addWidget(self.slider_1)
            group.addPlaceholder(8)
            group.addWidget(self.label_slider_2)
            group.addWidget(self.slider_2)

        group.addPlaceholder(64)

        self.drawer_page.setAttachment(self.drawer_widget_group)

    def setOpened(self, state):
        super().setOpened(state)
        if state:
            self.drawer.moveTo(0, 0)
        else:
            self.drawer.moveTo(-self.drawer.width(), 0)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.drawer_panel.setStyleSheet(
            f"background-color: {self.getColor(SiColor.INTERFACE_BG_C)};"
            f"border-right: 1px solid {self.getColor(SiColor.INTERFACE_BG_D)}"
        )

    def showLayer(self):
        super().showLayer()
        SiGlobal.siui.windows["MAIN_WINDOW"].groups()["MAIN_INTERFACE"].moveTo(100, 0)

    def closeLayer(self):
        super().closeLayer()
        SiGlobal.siui.windows["MAIN_WINDOW"].groups()["MAIN_INTERFACE"].moveTo(0, 0)
