# -*- coding: utf-8 -*-
#  Copyright (c) 2025 UF4OVER
#   All rights reserved.
# -------------------------------
#  @Project : siui
#  @Time    : 2025 - 01-17 17:19
#  @FileName: music_displayer.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact :
#  @Python  :
# -------------------------------

from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from siui.components import SiSimpleButton, SiDenseVContainer, SiPixLabel, SiLabel, SiDenseHContainer
from siui.components import SiWidget
from siui.core import Si, SiQuickEffect
from siui.core import SiColor, SiGlobal, GlobalFont
from siui.gui import SiFont
from siui.templates.application.components.message.box import SiSideMessageBox


def send_music_message(png_path: str, music_name: str, music_artist: str, music_album: str):
    container = SiDenseHContainer()
    container.setAdjustWidgetsSize(True)
    container.setFixedHeight(80)
    container.setSpacing(0)

    info_label = SiLabel()
    info_label.setFont(SiFont.tokenized(GlobalFont.S_NORMAL))
    info_label.setStyleSheet(f"color: {info_label.getColor(SiColor.TEXT_D)}; padding-left: 16px")
    info_label.setText(f"正在播放歌曲:{music_name}")
    info_label.adjustSize()

    split_line = SiLabel()
    split_line.resize(300, 1)
    split_line.setFixedStyleSheet("margin-left: 20px")
    split_line.setColor(SiColor.trans(split_line.getColor(SiColor.TEXT_D), 0.3))

    avatar = SiPixLabel(container)
    avatar.resize(80, 120)
    avatar.setBorderRadius(20)
    avatar.load(f"{png_path}")

    container_v = SiDenseVContainer(container)
    container_v.setFixedWidth(200)
    container_v.setSpacing(0)

    name_label = SiLabel()
    name_label.setFont(SiFont.tokenized(GlobalFont.M_BOLD))
    name_label.setStyleSheet(f"color: white; padding-left:8px")
    name_label.setText(f"{music_name}")
    name_label.adjustSize()

    button_1 = SiLabel()
    button_1.setFixedHeight(26)
    button_1.setText(f"作者:{music_artist}")
    button_1.setFont(SiFont.tokenized(GlobalFont.L_LIGHT))
    button_1.setStyleSheet(f"color: white; padding-left:8px")
    button_1.adjustSize()
    button_1.reloadStyleSheet()

    button_2 = SiLabel()
    button_2.setFixedHeight(22)
    button_2.setText(f"专辑:{music_album}")
    button_2.setFont(SiFont.tokenized(GlobalFont.S_NORMAL))
    button_2.setStyleSheet(f"color: white; padding-left:8px")
    button_2.adjustSize()
    button_2.reloadStyleSheet()

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
    new_message_box.setMessageType(3)
    # new_message_box.setFoldAfter(1000)
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


class InfoPanel(SiWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.background_image_label_frame = SiWidget(self)
        self.background_image_label_frame.move(12, 0)

        self.background_image_label = SiPixLabel(self.background_image_label_frame)
        self.background_image_label.setBorderRadius(12)
        self.background_image_label.resize(512 - 128 + 12 - 12 - 12, 128)

        self.transition_label = SiLabel(self)
        self.transition_label.setFixedStyleSheet("border-radius: 12px")

        self.content_container = SiDenseVContainer(self)
        self.content_container.setAdjustWidgetsSize(True)
        self.content_container.setAlignment(Qt.AlignLeft)
        self.content_container.setSpacing(0)
        SiQuickEffect.applyDropShadowOn(self.content_container, blur_radius=8, color=(0, 0, 0, 255))

        self.title_label = SiLabel(self)
        self.title_label.setFont(SiFont.getFont(size=18, weight=QFont.Weight.Bold))
        self.title_label.setFixedHeight(27)

        self.artist_label = SiLabel(self)
        self.artist_label.setFont(SiFont.getFont(size=16))
        self.artist_label.setFixedHeight(25)

        self.album_label = SiLabel(self)
        self.album_label.setFont(SiFont.getFont(size=14))
        self.album_label.setFixedHeight(16)

        self.content_container.addPlaceholder(10)
        self.content_container.addWidget(self.title_label)
        self.content_container.addWidget(self.artist_label)
        self.content_container.addWidget(self.album_label)

        # 成就铭牌
        self.achievement_label = SiLabel(self)
        self.achievement_label.setFixedStyleSheet("border-radius: 10px; padding-left: 12px; padding-right: 12px")
        self.achievement_label.setFixedHeight(20)
        self.achievement_label.setFont(SiFont.getFont(size=10))
        self.achievement_label.setAlignment(Qt.AlignCenter)
        self.achievement_label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.achievement_label.setVisible(False)

    def loadInfo(self, cover_path, title, artist, album):
        self.background_image_label.load(cover_path)
        self.title_label.setText(title)
        self.artist_label.setText(f"by {artist}")
        self.album_label.setText(album)

    def loadAchievement(self, achievement):
        self.achievement_label.setText(achievement)
        self.achievement_label.setVisible(True)
        self.resize(self.size())

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.title_label.setTextColor(self.getColor(SiColor.TEXT_A))
        self.artist_label.setTextColor(self.getColor(SiColor.TEXT_A))
        self.album_label.setTextColor(self.getColor(SiColor.TEXT_D))
        self.transition_label.setStyleSheet(
            "background-color: qlineargradient("
            "    x1:0.1, y1:0, x2:1, y2:0,"
            f"   stop:0 {SiColor.trans(self.getColor(SiColor.INTERFACE_BG_D), 1.0)},"
            f"   stop:1 {SiColor.trans(self.getColor(SiColor.INTERFACE_BG_D), 0.7)}"
            ")"
        )
        self.achievement_label.setStyleSheet(
            "background-color: #28222a;"
            "color: #b344db"
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.background_image_label.move(self.width() - self.background_image_label.width() - 12, 0)
        self.background_image_label_frame.resize(self.width() - 12, 128)
        self.transition_label.resize(event.size())
        self.content_container.setGeometry(16, 0, event.size().width() - 16, event.size().height())
        self.achievement_label.move(event.size().width() - self.achievement_label.width() - 12, 40)


class QuickPlayPanel(SiWidget):
    triggered = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dim_layer = SiLabel(self)
        self.dim_layer.resize(160, 128)
        self.dim_layer.setFixedStyleSheet("border-radius: 12px")
        self.dim_layer.setColor("#00000000")

        self.play_button_frame = SiLabel(self)
        self.play_button_frame.resize(128 - 12, 128)
        self.play_button_frame.setOpacity(0)

        self.play_button_frame_widget = SiWidget(self.play_button_frame)
        self.play_button_frame_widget.resize(128 - 12, 128)

        self.play_button = SiSimpleButton(self.play_button_frame)
        self.play_button.resize(64, 64)
        self.play_button.attachment().setSvgSize(48, 48)
        self.play_button.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_play_filled"))
        self.play_button.move(32, 32)
        self.play_button_frame_widget.setCenterWidget(self.play_button)
        self.play_button.clicked.connect(self.on_play_button_clicked)
        self.is_playing = True

    def on_play_button_clicked(self):
        # 切换图标状态
        if not self.is_playing:
            self.play_button.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_play_filled"))
        else:
            self.play_button.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_pause_filled"))

        # 切换状态变量
        self.is_playing = not self.is_playing
        self.triggered.emit()

    def enterEvent(self, a0):
        super().enterEvent(a0)
        self.dim_layer.setColorTo("#70000000")
        self.play_button_frame.setOpacityTo(1)

    def leaveEvent(self, a0):
        super().leaveEvent(a0)
        self.dim_layer.setColorTo("#00000000")
        self.play_button_frame.setOpacityTo(0)


class SiMusicDisplayer(SiWidget):
    played = pyqtSignal()
    stopped = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cover_label = SiPixLabel(self)
        self.cover_label.setFixedSize(128, 128)
        self.cover_label.setBorderRadius(12)

        self.cover_lower_fix = SiWidget(self)
        self.cover_lower_fix.move(12, 0)
        self.cover_lower_fix.resize(128 - 12, 128)

        self.cover_lower_fix_label = SiPixLabel(self.cover_lower_fix)
        self.cover_lower_fix_label.move(-12, 0)
        self.cover_lower_fix_label.setFixedSize(128, 128)
        self.cover_lower_fix_label.setBorderRadius(0)

        # 状态指示标签，按钮容器，按钮
        self.state_label = SiLabel(self)
        self.state_label.resize(64, 128)
        self.state_label.setFixedStyleSheet("border-radius: 12px")
        self.state_label.setColor(self.getColor(SiColor.INTERFACE_BG_C))

        self.folded_container = SiDenseVContainer(self.state_label)
        self.folded_container.setAlignment(Qt.AlignHCenter)
        self.folded_container.setFixedSize(48, 128 - 24)
        self.folded_container.setSpacing(4)

        self.button_like = SiSimpleButton(self)
        self.button_like.resize(32, 50)
        self.button_like.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_heart_regular"))
        self.folded_container.addWidget(self.button_like)

        self.button_download = SiSimpleButton(self)
        self.button_download.resize(32, 50)
        self.button_download.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_arrow_download_regular"))
        self.folded_container.addWidget(self.button_download)

        # 快捷播放面板
        self.quick_play_panel = QuickPlayPanel(self)
        self.quick_play_panel.resize(160, 128)
        self.quick_play_panel.triggered.connect(self.on_quick_play_panel_triggered)

        # 信息面板
        self.info_panel = InfoPanel(self)
        self.info_panel.setFixedHeight(128)
        self.info_panel.resize(512 - 128 + 12 - 12, 128)
        self.info_panel.animationGroup().fromToken("resize").setFactor(1 / 6)
        self.info_panel.animationGroup().fromToken("resize").setBias(1)
        self.info_panel.loadAchievement("OVER 10K PLAYS")

    def setStart(self):
        self.quick_play_panel.play_button.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_pause_filled"))
        self.quick_play_panel.is_playing = False

    def setStop(self):
        self.quick_play_panel.play_button.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_play_filled"))
        self.quick_play_panel.is_playing = True

    def loadInfo(self, cover_path, title, artist, album):
        self.png_path = cover_path
        self.title = title
        self.artist = artist
        self.album = album

        self.info_panel.loadInfo(cover_path, title, artist, album)
        self.cover_label.load(cover_path)
        self.cover_lower_fix_label.load(cover_path)

    def enterEvent(self, a0):
        super().enterEvent(a0)
        self.info_panel.resizeTo(512 - 128 + 12 - 12 - 32, 128)

    def leaveEvent(self, a0):
        super().leaveEvent(a0)
        self.info_panel.resizeTo(512 - 128 + 12 - 12, 128)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.state_label.move(event.size().width() - 64, 0)
        self.folded_container.move(self.state_label.width() - self.folded_container.width(), 12)
        self.info_panel.move(128 - 12, 0)

    def on_quick_play_panel_triggered(self):
        if self.quick_play_panel.is_playing:
            self.stopped.emit()
        else:
            self.played.emit()
            send_music_message(self.png_path, self.title, self.artist, self.album)
