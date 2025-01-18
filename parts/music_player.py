# -*- coding: utf-8 -*-

#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

# -------------------------------
#  @Project : siui
#  @Time    : 2025 - 01-17 18:44
#  @FileName: music_player.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------

from pygame import mixer
import time
from mutagen.mp3 import MP3

class MP3Player:
    def __init__(self, file_path):
        # 初始化播放器
        mixer.init()
        self.file_path = file_path
        self.audio = MP3(file_path)
        self.is_paused = False
        self.total_length = self.audio.info.length  # 获取音频总时长（秒）
    def play(self):
        """播放音频"""
        mixer.music.load(self.file_path)
        mixer.music.play()
        print(f"正在播放: {self.file_path}, 总时长: {self.total_length:.2f} 秒")

    def pause(self):
        """暂停或继续播放"""
        if not self.is_paused:
            mixer.music.pause()
            self.is_paused = True
            print("已暂停播放")
        else:
            mixer.music.unpause()
            self.is_paused = False
            print("继续播放")

    def stop(self):
        """停止播放"""
        mixer.music.stop()
        print("播放已停止")

    def seek(self, seconds):
        """跳转到指定时间"""
        if 0 <= seconds <= self.total_length:
            mixer.music.play(start=seconds)
            print(f"跳转到: {seconds:.2f} 秒")
        else:
            print("时间超出范围")

    def get_position(self):
        """获取当前播放位置"""
        current_pos = mixer.music.get_pos() / 1000.0  # 返回的值是毫秒
        print(f"当前播放位置: {current_pos:.2f} 秒")
        return current_pos


# 示例用法
if __name__ == "__main__":
    player = MP3Player("music/mp3/001.mp3")  # 替换为你的 MP3 文件路径
    player.play()

    time.sleep(5)  # 播放 5 秒
    player.get_position()

    player.pause()
    time.sleep(2)  # 暂停 2 秒

    player.pause()  # 恢复播放
    time.sleep(5)  # 再播放 5 秒

    player.seek(55)  # 跳转到第 10 秒
    time.sleep(5)  # 播放 5 秒

    player.stop()
