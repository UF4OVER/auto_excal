# -*- coding: utf-8 -*-

#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

# -------------------------------
#  @Project : 11.py
#  @Time    : 2025 - 02-22 20:10
#  @FileName: test_lofin.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------

from PyQt5.QtWidgets import QApplication

from event.login import LoginHuawei

if __name__ == "__main__":
    app = QApplication([])  # 必须创建应用实例
    login = LoginHuawei()
    login.start()
    app.exec_()  # 必须启动事件循环
