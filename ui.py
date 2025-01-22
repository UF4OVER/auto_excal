#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

import configparser
import icons

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QDesktopWidget, QShortcut

from siui.core import SiColor, SiGlobal
from siui.templates.application.application import SiliconApplication

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
import config.CONFIG

PATH_CONFIG = config.CONFIG.CONFIG_PATH


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
        self.dynamic_island.move(self.size().width() // 2 - 150, 15)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # print(f"event.size().width()//2::{event.size().width() // 3}")
        self.dynamic_island.move(event.size().width() // 2 - 150, 15)


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
        self.setWindowIcon(QIcon("pic/圆角-default.jpg"))

        self.layerMain().addPage(Homepage(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_home_filled"),
                                 hint="主页", side="top")
        self.layerMain().addPage(Autoexcal(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_table_stack_right_filled"),
                                 hint="表单", side="top")
        self.layerMain().addPage(PageMusicPage(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_music_note_2_play_filled"),
                                 hint="音乐", side="top")
        self.layerMain().addPage(About(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_info_filled"),
                                 hint="关于", side="bottom")
        self.layerMain().addPage(PageSettingPage(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_settings_filled"),
                                 hint="设置", side="bottom")

        self.layerMain().setPage(0)

        SiGlobal.siui.reloadAllWindowsStyleSheet()

    def GlobalLeft(self):
        SiGlobal.siui.windows["MAIN_WINDOW"].layerLeftGlobalDrawer().showLayer()

    def ShortcutKey(self):
        shortcut_show = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_A), self)
        shortcut_show.setContext(Qt.ApplicationShortcut)  # 设置为全局快捷键
        shortcut_show.activated.connect(self.GlobalLeft)  # 连接 GlobalLeft 方法

    def closeEvent(self, event):
        config = configparser.ConfigParser()
        config.read(PATH_CONFIG)
        config = config["switch_options"]
        config_content = config.getboolean("enable_switch")
        print(f"read_ui_enable_switch:{config_content}")

        if config_content:
            self.event = event
            if self.stu:
                event.accept()
            else:
                self.event.ignore()
                temp_widget = CloseModalDialog(self)
                SiGlobal.siui.windows["MAIN_WINDOW"].layerModalDialog().setDialog(temp_widget)
                temp_widget.user_decision.connect(self._sw_stu)  # 连接信号到槽
        else:
            SiGlobal.siui.windows["MAIN_WINDOW"].close()
            event.accept()

    def _sw_stu(self):
        self.stu = not self.stu
        SiGlobal.siui.windows["MAIN_WINDOW"].close()
