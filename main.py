import sys

from PyQt5.QtCore import Qt, QSize, QEventLoop, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QApplication
from qfluentwidgets import NavigationItemPosition, FluentWindow, SubtitleLabel, setFont, Theme, setTheme, SplashScreen
from qfluentwidgets import FluentIcon as FIF

from config.interface import SettingInterface
from page import auto_excal


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)

        # 必须给子界面设置全局唯一的对象名
        self.setObjectName(text.replace(' ', '-'))


class Auto_excal_page(QFrame, auto_excal.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)


class Window(FluentWindow):
    """ 主界面 """

    def __init__(self):
        super().__init__()
        setTheme(Theme.DARK)

        self.setWindowTitle('PyQt-Fluent-Widgets')
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(200, 200))

        # 2. 在创建其他子页面前先显示主界面
        self.show()

        # 3. 创建子界面
        self.createSubInterface()
        # 4. 隐藏启动页面
        self.splashScreen.finish()
        # 创建子界面，实际使用时将 Widget 换成自己的子界面
        self.homeInterface = Widget('Home Interface', self)
        self.musicInterface = Widget('Music Interface', self)
        self.autoInterface = Auto_excal_page()
        self.settingInterface = SettingInterface()
        self.albumInterface = Widget('Album Interface', self)
        self.albumInterface1 = Widget('Album Interface 1', self)

        self.initNavigation()
        self.initWindow()

    def createSubInterface(self):
        loop = QEventLoop(self)
        QTimer.singleShot(1000, loop.quit)
        loop.exec()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, 'Home')
        self.addSubInterface(self.musicInterface, FIF.MUSIC, 'Music library')
        self.addSubInterface(self.autoInterface, FIF.VIDEO, 'Auto_excal')

        self.navigationInterface.addSeparator()

        self.addSubInterface(self.albumInterface, FIF.ALBUM, 'Albums', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.albumInterface1, FIF.ALBUM, 'Album 1', parent=self.albumInterface)

        self.addSubInterface(self.settingInterface, FIF.SETTING, 'Settings')

    def initWindow(self):
        self.resize(800, 600)
        # 获取屏幕的可用几何尺寸
        rect = self.screen().availableGeometry()
        # 将窗口移动到屏幕中央
        self.move(rect.width() // 2 - self.width() // 2, rect.height() // 2 - self.height() // 2)

        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('PyQt-Fluent-Widgets')


if __name__ == '__main__':
    # 设置高分辨率的缩放
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    sys.argv.append("--enable-highdpi-support")
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
