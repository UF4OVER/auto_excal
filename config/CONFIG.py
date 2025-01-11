# -*- coding: utf-8 -*-

#  Copyright (c) 2025. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

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
