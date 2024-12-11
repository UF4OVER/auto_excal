# other_file.py
from siui.core import SiGlobal
import sys
from PyQt5.QtWidgets import QApplication
from ui import MySiliconApp


def show_version_message(window):
    window.LayerRightMessageSidebar().send(
        title="Welcome to this",
        text="You are currently running v0.0.1\n"
             "Click this message box to check out what's new.",
        msg_type=1,
        icon=SiGlobal.siui.iconpack.get("ic_fluent_hand_wave_regular"),
        fold_after=5000,
        slot=lambda: window.LayerRightMessageSidebar().send("Oops, it seems that nothing will happen due to the fact "
                                                            "that this function is currently not completed.",
                                                            icon=SiGlobal.siui.iconpack.get("ic_fluent_info_regular"))
    )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MySiliconApp()
    window.show()
    show_version_message(window)
    sys.exit(app.exec_())
