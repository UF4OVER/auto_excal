# -*- coding: utf-8 -*-

#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

# -------------------------------
#  @Project : 11.py
#  @Time    : 2025 - 02-20 19:19
#  @FileName: logInToPortlet.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------


import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGraphicsOpacityEffect, QStyleOptionButton,
    QStyle
)
from PyQt5.QtGui import QPainter, QBrush, QColor, QIcon, QPixmap, QPainterPath, QFont
from PyQt5.QtCore import Qt, QSize, QTimer, QPropertyAnimation, QRect, pyqtProperty

from config.qss import LoginBtuQss
import config.CONFIG as F


# 自定义按钮，实现按下/抬起的缩放动画
class AnimatedButton(QLabel):
    def __init__(self, text="", parent=None):
        # 为了方便使用样式和图标，这里继承自 QLabel 并模拟按钮效果
        super(AnimatedButton, self).__init__(parent)
        self.setText(text)
        self.setFont(QFont("微软雅黑", 12))
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(LoginBtuQss)
        self._scale = 1.0
        self.press_anim = QPropertyAnimation(self, b"scale", self)
        self.press_anim.setDuration(100)
        self.release_anim = QPropertyAnimation(self, b"scale", self)
        self.release_anim.setDuration(100)
        self.setFixedSize(200, 50)
        # 鼠标跟踪开启，用于改变光标
        self.setMouseTracking(True)
        self.setCursor(Qt.PointingHandCursor)
        self._icon = None
        self._iconSize = QSize(30, 30)

    def setIcon(self, icon):
        if isinstance(icon, QIcon):
            self._icon = icon
        else:
            self._icon = QIcon(icon)
        self.update()

    def setIconSize(self, size):
        if isinstance(size, QSize):
            self._iconSize = size
        else:
            self._iconSize = QSize(size, size)
        self.update()

    def mousePressEvent(self, event):
        self.start_press_animation()
        super(AnimatedButton, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.start_release_animation()
        # 发射 clicked 信号，方便外部连接槽函数
        self.clicked()
        super(AnimatedButton, self).mouseReleaseEvent(event)

    # 自定义信号的模拟，这里直接调用函数
    def clicked(self):
        # 可重载或通过外部赋值实现
        if hasattr(self, "_click_callback") and self._click_callback:
            self._click_callback()

    def setClickedCallback(self, callback):
        self._click_callback = callback

    def getScale(self):
        return self._scale

    def setScale(self, scale):
        self._scale = scale
        self.update()

    scale = pyqtProperty(float, getScale, setScale)

    def start_press_animation(self):
        self.press_anim.stop()
        self.press_anim.setStartValue(self._scale)
        self.press_anim.setEndValue(0.95)
        self.press_anim.start()

    def start_release_animation(self):
        self.release_anim.stop()
        self.release_anim.setStartValue(self._scale)
        self.release_anim.setEndValue(1.0)
        self.release_anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # 缩放变换，中心缩放
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(self._scale, self._scale)
        painter.translate(-self.width() / 2, -self.height() / 2)
        # 绘制背景（使用样式表绘制的效果就不调用父类绘制了）
        opt = QStyleOptionButton()
        opt.initFrom(self)
        opt.rect = self.rect()
        self.style().drawControl(QStyle.CE_PushButton, opt, painter, self)
        # 绘制图标和文字
        margin = 10
        x = margin
        if self._icon:
            iconRect = QRect(x, (self.height() - self._iconSize.height()) // 2, self._iconSize.width(),
                             self._iconSize.height())
            self._icon.paint(painter, iconRect)
            x += self._iconSize.width() + margin
        # 绘制文本
        textRect = QRect(x, 0, self.width() - x, self.height())
        painter.drawText(textRect, Qt.AlignVCenter | Qt.AlignLeft, self.text())


class CarouselWidget(QWidget):
    def __init__(self, image_paths, parent=None):
        super(CarouselWidget, self).__init__(parent)
        self.image_paths = image_paths
        self.current_index = 0

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.update_image()

        self.opacity_effect = QGraphicsOpacityEffect(self.label)
        self.label.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_image)
        self.timer.start(3000)

        self.fade_out = None
        self.fade_in = None

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def update_image(self):
        pixmap = QPixmap(self.image_paths[self.current_index])
        if pixmap.isNull():
            return
        # 裁剪为正方形：以中心区域为准
        side = min(pixmap.width(), pixmap.height())
        x = (pixmap.width() - side) // 2
        y = (pixmap.height() - side) // 2
        square_pixmap = pixmap.copy(QRect(x, y, side, side))
        square_pixmap = square_pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        rounded_pixmap = self.getRoundedPixmap(square_pixmap, 50)
        self.label.setPixmap(rounded_pixmap)

    def getRoundedPixmap(self, pixmap, radius):
        rounded = QPixmap(pixmap.size())
        rounded.fill(Qt.transparent)
        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0, 0, pixmap.width(), pixmap.height(), radius, radius)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()
        return rounded

    def next_image(self):
        self.fade_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out.setDuration(500)
        self.fade_out.setStartValue(1)
        self.fade_out.setEndValue(0)
        self.fade_out.finished.connect(self.on_fade_out_finished)
        self.fade_out.start()

    def on_fade_out_finished(self):
        self.current_index = (self.current_index + 1) % len(self.image_paths)
        self.update_image()
        self.fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in.setDuration(500)
        self.fade_in.setStartValue(0)
        self.fade_in.setEndValue(1)
        self.fade_in.start()


class LoginWindow(QMainWindow):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setWindowTitle("第三方登录")
        self.resize(800, 400)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

        mainWidget = QWidget(self)
        mainWidget.setObjectName("mainWidget")
        mainWidget.setStyleSheet("""
            QWidget#mainWidget {
                background-color: rgba(255, 255, 255, 80);
                border: 1px solid #ccc;
                border-radius: 15px;
            }
        """)
        self.setCentralWidget(mainWidget)

        mainLayout = QHBoxLayout(mainWidget)
        mainLayout.setContentsMargins(20, 20, 20, 20)
        mainLayout.setSpacing(20)

        # 左侧轮播图区域
        image_paths = [f"{F.PIC_LOGIN_PATH}\\1.jpg", f"{F.PIC_LOGIN_PATH}\\2.jpg", f"{F.PIC_LOGIN_PATH}\\3.jpg"]  # 替换为实际图片路径
        carousel = CarouselWidget(image_paths)
        carousel.setFixedSize(300, 300)
        mainLayout.addWidget(carousel)

        loginWidget = QWidget()
        loginLayout = QVBoxLayout(loginWidget)
        loginLayout.setAlignment(Qt.AlignCenter)
        loginLayout.setSpacing(20)

        h_loginLayout = QVBoxLayout(loginWidget)
        h_loginLayout.setAlignment(Qt.AlignCenter)
        h_loginLayout.setSpacing(10)

        titleLabel = QLabel("使用第三方登录")
        titleLabel.setStyleSheet("font-size: 18px;")
        titleLabel.setFont(QFont("微软雅黑", 12))

        h_loginLayout.addWidget(titleLabel)

        loginLayout.addLayout(h_loginLayout)

        self.btnHUAWEI = AnimatedButton("  HUAWEI登录")
        self.btnHUAWEI.setIcon(f"{F.PIC_LOGIN_PATH}\\login_huawei.png")  # 请确保该图片存在
        self.btnHUAWEI.setIconSize(QSize(30, 30))
        loginLayout.addWidget(self.btnHUAWEI)

        # Facebook 登录按钮
        self.btnGITHUB = AnimatedButton("  GitHub登录")
        self.btnGITHUB.setIcon(f"{F.PIC_LOGIN_PATH}\\logo_github.png")
        self.btnGITHUB.setIconSize(QSize(30, 30))
        loginLayout.addWidget(self.btnGITHUB)

        mainLayout.addWidget(loginWidget)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        painter.setBrush(QBrush(QColor(51, 46, 56, 80)))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 15, 15)

    def HuaweiBtn(self):
        return self.btnHUAWEI

    def GithubBtn(self):
        return self.btnGITHUB


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())



