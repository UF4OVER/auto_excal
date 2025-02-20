#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

from PyQt5.QtCore import Qt, QEventLoop, QTimer, QRectF, pyqtProperty, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QIcon, QKeySequence, QPixmap, QPainter, QColor, QBrush, QPainterPath, QRegion, QFont, \
    QLinearGradient
from PyQt5.QtWidgets import QDesktopWidget, QShortcut, QSystemTrayIcon, QAction, QMenu, QWidget, QLabel, \
    QGraphicsOpacityEffect
from siui.core import SiGlobal
from siui.templates.application.application import SiliconApplication

import config.CONFIG as F
from parts.component import DynamicIsland, QuickActions
from parts.component.layer_left_global import LayerLeftGlobalDrawer
from parts.page import (AboutPage,
                        UserPage,
                        HomePage,
                        AutoFormPage,
                        MusicPage,
                        SettingPage,
                        UpdatePage)

PATH_CONFIG = F.CONFIG_PATH
PATH_PIC = F.PNG_PATH


class My_SiliconApplication(SiliconApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layer_left_global_drawer = LayerLeftGlobalDrawer(self)
        self.dynamic_island = DynamicIsland(self)
        self.quick_actions = QuickActions(self)
        self.layerMain().container_title.addWidget(self.dynamic_island)
        self.layerMain().container_title.addWidget(self.quick_actions, "right")

    def Dynamic_Island(self):
        return self.dynamic_island

    def QuickActions(self):
        return self.quick_actions

    def showEvent(self, event):
        super().showEvent(event)
        self.dynamic_island.move(self.size().width() // 2 - 200, 15)
        self.quick_actions.move(self.size().width() - 200, 15)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.dynamic_island.move(event.size().width() // 2 - 200, 15)


class MySiliconApp(My_SiliconApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        screen_geo = QDesktopWidget().screenGeometry()
        self.stu = False
        self.setMinimumSize(1200, 500)
        self.resize(1350, 900)
        self.setMaximumSize(1500, 1200)
        self.move((screen_geo.width() - self.width()) // 2, (screen_geo.height() - self.height()) // 2)
        self.layerMain().setTitle("Loot Hearts系列")
        self.setWindowTitle("Wedding Invitation")
        print("$" * 50)
        self.slashScreen = SplashScreen()
        self.slashScreen.show()
        self.createSubInterface()
        print("$" * 50)

        self.ShortcutKey()
        self.setWindowIcon(QIcon(f"{PATH_PIC}/圆角-default.jpg"))

        self.layerMain().addPage(HomePage(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_home_filled"),
                                 hint="主页", side="top")
        self.layerMain().addPage(AutoFormPage(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_table_stack_right_filled"),
                                 hint="表单", side="top")
        self.layerMain().addPage(MusicPage(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_music_note_2_play_filled"),
                                 hint="音乐", side="top")
        # self.layerMain().addPage(UserPage(self),
        #                          icon=SiGlobal.siui.iconpack.get("ic_fluent_content_view_gallery_lightning_regular"),
        #                          hint="我的", side="bottom")

        self.layerMain().addPage(AboutPage(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_info_filled"),
                                 hint="关于", side="bottom")
        self.layerMain().addPage(SettingPage(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_settings_filled"),
                                 hint="设置", side="bottom")
        self.layerMain().addPage(UpdatePage(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_cloud_sync_filled"),
                                 hint="更新", side="bottom")

        self.layerMain().setPage(0)

        SiGlobal.siui.reloadAllWindowsStyleSheet()
        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(QIcon(f"{PATH_PIC}/圆角-default.jpg"), self)
        self.tray_icon.setToolTip("Wedding Invitation")

        # 创建托盘菜单
        self.tray_menu = QMenu(self)
        show_action = QAction("作者:UF4OVER", self)
        quit_action = QAction("退出", self)

        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(self.quit_app)

        self.tray_menu.addAction(show_action)
        self.tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_menu.setStyleSheet("""
            QMenu {
                background-color: #2c313c;
                border: 1px solid #2c313c;
                border-radius: 5px;
                color: #ffffff;
                font-size: 12px;
            }
            QMenu::item:selected {
                background-color: #3a3f4b;
            }
        """)

        # 显示托盘图标
        self.tray_icon.show()
        self.slashScreen.close()

    def GlobalLeft(self):
        SiGlobal.siui.windows["MAIN_WINDOW"].layerLeftGlobalDrawer().showLayer()

    def ShortcutKey(self):
        shortcut_show = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_A), self)
        shortcut_show.setContext(Qt.ApplicationShortcut)  # 设置为全局快捷键
        shortcut_show.activated.connect(self.GlobalLeft)  # 连接 GlobalLeft 方法

    def quit_app(self):
        self.close()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()

    def createSubInterface(self):
        loop = QEventLoop(self)
        QTimer.singleShot(1200, loop.quit)
        loop.exec()


class Label(QLabel):
    def __init__(self, p=None, text=None, size=None):
        super().__init__(p)
        self._text = text
        self._size = size
        self.setText(self._text)
        self.setStyleSheet("color: #ffffff;")
        self.setFont(QFont("Microsoft YaHei", self._size, QFont.Bold))


class SplashScreen(QWidget):
    # 启动界面
    def __init__(self):
        super().__init__()
        # 去除系统边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 确保此时窗口在最顶层
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        # 设置窗口透明背景
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(800, 600)
        # 获取屏幕尺寸
        screen_geo = QDesktopWidget().screenGeometry()

        # 初始设置圆角区域
        self.updateMask()
        self.setup_labels()

        self.scale_animation = QPropertyAnimation(self, b"geometry")
        self.scale_animation.setDuration(400)
        # 计算屏幕底部中央的起始位置
        start_x = (screen_geo.width() - self.width()) // 2
        start_y = screen_geo.height() - 100  # 起始时距离屏幕底部100像素
        start_width = self.width()
        start_height = 100  # 初始高度较小

        # 设置起始值为屏幕底部中央的小窗口
        self.scale_animation.setStartValue(QRect(start_x, start_y, start_width, start_height))

        # 计算屏幕中心的目标位置
        end_x = (screen_geo.width() - 800) // 2
        end_y = (screen_geo.height() - 600) // 2
        end_width = 800
        end_height = 600

        # 设置结束值为目标窗口大小
        self.scale_animation.setEndValue(QRect(end_x, end_y, end_width, end_height))
        self.scale_animation.setEasingCurve(QEasingCurve.InOutExpo)  # 反弹效果
        self.scale_animation.start()

        self._radius = 55

        # 创建动画
        self.animation = QPropertyAnimation(self, b"radius")
        self.animation.setDuration(600)  # 动画持续时间
        self.animation.setStartValue(0)
        self.animation.setEndValue(500)  # 扩散的最大半径
        self.animation.setLoopCount(1)  # 无限循环
        self.animation.setEasingCurve(QEasingCurve.InOutSine)
        self.animation.start()

    def updateMask(self):
        path = QPainterPath()
        # 将 self.rect() 转换为 QRectF
        rectF = QRectF(self.rect())
        radius = 20  # 调整圆角半径
        path.addRoundedRect(rectF, radius, radius)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def resizeEvent(self, event):
        self.updateMask()
        super().resizeEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制窗口背景
        painter.setBrush(QBrush(QColor(37, 34, 42)))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)
        # 绘制扩散效果
        painter.setBrush(QBrush(QColor(51, 46, 56)))  # 半透明白色
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(self.width() // 2 - self._radius, self.height() // 2 - self._radius, 2 * self._radius,
                            2 * self._radius)

        # 加载图片并缩放
        pixmap = QPixmap(f"{PATH_PIC}\\default.jpg")
        pixmap = pixmap.scaledToHeight(self.height(), Qt.SmoothTransformation)
        # 计算图片的绘制位置以使其垂直居中
        # x = (self.width() - pixmap.width()) // 2 居中
        x = 0
        y = 0  # 垂直居中

        # 绘制背景图片
        painter.drawPixmap(x, y, pixmap)
        # 创建一个矩形模板
        gradient = QLinearGradient(0, 0, self.height(), 0)
        gradient.setColorAt(0, QColor(255, 255, 255, 0))  # 透明
        gradient.setColorAt(0.7, QColor(51, 46, 56, 128))
        gradient.setColorAt(1, QColor(51, 46, 56))

        painter.setBrush(QBrush(gradient))
        painter.drawRect(0, 0, self.height() + 20, self.height())

        painter.end()

    @pyqtProperty(int)
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value
        self.update()

    def setup_labels(self):
        self.label_1 = Label(self, "Loot Hearts 系列", 11)
        self.label_1.move(610, 100)
        self.label_2 = Label(self, "Wedding Invitation", 9)
        self.label_2.move(610, 150)
        self.label_3 = Label(self, f"VERSION : {F.VERSION}", 8)
        self.label_3.move(610, 370)
        self.label_4 = Label(self, f"AUTHOR : {F.AUTHOR}", 8)
        self.label_4.move(610, 400)
        self.label_5 = Label(self, f"TODAY : {F.TODAY}", 8)
        self.label_5.move(610, 430)

        self.label_6 = Label(self, "Loading...", 11)
        self.label_6.move(630, 500)

        self.label_7 = Label(self, "Copyright © 2025 UF4OVER", 7)
        self.label_7.move(610, 570)
