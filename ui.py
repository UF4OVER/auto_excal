#  Copyright (c) 2025 UF4OVER
#   All rights reserved.
import icons

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QDesktopWidget, QShortcut, QSystemTrayIcon, QAction, QMenu

from siui.core import SiColor, SiGlobal
from siui.templates.application.application import SiliconApplication

from parts.page.page_electronicpage import PageElectronicComputing
from parts.page.page_updatepage import UpDatePage
from parts.component.DynamicIsland import DynamicIsland
from parts.event.close_event import CloseModalDialog
from parts.component.layer_left_global import LayerLeftGlobalDrawer
from parts.page.page_aboutpage import About
from parts.page.page_autoexcalpage import Autoexcal
from parts.page.page_homepage import Homepage
from parts.page.page_musicpage import PageMusicPage
from parts.page.page_settingpage import PageSettingPage

# 载入图标
SiGlobal.siui.loadIcons(
    icons.IconDictionary(
        color=SiGlobal.siui.colors.fromToken(SiColor.SVG_NORMAL)
    ).icons
)
import config.CONFIG as F

PATH_CONFIG = F.CONFIG_PATH
PATH_PIC = F.PNG_PATH


class My_SiliconApplication(SiliconApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layer_left_global_drawer = LayerLeftGlobalDrawer(self)
        self.dynamic_island = DynamicIsland(self)
        self.layerMain().container_title.addWidget(self.dynamic_island)
        # self.dynamic_island.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

    def Dynamic_Island(self):
        return self.dynamic_island

    def showEvent(self, event):
        super().showEvent(event)
        self.dynamic_island.move(self.size().width() // 2 - 200, 15)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # print(f"event.size().width()//2::{event.size().width() // 3}")
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
        self.ShortcutKey()
        self.setWindowIcon(QIcon(f"{PATH_PIC}/圆角-default.jpg"))

        self.layerMain().addPage(Homepage(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_home_filled"),
                                 hint="主页", side="top")
        self.layerMain().addPage(Autoexcal(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_table_stack_right_filled"),
                                 hint="表单", side="top")
        self.layerMain().addPage(PageMusicPage(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_music_note_2_play_filled"),
                                 hint="音乐", side="top")

        self.layerMain().addPage(PageElectronicComputing(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_content_view_gallery_lightning_regular"),
                                 hint="电子", side="top")

        self.layerMain().addPage(About(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_info_filled"),
                                 hint="关于", side="bottom")
        self.layerMain().addPage(PageSettingPage(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_settings_filled"),
                                 hint="设置", side="bottom")
        self.layerMain().addPage(UpDatePage(self),
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
