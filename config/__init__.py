# -*- coding: utf-8 -*-
# -------------------------------
#  @Project : siui_refactor
#  @Time    : 2025 - 07-17 18:19
#  @FileName: __init__.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------
from pathlib import Path

from .config_ini import SettingsManager as _SettingsManager
from .config_log import logger as _logger

INI_PATH = Path(__file__).resolve().parent / "config.ini"
if not INI_PATH.exists():
    INI_PATH.touch()

Settings = _SettingsManager(INI_PATH)
Logger = _logger


AUTHER_NAME = Settings.get("name", "auther_name")
WORKER_NAME = Settings.get("name", "worker_name")
SOFTWARE_NAME = Settings.get("name", "software_name")
VERSION = Settings.get("version", "version")


