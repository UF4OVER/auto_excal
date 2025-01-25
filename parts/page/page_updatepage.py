#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

import configparser
import os

import requests
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QFileDialog
from siui.components import SiLongPressButton
from siui.components.button import SiProgressPushButton
from siui.components.option_card import SiOptionCardLinear
from siui.components.page import SiPage
from siui.components.titled_widget_group import SiTitledWidgetGroup
from siui.core import Si, SiGlobal

import config.CONFIG as F
from parts.event.send_message import show_message

PATH_CONFIG = F.CONFIG_PATH

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


class UpDatePage(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPadding(64)
        self.setScrollMaximumWidth(1000)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("更新")  # 设置标题

        # 创建控件组
        self.titled_widgets_group = SiTitledWidgetGroup(self)
        self.titled_widgets_group.setSiliconWidgetFlag(Si.EnableAnimationSignals)

        SiGlobal.siui.reloadStyleSheetRecursively(self)
        self.setup_widgets()
        # 添加页脚的空白以增加美观性
        self.titled_widgets_group.addPlaceholder(64)
        # 设置控件组为页面对象
        self.setAttachment(self.titled_widgets_group)

    def setup_widgets(self):
        with self.titled_widgets_group as group:
            group.addTitle("文件夹")
            self.choose_btu = SiLongPressButton(self)
            self.choose_btu.resize(128, 32)
            self.choose_btu.setHint("长按选择文件夹")
            self.choose_btu.attachment().setText("选择文件夹")
            self.choose_btu.longPressed.connect(self.choose_folder)

            boswer_filter = SiOptionCardLinear(self)
            boswer_filter.setTitle("新版本所在文件夹", "选择文件夹来储存新版本")
            boswer_filter.load(SiGlobal.siui.iconpack.get("ic_fluent_folder_add_filled"))
            boswer_filter.addWidget(self.choose_btu)

            group.addWidget(boswer_filter)

        with self.titled_widgets_group as group:
            group.addTitle("检查更新")
            self.check_btu = SiProgressPushButton(self)
            self.check_btu.resize(128, 32)
            self.check_btu.setText("检查新版本")
            self.check_btu.clicked.connect(self.start_version_check)

            boswer_filter = SiOptionCardLinear(self)
            boswer_filter.setTitle("检查更新", "检测是否发布了新版本")
            boswer_filter.load(SiGlobal.siui.iconpack.get("ic_fluent_cloud_checkmark_filled"))
            boswer_filter.addWidget(self.check_btu)

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
        self.download_url = self.get_download_url()
        if not self.download_url:
            show_message(1, "下载错误", "无法获取下载 URL", "ic_fluent_globe_error_filled")
            return

        self.destination_folder = DOWNLOAD_PATH
        print(f"下载到目录文件夹{self.destination_folder}")
        if not self.destination_folder:
            show_message(1, "下载错误", "未选择文件夹", "ic_fluent_globe_error_filled")
            return

        self.destination_path = os.path.join(self.destination_folder, "Wedding Invitation.7z")

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
                if asset.get("name", "").endswith(".7z"):
                    return asset.get("browser_download_url", "")
                print(f"未找到 7z 文件: {latest_release['name']}")
                show_message(1, "下载错误", "未找到 7z 的安装文件，请联系开发者", "ic_fluent_globe_error_filled")
            return None  # 如果没有找到 7z 文件，返回 None
        except requests.exceptions.RequestException as e:
            show_message(1, "请求出错", f"请求出错: {e}", "ic_fluent_globe_error_filled")
            print(f"请求出错: {e}")
            return None

    def choose_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder_path:
            F.WRITE_CONFIG("version", "path", folder_path)
            print(f"路径已更改为:{folder_path}")
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
