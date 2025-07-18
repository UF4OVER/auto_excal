# -*- coding: utf-8 -*-
# -------------------------------
#  @Project : siui_refactor
#  @Time    : 2025 - 07-17 18:33
#  @FileName: uploader.py.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  :
#  @Desc    : 异步上传表格数据
# -------------------------------
from PyQt5.QtCore import QObject, pyqtSignal, QThread, QTimer
from config import Logger

from parts.component.ShowMessage import show_message
from parts.event.parser import get_data_by_order


class DownloadWorker(QObject):
    """
    主循环，从当前索引位置开始输入49个数据
    """
    progress = pyqtSignal(str, int)     # url, percent
    finished = pyqtSignal(str)                  # url
    error = pyqtSignal(str, str)        # url, errmsg
    def __init__(self, data: list, last_tab):
        super().__init__()
        self._index_current_data: int = 0   # 当前数据索引
        self._data = data
        self._last_tab = last_tab
        self._is_cancelled = False          # 是否取消
    def run(self):
        try:
            start_index = self._index_current_data
            end_index = min(start_index + 49, len(self._data))
            print(f": e1{start_index + 49},{len(self._data)}")
            if start_index >= len(self._data):
                show_message(3, "提示", "数据已全部输入完毕", "ic_fluent_checkmark_starburst_filled")
                return

            for i in range(start_index, end_index):
                xuehao = self._last_tab.ele(f"@id=txtstu{(i % 49) + 1}")
                score = self._last_tab.ele(f"@id=txtpoint{(i % 49) + 1}")

                Logger.info(f"输入数据:{get_data_by_order(self._data, i)[0]['stu_id']}")
                QTimer.singleShot(100, xuehao.input(get_data_by_order(self._data, i)[0]['stu_id']))
                QTimer.singleShot(100, score.input(get_data_by_order(self._data, i)[0]['score']))

            btus = self._last_tab.eles("@value=查询")
            for btu in btus:
                QTimer.singleShot(100, btu.click())
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

    def __id__(self):
        return id(self)
    def cancel(self):
        self._is_cancelled = True
class DownloaderThread(QObject):
    """
    保留线程
    """
    def __init__(self):
        super().__init__()
        self.threads = []  # 用于保存所有线程
    def addTask(self, task: DownloadWorker):
        # 检查是否已经有线程在运行
        if len(self.threads) > 0:
            Logger.warn("已有任务在运行，无法添加新任务")
            show_message(3, "提示", "已有任务在运行，请勿重复添加", "ic_fluent_wrench_filled")
            return
        thread = QThread()
        task.moveToThread(thread)
        Logger.debug(f"启动任务,任务ID:{task.__id__()}")
        thread.started.connect(task.run)

        task.finished.connect(thread.quit)
        task.finished.connect(task.deleteLater)
        thread.finished.connect(thread.deleteLater)

        thread.start()

        # 保存线程引用，防止被销毁
        self.threads.append(thread)