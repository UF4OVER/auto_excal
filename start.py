# other_file.py
from siui.core import SiGlobal

from main import login_form
import sys
from PyQt5.QtWidgets import QApplication
from ui import MySiliconApp


def show_version_message(window):
    window.LayerRightMessageSidebar().send(
        title="Welcome to Silicon UI Gallery",
        text="You are currently running v1.14.514\n"
             "Click this message box to check out what's new.",
        msg_type=1,
        icon=SiGlobal.siui.iconpack.get("ic_fluent_hand_wave_regular"),
        fold_after=5000,
        slot=lambda: window.LayerRightMessageSidebar().send("Oops, it seems that nothing will happen due to the fact "
                                                            "that this function is currently not completed.",
                                                            icon=SiGlobal.siui.iconpack.get("ic_fluent_info_regular"))
    )


def on_login(email, password):
    # 登录成功后启动主页面
    app = QApplication(sys.argv)
    window = MySiliconApp()
    window.show()
    show_version_message()
    sys.exit(app.exec_())


def main():
    app = QApplication(sys.argv)
    window_1 = login_form(on_login=on_login)
    window_1.show()
    app.exec_()


def test_main():
    app = QApplication(sys.argv)
    window = MySiliconApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    test_main()
