#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
import os

def get_mp3_info(mp3_path):
    audio = MP3(mp3_path, ID3=ID3)

    # 获取标签信息，并检查是否为空
    title = audio.tags.get('TIT2', [None])[0] or 'Unknown Title'
    artist = audio.tags.get('TPE1', [None])[0] or 'Unknown Artist'
    album = audio.tags.get('TALB', [None])[0] or 'Unknown Album'

    # 打印信息
    print('TIT2:', title, 'TPE1:', artist, 'TALB:', album)

    # 获取封面图片
    cover_path = None
    if 'APIC:' in audio.tags:
        apic_frame = audio.tags['APIC:']
        cover_path = os.path.join(os.path.dirname(mp3_path), f"{title}cover.{apic_frame.mime.split('/')[-1]}")
        with open(cover_path, 'wb') as img:
            img.write(apic_frame.data)

    # 返回三个值和封面路径
    return title, artist, album, cover_path

# 示例调用
mp3_file_path = r"E:\python\auto_excal_new\siui\music\mp3\001.mp3"
title, artist, album, cover_path = get_mp3_info(mp3_file_path)
print("Title:", title)
print("Artist:", artist)
print("Album:", album)
print("Cover Path:", cover_path)
