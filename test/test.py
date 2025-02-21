# -*- coding: utf-8 -*-

#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

# -------------------------------
#  @Project : 11.py
#  @Time    : 2025 - 02-20 19:36
#  @FileName: test.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize


class SiDenseContainer(QWidget):
    def __init__(self, parent=None, orientation=QVBoxLayout.TopToBottom):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

class ThirdPartyLoginWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # 创建 Huawei 登录按钮
        huawei_button = QPushButton("Huawei Login", self)
        huawei_button.setIcon(QIcon("path_to_huawei_icon.png"))
        huawei_button.setIconSize(QSize(24, 24))
        huawei_button.setStyleSheet("""
            QPushButton {
                background-color: #007D40;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005F31;
            }
        """)
        layout.addWidget(huawei_button)

        # 创建 GitHub 登录按钮
        github_button = QPushButton("GitHub Login", self)
        github_button.setIcon(QIcon("path_to_github_icon.png"))
        github_button.setIconSize(QSize(24, 24))
        github_button.setStyleSheet("""
            QPushButton {
                background-color: #171515;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #000;
            }
        """)
        layout.addWidget(github_button)

        self.setLayout(layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # 创建 SiDenseContainer
        self.base_container = SiDenseContainer(self, QVBoxLayout.TopToBottom)

        # 创建第三方登录组件
        third_party_login_widget = ThirdPartyLoginWidget(self.base_container)

        # 将第三方登录组件添加到 SiDenseContainer
        self.base_container.layout.addWidget(third_party_login_widget)

        layout.addWidget(self.base_container)
        self.setLayout(layout)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
