# other_file.py
from siui.core import SiGlobal
import sys
from PyQt5.QtWidgets import QApplication
from ui import MySiliconApp


def show_version_message(window):
    window.LayerRightMessageSidebar().send(
        title="欢迎来到这个APP",
        text="您正在运行的是1.0.0版本",
        msg_type=1,
        icon=SiGlobal.siui.iconpack.get("ic_fluent_hand_wave_regular"),
        fold_after=5000,

    )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MySiliconApp()
    window.show()
    show_version_message(window)
    sys.exit(app.exec_())

































