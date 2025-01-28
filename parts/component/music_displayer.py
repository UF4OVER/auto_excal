# -*- coding: utf-8 -*-
#  Copyright (c) 2025 UF4OVER
#   All rights reserved.
import os
import shutil

from PyQt5.QtCore import Qt, QObject, pyqtSignal, QUrl
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QFileDialog
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from siui.components import SiSimpleButton, SiDenseVContainer, SiPixLabel, SiLabel
from siui.components import SiWidget
from siui.core import Si, SiQuickEffect
from siui.core import SiColor, SiGlobal
from siui.gui import SiFont

from parts.component.DynamicIsland import Send_DynamicIsland_Message, Send_DynamicIsland_Message_Default


def get_mp3_info(mp3_path):
    audio = MP3(mp3_path, ID3=ID3)

    # 获取标签信息，并检查是否为空
    title = audio.tags.get('TIT2', [None])[0] or 'Unknown Title'
    artist = audio.tags.get('TPE1', [None])[0] or 'Unknown Artist'
    album = audio.tags.get('TALB', [None])[0] or 'Unknown Album'

    # 打印信息，使用 repr 函数处理特殊字符
    print(f'标题:, {repr(title)}, 作者:, {repr(artist)}, 专辑:{repr(album)}')

    # 获取封面图片
    cover_path = None
    if 'APIC:' in audio.tags:
        apic_frame = audio.tags['APIC:']
        cover_path = os.path.join(os.path.dirname(mp3_path), "png", f"{title}cover.{apic_frame.mime.split('/')[-1]}")
        with open(cover_path, 'wb') as img:
            img.write(apic_frame.data)

    # 返回三个值和封面路径
    return title, artist, album, cover_path


class MP3Player(QObject):
    finished = pyqtSignal()

    def __init__(self, file_path):
        super().__init__()
        self.player = QMediaPlayer()
        self.file_path = file_path
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
        self.is_paused = False
        audio = MP3(file_path, ID3=ID3)
        self.total_length = audio.info.length  # 获取音频总时长（秒）

        # 连接播放结束信号
        self.player.stateChanged.connect(self.on_state_changed)

    def play(self):
        """播放音频"""
        self.player.play()
        print(f"正在播放: {self.file_path}, 总时长: {self.total_length:.2f} 秒")

    def pause(self):
        """暂停或继续播放"""
        if not self.is_paused:
            self.player.pause()
            self.is_paused = True
            print("已暂停播放")
        else:
            self.player.play()
            self.is_paused = False
            print("继续播放")

    def stop(self):
        """停止播放"""
        self.player.stop()
        print("播放已停止")

    def seek(self, seconds):
        """跳转到指定时间"""
        if 0 <= seconds <= self.total_length:
            self.player.setPosition(int(seconds * 1000))
            print(f"跳转到: {seconds:.2f} 秒")
        else:
            print("时间超出范围")

    def get_position(self):
        """获取当前播放位置"""
        current_pos = self.player.position() / 1000.0  # 返回的值是毫秒
        print(f"当前播放位置: {current_pos:.2f} 秒")
        return current_pos

    def on_state_changed(self, state):
        """音乐播放结束时的回调函数"""
        if state == QMediaPlayer.StoppedState and not self.is_paused:
            self.finished.emit()
            print("音乐播放结束")


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

        self.music_player = MP3Player

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
        self.button_like.resize(32, 32)
        self.button_like.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_heart_regular"))
        self.folded_container.addWidget(self.button_like)

        self.button_download = SiSimpleButton(self)
        self.button_download.resize(32, 32)
        self.button_download.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_arrow_download_regular"))
        self.folded_container.addWidget(self.button_download)
        self.button_download.clicked.connect(self.DownloadMusic)

        self.button_pause = SiSimpleButton(self)
        self.button_pause.resize(32, 32)
        self.button_pause.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_pause_circle_regular"))
        self.folded_container.addWidget(self.button_pause)

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

    def DownloadMusic(self):
        if not os.path.exists(self.png_path):
            return
        else:
            folder_path = QFileDialog.getExistingDirectory(self, "选择保存位置")
            if folder_path == "":
                return
            else:
                shutil.copy(self.mp3_path, folder_path)

    def loadMusic(self, mp3_path: str):
        if not os.path.exists(mp3_path) and mp3_path.split(".")[1] != "mp3":
            raise print("不是有效的MP3的MP3文件")

        self.music_player = MP3Player(mp3_path)
        self.mp3_path = mp3_path
        self.title, self.artist, self.album, self.png_path = get_mp3_info(mp3_path)
        self.info_panel.loadInfo(self.png_path, self.title, self.artist, self.album)
        self.cover_label.load(self.png_path)
        self.cover_lower_fix_label.load(self.png_path)
        self.music_player.finished.connect(self.setStop)

    def loadAchievement(self, number: int):
        """
        加载人数
        :parm number:人数
        """
        _ten = number // 1000
        _one = number % 1000

        if _ten == 0:
            self.info_panel.loadAchievement(f"OVER {_one} PLAYS")
        else:
            self.info_panel.loadAchievement(f"OVER {_ten}K PLAYS")

    def setStart(self):
        self.quick_play_panel.play_button.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_pause_filled"))
        self.quick_play_panel.is_playing = False
        self.music_player.play()

    def setStop(self):
        self.quick_play_panel.play_button.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_play_filled"))
        self.quick_play_panel.is_playing = True
        self.music_player.stop()

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
            self.setStop()
            self.stopped.emit()
            Send_DynamicIsland_Message_Default()
        else:
            self.setStart()
            self.played.emit()
            Send_DynamicIsland_Message(self.title, self.artist, self.album)

    def is_playing(self):
        return not self.quick_play_panel.is_playing


class MusicManager:
    def __init__(self):
        self.music_displayer = []  # 存放SiMusicDisplayer的容器

    def add_music_displayer(self, music_displayer: SiMusicDisplayer):
        self.music_displayer.append(music_displayer)
        music_displayer.played.connect(lambda: self.on_music_played(music_displayer))

    def on_music_played(self, playing_music_displayer: SiMusicDisplayer):
        for music_displayer in self.music_displayer:
            if music_displayer != playing_music_displayer and music_displayer.is_playing():  # 其他的播放的才停止
                music_displayer.setStop()
            if music_displayer == playing_music_displayer:  # 当前点击的的播放
                music_displayer.setStart()
