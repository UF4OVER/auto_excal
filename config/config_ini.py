# -*- coding: utf-8 -*-
#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

# ------------------------------
#  @Project : upper_computer
#  @Time    : 2024 - 12-22 14:55
#  @FileName: config_ini.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact :
#  @Python  : 3.10
# -------------------------------
from pathlib import Path
from typing import Union

from PyQt5.QtCore import QSettings

import sys

class SettingsManager:
    def __init__(self, config_path: Path):
        self.config_path = str(config_path.resolve())
        self.settings = QSettings(self.config_path, QSettings.IniFormat)
        self.duplicate_filter: bool = False
    def get(self, section: str, option: str, fallback: Union[str, int, bool] = None) -> Union[str, int, bool]:
        key = f"{section}/{option}"
        if self.settings.contains(key):
            value = self.settings.value(key)
            if isinstance(fallback, bool):
                return value.lower() == 'true' if isinstance(value, str) else bool(value)
            if isinstance(fallback, int):
                try:
                    return int(value)
                except ValueError:
                    return fallback
            return value
        return fallback

    def set(self, section: str, option: str, value: Union[str, int, bool]):
        key = f"{section}/{option}"
        self.settings.setValue(key, value)
        self.settings.sync()

    @property
    def base_dir(self) -> Path:
        if getattr(sys, 'frozen', False):
            # 打包后
            return Path(sys.executable).resolve().parent
        else:
            # 正常运行
            return Path(__file__).resolve().parent.parent

    @property
    def png_dir(self) -> Path:
        return self.base_dir / "assets"


