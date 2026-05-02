#  Copyright (c) 2025 UF4OVER
#   All rights reserved.
#  逻辑有些糖了，新人刚开始的作品，但是杨东义没选到站长，他也加不了分了，所以应该也不会优化了，2025年7月9日12点38分

import subprocess

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDesktopWidget
from siui.core import SiGlobal
from siui.templates.application.application import SiliconApplication

import config.CONFIG as F
from parts.component import DynamicIsland
from parts.event.send import show_message
from parts.page import (AboutPage,
                        HomePage,
                        AutoFormPage,
                        SettingPage)

PATH_CONFIG = F.CONFIG_PATH
PATH_PIC = F.PNG_PATH


class My_SiliconApplication(SiliconApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dynamic_island = DynamicIsland(self)
        self.layerMain().container_title.addWidget(self.dynamic_island)

    def open_ini(self):
        try:
            subprocess.Popen(['notepad.exe', PATH_CONFIG])
        except Exception as e:
            print(f"打开文件时出错: {e}")
            show_message(3, "警告", f"打开文件时出错: {e}", "ic_fluent_task_list_ltr_filled")

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
        self.setWindowIcon(QIcon(f"{PATH_PIC}/logo.ico"))

        screen_geo = QDesktopWidget().screenGeometry()
        self.setMinimumSize(1200, 500)
        self.resize(1350, 900)
        self.setMaximumSize(1500, 1200)
        self.move((screen_geo.width() - self.width()) // 2, (screen_geo.height() - self.height()) // 2)
        self.layerMain().setTitle("Auto Excal")
        self.setWindowTitle("Auto Excal")

        self.layerMain().addPage(HomePage(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_home_filled"),
                                 hint="主页", side="top")
        self.layerMain().addPage(AutoFormPage(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_table_stack_right_filled"),
                                 hint="表单", side="top")
        self.layerMain().addPage(AboutPage(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_info_filled"),
                                 hint="关于", side="bottom")
        self.layerMain().addPage(SettingPage(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_wrench_settings_filled"),
                                 hint="更新", side="bottom")

        self.layerMain().setPage(0)

        SiGlobal.siui.reloadAllWindowsStyleSheet()

