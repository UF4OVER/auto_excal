# -*- coding: utf-8 -*-
# -------------------------------
#  @Project : flu_new
#  @Time    : 2025 - 02-06 23:08
#  @FileName: test.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------
import sys
from ctypes import *
from ctypes.wintypes import DWORD, BOOL, ULONG, HWND
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt


# 定义亚克力效果相关的枚举和结构体

class ACCENT_STATE:
    ACCENT_DISABLED = 0
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
    # 这里只需要用到 WCA_ACCENT_POLICY 这一项
    WCA_ACCENT_POLICY = 19


class WINDOWCOMPOSITIONATTRIBDATA(Structure):
    _fields_ = [
        ("Attribute", DWORD),
        ("Data", POINTER(ACCENT_POLICY)),
        ("SizeOfData", ULONG)
    ]


# 自定义一个实现亚克力效果的无边框窗口
class AcrylicWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Acrylic Effect Window")
        # 设置无边框窗口（注意这里与原始窗口标志或许需要保留其他样式）
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        # 为了使背景能透出效果，需要设置窗口透明属性
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.resize(800, 600)
        self.initAcrylicEffect()

    def initAcrylicEffect(self):
        # 获取窗口句柄（hWnd）
        hwnd = int(self.winId())
        # 设置亚克力效果
        # gradientColor 是 RGBA 十六进制字符串，这里给出 "F2F2F230"
        # 注意：这里需要把 RGBA 顺序转换为 Windows 接口需要的 BGRA 顺序：
        # 例如 "F2F2F230" 转换为 "30F2F2F2"
        gradientColor_str = "F2F2F230"
        # 转换顺序：取后两位为最高位，其次依次取中间部分
        gradientColor_swapped = gradientColor_str[6:] + gradientColor_str[4:6] + gradientColor_str[
                                                                                 2:4] + gradientColor_str[:2]
        gradientColor = DWORD(int(gradientColor_swapped, 16))
        # 设置是否启用阴影（这里只是标志位，具体阴影效果可以额外处理）
        accentFlags = DWORD(0x20 | 0x40 | 0x80 | 0x100)
        animationId = DWORD(0)  # 可按需求设置动画

        # 构造 ACCENT_POLICY 结构体
        accent = ACCENT_POLICY()
        accent.AccentState = ACCENT_STATE.ACCENT_ENABLE_ACRYLICBLURBEHIND
        accent.GradientColor = gradientColor
        accent.AccentFlags = accentFlags
        accent.AnimationId = animationId

        # 构造 WINDOWCOMPOSITIONATTRIBDATA 结构体
        data = WINDOWCOMPOSITIONATTRIBDATA()
        data.Attribute = WINDOWCOMPOSITIONATTRIB.WCA_ACCENT_POLICY
        data.Data = pointer(accent)
        data.SizeOfData = sizeof(accent)

        # 调用 SetWindowCompositionAttribute API
        user32 = windll.user32
        SetWindowCompositionAttribute = user32.SetWindowCompositionAttribute
        SetWindowCompositionAttribute.restype = BOOL
        SetWindowCompositionAttribute.argtypes = [HWND, POINTER(WINDOWCOMPOSITIONATTRIBDATA)]
        SetWindowCompositionAttribute(hwnd, pointer(data))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AcrylicWindow()
    window.show()
    sys.exit(app.exec_())
