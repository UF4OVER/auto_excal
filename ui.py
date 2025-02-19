#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

from PyQt5.QtCore import Qt, QEventLoop, QTimer, QRectF
from PyQt5.QtGui import QIcon, QKeySequence, QPixmap, QPainter, QColor, QPen, QBrush, QPainterPath, QRegion
from PyQt5.QtWidgets import QDesktopWidget, QShortcut, QSystemTrayIcon, QAction, QMenu, QWidget, QSplashScreen, \
    QScrollArea, QLabel, QTextEdit, QVBoxLayout
from siui.core import SiGlobal
from siui.templates.application.application import SiliconApplication

from parts.component.DynamicIsland import DynamicIsland
from parts.component.layer_left_global import LayerLeftGlobalDrawer
from parts.page import (AboutPage,
                        UserPage,
                        HomePage,
                        AutoFormPage,
                        MusicPage,
                        SettingPage,
                        UpdatePage)
import config.CONFIG as F

PATH_CONFIG = F.CONFIG_PATH
PATH_PIC = F.PNG_PATH


class My_SiliconApplication(SiliconApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layer_left_global_drawer = LayerLeftGlobalDrawer(self)
        self.dynamic_island = DynamicIsland(self)
        self.layerMain().container_title.addWidget(self.dynamic_island)

    def Dynamic_Island(self):
        return self.dynamic_island

    def showEvent(self, event):
        super().showEvent(event)
        self.dynamic_island.move(self.size().width() // 2 - 200, 15)

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
        self.layerMain().addPage(UserPage(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_content_view_gallery_lightning_regular"),
                                 hint="我的", side="bottom")

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
        QTimer.singleShot(1000, loop.quit)
        loop.exec()


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
        # 初始设置圆角区域
        self.updateMask()
        self.setup_labels()

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
        from PyQt5.QtGui import QPainter, QColor, QBrush
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setBrush(QBrush(QColor(87, 63, 101)))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)

        # pixmap = QPixmap(f"{PATH_PIC}\\default.jpg")
        # pixmap = pixmap.scaledToHeight(self.height(), Qt.SmoothTransformation)
        # # 计算图片的绘制位置以使其垂直居中
        # # x = (self.width() - pixmap.width()) // 2 居中
        # x = 0
        # y = 0  # 垂直居中
        #
        # # 绘制背景图片
        # painter.drawPixmap(x, y, pixmap)

    def setup_labels(self):
        self.label_1 = QLabel(self)
        self.label_1.setText("Wedding Invitation")
        self.label_1.setStyleSheet("""
            color: #ffffff;
            font-size: 12px;
            font-weight: bold;
        """)
        self.label_1.move(700, 20)

