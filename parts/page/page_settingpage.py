#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

import configparser
import shutil
import webbrowser

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog
from siui.components import SiDenseHContainer, SiLabel, SiDenseVContainer, SiOptionCardPlane, SiTitledWidgetGroup, \
    SiOptionCardLinear
from siui.components.button import SiRadioButtonRefactor, SiPushButtonRefactor, SiSwitchRefactor
from siui.components.editbox import SiLineEdit
from siui.components.page import SiPage
from siui.core import SiGlobal, Si, SiColor

import config.CONFIG as F
from parts.page.page_autoexcalpage import show_message
import re
PATH_CONFIG = F.CONFIG_PATH
PATH_PNG = F.PNG_PATH


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
    config.read(PATH_CONFIG, encoding='utf-8')
    dpi_policy = config.get('Settings', 'dpi_policy', fallback='PassThrough')
    enable_hdpi_scaling = config.getboolean('Settings', 'enable_hdpi_scaling', fallback=False)
    use_hdpi_pixmaps = config.getboolean('Settings', 'use_hdpi_pixmaps', fallback=False)
    return dpi_policy, enable_hdpi_scaling, use_hdpi_pixmaps


def save_config(dpi_policy, enable_hdpi_scaling, use_hdpi_pixmaps):
    config = configparser.ConfigParser()
    config.read(PATH_CONFIG, encoding='utf-8')  # 读取整个配置文件

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


def save_close_options(b_: bool):
    config = configparser.ConfigParser()
    config.read(PATH_CONFIG, encoding='utf-8')
    config1 = config["switch_options"]
    config1['enable_switch'] = str(b_)
    with open(PATH_CONFIG, 'w') as configfile:
        config.write(configfile)


def read_close_options() -> bool:
    config = configparser.ConfigParser()
    config.read(PATH_CONFIG, encoding='utf-8')
    return config.getboolean('switch_options', 'enable_switch')


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
            group.addTitle("主页背景")

            self.change_background_btu = SiPushButtonRefactor(self)
            self.change_background_btu.setText("更换背景")
            self.change_background_btu.resize(128, 32)
            self.change_background_btu.clicked.connect(self.change_background)

            self.background_options = SiOptionCardLinear(self)
            self.background_options.setTitle("主页背景", "启用后主页背景为图片")
            self.background_options.load(SiGlobal.siui.iconpack.get("ic_fluent_image_arrow_back_filled"))
            self.background_options.addWidget(self.change_background_btu)

            group.addWidget(self.background_options)

        with self.titled_widgets_group as group:

            group.addTitle("OCR识别Token")

            self.key_code_input = SiLineEdit(self)
            self.key_code_input.resize(500, 36)
            self.key_code_input.setTitleWidth(100)
            self.key_code_input.setTitle("百度云Token")
            self.key_code_input.setText("请不要将这个Token交给别人")

            self.change_api_key_btu = SiPushButtonRefactor(self)
            self.change_api_key_btu.setText("确认")
            self.change_api_key_btu.resize(96, 32)
            self.change_api_key_btu.clicked.connect(self.save_api_key)

            self.api_key_options = SiOptionCardLinear(self)
            self.api_key_options.setTitle("填写您的OCR识别Token", "百度云的OCR_Token")
            self.api_key_options.load(SiGlobal.siui.iconpack.get("ic_fluent_mail_edit_filled"))

            self.api_key_options.addWidget(self.change_api_key_btu)
            self.api_key_options.addWidget(self.key_code_input)

            group.addWidget(self.api_key_options)
        with self.titled_widgets_group as g:
            g.addTitle("VPN账号密码")

            self.vpn_account_input = SiLineEdit(self)
            self.vpn_account_input.resize(240, 36)
            self.vpn_account_input.setTitleWidth(60)
            self.vpn_account_input.setTitle("账号")

            self.vpn_password_input = SiLineEdit(self)
            self.vpn_password_input.resize(240, 36)
            self.vpn_password_input.setTitleWidth(60)
            self.vpn_password_input.setTitle("密码")

            self.save_vpn_btu = SiPushButtonRefactor(self)
            self.save_vpn_btu.setText("保存")
            self.save_vpn_btu.resize(96, 32)
            self.save_vpn_btu.clicked.connect(self.save_vpn)

            self.vpn_options = SiOptionCardLinear(self)
            self.vpn_options.setTitle("VPN账号密码", "VPN账号密码")
            self.vpn_options.load(SiGlobal.siui.iconpack.get("ic_fluent_mail_edit_filled"))
            self.vpn_options.addWidget(self.save_vpn_btu)
            self.vpn_options.addWidget(self.vpn_password_input)
            self.vpn_options.addWidget(self.vpn_account_input)

            g.addWidget(self.vpn_options)

    def save_vpn(self):
        if len(self.vpn_account_input.text()) > 10 and len(self.vpn_password_input.text()) > 1:
            F.WRITE_CONFIG("vpn", "vpn_name", self.vpn_account_input.text())
            F.WRITE_CONFIG("vpn", "vpn_password", self.vpn_password_input.text())
            show_message(1, "VPN更新成功", "下次重启生效", "ic_fluent_emoji_hand_filled")
        else:
            show_message(3, "不合理", "请合理输入", "ic_fluent_emoji_hand_filled")

    def save_api_key(self):
        if len(self.key_code_input.text()) > 10:
            F.WRITE_CONFIG("ocr", "ocr_api_token", self.key_code_input.text())
            show_message(1, "Token更新成功", "下次重启生效", "ic_fluent_emoji_hand_filled")
        else:
            show_message(3, "Token不合理", "请输入合理的Token", "ic_fluent_emoji_hand_filled")

    def change_background(self):
        png_file_path = QFileDialog.getOpenFileName(self, "选择PNG文件", "", "JPG(嘿嘿嘿) Files (*.jpg)")[0]
        if png_file_path:
            shutil.copy(png_file_path, f"{PATH_PNG}\\back.jpg")
            show_message(1, "背景更换成功", "下次重启生效", "ic_fluent_emoji_hand_filled")

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

        use_hdpi_pixmaps = True
        save_config(dpi_policy, self.enable_dpi_staus, use_hdpi_pixmaps)
