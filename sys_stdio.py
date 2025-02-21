# -*- coding: utf-8 -*-
#  Copyright (c) 2025 UF4OVER
#   All rights reserved.
# -------------------------------
#  @Project : siui
#  @Time    : 2025 - 01-21 22:13
#  @FileName: sys_stdio.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact :
#  @Python  :
# -------------------------------
import sys

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import logging
from typing import overload

from parts.event.send_message import show_message


class StreamToLogger:
    def __init__(self, logger, log_level):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass


@overload
def setup_logging(arg: bool):
    pass


def setup_logging(arg: bool):
    if arg:
        print("Logging is enabled.")
        logging.basicConfig(filename='debug.log',
                            level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            filemode="w")

        logger = logging.getLogger()
        sys.stdout = StreamToLogger(logger, logging.INFO)
        sys.stderr = StreamToLogger(logger, logging.ERROR)

    else:
        print("Logging is disabled.")
        pass


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        # 用户中断，不记录日志
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    show_message(0, "注意，注意！！！！",
                 '假如这个出现了，就是出现了我也不知道的BUG，请截图联系开发者或者发送根目录下的app.log文件到开发者的邮箱，并且说明BUG复现步骤',
                 "error")
    print(exc_value)


# 设置全局异常处理
sys.excepthook = handle_exception
