# -*- coding: utf-8 -*-
# -------------------------------
#  @Project : QTMusicplayer
#  @Time    : 2025 - 03-21 22:03
#  @FileName: test.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------
import json


class SvgIcon:

    def __init__(self):
        self.icon_dict = {}

    def cache_icon(self):
        with open("icons.json", "r", encoding="utf-8") as f:
            self.icon_dict = json.load(f)

    def get_icon(self, icon_name):
        _name1 = icon_name.split("-")[0][0].upper() + icon_name.split("-")[0][1:]
        _name2 = icon_name.split("-")[1][0].upper() + icon_name.split("-")[1][1:]
        _name = _name1 + " " + _name2
        print(_name)
        if _name in self.icon_dict:
            return _name

    def get_all_icon_name(self):
        for key in self.icon_dict:
            key1 = key.replace(" ", "-")
            key2 = key1.replace("-", "_")
            print(f"{key2} = '{key1.lower()}'")

a = SvgIcon()
a.cache_icon()
a.get_all_icon_name()