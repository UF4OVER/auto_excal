#  Copyright (c) 2025 UF4OVER
#  All rights reserved.
#  逻辑有些糖了，新人刚开始的作品，但是杨东义没选到站长，他也加不了分了，所以应该也不会优化了，2025年7月9日12点38分

import sys
import logging
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import config.CONFIG as F

F.initialize_runtime()




def main():
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    from parts.event.send import send_custom_message, show_message
    from ui import MySiliconApp

    try:
        window = MySiliconApp()
        window.show()
        send_custom_message()
    except Exception as e:
        logging.error("Exception in main", exc_info=True)
        show_message(0, "注意，注意！！！！",
                     '程序启动失败，请截图联系开发者，或者附上 Logs/app.log 并说明复现步骤。',
                     "ic_fluent_error_circle_filled")
        print(e)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
