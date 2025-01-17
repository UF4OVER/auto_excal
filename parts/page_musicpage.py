import configparser
import os

from PyQt5.QtWidgets import QBoxLayout
from siui.components.button import SiPushButtonRefactor
from siui.components.container import SiDenseContainer
from siui.components.slider_ import SiSlider

from music_player import MP3Player
from PyQt5.QtCore import Qt
from siui.components.page import SiPage
from siui.components import SiTitledWidgetGroup, SiMasonryContainer, SiOptionCardPlane
from siui.components.widgets import (
    SiDenseVContainer,
    SiSimpleButton,
    SiLineEdit)
from siui.core import Si, SiGlobal
from music_displayer import SiMusicDisplayer

music_info_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "music\\info\\music.ini")
music_png_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "music\\png")
music_mp3_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "music\\mp3")

print(f"music_info_path:{music_info_path}")
print(f"music_png_path:{music_png_path}")
print(f"music_mp3_path:{music_mp3_path}")

config = configparser.ConfigParser()
# 使用 open 函数指定编码为 utf-8
with open("E:\\python\\auto_excal_new\\siui\\music\\info\\music.ini", 'r', encoding='utf-8') as fp:
    config.read_file(fp)


def load_music_info(index: int = 1) -> tuple:
    music_info = config[f"00{index}"]
    return music_info["title"], music_info["artist"], music_info["album"]


mp1_title, mp1_artist, mp1_album = load_music_info(1)
mp2_title, mp2_artist, mp2_album = load_music_info(2)
mp3_title, mp3_artist, mp3_album = load_music_info(3)
mp4_title, mp4_artist, mp4_album = load_music_info(4)
mp5_title, mp5_artist, mp5_album = load_music_info(5)
mp6_title, mp6_artist, mp6_album = load_music_info(6)


class search_box(SiLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.button = SiSimpleButton(self)
        self.button.resize(24, 24)
        self.button.attachment().setSvgSize(16, 16)
        self.button.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_search_filled"))
        self.button.clicked.connect(self.llll)
        self.container().setSpacing(0)
        self.container().addPlaceholder(8, "right")
        self.container().addWidget(self.button, "right")

    def llll(self):
        self.lineEdit().setText("嘿嘿嘿~ ~ ~，这功能我还没写呢:)")

    def setText(self, txt: str):
        self.lineEdit().setText(txt)


class PageMusicPage(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPadding(64)
        self.setScrollMaximumWidth(1100)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("音乐")  # 设置标题

        # 创建控件组
        self.line_edit_with_button = search_box(self)
        self.line_edit_with_button.resize(512, 32)
        self.line_edit_with_button.setText("点击右侧按钮搜索")

        self.titled_widgets_group = SiTitledWidgetGroup(self)
        self.titled_widgets_group.setSiliconWidgetFlag(Si.EnableAnimationSignals)

        self.scroll_container = SiDenseVContainer(self.titled_widgets_group)
        self.scroll_container.addWidget(self.line_edit_with_button)
        self.scroll_container.adjustSize()

        self.titled_widgets_group.addWidget(self.scroll_container)

        self.setupUi()

        SiGlobal.siui.reloadStyleSheetRecursively(self)
        self.titled_widgets_group.adjustSize()
        self.setAttachment(self.titled_widgets_group)

    def setupUi(self):
        with self.titled_widgets_group as group:
            self.displayer_container = SiMasonryContainer(self)
            self.displayer_container.setColumns(2)
            self.displayer_container.setColumnWidth(512)
            self.displayer_container.setFixedWidth(512 + 512 + 16)
            self.displayer_container.setSpacing(horizontal=16, vertical=16)

            self.displayer_1 = SiMusicDisplayer(self)
            self.displayer_1.resize(512, 128)
            self.displayer_1.loadInfo(f"{music_png_path}/I Really Want to Stay at Your House.png",
                                      mp1_title, mp1_artist,
                                      mp1_album)  # noqa: E501
            self.displayer_1.played.connect(self.start_music)
            self.displayer_1.stopped.connect(self.end_music)

            self.displayer_2 = SiMusicDisplayer(self)
            self.displayer_2.resize(512, 128)
            self.displayer_2.loadInfo(f"{music_png_path}/002.jpg", mp2_title, mp2_artist,
                                      mp2_album)  # noqa: E501

            self.displayer_3 = SiMusicDisplayer(self)
            self.displayer_3.resize(512, 128)
            self.displayer_3.loadInfo(f"{music_png_path}/003.jpg", mp3_title, mp3_artist,
                                      mp3_album)  # noqa: E501

            self.displayer_4 = SiMusicDisplayer(self)
            self.displayer_4.resize(512, 128)
            self.displayer_4.loadInfo(f"{music_png_path}/004.jpg", "雨中的重逢", "Parion圆周率",
                                      "Reunion In The Rain")  # noqa: E501

            self.displayer_5 = SiMusicDisplayer(self)
            self.displayer_5.resize(512, 128)
            self.displayer_5.loadInfo(f"{music_png_path}/005.jpg", "Melting White",
                                      "塞壬唱片-MSR / Cubes Collective", "Melting White")  # noqa: E501

            self.displayer_6 = SiMusicDisplayer(self)
            self.displayer_6.resize(512, 128)
            self.displayer_6.loadInfo(f"{music_png_path}/006.jpg", "Axolotl", "C418", "Axolotl")  # noqa: E501

            self.displayer_container.addWidget(self.displayer_1)
            self.displayer_container.addWidget(self.displayer_2)
            self.displayer_container.addWidget(self.displayer_3)
            self.displayer_container.addWidget(self.displayer_4)
            self.displayer_container.addWidget(self.displayer_5)
            self.displayer_container.addWidget(self.displayer_6)

            group.addWidget(self.displayer_container)
            group.adjustSize()
        with self.titled_widgets_group as group:
            # group.addTitle("容器")

            self.containers = SiOptionCardPlane(self)
            self.containers.setFixedWidth(512 + 512 + 16)
            # self.containers.setTitle("密堆积容器")

            self.container_v = SiDenseContainer(self, QBoxLayout.TopToBottom)
            self.container_h = SiDenseContainer(self, QBoxLayout.LeftToRight)
            # self.container_h.setFixedHeight(300)

            button1 = SiPushButtonRefactor.withText("按钮1", parent=self)
            button2 = SiPushButtonRefactor.withText("按钮2", parent=self)
            button3 = SiPushButtonRefactor.withText("按钮3", parent=self)

            self.container_h.addWidget(button1)
            self.container_h.addWidget(button2)
            self.container_h.addWidget(button3)

            slider1 = SiSlider(self)
            # slider1.setMaximumWidth(600)

            self.container_v.addWidget(slider1)
            self.container_v.addWidget(self.container_h)
            self.container_v.layout().setAlignment(self.container_h, Qt.AlignHCenter)
            self.container_v.adjustSize()

            self.containers.body().setAdjustWidgetsSize(True)
            self.containers.body().addWidget(self.container_v)
            self.containers.body().addPlaceholder(12)
            self.containers.adjustSize()

            group.addWidget(self.containers)

    def load_music_mp3(self):
        self.mp3_1 = MP3Player(f"{music_mp3_path}/001.mp3")

    def start_music(self):
        print("start")

    def end_music(self):
        print("end")


def read_config():  # 读取配置文件
    config = configparser.ConfigParser()
    config.read(music_info_path)
