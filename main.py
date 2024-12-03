from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, QTimer
from qframelesswindow import StandardTitleBar, AcrylicWindow
from qfluentwidgets import Flyout, InfoBarIcon, FlyoutAnimationType, \
    setThemeColor, setTheme, Theme
from app_form import Ui_Form
import sys
import configparser
import re


class login_form(AcrylicWindow, Ui_Form):
    CONFIG_FILE = 'config.ini'

    def __init__(self, on_login=None):
        super().__init__()
        self.setupUi(self)
        self.ui = Ui_Form()
        self.setTitleBar(StandardTitleBar(self))
        self.titleBar.raise_()
        self.resize(1400, 900)
        self.setWindowTitle("登录")
        rect = QApplication.desktop().availableGeometry()
        self.move(rect.width() // 2 - self.width() // 2, rect.height() // 2 - self.height() // 2)
        setThemeColor("#D55FDE")
        setTheme(Theme.DARK)
        self.config = configparser.ConfigParser()
        self._initui()
        self._solt()
        self.sig = False
        QTimer.singleShot(500, self.load_config)
        self.on_login = on_login

    def _initui(self):
        self.login_btu = self.pushButton_2
        self.go_register_btu = self.pushButton
        self.forget_psd_btu = self.pushButton_3
        self.backto_login_btu = self.pushButton_5
        self.register_btu = self.pushButton_4

        self.log_psd_input = self.lineEdit_2
        self.log_mail_input = self.lineEdit

        self.register_mail_input = self.lineEdit_4
        self.register_psd_input = self.lineEdit_5
        self.register_repsd_input = self.lineEdit_6
        self.register_name_input = self.lineEdit_3

    def _solt(self):
        self.login_btu.clicked.connect(self.login)
        self.register_btu.clicked.connect(self.register)
        self.backto_login_btu.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.go_register_btu.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

    def login(self) -> None:
        email = self.log_mail_input.text()
        password = self.log_psd_input.text()

        if not email:
            self.info_bar(0, "请输入邮箱", "邮箱不能为空")
        elif not password:
            self.info_bar(0, "请输入密码", "密码不能为空")
        else:
            self.save_config("Login", email, password)
            self.config.read(self.CONFIG_FILE)
            if 'Register' in self.config and 'email' in self.config['Register'] and 'password' in self.config[
                'Register']:
                email_from_config = self.config['Register']['email']
                password_from_config = self.config['Register']['password']
                if email == email_from_config and password == password_from_config:
                    self.info_bar(1, "登录成功", "欢迎回来")
                    self.sig = True
                    if self.on_login:
                        self.on_login(email, password)
                    self.close()

                else:
                    self.info_bar(0, "邮箱或密码错误", "请重新输入")
            else:
                self.info_bar(0, "请先注册", "未检测到该账号，请先注册账号后重试")

            self.stackedWidget.setCurrentIndex(2)  # 假设主界面的索引是2

    def register(self) -> None:
        email = self.register_mail_input.text()
        password = self.register_psd_input.text()
        re_password = self.register_repsd_input.text()
        name = self.register_name_input.text()
        if not email:
            self.info_bar(0, "请输入邮箱", "邮箱不能为空")
        elif not password:
            self.info_bar(0, "请输入密码", "密码不能为空")
        elif password != re_password:
            self.info_bar(0, "两次密码不一致", "请重新输入")
        elif not self.is_valid_email(email):
            self.info_bar(0, "邮箱格式不正确", "请输入正确的邮箱地址")
        elif len(name) > 12:
            self.info_bar(0, "用户名长度不能大于12", "请重新输入")
        elif len(name) < 3:
            self.info_bar(0, "用户名长度不能小于3", "请重新输入")
        elif len(password) > 12:
            self.info_bar(0, "密码长度不能大于12", "请重新输入")
        elif len(password) < 6:
            self.info_bar(0, "密码长度不能小于6", "请重新输入")
        else:
            self.info_bar(1, "注册成功", "请登录")
            self.save_config("Register", email, password)

    def is_valid_email(self, email) -> bool:
        """
        :rtype: bool
        """
        # 定义邮箱格式的正则表达式
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def info_bar(self, _type: int, til: str, msg: str) -> None:
        def show_info_bar(method):
            Flyout.create(
                icon=method,
                title=self.tr(til),
                content=self.tr(msg),
                target=self,
                parent=self,
                isClosable=True,
                aniType=FlyoutAnimationType.FADE_IN
            )

        if _type == 0:
            show_info_bar(InfoBarIcon.ERROR)
        elif _type == 1:
            show_info_bar(InfoBarIcon.SUCCESS)
        elif _type == 2:
            show_info_bar(InfoBarIcon.WARNING)
        elif _type == 3:
            show_info_bar(InfoBarIcon.INFORMATION)

    def load_config(self) -> None:
        self.config.read(self.CONFIG_FILE)

        if 'Login' in self.config and 'email' in self.config['Login'] and 'password' in self.config['Login']:
            email = self.config['Login']['email']
            password = self.config['Login']['password']

            if email and password:
                self.log_mail_input.setText(email)
                self.log_psd_input.setText(password)
                self.login()

    def save_config(self, _type, email, password) -> None:

        self.config[f'{_type}'] = {'email': email, 'password': password}

        with open(self.CONFIG_FILE, 'w') as configfile:
            self.config.write(configfile)

    def __bool__(self) -> bool:
        return self.sig


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = login_form(on_login=lambda email, password: print(f"登录成功: {email}, {password}"))
    myWindow.show()
    app.exec_()
