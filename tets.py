# -*- coding: utf-8 -*-

#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

# -------------------------------
#  @Project : siui
#  @Time    : 2025 - 01-19 18:31
#  @FileName: tets.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

# 获取系统的音频设备
# 获取所有音频设备
devices = AudioUtilities.GetAllDevices()

device = AudioUtilities.GetSpeakers()
interface = device.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None
)
volume = interface.QueryInterface(IAudioEndpointVolume)

# 列出设备的音量信息
# current_volume = volume.GetMasterVolumeLevel()
# volume_range = volume.GetVolumeRange()
# is_muted = volume.GetMute()
#
# print(f"当前音量: {current_volume}")
# print(f"音量范围: {volume_range}")  # (min, max, step)
# print(f"是否静音: {'是' if is_muted else '否'}")

# 设置音量为 50%
new_volume = 0.5  # 范围在 0.0 到 1.0
volume.SetMasterVolumeLevelScalar(new_volume, None)
print(f"已设置音量为: {new_volume * 100}%")

# # 设置静音或取消静音
# volume.SetMute(1, None)  # 1 表示静音，0 表示取消静音
# print("静音已设置。")
