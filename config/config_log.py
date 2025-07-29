# -*- coding: utf-8 -*-
# -------------------------------
#  @Project : MCServer
#  @Time    : 2025 - 06-25 16:44
#  @FileName: config_log.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  :
#  @Description: 简单日志记录器
# -------------------------------
import logging
import sys
from datetime import datetime
from pathlib import Path

if getattr(sys, 'frozen', False):
    # 打包后
    LOG_DIR = Path(sys.executable).resolve().parent
else:
    # 正常运行
    LOG_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = LOG_DIR/ "logs"
LOG_DIR.mkdir(exist_ok=True)

# 按年月日_时分生成文件名
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
LOG_PATH = LOG_DIR / f"{timestamp}.log"

# 创建日志器
logger = logging.getLogger("MCServerLauncher")
logger.setLevel(logging.DEBUG)

# 控制台输出
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 文件输出
file_handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# 日志格式
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# 添加处理器（避免重复）
if not logger.hasHandlers():
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

if __name__ == '__main__':
    logger.info("单例模式哦")
