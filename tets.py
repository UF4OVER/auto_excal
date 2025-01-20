# -*- coding: utf-8 -*-
# @Time : 2023/9/3 21:41
# @Author : Leuanghing Chen
# @Blog : https://blog.csdn.net/weixin_46153372?spm=1010.2135.3001.5421
# @File : 基于pyqt5的Qlabel字幕滚动.py
# @Software : PyCharm

from PyQt5.QtCore import QTimer
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("滚动字幕示例")
        self.resize(300, 100)

        layout = QVBoxLayout()

        self.label = QLabel("时间不会辜负奋斗者的每一滴汗水，所有的努力都是在为更好的未来添砖加瓦。")
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        layout.addWidget(self.label)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.scroll_text)
        self.timer.start(100)  # 设置滚动速度，单位为毫秒

    def scroll_text(self):
        current_text = self.label.text()
        scroll_text = current_text[1:] + current_text[0]
        self.label.setText(scroll_text)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

