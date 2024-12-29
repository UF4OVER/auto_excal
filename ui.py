from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDesktopWidget

import siui
from siui.core import SiColor, SiGlobal
from siui.templates.application.application import SiliconApplication

import icons
from parts.close_event import CloseModalDialog
from parts.page_homepage import Homepage
from parts.page_autoexcalpage import Autoexcal
from parts.page_login_for_github import login_for_github

# 载入图标
siui.core.globals.SiGlobal.siui.loadIcons(
    icons.IconDictionary(color=SiGlobal.siui.colors.fromToken(SiColor.SVG_NORMAL)).icons
)


class MySiliconApp(SiliconApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        screen_geo = QDesktopWidget().screenGeometry()
        self.stu = False
        self.setMinimumSize(1024, 380)
        self.resize(1366, 916)
        self.move((screen_geo.width() - self.width()) // 2, (screen_geo.height() - self.height()) // 2)
        self.layerMain().setTitle("Silicon UI Gallery")
        self.setWindowTitle("Silicon UI Gallery")
        self.setWindowIcon(QIcon("pic/圆角-default.jpg"))

        self.layerMain().addPage(Homepage(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_home_filled"),
                                 hint="主页", side="top")
        self.layerMain().addPage(Autoexcal(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_table_stack_right_filled"),
                                 hint="表单", side="top")
        # self.layerMain().addPage(repo_page(self),
        #                          icon=SiGlobal.siui.iconpack.get("ic_fluent_picture_in_picture_filled"),
        #                          hint="仓库", side="top")
        # self.layerMain().addPage(I2C_page(self),
        #                          icon=SiGlobal.siui.iconpack.get("ic_fluent_person_circle_filled"),
        #                          hint="I2C设备", side="top")
        self.layerMain().addPage(login_for_github(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_person_circle_filled"),
                                 hint="个人信息", side="bottom")

        self.layerMain().setPage(0)

        SiGlobal.siui.reloadAllWindowsStyleSheet()

    def closeEvent(self, event):
        self.event = event
        if self.stu:
            event.accept()
        else:
            self.event.ignore()
            temp_widget = CloseModalDialog(self)
            SiGlobal.siui.windows["MAIN_WINDOW"].layerModalDialog().setDialog(temp_widget)
            temp_widget.user_decision.connect(self._sw_stu)  # 连接信号到槽

    def _sw_stu(self):
        self.stu = not self.stu
        SiGlobal.siui.windows["MAIN_WINDOW"].close()
