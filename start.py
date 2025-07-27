import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

from config import Logger
from refactor_ui import MySiliconApp
from siui.core import SiGlobal
import time

def show_version_message(window):
    window.LayerRightMessageSidebar().send(
        title="Welcome to Silicon UI Gallery",
        text="You are currently running v1.14.514\n"
             "Click this message box to check out what's new.",
        msg_type=1,
        icon=SiGlobal.siui.iconpack.get("ic_fluent_hand_wave_filled"),
        fold_after=5000,
        slot=lambda: window.LayerRightMessageSidebar().send("Oops, it seems that nothing will happen due to the fact "
                                                            "that this function is currently not completed.",
                                                            icon=SiGlobal.siui.iconpack.get("ic_fluent_info_regular"))
    )

    window.LayerRightMessageSidebar().send(
        title="Refactoring in Progress",
        text="To optimize the project structure, "
             "we are currently undergoing a refactoring process.\n\n"
             "We strongly discourage you from using any deprecated components "
             'other than those displayed on the "Refactored Components" page.',
        msg_type=4,
        icon=SiGlobal.siui.iconpack.get("ic_fluent_warning_filled"),
    )




if __name__ == "__main__":
    try:
        time_ = time.time()
        app = QApplication(sys.argv)

        window = MySiliconApp()
        window.show()
        time_1 = time.time()
        Logger.info(f"启动时间: {time_1 - time_}s")

        timer = QTimer(window)
        timer.singleShot(500, lambda: show_version_message(window))

        sys.exit(app.exec_())
    except Exception as e:
        Logger.error(e)