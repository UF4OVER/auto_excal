# -*- coding: utf-8 -*-
# -------------------------------
#  @Project : flu_new
#  @Time    : 2025 - 02-14 14:43
#  @FileName: interface.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------
# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog
from qfluentwidgets import FluentIcon as FIF, PushSettingCard
from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, OptionsSettingCard, HyperlinkCard,
                            PrimaryPushSettingCard, ScrollArea,
                            ComboBoxSettingCard, ExpandLayout, Theme, InfoBar, CustomColorSettingCard,
                            setTheme, setThemeColor, isDarkTheme)

from config.config import cfg, HELP_URL, VERSION, YEAR, AUTHOR, FEEDBACK_URL


class SettingInterface(ScrollArea):
    """ Setting interface """

    checkUpdateSig = pyqtSignal()
    acrylicEnableChanged = pyqtSignal(bool)
    browserPortChanged = pyqtSignal(int)  # 定义一个信号，传递字符串类型的端口号
    browserPathChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.setObjectName("ces")
        self.defult_browserpath_text = r"C:\Program Files (x86)\Microsoft\Edge\Application"
        # setting label
        self.settingLabel = QLabel("设置（右键关闭）", self)
        # 浏览器配置
        # 浏览器路径
        self.browserGroup = SettingCardGroup(self.tr('Browser'), self.scrollWidget)
        self.browserPathCard = PushSettingCard(
            text="选择浏览器根目录",
            icon=FIF.FOLDER,
            title="Edge浏览器根目录",
            content="emmm这里不能更新，不知道为什么"
        )
        # 浏览器端口
        self.browserPortCard = ComboBoxSettingCard(
            configItem=cfg.browserPort,
            icon=FIF.APPLICATION,
            title="端口",
            texts=['9222', '9223', '9224', '0'],
            parent=self.browserGroup

        )

        # personalization
        self.personalGroup = SettingCardGroup(self.tr('Personalization'), self.scrollWidget)
        self.enableAcrylicCard = SwitchSettingCard(
            FIF.TRANSPARENT,
            self.tr("Use Acrylic effect"),
            self.tr("Acrylic effect has better visual experience, but it may cause the window to become stuck"),
            configItem=cfg.enableAcrylicBackground,
            parent=self.personalGroup
        )
        self.themeCard = OptionsSettingCard(
            cfg.themeMode,
            FIF.BRUSH,
            self.tr('Application theme'),
            self.tr("Change the appearance of your application"),
            texts=[
                self.tr('Light'), self.tr('Dark'),
                self.tr('Use system setting')
            ],
            parent=self.personalGroup
        )
        self.themeColorCard = CustomColorSettingCard(
            cfg.themeColor,
            FIF.PALETTE,
            self.tr('Theme color'),
            self.tr('Change the theme color of you application'),
            self.personalGroup
        )
        self.zoomCard = OptionsSettingCard(
            cfg.dpiScale,
            FIF.ZOOM,
            self.tr("Interface zoom"),
            self.tr("Change the size of widgets and fonts"),
            texts=[
                "100%", "125%", "150%", "175%", "200%",
                self.tr("Use system setting")
            ],
            parent=self.personalGroup
        )
        # application
        self.aboutGroup = SettingCardGroup(self.tr('About'), self.scrollWidget)
        self.helpCard = HyperlinkCard(
            HELP_URL,
            self.tr('Open help page'),
            FIF.HELP,
            self.tr('Help'),
            self.tr('Discover'),
            self.aboutGroup
        )
        self.feedbackCard = PrimaryPushSettingCard(
            self.tr('Provide feedback'),
            FIF.FEEDBACK,
            self.tr('Provide feedback'),
            self.tr('feedback'),
            self.aboutGroup
        )
        self.aboutCard = PrimaryPushSettingCard(
            self.tr('Check update'),
            FIF.INFO,
            self.tr('About'),
            '© ' + self.tr('Copyright') + f" {YEAR}, {AUTHOR}. " +
            self.tr('Version') + f" {VERSION}",
            self.aboutGroup
        )

        self.__initWidget()

    def close(self):
        super().close()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 120, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)

        # initialize style sheet
        self.__setQss()

        # initialize layout
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.settingLabel.move(60, 63)
        self.browserGroup.addSettingCard(self.browserPathCard)
        self.browserGroup.addSettingCard(self.browserPortCard)
        self.personalGroup.addSettingCard(self.enableAcrylicCard)
        self.personalGroup.addSettingCard(self.themeCard)
        self.personalGroup.addSettingCard(self.themeColorCard)
        self.personalGroup.addSettingCard(self.zoomCard)
        self.aboutGroup.addSettingCard(self.helpCard)
        self.aboutGroup.addSettingCard(self.feedbackCard)
        self.aboutGroup.addSettingCard(self.aboutCard)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.expandLayout.addWidget(self.browserGroup)
        self.expandLayout.addWidget(self.personalGroup)
        self.expandLayout.addWidget(self.aboutGroup)

    def __setQss(self):
        """ set style sheet """
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')

        theme = 'dark' if isDarkTheme() else 'light'
        with open(f'resource/qss/{theme}/setting_interface.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def __showRestartTooltip(self):
        """ show restart tooltip """
        InfoBar.warning(
            '',
            self.tr('Configuration takes effect after restart'),
            parent=self.window()
        )

    def __onThemeChanged(self, theme: Theme):
        """ theme changed slot """
        # change the theme of qfluentwidgets
        setTheme(theme)

        # chang the theme of setting interface
        self.__setQss()

    def __connectSignalToSlot(self):
        """ connect signal to slot """
        cfg.appRestartSig.connect(self.__showRestartTooltip)
        cfg.themeChanged.connect(self.__onThemeChanged)
        # 浏览器配置
        cfg.browserPort.valueChanged.connect(self.on_browser_port_changed)
        # personalization
        self.enableAcrylicCard.checkedChanged.connect(self.acrylicEnableChanged)
        self.themeColorCard.colorChanged.connect(setThemeColor)
        self.browserPathCard.clicked.connect(self.chooseBrowserPath)

        # about
        self.aboutCard.clicked.connect(self.checkUpdateSig)
        self.feedbackCard.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(FEEDBACK_URL)))

    def on_browser_port_changed(self, new_value):
        # 发出信号，通知端口变化
        self.browserPortChanged.emit(new_value)

    def chooseBrowserPath(self):
        """ choose browser path """
        path,_ = QFileDialog.getOpenFileName(
            self, self.tr('选择浏览器路径'), self.defult_browserpath_text, "可执行文件路径(*.exe)")
        print(path)
        self.defult_browserpath_text = path

        if path:
            self.browserPathChanged.emit(path)
