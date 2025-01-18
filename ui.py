import configparser
import webbrowser

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QDesktopWidget, QShortcut

import siui
from siui.components import SiSimpleButton, SiDenseVContainer, SiPixLabel, SiLabel, SiDenseHContainer
from siui.core import SiColor, SiGlobal, GlobalFont
from siui.gui import SiFont
from siui.templates.application.application import SiliconApplication
from siui.templates.application.components.message.box import SiSideMessageBox

import icons
from page_aboutpage import About
from parts.layer_left_global import LayerLeftGlobalDrawer
from parts.page_musicpage import PageMusicPage
from parts.close_event import CloseModalDialog
from parts.page_homepage import Homepage
from parts.page_autoexcalpage import Autoexcal
from parts.page_settingpage import PageSettingPage

# 载入图标
siui.core.globals.SiGlobal.siui.loadIcons(
    icons.IconDictionary(color=SiGlobal.siui.colors.fromToken(SiColor.SVG_NORMAL)).icons
)

import config.CONFIG

PATH_CONFIG = config.CONFIG.CONFIG_PATH


def send_custom_message():
    container = SiDenseHContainer()
    container.setAdjustWidgetsSize(True)
    container.setFixedHeight(80)
    container.setSpacing(0)

    info_label = SiLabel()
    info_label.setFont(SiFont.tokenized(GlobalFont.S_NORMAL))
    info_label.setStyleSheet(f"color: {info_label.getColor(SiColor.TEXT_D)}; padding-left: 16px")
    info_label.setText("Welcome to Wedding Invitation")
    info_label.adjustSize()

    split_line = SiLabel()
    split_line.resize(300, 1)
    split_line.setFixedStyleSheet("margin-left: 20px")
    split_line.setColor(SiColor.trans(split_line.getColor(SiColor.TEXT_D), 0.3))

    avatar = SiPixLabel(container)
    avatar.resize(80, 80)
    avatar.setBorderRadius(40)
    avatar.load(r"pic/圆角-default.jpg")

    container_v = SiDenseVContainer(container)
    container_v.setFixedWidth(200)
    container_v.setSpacing(0)

    name_label = SiLabel()
    name_label.setFont(SiFont.tokenized(GlobalFont.M_BOLD))
    name_label.setStyleSheet(f"color: {name_label.getColor(SiColor.TEXT_B)}; padding-left:8px")
    name_label.setText("Wedding Collection")
    name_label.adjustSize()

    button_1 = SiSimpleButton()
    button_1.setFixedHeight(22)
    button_1.attachment().setText("打开我的主页")
    button_1.colorGroup().assign(SiColor.TEXT_B, button_1.getColor(SiColor.TITLE_INDICATOR))
    button_1.adjustSize()
    button_1.reloadStyleSheet()
    button_1.clicked.connect(lambda: webbrowser.open("https://github.com/UF4OVER/auto_excal"))

    button_2 = SiSimpleButton()
    button_2.setFixedHeight(22)
    button_2.attachment().setText("退出应用")
    button_2.colorGroup().assign(SiColor.TEXT_B, button_2.getColor(SiColor.TITLE_INDICATOR))
    button_2.adjustSize()
    button_2.reloadStyleSheet()
    button_2.clicked.connect(lambda: SiGlobal.siui.windows["MAIN_WINDOW"].close())

    container_v.addWidget(name_label)
    container_v.addPlaceholder(8)
    container_v.addWidget(button_1)
    container_v.addWidget(button_2)
    container_v.adjustSize()

    container.addPlaceholder(24)
    container.addWidget(avatar)
    container.addPlaceholder(8)
    container.addWidget(container_v)
    container.adjustSize()

    new_message_box = SiSideMessageBox()
    new_message_box.setMessageType(1)
    new_message_box.content().container().setSpacing(0)
    new_message_box.content().container().addPlaceholder(16)
    new_message_box.content().container().addWidget(info_label)
    new_message_box.content().container().addPlaceholder(8)
    new_message_box.content().container().addWidget(split_line)
    new_message_box.content().container().addPlaceholder(24)
    new_message_box.content().container().addWidget(container)
    new_message_box.content().container().addPlaceholder(32)
    new_message_box.adjustSize()

    # new_message_box.setFoldAfter(fold_after)

    SiGlobal.siui.windows["MAIN_WINDOW"].LayerRightMessageSidebar().sendMessageBox(new_message_box)


class My_SiliconApplication(SiliconApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layer_left_global_drawer = LayerLeftGlobalDrawer(self)


class MySiliconApp(My_SiliconApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        screen_geo = QDesktopWidget().screenGeometry()
        self.stu = False
        self.setMinimumSize(1200, 500)
        self.resize(1350, 900)
        self.setMaximumSize(1500, 1200)
        self.move((screen_geo.width() - self.width()) // 2, (screen_geo.height() - self.height()) // 2)
        self.layerMain().setTitle("Wedding Invitation")
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
