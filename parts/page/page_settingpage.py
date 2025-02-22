#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

import configparser
import os
import shutil
import webbrowser

import requests
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QFileDialog
from siui.components import SiDenseHContainer, SiLabel, SiDenseVContainer, SiOptionCardPlane
from siui.components import SiLongPressButton
from siui.components.button import SiProgressPushButton
from siui.components.button import SiRadioButtonRefactor, SiPushButtonRefactor, SiSwitchRefactor
from siui.components.combobox import SiComboBox
from siui.components.editbox import SiLineEdit
from siui.components.option_card import SiOptionCardLinear
from siui.components.page import SiPage
from siui.components.titled_widget_group import SiTitledWidgetGroup
from siui.core import Si, SiGlobal
from siui.core import SiColor

import config.CONFIG as F
from parts.event.send import show_message

PATH_CONFIG = F.CONFIG_PATH
PATH_PNG = F.PNG_PATH

VERSION = F.READ_CONFIG("version", "version")
REPO_OWNER = F.READ_CONFIG("version", "repo_owner")
REPO_NAME = F.READ_CONFIG("version", "repo_name")
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"
DOWNLOAD_PATH = F.READ_CONFIG("version", "path")
try:
    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)
except FileNotFoundError:
    print("配置文件不存在，请检查路径")


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

class VersionChecker(QObject):
    finished = pyqtSignal(bool, str, str, str)
    error = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.VERSION = VERSION
        self.REPO_OWNER = REPO_OWNER
        self.REPO_NAME = REPO_NAME
        self.GITHUB_API_URL = GITHUB_API_URL

    def run(self):
        try:
            response = requests.get(self.GITHUB_API_URL)
            response.raise_for_status()  # 检查请求是否成功
            latest_release = response.json()

            latest_version = latest_release.get("tag_name", "")
            release_notes = latest_release.get("body", "")
            download_url = latest_release.get("zipball_url", "")

            if latest_version == self.VERSION:
                self.finished.emit(False, "版本更新", f"当前版本已是最新版本 {self.VERSION}",
                                   "ic_fluent_globe_error_filled")
                print(f"当前版本已是最新版本 {self.VERSION}")
            else:
                self.finished.emit(True, "版本更新", f"发现了最新版本 {latest_version}\n\n{release_notes}",
                                   "ic_fluent_globe_arrow_up_filled")
                print(f"发现了最新版本 {latest_version}")
                self.finished.emit(True, "下载", f"下载 URL: {download_url}", "ic_fluent_globe_arrow_up_filled")

        except requests.exceptions.RequestException as e:
            print(f"请求出错: {e}")
            self.error.emit(f"请求出错: {e}")


class VersionCheckThread(QThread):
    finished = pyqtSignal(bool, str, str, str)
    error = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.version_checker = VersionChecker()
        self.version_checker.moveToThread(self)
        self.version_checker.finished.connect(self.on_finished)
        self.version_checker.error.connect(self.on_error)
        self.started.connect(self.version_checker.run)

    def on_finished(self, has_new_version, title, message, icon):
        self.finished.emit(has_new_version, title, message, icon)
        self.quit()
        self.deleteLater()

    def on_error(self, error_message):
        self.error.emit(error_message)
        self.quit()
        self.deleteLater()


class Downloader(QObject):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, url, destination, parent=None):
        super().__init__(parent)
        self.url = url
        self.destination = destination

    def run(self):
        try:
            response = requests.get(self.url, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 Kibibyte
            progress = 0

            with open(self.destination, 'wb') as file:
                for data in response.iter_content(block_size):
                    file.write(data)
                    progress += len(data)
                    if total_size > 0:
                        percent = int((progress / total_size) * 100)
                        self.progress.emit(percent)

            self.finished.emit("下载完成")
        except requests.exceptions.RequestException as e:
            self.error.emit(f"下载出错: {e}")


class DownloadThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, url, destination, parent=None):
        super().__init__(parent)
        self.downloader = Downloader(url, destination)
        self.downloader.moveToThread(self)
        self.downloader.progress.connect(self.on_progress)
        self.downloader.finished.connect(self.on_finished)
        self.downloader.error.connect(self.on_error)
        self.started.connect(self.downloader.run)

    def on_progress(self, percent):
        self.progress.emit(percent)

    def on_finished(self, message):
        self.finished.emit(message)
        self.quit()
        self.deleteLater()

    def on_error(self, error_message):
        self.error.emit(error_message)
        self.quit()
        self.deleteLater()
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
        self.file_suffix_f = ".exe"
        # 创建控件组
        self.titled_widgets_group = SiTitledWidgetGroup(self)
        self.titled_widgets_group.setSiliconWidgetFlag(Si.EnableAnimationSignals)

        self.setupUi()
        self.setup_updata_widgets()

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
    def setup_updata_widgets(self):
        with self.titled_widgets_group as group:
            group.addTitle("检查更新")
            self.choose_btu = SiLongPressButton(self)
            self.choose_btu.resize(128, 32)
            self.choose_btu.setHint("长按选择文件夹")
            self.choose_btu.attachment().setText("选择下载位置")
            self.choose_btu.longPressed.connect(self.choose_folder)

            self.boswer_filter = SiOptionCardLinear(self)
            self.boswer_filter.setTitle("新版本所在文件夹", "选择文件夹来储存新版本")
            self.boswer_filter.load(SiGlobal.siui.iconpack.get("ic_fluent_folder_add_filled"))
            self.boswer_filter.addWidget(self.choose_btu)

            group.addWidget(self.boswer_filter)

            self.check_btu = SiProgressPushButton(self)
            self.check_btu.resize(128, 32)
            self.check_btu.setText("检查新版本")
            self.check_btu.clicked.connect(self.start_version_check)

            boswer_filter = SiOptionCardLinear(self)
            boswer_filter.setTitle("检查更新", "检测是否发布了新版本")
            boswer_filter.load(SiGlobal.siui.iconpack.get("ic_fluent_cloud_checkmark_filled"))

            self.type_selection = SiComboBox(self)
            self.type_selection.resize(150, 32)
            self.type_selection.addOption("压缩文件（.7z）")
            self.type_selection.addOption("分发文件（.exe）")
            self.type_selection.menu().setShowIcon(False)
            self.type_selection.menu().setIndex(0)

            boswer_filter.addWidget(self.check_btu)
            boswer_filter.addWidget(self.type_selection)

        group.addWidget(boswer_filter)

    def start_version_check(self):
        self.version_check_thread = VersionCheckThread()
        self.version_check_thread.finished.connect(self.on_version_check_finished)
        self.version_check_thread.error.connect(self.on_version_check_error)
        self.version_check_thread.start()

    def on_version_check_finished(self, has_new_version, title, message, icon):
        show_message(1 if not has_new_version else 3, title, message, icon)
        if has_new_version:
            self.check_btu.clicked.disconnect()
            self.check_btu.setText("下载新版本")
            self.check_btu.clicked.connect(self.download_new_version)

    def on_version_check_error(self, error_message):
        show_message(1, "请求出错", error_message, "ic_fluent_globe_error_filled")
        print(f"请求出错: {error_message}")

    def download_new_version(self):
        self.check_btu.setEnabled(False)
        self.download_url = self.get_download_url()
        if not self.download_url:
            show_message(1, "下载错误", "无法获取下载 URL", "ic_fluent_globe_error_filled")
            return
        self.destination_folder = DOWNLOAD_PATH
        print(f"下载到目录文件夹{self.destination_folder}")
        if not self.destination_folder:
            show_message(1, "下载错误", "未选择文件夹", "ic_fluent_globe_error_filled")
            return

        self.destination_path = os.path.join(self.destination_folder, "Wedding Invitation" + self.file_suffix_f)

        self.download_thread = DownloadThread(self.download_url, self.destination_path)
        self.download_thread.progress.connect(self.update_progress)
        self.download_thread.finished.connect(self.on_download_finished)
        self.download_thread.error.connect(self.on_download_error)
        self.download_thread.start()

    def get_download_url(self):
        try:
            response = requests.get(GITHUB_API_URL)
            response.raise_for_status()
            latest_release = response.json()
            assets = latest_release.get("assets", [])
            for asset in assets:

                if self.type_selection.menu().value() == "分发文件（.exe）":
                    self.file_suffix_f = ".exe"
                elif self.type_selection.menu().value() == "压缩文件（.7z）":
                    self.file_suffix_f = ".7z"
                else:
                    self.file_suffix_f = ".exe"

                if asset.get("name", "").endswith(self.file_suffix_f):
                    show_message(1, "下载", "下载中.....请稍后", "ic_fluent_globe_arrow_up_filled")
                    return asset.get("browser_download_url", "")
            return None
        except requests.exceptions.RequestException as e:
            show_message(1, "请求出错", f"请求出错: {e}", "ic_fluent_globe_error_filled")
            print(f"请求出错: {e}")
            return None

    def choose_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")

        if folder_path:
            F.WRITE_CONFIG("version", "path", folder_path)
            print(f"路径已更改为:{folder_path}")
            self.boswer_filter.setTitle("新版本所在文件夹", "选择文件夹来储存新版本")
        else:
            pass

    def update_progress(self, percent):
        self.check_btu.setProgress(percent/100)

    def on_download_finished(self, message):
        show_message(1, "下载完成", f"{message}到\r\n文件夹{DOWNLOAD_PATH}", "ic_fluent_globe_arrow_up_filled")
        print(f"{message}到文件夹：{DOWNLOAD_PATH}")
        self.check_btu.setText("检查新版本")
        self.check_btu.clicked.disconnect()
        self.check_btu.clicked.connect(self.start_version_check)

    def on_download_error(self, error_message):
        show_message(1, "下载错误", error_message, "ic_fluent_globe_error_filled")
        print(f"下载出错: {error_message}")
        self.check_btu.setText("检查新版本")
        self.check_btu.clicked.disconnect()
        self.check_btu.clicked.connect(self.start_version_check)
