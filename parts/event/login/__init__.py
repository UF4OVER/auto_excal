# -*- coding: utf-8 -*-

#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

# -------------------------------
#  @Project : 11.py
#  @Time    : 2025 - 02-19 14:14
#  @FileName: __init__.py.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------

from PyQt5.QtCore import QThread, pyqtSignal


class Login(QThread):  # 登录线程的基类
    loginStarted = pyqtSignal()
    loginFinished = pyqtSignal()
    loginError = pyqtSignal(str)

    def __init__(self, parent=None, main=None):
        super().__init__(parent)
        self.main_login = main

    def run(self):
        self.loginStarted.emit()
        try:
            success = self.main_login()
            if success:
                self.loginFinished.emit()
            else:
                self.loginError.emit("登录失败，请重试")
        except Exception as e:
            self.loginError.emit(str(e))


class LoginGithub(Login):
    from .login_github import main

    def __init__(self, parent=None):
        super().__init__(parent, self.main)


class LoginHuawei(Login):
    from .login_huawei import main

    def __init__(self, parent=None):
        super().__init__(parent, self.main)
