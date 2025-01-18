# -*- coding: utf-8 -*-
#  Copyright (c) 2025 UF4OVER
#   All rights reserved.
# -------------------------------
#  @Project : siui
#  @Time    : 2025 - 01-18 15:20
#  @FileName: MusicPlaybackBoxer.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from siui.components import SiLabel, SiWidget
from siui.components.button import SiFlatButton
from siui.components.slider import SiSliderH
from siui.components.widgets import SiDenseVContainer
from siui.core import Si, SiColor, SiGlobal
from siui.gui import SiFont
from parts.music_player import MP3Player


class MusicPlay(SiWidget):
    nexted = pyqtSignal()
    lasted = pyqtSignal()
    started = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.resize(1024, 100)
        self.start_stop_button_icon_flag = False
        self.setupui()
        self.playtime = DataItem("当前进度", "-", 14, 20, parent=self.cover_label)

    def setupui(self):
        self.bottom_window = SiWidget(self)
        self.cover_label = SiLabel(self.bottom_window)
        self.cover_label.setFixedSize(int(self.width()), self.height())

        self.music_progress_bar = SiSliderH(self)
        self.music_progress_bar.resize(self.width() - 50, 80)
        self.music_progress_bar.setMinimum(0)
        self.music_progress_bar.setValue(0)

        self.start_stop_button = SiFlatButton(self.cover_label)
        self.start_stop_button.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_triangle_right_filled"))
        self.start_stop_button.setFixedSize(50, 50)
        self.start_stop_button.adjustSize()
        self.start_stop_button.clicked.connect(self.switch_button_icon)

        self.next_button = SiFlatButton(self.cover_label)
        self.next_button.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_triangle_right_regular"))
        self.next_button.setFixedSize(50, 50)
        self.next_button.clicked.connect(self.nexted_music)
        self.next_button.adjustSize()

        self.last_button = SiFlatButton(self.cover_label)
        self.last_button.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_triangle_left_regular"))
        self.last_button.setFixedSize(50, 50)
        self.last_button.clicked.connect(self.lasted_music)
        self.last_button.adjustSize()

        self.music_progress_bar.valueChanged.connect(lambda _: self.refresh_time(_))

    def setTotalTime(self, total_time: int):
        self.music_progress_bar.setMaximum(total_time)

    def nexted_music(self):
        self.nexted.emit()

    def lasted_music(self):
        self.lasted.emit()

    def refresh_time(self, value: int):
        minutes = value // 60
        seconds = value % 60
        self.playtime.load("当前进度", f"{minutes:02}:{seconds:02}")

    def switch_button_icon(self):
        # print(f"self.start_stop_button_icon_flag = {self.start_stop_button_icon_flag}")
        if self.start_stop_button_icon_flag:
            self.start_stop_button.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_triangle_right_filled"))
            self.finished.emit()
        else:
            self.start_stop_button.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_pause_filled"))
            self.started.emit()
        self.start_stop_button_icon_flag = not self.start_stop_button_icon_flag

    def setValue(self, value: int):
        self.music_progress_bar.setValue(value)

    def setMaximum(self, value: int):
        self.music_progress_bar.setMaximum(value)

    def setMinimum(self, value: int):
        self.music_progress_bar.setMinimum(value)

    def reloadStyleSheet(self):
        print(f"border-radius: {int(self.height() / 2)}px")
        self.cover_label.setStyleSheet(
            f"background-color: {self.getColor(SiColor.INTERFACE_BG_C)};"
            f"border-radius: {int(self.height() / 2)}px;")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.music_progress_bar.move(25, -20)
        self.start_stop_button.move(int(self.width() / 2) - self.start_stop_button.width(),
                                    int(self.height() / 2) - int(self.start_stop_button.height() / 5))
        self.next_button.move(int(self.width() / 2) - self.start_stop_button.width() + 60,
                              int(self.height() / 2) - int(self.start_stop_button.height() / 5))
        self.last_button.move(int(self.width() / 2) - self.start_stop_button.width() - 60,
                              int(self.height() / 2) - int(self.start_stop_button.height() / 5))

        self.playtime.move(int(self.width() / 4),
                           int(self.height() / 2) - int(self.start_stop_button.height() / 5))


class MusicPlaybackBoxer(MusicPlay, MP3Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.started.connect(self.play)
        self.finished.connect(self.stop)
    def refresh_time(self, value: int):
        minutes = value // 60
        seconds = value % 60
        self.playtime.load("当前进度", f"{minutes:02}:{seconds:02}")

class DataItem(SiDenseVContainer):
    def __init__(self, title, data, size_title, size_data, parent=None):
        super().__init__(parent)

        self.title = SiLabel(self)
        self.title.setFont(SiFont.getFont(size=size_title, weight=QFont.Weight.Normal))
        self.title.setTextColor(self.getColor(SiColor.TEXT_D))
        self.title.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.title.setText(str(title))

        self.data = SiLabel(self)
        self.data.setFont(SiFont.getFont(size=size_data, weight=QFont.Weight.Light))
        self.data.setTextColor(self.getColor(SiColor.TEXT_B))
        self.data.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.data.setText(str(data))

        self.setAlignment(Qt.AlignLeft)
        self.setSpacing(0)
        self.addWidget(self.title)
        self.addWidget(self.data)

    def load(self, title, data):
        self.title.setText(str(title))
        self.data.setText(str(data))
