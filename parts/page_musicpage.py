import configparser
import os

from PyQt5.QtCore import Qt
from siui.components import SiTitledWidgetGroup, SiMasonryContainer
from siui.components.page import SiPage
from siui.components.widgets import (
    SiDenseVContainer,
    SiSimpleButton,
    SiLineEdit)
from siui.core import Si, SiGlobal

from parts.music_displayer import SiMusicDisplayer

music_info_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "music\\info\\music.ini")
music_png_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "music\\png")

print(f"music_info_path:{music_info_path}")
print(f"music_png_path:{music_png_path}")

config = configparser.ConfigParser()
# 使用 open 函数指定编码为 utf-8
with open(music_info_path, 'r', encoding='utf-8') as fp:
    config.read_file(fp)


def load_music_info(index: int = 1) -> tuple:
    music_info = config[f"00{index}"]
    return music_info["title"], music_info["artist"], music_info["album"], music_info["path"]


mp1_title, mp1_artist, mp1_album, mp1_path = load_music_info(1)
mp2_title, mp2_artist, mp2_album, mp2_path = load_music_info(2)
mp3_title, mp3_artist, mp3_album, mp3_path = load_music_info(3)
mp4_title, mp4_artist, mp4_album, mp4_path = load_music_info(4)
mp5_title, mp5_artist, mp5_album, mp5_path = load_music_info(5)
mp6_title, mp6_artist, mp6_album, mp6_path = load_music_info(6)

mp1_path = str(os.path.join(os.path.dirname(os.path.dirname(__file__)), mp1_path))

print("mp1_" + mp1_path)


def read_config():  # 读取配置文件
    config = configparser.ConfigParser()
    config.read(music_info_path)


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
        # 添加页脚的空白以增加美观性
        self.titled_widgets_group.addPlaceholder(64)
        self.setAttachment(self.titled_widgets_group)

    def setupUi(self):
        self.players: list = []
        with self.titled_widgets_group as group:
            self.displayer_container = SiMasonryContainer(self)
            self.displayer_container.setColumns(2)
            self.displayer_container.setColumnWidth(512)
            self.displayer_container.setFixedWidth(512 + 512 + 16)
            self.displayer_container.setSpacing(horizontal=16, vertical=16)

            self.displayer_1 = SiMusicDisplayer(self)
            self.displayer_1.resize(512, 128)
            self.displayer_1.loadMusic(mp1_path, f"{music_png_path}/I Really Want to Stay at Your House.png",
                                       mp1_title, mp1_artist, mp1_album)  # noqa: E501

            self.displayer_2 = SiMusicDisplayer(self)
            self.displayer_2.resize(512, 128)
            self.displayer_2.loadMusic(mp2_path, f"{music_png_path}/002.jpg", mp2_title,
                                       mp2_artist, mp2_album)  # noqa: E501

            self.displayer_3 = SiMusicDisplayer(self)
            self.displayer_3.resize(512, 128)
            self.displayer_3.loadMusic(mp3_path, f"{music_png_path}/003.jpg", mp3_title,
                                       mp3_artist, mp3_album)  # noqa: E501

            self.displayer_4 = SiMusicDisplayer(self)
            self.displayer_4.resize(512, 128)
            self.displayer_4.loadMusic(mp4_path, f"{music_png_path}/004.jpg", mp4_title,
                                       mp4_artist, mp4_album)  # noqa: E501

            self.displayer_5 = SiMusicDisplayer(self)
            self.displayer_5.resize(512, 128)
            self.displayer_5.loadMusic(mp5_path, f"{music_png_path}/005.jpg", mp5_title,
                                       mp5_artist, mp5_album)  # noqa: E501

            self.displayer_6 = SiMusicDisplayer(self)
            self.displayer_6.resize(512, 128)
            self.displayer_6.loadMusic(mp6_path, f"{music_png_path}/006.jpg", mp6_title,
                                       mp6_artist, mp6_album)  # noqa: E501

            self.displayer_container.addWidget(self.displayer_1)
            self.displayer_container.addWidget(self.displayer_2)
            self.displayer_container.addWidget(self.displayer_3)
            self.displayer_container.addWidget(self.displayer_4)
            self.displayer_container.addWidget(self.displayer_5)
            self.displayer_container.addWidget(self.displayer_6)

            group.addWidget(self.displayer_container)
            group.adjustSize()
