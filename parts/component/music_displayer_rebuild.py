# -*- coding: utf-8 -*-
import os

#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

# -------------------------------
#  @Project : siui
#  @Time    : 2025 - 01-23 22:01
#  @FileName: music_displayer_rebuild.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------

from PyQt5.QtCore import Qt, QObject, pyqtSignal, QUrl
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QFileDialog, QWidget, QLabel, QApplication
from mutagen.id3 import ID3
from mutagen.mp3 import MP3


def get_mp3_info(mp3_path):
    audio = MP3(mp3_path, ID3=ID3)

    # 获取标签信息，并检查是否为空
    title = audio.tags.get('TIT2', [None])[0] or 'Unknown Title'
    artist = audio.tags.get('TPE1', [None])[0] or 'Unknown Artist'
    album = audio.tags.get('TALB', [None])[0] or 'Unknown Album'

    # 打印信息
    print(f'标题:, {title}, 作者:, {artist}, 专辑:{album}')

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


class SiMusicDisplayer(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = QLabel(self)
        self.label.setStyleSheet("background-color: rgba(22, 33, 111, 0);")
        self.label.resize(512, 128)
    def showEvent(self, a0):
        pass


    def resizeEvent(self, event):
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication([])
    window = SiMusicDisplayer()
    window.show()
    app.exec_()
