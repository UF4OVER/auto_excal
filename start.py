# -*- coding: utf-8 -*-

#  Copyright (c) 2025. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

# -------------------------------

import argparse
import configparser
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from ui import MySiliconApp, send_custom_message

import config.CONFIG

PATH_CONFIG = config.CONFIG.CONFIG_PATH


def read_config() -> tuple:  # 读取配置文件
    config = configparser.ConfigParser()
    config.read(PATH_CONFIG)
    dpi_policy = config.get('Settings', 'dpi_policy', fallback='PassThrough')
    enable_hdpi_scaling = config.getboolean('Settings', 'enable_hdpi_scaling', fallback=False)
    use_hdpi_pixmaps = config.getboolean('Settings', 'use_hdpi_pixmaps', fallback=False)
    return dpi_policy, enable_hdpi_scaling, use_hdpi_pixmaps


def main():
    parser = argparse.ArgumentParser(description="Configure High DPI settings for the application.")  # 创建解析器
    parser.add_argument('--dpi-policy', type=str, default=None,
                        choices=['PassThrough', 'Floor', 'Ceil', 'Round'],
                        help='Set the High DPI scale factor rounding policy')  # 添加命令行参数
    parser.add_argument('--enable-hdpi-scaling', action='store_true',
                        help='Enable high DPI scaling')  # 添加命令行参数
    parser.add_argument('--disable-hdpi-scaling', action='store_true',
                        help='Disable high DPI scaling')  # 添加命令行参数
    parser.add_argument('--use-hdpi-pixmaps', action='store_true',
                        help='Use high DPI pixmaps')  # 添加命令行参数
    parser.add_argument('--disable-hdpi-pixmaps', action='store_true',
                        help='Do not use high DPI pixmaps')

    args = parser.parse_args()  # 解析命令行参数

    # 读取配置文件
    dpi_policy, enable_hdpi_scaling, use_hdpi_pixmaps = read_config()  # 读取配置文件

    # 命令行参数优先级高于配置文件
    if args.dpi_policy is not None:
        dpi_policy = args.dpi_policy
    if args.enable_hdpi_scaling:
        enable_hdpi_scaling = True
    if args.disable_hdpi_scaling:
        enable_hdpi_scaling = False
    if args.use_hdpi_pixmaps:
        use_hdpi_pixmaps = True
    if args.disable_hdpi_pixmaps:
        use_hdpi_pixmaps = False

    dpi_policy_map = {
        'PassThrough': Qt.HighDpiScaleFactorRoundingPolicy.PassThrough,
        'Floor': Qt.HighDpiScaleFactorRoundingPolicy.Floor,
        'Ceil': Qt.HighDpiScaleFactorRoundingPolicy.Ceil,
        'Round': Qt.HighDpiScaleFactorRoundingPolicy.Round
    }  # 创建字典

    # 设置高DPI缩放
    QApplication.setHighDpiScaleFactorRoundingPolicy(dpi_policy_map[dpi_policy])
    if enable_hdpi_scaling:
        QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    if use_hdpi_pixmaps:
        QtWidgets.QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    window = MySiliconApp()
    window.show()
    send_custom_message()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()