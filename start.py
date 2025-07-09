#  Copyright (c) 2025 UF4OVER
#  All rights reserved.
#  逻辑有些糖了，新人刚开始的作品，但是杨东义没选到站长，他也加不了分了，所以应该也不会优化了，2025年7月9日12点38分

from sys_stdio import setup_logging
setup_logging(False)  # 配置日志

import sys
import logging
from PyQt5.QtWidgets import QApplication
from ui import MySiliconApp
from parts.event.send import send_custom_message, show_message

import config.CONFIG as F

PATH_CONFIG = F.CONFIG_PATH



def main():
    app = QApplication(sys.argv)
    try:
        window = MySiliconApp()
        window.show()
        send_custom_message()
    except Exception as e:
        logging.error("Exception in main", exc_info=True)
        show_message(0, "注意，注意！！！！",
                     '假如这个出现了，就是出现了我也不知道的BUG，请截图联系开发者或者发送根目录下的app.log文件到开发者的邮箱，并且说明BUG复现步骤',
                     "error")
        print(e)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
