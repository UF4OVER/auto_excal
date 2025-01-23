# -*- coding: utf-8 -*-

#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

import logging
import sys
from typing import overload


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
        logging.basicConfig(filename='app.log',
                            level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            filemode="w")

        logger = logging.getLogger()
        sys.stdout = StreamToLogger(logger, logging.INFO)
        sys.stderr = StreamToLogger(logger, logging.ERROR)

    else:
        print("Logging is disabled.")
        pass
