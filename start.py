# -*- coding: utf-8 -*-
# -------------------------------
#  @Project : personalHome
#  @Time    : 2025 - 04-02 11:33
#  @FileName: ui.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact :
#  @Python  :
# -------------------------------
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from parts.pages.main import Ui_Form as form
from qframelesswindow import FramelessWindow, StandardTitleBar
from icons import GlobalPng, PngIcon, PngSize, PngColor


class TestWindow(FramelessWindow, form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setTitleBar(StandardTitleBar(self))
        self.titleBar.setTitle("Markdown Editor")
        self.titleBar.setIcon(QIcon(GlobalPng.get(PngIcon.Credit_Card, PngSize.SMALL, PngColor.BLACK)))

        self.solt()

    def solt(self):
        self.stackedWidget.setCurrentIndex(0)

        self.edit_btu.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.home_btu.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())
