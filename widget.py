import ctypes
import sys
from ctypes import *
from ctypes.wintypes import DWORD, BOOL, HWND, ULONG

from PyQt5.QtCore import QPropertyAnimation, Qt, QRect
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPainterPath, QRegion
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, \
    QGraphicsDropShadowEffect, QFrame


# ================ 亚克力效果相关结构体和枚举 =================

class ACCENT_STATE:
    ACCENT_DISABLED = 1
    ACCENT_ENABLE_GRADIENT = 1
    ACCENT_ENABLE_TRANSPARENTGRADIENT = 2
    ACCENT_ENABLE_BLURBEHIND = 3  # Aero效果
    ACCENT_ENABLE_ACRYLICBLURBEHIND = 4  # 亚克力效果
    ACCENT_INVALID_STATE = 5


class ACCENT_POLICY(Structure):
    _fields_ = [
        ("AccentState", DWORD),
        ("AccentFlags", DWORD),
        ("GradientColor", DWORD),
        ("AnimationId", DWORD)
    ]


class WINDOWCOMPOSITIONATTRIB:
    WCA_ACCENT_POLICY = 20


class WINDOWCOMPOSITIONATTRIBDATA(Structure):
    _fields_ = [
        ("Attribute", DWORD),
        ("Data", POINTER(ACCENT_POLICY)),
        ("SizeOfData", ULONG)
    ]


# ================ 自定义标题栏 =================
class TitleBar(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(40)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 80);")
        self.initUI()
        self._startPos = None
        self.parent_window = parent  # 保存父窗口的引用

    def initUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(5)

        self.titleLabel = QLabel("Acrylic Frameless Window")
        self.titleLabel.setStyleSheet("color: white; font-size: 16px;")
        layout.addWidget(self.titleLabel)
        layout.addStretch()

        self.minButton = QPushButton("-")
        self.minButton.setFixedSize(30, 30)
        self.minButton.setStyleSheet(
            "QPushButton {background-color: rgba(255,255,255,0.3); color: white; border: none; border-radius: 5px;}"
            "QPushButton:hover {background-color: rgba(255,255,255,0.5);}"
        )
        self.minButton.clicked.connect(self.onMinimize)
        layout.addWidget(self.minButton)

        self.maxButton = QPushButton("□")
        self.maxButton.setFixedSize(30, 30)
        self.maxButton.setStyleSheet(
            "QPushButton {background-color: rgba(255,255,255,0.3); color: white; border: none; border-radius: 5px;}"
            "QPushButton:hover {background-color: rgba(255,255,255,0.5);}"
        )
        self.maxButton.clicked.connect(self.onMaximize)
        layout.addWidget(self.maxButton)

        self.closeButton = QPushButton("×")
        self.closeButton.setFixedSize(30, 30)
        self.closeButton.setStyleSheet(
            "QPushButton {background-color: rgba(255,0,0,0.5); color: white; border: none; border-radius: 5px;}"
            "QPushButton:hover {background-color: rgba(255,0,0,0.7);}"
        )
        self.closeButton.clicked.connect(self.onClose)
        layout.addWidget(self.closeButton)

    def onMinimize(self):
        self.parent_window.minimize_animation.setStartValue(self.parent_window.geometry())
        self.parent_window.minimize_animation.setEndValue(QRect(0, 0, 1, 1))  # 缩小到最小
        self.parent_window.minimize_animation.start()

    def onMaximize(self):
        if self.parent_window.isMaximized():
            self.parent_window.maximize_animation.setStartValue(self.parent_window.geometry())
            self.parent_window.maximize_animation.setEndValue(self.parent_window.normalGeometry())
            self.parent_window.maximize_animation.start()
            self.maxButton.setText("□")
        else:
            self.parent_window.maximize_animation.setStartValue(self.parent_window.geometry())
            self.parent_window.maximize_animation.setEndValue(self.parent_window.screen().geometry())
            self.parent_window.maximize_animation.start()
            self.maxButton.setText("❐")

    def onClose(self):
        self.parent_window.fade_out_animation.start()

    # 拖动窗口实现：仅在标题栏上实现拖动
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._startPos = event.globalPos()
        event.accept()

    def mouseMoveEvent(self, event):
        if self._startPos:
            delta = event.globalPos() - self._startPos
            self.window().move(self.window().pos() + delta)
            self._startPos = event.globalPos()
        event.accept()

    def mouseReleaseEvent(self, event):
        self._startPos = None
        event.accept()

    def resizeEvent(self, event):
        super().resizeEvent(event)


# ================ 主窗口：亚克力 + 无边框 + 自定义标题栏 + 边缘缩放 + 圆角 =================


class AcrylicFramelessWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._border_width = 10
        self.initWindow()
        self.initAcrylicEffect()
        self.initDropShadow()
        self.initUI()
        self.updateMask()

        # 创建透明度动画
        self.fade_in_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_animation.setDuration(100)  # 动画持续时间
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)

        self.fade_out_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_out_animation.setDuration(100)  # 动画持续时间
        self.fade_out_animation.setStartValue(1.0)
        self.fade_out_animation.setEndValue(0.0)
        self.fade_out_animation.finished.connect(self.close)  # 动画结束后关闭窗口

        self.maximize_animation = QPropertyAnimation(self, b"geometry")
        self.maximize_animation.setDuration(200)  # 动画持续时间

        self.minimize_animation = QPropertyAnimation(self, b"geometry")
        self.minimize_animation.setDuration(200)  # 动画持续时间

        self.fade_in_animation.start()

    def initWindow(self):
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint |
                            Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.resize(800, 600)

    def initAcrylicEffect(self):
        hwnd = int(self.winId())
        gradientColor_str = "FFFFFFFF"
        gradientColor_swapped = gradientColor_str[6:] + gradientColor_str[4:6] + gradientColor_str[
                                                                                 2:4] + gradientColor_str[:2]
        gradientColor = DWORD(int(gradientColor_swapped, 16))
        accentFlags = DWORD(0x20 | 0x40 | 0x80 | 0x100)
        accent = ACCENT_POLICY()
        accent.AccentState = ACCENT_STATE.ACCENT_ENABLE_ACRYLICBLURBEHIND
        accent.GradientColor = gradientColor
        accent.AccentFlags = accentFlags
        accent.AnimationId = DWORD(0)  # 设置为 0，不使用动画

        data = WINDOWCOMPOSITIONATTRIBDATA()
        data.Attribute = WINDOWCOMPOSITIONATTRIB.WCA_ACCENT_POLICY
        data.Data = pointer(accent)
        data.SizeOfData = sizeof(accent)

        user32 = ctypes.windll.user32
        SetWindowCompositionAttribute = user32.SetWindowCompositionAttribute
        SetWindowCompositionAttribute.restype = BOOL
        SetWindowCompositionAttribute.argtypes = [HWND, POINTER(WINDOWCOMPOSITIONATTRIBDATA)]
        SetWindowCompositionAttribute(hwnd, pointer(data))

    def initDropShadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)

    def initUI(self):
        container = QWidget(self)
        container.setObjectName("container")
        container.setStyleSheet("""
            #container {
                background-color: rgba(255, 255, 255, 30);
                border-radius: 8px;
            }
        """)
        self.setCentralWidget(container)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.titleBar = TitleBar(self)
        layout.addWidget(self.titleBar)

        content = QWidget(self)
        content.setStyleSheet("background-color: transparent;")
        layout.addWidget(content)
        # content_layout = QVBoxLayout(content)
        # content_layout.addStretch()
        # label = QLabel("这里是窗口的主要内容区域", self)
        # label.setStyleSheet("color: white; font-size: 20px;")
        # label.setAlignment(Qt.AlignCenter)
        # content_layout.addWidget(label)
        # content_layout.addStretch()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._mouse_press_pos = event.globalPos()
            self._mouse_press_geometry = self.geometry()
            pos = event.pos()
            rect = self.rect()
            if pos.x() >= rect.width() - self._border_width and pos.y() >= rect.height() - self._border_width:
                self._resizing = True
                self._resize_direction = "bottomright"
            elif pos.x() >= rect.width() - self._border_width:
                self._resizing = True
                self._resize_direction = "right"
            elif pos.y() >= rect.height() - self._border_width:
                self._resizing = True
                self._resize_direction = "bottom"
            else:
                self._resizing = False
                self._resize_direction = None
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        pos = event.pos()
        rect = self.rect()
        if not (event.buttons() & Qt.LeftButton):
            if pos.x() >= rect.width() - self._border_width and pos.y() >= rect.height() - self._border_width:
                self.setCursor(Qt.SizeFDiagCursor)
            elif pos.x() >= rect.width() - self._border_width:
                self.setCursor(Qt.SizeHorCursor)
            elif pos.y() >= rect.height() - self._border_width:
                self.setCursor(Qt.SizeVerCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
        if event.buttons() & Qt.LeftButton and getattr(self, '_resizing', False):
            delta = event.globalPos() - self._mouse_press_pos
            new_geo = self._mouse_press_geometry
            if self._resize_direction == "bottomright":
                new_width = max(new_geo.width() + delta.x(), 200)
                new_height = max(new_geo.height() + delta.y(), 150)
                self.setGeometry(new_geo.x(), new_geo.y(), new_width, new_height)
            elif self._resize_direction == "right":
                new_width = max(new_geo.width() + delta.x(), 200)
                self.setGeometry(new_geo.x(), new_geo.y(), new_width, new_geo.height())
            elif self._resize_direction == "bottom":
                new_height = max(new_geo.height() + delta.y(), 150)
                self.setGeometry(new_geo.x(), new_geo.y(), new_geo.width(), new_height)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._resizing = False
        self._resize_direction = None
        self.setCursor(Qt.ArrowCursor)
        super().mouseReleaseEvent(event)

    def updateMask(self):
        radius = 15
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), radius, radius)
        region = QRegion(path.toFillPolygon().toPolygon())

        self.setMask(region)
        if self.centralWidget():
            self.centralWidget().setMask(region)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateMask()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AcrylicFramelessWindow()
    window.show()
    sys.exit(app.exec_())
