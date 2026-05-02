#  Copyright (c) 2025 UF4OVER
#   All rights reserved.
from pathlib import Path
import requests
from PyQt5.QtCore import QObject, QThread, Qt, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
from siui.components import SiLabel, SiLongPressButton, SiOptionCardLinear, SiTitledWidgetGroup
from siui.components.button import SiProgressPushButton
from siui.components.combobox import SiComboBox
from siui.components.page import SiPage
from siui.core import Si, SiColor, SiGlobal
import config.CONFIG as F
from parts.event.send import show_message
GITHUB_API_URL = f"https://api.github.com/repos/{F.REPO_OWNER}/{F.REPO_NAME}/releases/latest"
REQUEST_HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": f"auto-excal/{F.VERSION}",
}
def parse_version(version_text: str):
    raw = version_text.strip().lstrip("vV")
    parts = []
    for item in raw.split("."):
        digits = "".join(ch for ch in item if ch.isdigit())
        parts.append(int(digits or 0))
    return tuple(parts)
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
    finished = pyqtSignal(bool, str, str, str, str)
    error = pyqtSignal(str)
    def __init__(self, current_version: str, parent=None):
        super().__init__(parent)
        self.current_version = current_version.strip().lstrip("vV")
        self.current_version_tuple = parse_version(self.current_version)
    def run(self):
        try:
            response = requests.get(GITHUB_API_URL, headers=REQUEST_HEADERS, timeout=(10, 30))
            response.raise_for_status()
            release = response.json()
            latest_version = str(release.get("tag_name", "")).strip().lstrip("vV")
            latest_version_tuple = parse_version(latest_version)
            release_notes = str(release.get("body", "")).strip() or "No release notes."
            release_url = str(release.get("html_url", F.LATEST_RELEASE_URL))
            if not latest_version:
                self.error.emit("Unable to get latest version from GitHub Releases.")
                return
            has_new_version = latest_version_tuple > self.current_version_tuple
            if has_new_version:
                message = f"Found new version: {latest_version}\n\n{release_notes}"
            elif latest_version_tuple < self.current_version_tuple:
                message = f"Local version {self.current_version} is newer than latest release {latest_version}."
            else:
                message = f"You are already on the latest version: {self.current_version}"
            self.finished.emit(has_new_version, latest_version, message, release_url, release_notes)
        except requests.RequestException as e:
            self.error.emit(f"Check update failed: {e}")
class VersionCheckThread(QThread):
    finished = pyqtSignal(bool, str, str, str, str)
    error = pyqtSignal(str)
    def __init__(self, current_version: str, parent=None):
        super().__init__(parent)
        self.worker = VersionChecker(current_version)
        self.worker.moveToThread(self)
        self.started.connect(self.worker.run)
        self.worker.finished.connect(self._on_finished)
        self.worker.error.connect(self._on_error)
    def _on_finished(self, has_new_version, latest_version, message, release_url, release_notes):
        self.finished.emit(has_new_version, latest_version, message, release_url, release_notes)
        self.quit()
        self.wait(1000)
    def _on_error(self, error_message):
        self.error.emit(error_message)
        self.quit()
        self.wait(1000)
class Downloader(QObject):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    def __init__(self, url: str, destination: Path, parent=None):
        super().__init__(parent)
        self.url = url
        self.destination = destination
    def run(self):
        try:
            response = requests.get(self.url, headers=REQUEST_HEADERS, stream=True, timeout=(10, 60))
            response.raise_for_status()
            total_size = int(response.headers.get("content-length", 0))
            downloaded_size = 0
            block_size = 1024 * 64
            with open(self.destination, "wb") as file:
                for chunk in response.iter_content(block_size):
                    if not chunk:
                        continue
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    if total_size > 0:
                        self.progress.emit(int(downloaded_size * 100 / total_size))
            self.progress.emit(100)
            self.finished.emit(str(self.destination))
        except requests.RequestException as e:
            self.error.emit(f"Download failed: {e}")
        except OSError as e:
            self.error.emit(f"Write file failed: {e}")
class DownloadThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    def __init__(self, url: str, destination: Path, parent=None):
        super().__init__(parent)
        self.worker = Downloader(url, destination)
        self.worker.moveToThread(self)
        self.started.connect(self.worker.run)
        self.worker.progress.connect(self.progress.emit)
        self.worker.finished.connect(self._on_finished)
        self.worker.error.connect(self._on_error)
    def _on_finished(self, message):
        self.finished.emit(message)
        self.quit()
        self.wait(1000)
    def _on_error(self, error_message):
        self.error.emit(error_message)
        self.quit()
        self.wait(1000)
class PageSettingPage(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPadding(64)
        self.setScrollMaximumWidth(1000)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("Update")
        self.latest_version = ""
        self.release_notes = ""
        self.download_thread = None
        self.version_check_thread = None
        self.titled_widgets_group = SiTitledWidgetGroup(self)
        self.titled_widgets_group.setSiliconWidgetFlag(Si.EnableAnimationSignals)
        self.setup_update_widgets()
        self.titled_widgets_group.addPlaceholder(64)
        self.setAttachment(self.titled_widgets_group)
    def current_download_dir(self) -> Path:
        configured = str(F.READ_CONFIG("version", "path", "")).strip()
        path = Path(configured) if configured else Path.home() / "Downloads" / "AutoExcal"
        path.mkdir(parents=True, exist_ok=True)
        if not configured:
            F.WRITE_CONFIG("version", "path", str(path))
        return path
    def safe_icon(self, icon_name: str, fallback: str):
        try:
            return SiGlobal.siui.iconpack.get(icon_name)
        except Exception:
            return SiGlobal.siui.iconpack.get(fallback)
    def setup_update_widgets(self):
        with self.titled_widgets_group as group:
            group.addTitle("Update Download")
            self.choose_folder_btu = SiLongPressButton(self)
            self.choose_folder_btu.resize(148, 32)
            self.choose_folder_btu.attachment().setText("Choose Folder")
            self.choose_folder_btu.setHint("Long press to choose the download folder")
            self.choose_folder_btu.longPressed.connect(self.choose_folder)
            self.folder_card = SiOptionCardLinear(self)
            self.folder_card.setTitle("Download Folder", str(self.current_download_dir()))
            self.folder_card.load(self.safe_icon("ic_fluent_home_database_regular", "ic_fluent_info_filled"))
            self.folder_card.addWidget(self.choose_folder_btu)
            group.addWidget(self.folder_card)
            self.check_button = SiProgressPushButton(self)
            self.check_button.resize(148, 32)
            self.check_button.setText("Check Update")
            self.check_button.clicked.connect(self.start_version_check)
            self.type_selection = SiComboBox(self)
            self.type_selection.resize(150, 32)
            self.type_selection.addOption("Archive (.7z)")
            self.type_selection.addOption("Installer (.exe)")
            self.type_selection.menu().setShowIcon(False)
            self.type_selection.menu().setIndex(1)
            self.update_card = SiOptionCardLinear(self)
            self.update_card.setTitle("Old Download UI", "Restore the old update UI: check version, choose type, download asset.")
            self.update_card.load(self.safe_icon("ic_fluent_wrench_settings_filled", "ic_fluent_info_filled"))
            self.update_card.addWidget(self.check_button)
            self.update_card.addWidget(self.type_selection)
            group.addWidget(self.update_card)
            self.status_card = SiOptionCardLinear(self)
            self.status_card.setTitle("Status", f"Current version: {F.VERSION}")
            self.status_card.load(self.safe_icon("ic_fluent_info_filled", "ic_fluent_task_list_ltr_filled"))
            group.addWidget(self.status_card)
            note = Label(self, "Check the latest release first, then download exe or 7z asset.")
            group.addWidget(note)
    def selected_suffix(self) -> str:
        value = self.type_selection.menu().value()
        return ".7z" if "7z" in value else ".exe"
    def choose_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Choose Download Folder", str(self.current_download_dir()))
        if not folder_path:
            return
        F.WRITE_CONFIG("version", "path", folder_path)
        self.folder_card.setTitle("Download Folder", folder_path)
        show_message(1, "Success", "Download folder updated.", "ic_fluent_task_list_ltr_filled")
    def start_version_check(self):
        self.check_button.setEnabled(False)
        self.check_button.setText("Checking...")
        self.check_button.setProgress(0)
        self.status_card.setTitle("Status", "Checking GitHub Releases...")
        self.version_check_thread = VersionCheckThread(F.VERSION, self)
        self.version_check_thread.finished.connect(self.on_version_check_finished)
        self.version_check_thread.error.connect(self.on_version_check_error)
        self.version_check_thread.start()
    def on_version_check_finished(self, has_new_version, latest_version, message, release_url, release_notes):
        self.latest_version = latest_version
        self.release_notes = release_notes
        self.check_button.setEnabled(True)
        self.check_button.setProgress(0)
        if has_new_version:
            self.check_button.setText("Download Update")
            try:
                self.check_button.clicked.disconnect()
            except TypeError:
                pass
            self.check_button.clicked.connect(self.download_new_version)
            self.status_card.setTitle("Status", f"New version found: {latest_version}")
            show_message(3, "Update Found", message, "ic_fluent_info_filled")
        else:
            self.restore_check_button()
            self.status_card.setTitle("Status", message)
            show_message(1, "Version", message, "ic_fluent_task_list_ltr_filled")
    def on_version_check_error(self, error_message):
        self.restore_check_button()
        self.status_card.setTitle("Status", error_message)
        show_message(0, "Check Failed", error_message, "ic_fluent_error_circle_filled")
    def restore_check_button(self):
        self.check_button.setEnabled(True)
        self.check_button.setProgress(0)
        self.check_button.setText("Check Update")
        try:
            self.check_button.clicked.disconnect()
        except TypeError:
            pass
        self.check_button.clicked.connect(self.start_version_check)
    def get_download_asset(self):
        response = requests.get(GITHUB_API_URL, headers=REQUEST_HEADERS, timeout=(10, 30))
        response.raise_for_status()
        latest_release = response.json()
        suffix = self.selected_suffix()
        for asset in latest_release.get("assets", []):
            name = str(asset.get("name", ""))
            if name.endswith(suffix):
                return {"name": name, "url": asset.get("browser_download_url", "")}
        return None
    def download_new_version(self):
        self.check_button.setEnabled(False)
        self.check_button.setText("Preparing...")
        self.status_card.setTitle("Status", "Resolving download URL...")
        try:
            asset = self.get_download_asset()
        except requests.RequestException as e:
            self.restore_check_button()
            show_message(0, "Download Failed", f"Resolve download URL failed: {e}", "ic_fluent_error_circle_filled")
            return
        if not asset or not asset.get("url"):
            self.restore_check_button()
            show_message(0, "Download Failed", "No matching asset found in latest release.", "ic_fluent_error_circle_filled")
            return
        destination = self.current_download_dir() / asset["name"]
        self.download_thread = DownloadThread(asset["url"], destination, self)
        self.download_thread.progress.connect(self.update_progress)
        self.download_thread.finished.connect(self.on_download_finished)
        self.download_thread.error.connect(self.on_download_error)
        self.download_thread.start()
        self.status_card.setTitle("Status", f"Downloading: {asset['name']}")
        self.check_button.setText("Downloading...")
        show_message(1, "Download", f"Downloading {asset['name']}...", "ic_fluent_info_filled")
    def update_progress(self, percent):
        self.check_button.setProgress(percent / 100)
        self.status_card.setTitle("Status", f"Progress: {percent}%")
    def on_download_finished(self, destination_path: str):
        self.restore_check_button()
        self.status_card.setTitle("Status", f"Done: {destination_path}")
        show_message(1, "Download Complete", f"Saved to:\n{destination_path}", "ic_fluent_task_list_ltr_filled")
    def on_download_error(self, error_message: str):
        self.restore_check_button()
        self.status_card.setTitle("Status", error_message)
        show_message(0, "Download Failed", error_message, "ic_fluent_error_circle_filled")
