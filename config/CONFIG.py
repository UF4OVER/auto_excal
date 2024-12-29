# -*- coding: utf-8 -*-
# -------------------------------
#  @Project : upper_computer
#  @Time    : 2024 - 12-22 14:55
#  @FileName: CONFIG.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 3.10
# -------------------------------
import enum
import os


class CONFIG(enum.Enum):
    PATH_CONFIG: str = os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        ), 'config\config.ini')


CONFIG_PATH: str = CONFIG.PATH_CONFIG.value
print(f"全局配置文件路径:{CONFIG_PATH}")
