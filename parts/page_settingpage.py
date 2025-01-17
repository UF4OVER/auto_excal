#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

import configparser
import webbrowser

from PyQt5.QtCore import Qt
from siui.components import SiDenseHContainer, SiLabel, SiDenseVContainer, SiOptionCardPlane, SiTitledWidgetGroup, \
    SiOptionCardLinear
from siui.components.button import SiRadioButtonRefactor, SiPushButtonRefactor, SiSwitchRefactor
from siui.components.page import SiPage
from siui.core import SiGlobal, Si, SiColor
from page_autoexcalpage import show_message
import config.CONFIG

PATH_CONFIG = config.CONFIG.CONFIG_PATH


class Label(SiLabel):
    def __init__(self, parent, text):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(32)

        self.setText(text)
        self.adjustSize()
        self.resize(self.width() + 24, self.height())

    def reloadStyleSheet(self):
        self.setStyleSheet(f"color: {self.getColor(SiColor.TEXT_B)};")


def read_config():
    config = configparser.ConfigParser()
    config.read(PATH_CONFIG)
    dpi_policy = config.get('Settings', 'dpi_policy', fallback='PassThrough')
    enable_hdpi_scaling = config.getboolean('Settings', 'enable_hdpi_scaling', fallback=False)
    use_hdpi_pixmaps = config.getboolean('Settings', 'use_hdpi_pixmaps', fallback=False)
    return dpi_policy, enable_hdpi_scaling, use_hdpi_pixmaps


def save_config(dpi_policy, enable_hdpi_scaling, use_hdpi_pixmaps):
    config = configparser.ConfigParser()
    config.read(PATH_CONFIG)  # 读取整个配置文件

    # 修改或添加 Settings 部分
    if not config.has_section('Settings'):
        config.add_section('Settings')
    config['Settings'] = {
        'dpi_policy': dpi_policy,
        'enable_hdpi_scaling': str(enable_hdpi_scaling),
        'use_hdpi_pixmaps': str(use_hdpi_pixmaps)
    }

    with open(PATH_CONFIG, 'w') as configfile:
        config.write(configfile)


class PageSettingPage(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPadding(64)
        self.setScrollMaximumWidth(1000)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("Settings")
        # 创建控件组
        self.titled_widgets_group = SiTitledWidgetGroup(self)
        self.titled_widgets_group.setSiliconWidgetFlag(Si.EnableAnimationSignals)

        self.setupUi()

        SiGlobal.siui.reloadStyleSheetRecursively(self)

        # 添加页脚的空白以增加美观性
        self.titled_widgets_group.addPlaceholder(64)
        # 设置控件组为页面对象
        self.setAttachment(self.titled_widgets_group)

    def enable_dpi_sw(self):
        print(self.enable_dpi_staus)
        self.enable_dpi_staus = not self.enable_dpi_staus

    def setupUi(self):
        """
        设置界面
        """

        with self.titled_widgets_group as group:
            group.addTitle("DPI 设置")

            self.refactor_radiobuttons = SiOptionCardPlane(self)
            self.refactor_radiobuttons.setTitle("DPI 策略:")

            self.enable_dpi_scaling = SiSwitchRefactor(self)
            enable_dpi_scaling_label = Label(self, "打开DPI缩放")

            self.refactor_radiobuttons.header().addWidget(self.enable_dpi_scaling, "right")
            self.refactor_radiobuttons.header().addWidget(enable_dpi_scaling_label, "right")

            self.enable_dpi_scaling.setChecked(False)
            self.enable_dpi_staus = False
            self.refactor_radiobuttons.body().setEnabled(False)
            self.refactor_radiobuttons.footer().setEnabled(False)

            self.enable_dpi_scaling.toggled.connect(
                lambda checked: self.refactor_radiobuttons.body().setEnabled(checked))
            self.enable_dpi_scaling.toggled.connect(
                lambda checked: self.refactor_radiobuttons.footer().setEnabled(checked))
            self.enable_dpi_scaling.toggled.connect(self.enable_dpi_sw)

            check_dpi_btu = SiPushButtonRefactor(self)
            check_dpi_btu.setText("关于 DPI")
            check_dpi_btu.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_tap_single_filled"))

            check_dpi_btu.clicked.connect(lambda: webbrowser.open("https://www.google.com/"))

            body_horizontal_container = SiDenseHContainer(self)

            radio_button_container = SiDenseVContainer(self)
            radio_button_container.setSpacing(6)

            introduction_dpi_container = SiDenseHContainer(self)
            introduction_dpi_textbroswer = Label(self,
                                                 "1.默认->:适用场景: 当你希望应用程序使用操作系统的默认设置时。\r\n"
                                                 "2.缩小->:适用场景: 当你希望应用程序的界面元素稍微小一些时。\r\n"
                                                 "3.放大->:适用场景: 当你希望应用程序的界面元素稍微大一些时。\r\n"
                                                 "4.理想->:适用场景: 当你希望应用程序的界面元素大小更接近于理想的缩放值时。\r\n")
            introduction_dpi_textbroswer.setAlignment(Qt.AlignLeft)
            introduction_dpi_textbroswer.setFixedHeight(100)
            introduction_dpi_container.adjustSize()
            introduction_dpi_container.addWidget(introduction_dpi_textbroswer)

            self.refactor_radio_button = SiRadioButtonRefactor(self)
            self.refactor_radio_button.setText("默认")
            self.refactor_radio_button.adjustSize()

            self.refactor_radio_button2 = SiRadioButtonRefactor(self)
            self.refactor_radio_button2.setText("缩小")
            self.refactor_radio_button2.adjustSize()

            self.refactor_radio_button3 = SiRadioButtonRefactor(self)
            self.refactor_radio_button3.setText("放大")
            self.refactor_radio_button3.adjustSize()

            self.refactor_radio_button4 = SiRadioButtonRefactor(self)
            self.refactor_radio_button4.setText("理想")
            self.refactor_radio_button4.adjustSize()

            radio_button_container.addWidget(self.refactor_radio_button)
            radio_button_container.addWidget(self.refactor_radio_button2)
            radio_button_container.addWidget(self.refactor_radio_button3)
            radio_button_container.addWidget(self.refactor_radio_button4)

            # 保存设置按钮
            save_button = SiPushButtonRefactor(self)
            save_button.setText("保存")
            save_button.clicked.connect(self.save_settings)
            save_button.clicked.connect(
                lambda: show_message(1, "设置已保存", "下次重启生效", "ic_fluent_emoji_hand_filled"))
            check_dpi_btu.adjustSize()

            radio_button_container.adjustSize()

            body_horizontal_container.adjustSize()

            body_horizontal_container.addWidget(radio_button_container)
            body_horizontal_container.addWidget(introduction_dpi_container)

            self.refactor_radiobuttons.footer().addWidget(save_button, "right")
            self.refactor_radiobuttons.footer().addWidget(check_dpi_btu, "right")
            self.refactor_radiobuttons.footer().addWidget(Label(self, "调整DPI缩放，下次重启生效"))
            self.refactor_radiobuttons.footer().setFixedHeight(40)

            self.refactor_radiobuttons.body().addWidget(body_horizontal_container)
            save_button.adjustSize()
            self.refactor_radiobuttons.footer().adjustSize()

            self.refactor_radiobuttons.body().addPlaceholder(12)
            self.refactor_radiobuttons.adjustSize()

            # 加载当前设置
            self.load_settings()

            group.addWidget(self.refactor_radiobuttons)
        with self.titled_widgets_group as group:
            group.addTitle("关闭")
            close_options = SiOptionCardLinear(self)
            close_options.setTitle("关闭应用时询问", "启用后关闭应用时会询问")
            self.close_options_toggle = SiSwitchRefactor(self)
            # 确保读取的值被正确转换为布尔类型
            self.close_options_toggle.setChecked(True)
            self.close_options_toggle.setChecked(self.read_close_options())
            print(f"read_setting_enable_switch:{self.read_close_options()}")
            self.close_options_toggle.toggled.connect(lambda b_: self.save_close_options(b_))
            close_options.load(SiGlobal.siui.iconpack.get("ic_fluent_closed_caption_off_filled"))
            close_options.addWidget(self.close_options_toggle)
            group.addWidget(close_options)

    def read_close_options(self) -> bool:
        config = configparser.ConfigParser()
        config.read(PATH_CONFIG)
        return config.getboolean('switch_options', 'enable_switch')

    def save_close_options(self, b_: bool):
        config = configparser.ConfigParser()
        config.read(PATH_CONFIG)
        config1 = config["switch_options"]
        config1['enable_switch'] = str(b_)
        with open(PATH_CONFIG, 'w') as configfile:
            config.write(configfile)

    def load_settings(self):
        dpi_policy, enable_hdpi_scaling, use_hdpi_pixmaps = read_config()
        self.refactor_radio_button.setChecked(dpi_policy == 'PassThrough')
        self.refactor_radio_button2.setChecked(dpi_policy == 'Floor')
        self.refactor_radio_button3.setChecked(dpi_policy == 'Ceil')
        self.refactor_radio_button4.setChecked(dpi_policy == 'Round')

    def save_settings(self):
        if self.refactor_radio_button.isChecked():
            dpi_policy = 'PassThrough'
        elif self.refactor_radio_button2.isChecked():
            dpi_policy = 'Floor'
        elif self.refactor_radio_button3.isChecked():
            dpi_policy = 'Ceil'
        elif self.refactor_radio_button4.isChecked():
            dpi_policy = 'Round'
        else:
            dpi_policy = 'PassThrough'

        use_hdpi_pixmaps = True  # todo

        save_config(dpi_policy, self.enable_dpi_staus, use_hdpi_pixmaps)
