#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

from PyQt5.QtWidgets import QDesktopWidget
from siui.core import SiGlobal
from siui.templates.application.application import SiliconApplication

from parts.component.DynamicIsland import DynamicIsland
from parts.component.GlobalLeftWindow import LayerLeftGlobalDrawer
from parts.page.page_home import Homepage
from parts.page.page_excal import Excal
class My_SiliconApplication(SiliconApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layer_left_global_drawer = LayerLeftGlobalDrawer(self)
        self.dynamic_island = DynamicIsland(self)
        self.layerMain().container_title.addWidget(self.dynamic_island)

    def Dynamic_Island(self):
        return self.dynamic_island

    def QuickActions(self):
        return self.quick_actions

    def showEvent(self, event):
        super().showEvent(event)
        self.dynamic_island.move(self.size().width() // 2 - 200, 15)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.dynamic_island.move(event.size().width() // 2 - 200, 15)


class MySiliconApp(My_SiliconApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.setWindowIcon(QIcon(f"{PATH_PIC}/圆角-default.jpg"))

        screen_geo = QDesktopWidget().screenGeometry()
        self.stu = False
        self.setMinimumSize(1200, 500)
        self.resize(1350, 900)
        self.setMaximumSize(1500, 1200)
        self.move((screen_geo.width() - self.width()) // 2, (screen_geo.height() - self.height()) // 2)
        self.layerMain().setTitle("Loot Hearts系列")
        self.setWindowTitle("Wedding Invitation")

        self.layerMain().addPage(Homepage(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_home_filled"),
                                 hint="主页", side="top")
        self.layerMain().addPage(Excal(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_text_bullet_list_square_search_filled"),
                                 hint="Excal",side="top")

        self.layerMain().setPage(0)

        SiGlobal.siui.reloadAllWindowsStyleSheet()


