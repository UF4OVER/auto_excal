from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QMouseEvent

class auto_main(QMainWindow, Ui_app):

    def __init__(self):
        super(auto_main, self).__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)  # 设置窗口无边框
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置背景透明
        #显示主窗口
        self.show()
        #创建托盘图标并显示
        self.create_tray_icon()
        #关闭事件
        self.pushButton.clicked.connect(self.hide)
        # 设置鼠标按下时的位置，保证无边框时窗口可以用鼠标拖动
        self.drag_position = None

    def icon_activated(self,reason):
        '''
        双击托盘图标，恢复窗口
        :param reason:
        :return:
        '''
        if reason == QSystemTrayIcon.DoubleClick:
            self.setWindowState(Qt.WindowActive)
            self.show()
            # 在这里可以添加双击托盘图标时的处理逻辑

    def create_tray_icon(self):
        '''
        创建托盘图标
        :return:
        '''

        # 创建一个QSystemTrayIcon对象
        tray_icon = QSystemTrayIcon(self)
        #设置托盘图标
        tray_icon.setIcon(QIcon(QIcon('image/托盘_图标.png')))

        # 创建一个上下文菜单（右击托盘图标显示的菜单栏选项）
        menu = QMenu()
        quit_action = QAction("退出程序", menu)
        quit_action.triggered.connect(sys.exit)
        menu.addAction(quit_action)

        # 设置鼠标悬停提示文本
        tray_icon.setToolTip('远程升级检测程序')

        # 设置托盘图标的上下文菜单
        tray_icon.setContextMenu(menu)

        # 连接激活信号到槽函数
        tray_icon.activated.connect(self.icon_activated)

        # 显示托盘图标
        tray_icon.show()

        # 气泡文本
        # tray_icon.showMessage("标题","这是描述性文本")

    #窗口拖动实现
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & Qt.LeftButton and self.drag_position is not None:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.drag_position = None

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = auto_main()
    sys.exit(app.exec_())

