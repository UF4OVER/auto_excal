# -*- coding: utf-8 -*-

#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

import logging
import sys
from datetime import datetime
from functools import cached_property
from pathlib import Path
from typing import Any

import pytz
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication, QMessageBox


class DirPaths:
    def _ensure_dir(self, *parts: str) -> Path:
        directory = self.BaseDir.joinpath(*parts)
        directory.mkdir(parents=True, exist_ok=True)
        return directory

    @cached_property
    def BaseDir(self) -> Path:
        if getattr(sys, "frozen", False):
            return Path(sys.executable).resolve().parent
        return Path(__file__).resolve().parent.parent

    @cached_property
    def ConfigDir(self) -> Path:
        return self._ensure_dir("config")

    @cached_property
    def LogDir(self) -> Path:
        return self._ensure_dir("Logs")

    @cached_property
    def PicDir(self) -> Path:
        return self._ensure_dir("pic", "res")


class SettingsManager:
    def __init__(self, config_path: Path):
        self.config_path = str(config_path.resolve())
        self.settings = QSettings(self.config_path, QSettings.IniFormat)

    def get(self, section: str, option: str, fallback: Any = "") -> Any:
        key = f"{section}/{option}"
        if not self.settings.contains(key):
            return fallback

        value = self.settings.value(key, fallback)

        if isinstance(fallback, bool):
            if isinstance(value, str):
                return value.lower() == "true"
            return bool(value)

        if isinstance(fallback, int) and not isinstance(fallback, bool):
            try:
                return int(value)
            except (TypeError, ValueError):
                return fallback

        return value

    def set(self, section: str, option: str, value: Any):
        key = f"{section}/{option}"
        self.settings.setValue(key, value)
        self.settings.sync()


class StreamToLogger:
    def __init__(self, logger: logging.Logger, log_level: int):
        self.logger = logger
        self.log_level = log_level

    def write(self, buf: str):
        text = buf.rstrip()
        if text:
            for line in text.splitlines():
                self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        return None


_dir_paths = DirPaths()

BASE_DIR: Path = _dir_paths.BaseDir
CONFIG_PATH: Path = _dir_paths.ConfigDir / "config.ini"
LOG_DIR: Path = _dir_paths.LogDir
LOG_PATH: Path = LOG_DIR / "app.log"
PNG_PATH: Path = _dir_paths.PicDir

settings = SettingsManager(CONFIG_PATH)


def READ_CONFIG(section: str, option: str, fallback: Any = "") -> Any:
    return settings.get(section, option, fallback)


def WRITE_CONFIG(section: str, option: str, value: Any):
    settings.set(section, option, value)


def sync_today():
    utc_now = datetime.utcnow()
    china_tz = pytz.timezone("Asia/Shanghai")
    today = utc_now.replace(tzinfo=pytz.utc).astimezone(china_tz).strftime("%Y-%m-%d")

    if READ_CONFIG("date", "time", "") != today:
        WRITE_CONFIG("date", "time", today)
    else:
        print("时间未更新")

    return today


def setup_logging(redirect_streams: bool = False):
    root_logger = logging.getLogger()

    if getattr(setup_logging, "_configured", False):
        return root_logger

    root_logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    if redirect_streams:
        sys.stdout = StreamToLogger(root_logger, logging.INFO)
        sys.stderr = StreamToLogger(root_logger, logging.ERROR)

    setup_logging._configured = True
    root_logger.info("日志已初始化: %s", LOG_PATH)
    return root_logger


def _show_fallback_dialog(title: str, text: str):
    app = QApplication.instance()
    if app is not None:
        QMessageBox.critical(None, title, text)
    else:
        print(f"{title}: {text}")


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.getLogger(__name__).error(
        "Uncaught exception",
        exc_info=(exc_type, exc_value, exc_traceback),
    )

    title = "注意，注意！！！！"
    text = (
        "程序发生未处理异常，请截图联系开发者，或者附上 Logs/app.log 文件并说明复现步骤。"
    )

    try:
        from parts.event.send import show_message

        show_message(0, title, text, "ic_fluent_error_circle_filled")
    except Exception:
        _show_fallback_dialog(title, text)

    print(exc_value)


def install_exception_hook():
    sys.excepthook = handle_exception


def initialize_runtime(redirect_streams: bool = False):
    setup_logging(redirect_streams=redirect_streams)
    install_exception_hook()


TODAY = sync_today()
VERSION: str = str(READ_CONFIG("version", "version", "1.3.0"))
AUTHOR: str = str(READ_CONFIG("version", "author", "UF4OVER"))
VERSION_SOURCE_URL: str = str(READ_CONFIG("version", "url", ""))
REPO_OWNER: str = str(READ_CONFIG("version", "repo_owner", "UF4OVER"))
REPO_NAME: str = str(READ_CONFIG("version", "repo_name", "auto_excal"))
DOWNLOAD_PATH: str = str(READ_CONFIG("version", "path", ""))
REPO_URL: str = f"https://github.com/{REPO_OWNER}/{REPO_NAME}"
RELEASES_URL: str = f"{REPO_URL}/releases"
LATEST_RELEASE_URL: str = f"{RELEASES_URL}/latest"

print(f"配置路径: {BASE_DIR}")
print(f"配置文件路径: {CONFIG_PATH}")
print("-" * 20 + "info" + "-" * 20)
print(f"全局版本: {VERSION}")
print(f"全局作者: {AUTHOR}")
print(f"版本源: {VERSION_SOURCE_URL}")
print("-" * 20 + "file" + "-" * 20)
print(f"全局图片文件路径: {PNG_PATH}")
print("-" * 20 + "start" + "-" * 20)


