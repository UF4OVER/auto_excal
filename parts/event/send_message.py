#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

import webbrowser

from siui.components import SiSimpleButton, SiDenseVContainer, SiPixLabel, SiLabel, SiDenseHContainer
from siui.core import SiColor, SiGlobal, GlobalFont
from siui.gui import SiFont
from siui.templates.application.components.message.box import SiSideMessageBox
import config.CONFIG

PATH_PNG = config.CONFIG.PNG_PATH


def send_custom_message():
    container = SiDenseHContainer()
    container.setAdjustWidgetsSize(True)
    container.setFixedHeight(80)
    container.setSpacing(0)

    info_label = SiLabel()
    info_label.setFont(SiFont.tokenized(GlobalFont.S_NORMAL))
    info_label.setStyleSheet(f"color: {info_label.getColor(SiColor.TEXT_D)}; padding-left: 16px")
    info_label.setText("Welcome to Loot Hearts")
    info_label.adjustSize()

    split_line = SiLabel()
    split_line.resize(300, 1)
    split_line.setFixedStyleSheet("margin-left: 20px")
    split_line.setColor(SiColor.trans(split_line.getColor(SiColor.TEXT_D), 0.3))

    avatar = SiPixLabel(container)
    avatar.resize(80, 80)
    avatar.setBorderRadius(40)
    avatar.load(f"{PATH_PNG}\\logo.ico")

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


def show_message(_type: int, title: str, text: str, icon: str):
    SiGlobal.siui.windows["MAIN_WINDOW"].LayerRightMessageSidebar().send(
        title=title,
        text=text,
        msg_type=_type,
        icon=SiGlobal.siui.iconpack.get(f"{icon}"),
        fold_after=5000)
