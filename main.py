import json
import pyautogui
import main_window as m
import small_window as s
import threading
import time
import sys

from qt_material import apply_stylesheet
from openpyxl.reader.excel import load_workbook
from pynput import mouse

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QColor, QTextCharFormat
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox, \
    QInputDialog, QLineEdit, QTableWidget


class mouse_detection_threads(threading.Thread):
    """
    处理鼠标双击的子线程
    """

    def __init__(self, parent=None):
        print("mouse_detection_threads")
        super().__init__()
        self.running = False
        self.paused = False
        self.double_click_count = 0
        self.double_click_threshold = 0.3  # 双击时间阈值（秒）
        self.last_click_time = 0
        self.parent = parent
        self.listener = None

    def on_click(self, x, y, button, pressed):
        """处理鼠标点击事件"""
        if pressed and button == mouse.Button.left:
            current_time = time.time()
            if current_time - self.last_click_time < self.double_click_threshold:
                self.double_click_count += 1
                self.last_click_time = current_time
                if self.double_click_count >= 2:
                    self.parent.on_double_click()
                    self.double_click_count = 0
            else:
                self.double_click_count = 1
                self.last_click_time = current_time

    def run(self):
        self.running = True
        while self.running:
            if not self.paused:
                if self.listener is None:
                    self.listener = mouse.Listener(on_click=self.on_click)
                    self.listener.start()
                self.listener.join(1)
            else:
                if self.listener is not None:
                    self.listener.stop()
                    self.listener = None
                time.sleep(0.1)

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.running = False
        if self.listener:
            self.listener.stop()


class CellClickThread(threading.Thread):
    def __init__(self, table_widget, row, column, signal):
        super().__init__()
        self.table_widget = table_widget
        self.row = row
        self.column = column
        self.signal = signal

    def run(self):
        if not self.table_widget.item(self.row, self.column):
            return
        cell_value = self.table_widget.item(self.row, self.column).text()

        self.signal.emit((self.row, self.column))


class SmallWindow(QMainWindow, s.Ui_MainWindow):
    # start_stop_signal = pyqtSignal(bool)

    def __init__(self):
        print("small_window")
        super().__init__()
        self.ui = s.Ui_MainWindow()
        self.main_window = MainWindow  # 保存 MainWindow 的引用
        self.ui.setupUi(self)
        self.init_ui()
        self.solt()
        self.ui.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # self.start_stop_bool = 0
        # self.start_stop_signal.connect(
            # lambda: self.main_window.get_start_stop_bool(value=self.start_stop_bool))

    def init_ui(self):
        self.back_btu = self.ui.pushButton_3
        self.paused_btu = self.ui.pushButton
        self.clear_btu = self.ui.pushButton_2

    def solt(self):
        self.back_btu.clicked.connect(self.close_window)
        self.clear_btu.clicked.connect(self.claer_table)

        # self.paused_btu.clicked.connect(self.reverse)

    # def reverse(self):
    #     print("点击了反转")
    #     self.start_stop_bool = not self.start_stop_bool
    #     value = self.start_stop_bool
    #     if value:
    #         self.paused_btu.setText("暂停")
    #     else:
    #         self.paused_btu.setText("开始")
    #     self.start_stop_signal.emit(value)

    def update_table_data(self, data, rows, cols):
        self.ui.tableWidget.setRowCount(rows)
        self.ui.tableWidget.setColumnCount(cols)
        self.ui.tableWidget.clearContents()

        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                self.ui.tableWidget.setItem(row, col, QTableWidgetItem(value))

    def highlight_row(self, row_index):
        for col in range(self.ui.tableWidget.columnCount()):
            item = self.ui.tableWidget.item(row_index, col)
            item.setBackground(QColor("lightblue"))
            if item:
                item.setSelected(True)
                item.setForeground(QColor("lightblue"))
                print("highlighted cell:", row_index, col)

    def update_heping_value(self, value):
        self.index_row = value

    def claer_table(self):
        print("small_window claer_table")
        self.ui.tableWidget.clearContents()

    def close_window(self):
        print("small_window hide")
        self.close()


class MainWindow(QMainWindow, m.Ui_MainWindow):
    cell_clicked_signal = pyqtSignal(tuple)
    data_updated = pyqtSignal(list, int, int)
    hightlighted_row_changed = pyqtSignal(int)  # 定义信号
    heping_updated = pyqtSignal(int)  # 定义信号
    global small_window_send_signal_to_main_window

    def __init__(self):
        super().__init__()

        self.ui = m.Ui_MainWindow()
        self.ui.setupUi(self)

        self.setupUI()
        self.slot()
        self.cell_clicked_signal.connect(self.handle_cell_clicked)
        self.ui.tableWidget_2.itemChanged.connect(self.on_item_changed)
        self.mouse_thread = None  # 鼠标双击线程
        self.sheet = None
        self.start_stop_bool = False  # 小窗传递的启动状态

        self.heping = 1  # 默认为0,order选取

        self.ui.tableWidget_2.verticalHeader().setVisible(False)  # 隐藏垂直表头
        self.ui.tableWidget_2.horizontalHeader().setVisible(False)  # 隐藏水平表头
        self.init_theme_combobox()

    def setupUI(self):

        self.flag = True
        self.sheet = None
        self.command_output = self.ui.textBrowser  # 输出框

        self.add_file_btu = self.ui.pushButton_3  # 添加文件
        self.add_file_line = self.ui.lineEdit_3  # 添加文件输入框

        self.start_btu = self.ui.pushButton_7  # 开始子线程监控鼠标双击事件
        # self.start_btu.clicked.connect(self.start_or_stop_detection)

        self.small_win_btu = self.ui.pushButton_6  # 打开小窗口
        self.preview_btu = self.ui.pushButton_5  # 预览按钮

        self.name_start_input = self.ui.lineEdit_4  # 名字开始
        self.name_end_input = self.ui.lineEdit_6

        self.xuehao_start_input = self.ui.lineEdit_5  # 学号开始
        self.xuehao_end_input = self.ui.lineEdit_8

        self.score_start_input = self.ui.lineEdit_7  # 分数开始
        self.score_end_input = self.ui.lineEdit_9

        self.add_one_data_btu = self.ui.pushButton_2  # 添加一行数据

        self.theme_comboBox = self.ui.comboBox

        # ['深琥珀色.xml','dark_amber.xml',
        #  '深蓝色.xml','dark_blue.xml',
        #  '深青色.xml','dark_cyan.xml',
        #  '深绿色.xml','dark_lightgreen.xml',
        #  '深粉色.xml','dark_pink.xml',
        #  '深紫色.xml','dark_purple.xml',
        #  '绯.xml','dark_red.xml',
        #  '深蓝绿色.xml','dark_teal.xml',
        #  '䵎.xml','dark_yellow.xml',
        #  '浅琥珀色.xml','light_amber.xml',
        #  '浅蓝色.xml','light_blue.xml',
        #  '浅青色.xml','light_cyan.xml',
        #  '浅青色 500.xml','light_cyan_500.xml',
        #  '浅绿色.xml','light_lightgreen.xml',
        #  '浅粉色.xml','light_pink.xml',
        #  '浅粉色.xml','light_pink.xml',
        #  '纁.xml','light_red.xml',
        #  '浅蓝绿色.xml','light_teal.xml',
        #  '浅黄色.xml''light_yellow.xml']

    def slot(self):
        self.add_file_btu.clicked.connect(self.add_file)
        self.ui.tableWidget.cellClicked.connect(self.on_cell_clicked)  # 绑定单元格点击事件
        self.ui.tableWidget_2.itemChanged.connect(self.save_to_json)  # 绑定单元格内容改变事件
        self.small_win_btu.clicked.connect(self.open_small_window)  # 打开小窗口
        self.preview_btu.clicked.connect(self.on_item_changed)
        # self.preview_btu.clicked.connect(self.save_to_json_btu)  # 保存到json
        self.start_btu.clicked.connect(self.start_or_stop_detection)  # 开启监控
        self.add_one_data_btu.clicked.connect(self.add_one_data)  # 添加一行数据
        self.theme_comboBox.currentIndexChanged.connect(self.change_theme)

    def init_theme_combobox(self):
        themes = [
            ('深琥珀色', 'dark_amber.xml'),
            ('深蓝色', 'dark_blue.xml'),
            ('深青色', 'dark_cyan.xml'),
            ('深绿色', 'dark_lightgreen.xml'),
            ('深粉色', 'dark_pink.xml'),
            ('深紫色', 'dark_purple.xml'),
            ('深红色', 'dark_red.xml'),
            ('深蓝绿色', 'dark_teal.xml'),
            ('深黄色', 'dark_yellow.xml'),
            ('浅琥珀色', 'light_amber.xml'),
            ('浅蓝色', 'light_blue.xml'),
            ('浅青色', 'light_cyan.xml'),
            ('浅青色 500', 'light_cyan_500.xml'),
            ('浅绿色', 'light_lightgreen.xml'),
            ('浅粉色', 'light_pink.xml'),
            ('亮红色', 'light_red.xml'),
            ('浅蓝绿色', 'light_teal.xml'),
            ('浅黄色', 'light_yellow.xml')
        ]

        for display_text, theme_file in themes:
            self.theme_comboBox.addItem(display_text, theme_file)

    def change_theme(self, index):
        theme_file = self.theme_comboBox.itemData(index)
        if theme_file:
            apply_stylesheet(app, theme=theme_file)
            self.command_output_print("info", f"已切换到主题: {theme_file}")

    def open_small_window(self):
        """
        打开小窗
        :return:
        """
        self.small_win = SmallWindow()
        print("open_small_window")
        self.small_win.show()
        self.data_updated.connect(self.small_win.update_table_data)
        self.hightlighted_row_changed.connect(self.small_win.highlight_row)
        # self.heping_updated.connect(small_win.update_heping_value)

        self.hightlighted_row_changed.emit(self.heping)
        # self.heping_updated.emit(self.heping)

    def on_item_changed(self):
        # 获取表格数据并发送信号
        data = self.get_table_data()
        rows = self.ui.tableWidget_2.rowCount()
        cols = self.ui.tableWidget_2.columnCount()
        self.data_updated.emit(data, rows, cols)

    def get_table_data(self):
        data = []
        for row in range(self.ui.tableWidget_2.rowCount()):
            row_data = []
            for col in range(self.ui.tableWidget_2.columnCount()):
                item = self.ui.tableWidget_2.item(row, col)
                if item:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            data.append(row_data)
        return data

    # ---------------------单元格点击事件---------------------------#
    def on_cell_clicked(self, row, column):  # 绑定单元格点击事件
        thread = CellClickThread(self.ui.tableWidget, row, column, self.cell_clicked_signal)  # 创建线程
        thread.start()

    def handle_cell_clicked(self, data):  # 处理单元格点击事件
        row, column = data
        cell_value = self.ui.tableWidget.item(row, column).text()
        print(f"点击了单元格 ({row + 1}, {column + 1})，内容为: {cell_value}")
        self.command_output_print("msg", f"点击了单元格 ({row + 1}, {column + 1})，内容为: {cell_value}")

    # @staticmethod
    # def get_start_stop_bool(value):
    #     small_window_send_signal_to_main_window = value
    #
    # def saas(self):
    #     print("sad")
    #     if small_window_send_signal_to_main_window != small_window_send_signal_to_main_window:
    #         self.command_output_print("info", "开始监控")
    #         self.mouse_thread.start()

    # ----------------------------------------------------------#

    # -------------------子线程监控鼠标双击事件---------------------#
    def start_or_stop_detection(self):
        try:
            if self.sheet:
                if self.mouse_thread is None:
                    self.mouse_thread = mouse_detection_threads(parent=self)
                    self.mouse_thread.start()
                    self.start_btu.setText("结束")
                else:
                    self.mouse_thread.stop()
                    self.mouse_thread.join()
                    self.mouse_thread = None
                    self.start_btu.setText("开始")
            else:
                self.command_output_print("error", "不选文件??")
        except Exception as e:
            print("错误", e)
            self.command_output_print("error", "先选择文件 (><) !!")

    def on_double_click(self) -> None:
        try:
            data = self.read_json_file()
            id = self.get_data_by_order(data, self.heping)
            id_dict_value = id[0]["xuehao"]
            col_conduct_points_dict_value = id[0]["score"]
            name_dict_value = id[0]["name"]

            self.heping = self.heping + 1

            self.hightlighted_row_changed.emit(self.heping - 2)
            self.heping_updated.emit(self.heping)

            self.command_output_print("warning", f"第{self.heping - 1}次:")
            self.command_output_print("info", f"当前键入:")
            self.command_output_print("msg", f"姓名:{name_dict_value}")
            self.command_output_print("msg", f"学号:{id_dict_value}")
            self.command_output_print("msg", f"操行分:{col_conduct_points_dict_value}")
            pyautogui.typewrite(str(id_dict_value))  # 键入学号
            time.sleep(0.1)

            pyautogui.press('tab')
            time.sleep(0.1)

            pyautogui.press('enter')
            time.sleep(0.1)

            pyautogui.typewrite(str(col_conduct_points_dict_value))  # 键入操行分
            time.sleep(0.1)

            pyautogui.press('tab')
            time.sleep(0.1)

        except Exception as e:
            self.command_output_print("error", f"{e}")

        finally:
            self.command_output_print("msg", "完成")

    def closeEvent(self, event) -> None:
        if self.mouse_thread is not None:
            self.mouse_thread.stop()
            self.mouse_thread.join()
        event.accept()

    # ----------------------------------------------------------#

    def add_file(self) -> None:
        """
        选择文件
        :return:
        """
        # 使用 QFileDialog 获取文件路径
        file_path_temp1, _ = QFileDialog.getOpenFileName(self, "选择文件", "/", "Excel文件 (*.xlsx *.xls)")
        file_path_temp2 = self.ui.lineEdit_3.text()
        file_paths = file_path_temp1 if file_path_temp1 else file_path_temp2

        if file_paths:
            self.command_output_print("info", f"加载了文件{file_paths}")

            try:
                self.ui.lineEdit_3.setText(file_paths)

                wb = load_workbook(file_paths)
                self.sheet = wb.active

                rows = self.sheet.max_row
                cols = self.sheet.max_column

                self.ui.tableWidget.setRowCount(rows)
                self.ui.tableWidget.setColumnCount(cols)

                for row in range(1, rows + 1):
                    for col in range(1, cols + 1):
                        cell_value = self.sheet.cell(row=row, column=col).value
                        cell_value = str(cell_value)  # 确保值为字符串

                        if cell_value.lower() == '姓名':
                            # 输出姓名该单元格所在列的所有数据
                            print(f"姓名所在列: {col}")
                            self.name_col = col
                            self.name_row = row + 1
                            print(self.name_row, self.name_col, )
                            self.command_output_print("msg", f"已定位到姓名{row, col}")
                            self.name_start_input.setText(f"{row + 1, col}")
                            self.name_end_input.setText(f"{self.sheet.max_row, col}")
                            self.ui.tableWidget_2.setRowCount(self.sheet.max_row - self.name_row + 1)
                            self.ui.tableWidget_2.setColumnCount(3)

                            for i in range(self.name_row, self.sheet.max_row + 1):
                                a = i - self.name_row
                                b = 0
                                item_2 = QTableWidgetItem(str(self.sheet.cell(row=i, column=self.name_col).value))
                                self.ui.tableWidget_2.setItem(a, b, item_2)

                        elif '学号' in cell_value:
                            # 输出姓名该单元格所在列的所有数据
                            print(f"学号所在列: {col}")
                            self.xuehao_col = col
                            self.xuehao_row = row + 1
                            print(self.xuehao_col, self.xuehao_row)
                            self.command_output_print("msg", f"已定位到学号{row, col}")
                            self.xuehao_start_input.setText(f"{row + 1, col}")
                            self.xuehao_end_input.setText(f"{self.sheet.max_row, col}")
                            for i in range(self.xuehao_row, self.sheet.max_row + 1):
                                a = i - self.xuehao_row
                                b = 1
                                item_2 = QTableWidgetItem(str(self.sheet.cell(row=i, column=self.xuehao_col).value))
                                self.ui.tableWidget_2.setItem(a, b, item_2)

                        elif '加分' in cell_value:
                            # 输出姓名该单元格所在列的所有数据
                            print(f"分数所在列: {col}")
                            self.score_col = col
                            self.score_row = row + 1
                            print(self.score_col, self.score_row)
                            self.command_output_print("msg", f"已定位到分数{row, col}")
                            self.score_start_input.setText(f"{row + 1, col}")
                            self.score_end_input.setText(f"{self.sheet.max_row, col}")
                            for i in range(self.score_row, self.sheet.max_row + 1):
                                a = i - self.score_row
                                b = 2
                                item_3 = QTableWidgetItem(str(self.sheet.cell(row=i, column=self.score_col).value))
                                self.ui.tableWidget_2.setItem(a, b, item_3)
                            self.command_output_print("info",
                                                      f"一共提取到{self.sheet.max_row - self.name_row}个数据")


                        else:
                            item = QTableWidgetItem(str(cell_value))
                            self.ui.tableWidget.setItem(row - 1, col - 1, item)
            except Exception as e:
                # 异常处理
                self.command_output_print("error", f"加载文件时发生错误: {e}")
                print(f"加载文件时发生错误: {e}")

    def add_one_data(self) -> None:
        self.command_output_print("info", "添加一行数据到输入")

        # 弹出一个对话框，里面有三个输入框，分别输入姓名，学号，分数
        # 有两个按钮分别是确定和取消，确定按钮按下后，将输入框中的数据添加到表格中，取消按钮按下后，不添加数据
        name, ok_name = QInputDialog.getText(self, "添加姓名", "姓名:", QLineEdit.Normal, "")

        if not ok_name:
            return

        xuehao, ok_xuehao = QInputDialog.getText(self, "添加学号", "学号:", QLineEdit.Normal, "")
        if not ok_xuehao:
            return

        score, ok_score = QInputDialog.getText(self, "添加分数", "分数:", QLineEdit.Normal, "")
        if not ok_score:
            return

        if name and xuehao and score:
            self.command_output_print("info", f"添加了姓名{name}，学号{xuehao}，分数{score}")

            # 获取当前表格的行数
            current_row_count = self.ui.tableWidget_2.rowCount()

            # 插入新行
            self.ui.tableWidget_2.insertRow(current_row_count)

            # 设置新行的数据
            self.ui.tableWidget_2.setItem(current_row_count, 0, QTableWidgetItem(name))
            self.ui.tableWidget_2.setItem(current_row_count, 1, QTableWidgetItem(xuehao))
            self.ui.tableWidget_2.setItem(current_row_count, 2, QTableWidgetItem(score))
        else:
            QMessageBox.critical(self, "错误", "请输入完整的信息")
            self.command_output_print("error", "请输入完整的信息")

    def command_output_print(self, level, msg) -> None:
        """
        打印命令行输出
        :param level: info:blue,error:red,msg:black,warning:orange,debug:green
        :param msg: 消息
        :return: None
        """

        if level == "info":
            color = QColor("blue")
        elif level == "error":
            color = QColor("red")
        elif level == "msg":
            color = QColor("black")
        elif level == "warning":
            color = QColor("orange")
        elif level == "debug":
            color = QColor("green")
        else:
            print("未知级别")

        format = QTextCharFormat()
        format.setForeground(color)
        cursor = self.ui.textBrowser.textCursor()
        cursor.insertText(f"[{level}] {msg}\n", format)
        self.ui.textBrowser.setTextCursor(cursor)

    def get_data_by_order(self, data, order) -> list:
        """
        根据指定的order值筛选数据

        :param data: 包含JSON数据的列表
        :param order: 要筛选的order值
        :return: 筛选出的数据列表
        """
        filtered_data = [item for item in data if item.get('order') == order]
        return filtered_data

    def save_to_json(self) -> None:
        data_list = []

        try:
            row_count = self.ui.tableWidget_2.rowCount()
            names = [self.ui.tableWidget_2.item(i, 0).text() if self.ui.tableWidget_2.item(i, 0) else None for i in
                     range(row_count)]
            xuehaos = [self.ui.tableWidget_2.item(i, 1).text() if self.ui.tableWidget_2.item(i, 1) else None for i in
                       range(row_count)]
            scores = [self.ui.tableWidget_2.item(i, 2).text() if self.ui.tableWidget_2.item(i, 2) else None for i in
                      range(row_count)]

            for name, xuehao, score in zip(names, xuehaos, scores):
                if name is not None and xuehao is not None and score is not None:
                    order = names.index(name) + 1
                    data = {
                        "order": order,
                        "name": name,
                        "xuehao": xuehao,
                        "score": score
                    }
                    data_list.append(data)
            with open('data.json', 'w') as f:
                json.dump(data_list, f, ensure_ascii=False, indent=4)

        except Exception as e:
            self.command_output_print("error", f"保存数据时发生错误: {e}")

    def get_int_to_str(self, a) -> tuple:
        """
        将整数转换为字符串，并在末尾添加逗号和空格
        :param a: 整数
        :return: 转换后的字符串
        """
        text = a.strip('()')
        parts = text.split(',')
        row = int(parts[0].strip())
        col = int(parts[1].strip())

        return row, col

    def save_to_json_btu(self) -> None:
        data_list = []

        try:
            self.command_output_print("debug", "还没写呢，不知道这个实现什么功能")

            # for name, xuehao, score in zip(names, xuehaos, scores):
            #     if name is not None and xuehao is not None and score is not None:
            #         order = names.index(name) + 1
            #         data = {
            #             "order": order,
            #             "name": name,
            #             "xuehao": xuehao,
            #             "score": score
            #         }
            #         data_list.append(data)
            # with open('data.json', 'w') as f:
            #     json.dump(data_list, f, ensure_ascii=False, indent=4)

        except Exception as e:
            self.command_output_print("error", f"保存数据时发生错误: {e}")

    def read_json_file(self) -> list:
        """
        从指定的JSON文件中读取数据并返回一个列表
        :return: 包含JSON数据的列表
        """
        file_path = "data.json"
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print(f"文件未找到: {file_path}")
            return []
        except json.JSONDecodeError:
            print(f"JSON解码错误: {file_path}")
            return []


if __name__ == "__main__":


    app = QApplication(sys.argv)
    try:
        ui = MainWindow()
        small_window = SmallWindow()
        ui.show()
        sys.exit(app.exec_())
    except Exception as e:
       print(e)
       sys.exit(app.exec_())
