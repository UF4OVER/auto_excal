# -*- coding: utf-8 -*-
# -------------------------------
#  @Project : siui_refactor
#  @Time    : 2025 - 07-17 19:23
#  @FileName: ShowMessage.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------
from siui.core import SiGlobal


def show_message(_type: int, title: str, text: str, icon: str):
    SiGlobal.siui.windows["MAIN_WINDOW"].LayerRightMessageSidebar().send(
        title=title,
        text=text,
        msg_type=_type,
        icon=SiGlobal.siui.iconpack.get(f"{icon}"),
        fold_after=5000)