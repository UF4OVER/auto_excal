# -*- coding: utf-8 -*-
# -------------------------------
#  @Project : siui_refactor
#  @Time    : 2025 - 07-17 18:33
#  @FileName: parser.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  :
#  @Desc    : 解析表格数据到json
# -------------------------------
import json
import os

from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog
from openpyxl.reader.excel import load_workbook

from config import Logger, Settings
from parts.component.ShowMessage import show_message

file_path = os.path.join(Settings.png_dir, "data.json")

def reload_data_for_new_table_widget(new_table_widget, table_widget,
                                     choose_switch,
                                     start_input, finish_input,
                                     start_input1, finish_input1,
                                     start_input2, finish_input2):
    new_table_widget.clear()
    try:
        if choose_switch.isChecked():
            name_start_strtuple = start_input.text()  # "(0,3)"
            name_end_strtuple = finish_input.text()

            xuehao_start_strtuple = start_input1.text()
            xuehao_end_strtuple = finish_input1.text()

            score_start_strtuple = start_input2.text()
            score_end_strtuple = finish_input2.text()

            name_start_int_row, name_start_int_col = name_start_strtuple.strip("()").split(',')
            name_end_int_row, name_end_int_col = name_end_strtuple.strip("()").split(',')
            xuehao_start_int_row, xuehao_start_int_col = xuehao_start_strtuple.strip("()").split(',')
            xuehao_end_int_row, xuehao_end_int_col = xuehao_end_strtuple.strip("()").split(',')
            score_start_int_row, score_start_int_col = score_start_strtuple.strip("()").split(',')
            score_end_int_row, score_end_int_col = score_end_strtuple.strip("()").split(',')

            # 在table_widget中加载上面的数据到new_table_widget
            # 清空 new_table_widget
            new_table_widget.clear()
            new_table_widget.setRowCount(0)
            new_table_widget.setColumnCount(0)

            # 获取起始和结束的行和列索引
            name_start_row = int(name_start_int_row) - 1
            name_end_row = int(name_end_int_row) - 1
            name_start_col = int(name_start_int_col) - 1
            name_end_col = int(name_end_int_col) - 1

            xuehao_start_row = int(xuehao_start_int_row) - 1
            xuehao_end_row = int(xuehao_end_int_row) - 1
            xuehao_start_col = int(xuehao_start_int_col) - 1
            xuehao_end_col = int(xuehao_end_int_col) - 1

            score_start_row = int(score_start_int_row) - 1
            score_end_row = int(score_end_int_row) - 1
            score_start_col = int(score_start_int_col) - 1
            score_end_col = int(score_end_int_col) - 1

            # 确保索引在有效范围内
            print(f"name_start_row:{name_start_row},name_end_row:{name_end_row}")
            print(f"name_start_col:{name_start_col},name_end_col:{name_end_col}")
            print(f"xuehao_start_row:{xuehao_start_row},xuehao_end_row:{xuehao_end_row}")
            print(f"xuehao_start_col:{xuehao_start_col},xuehao_end_col:{xuehao_end_col}")
            print(f"score_start_row:{score_start_row},score_end_row:{score_end_row}")
            print(f"score_start_col:{score_start_col},score_end_col:{score_end_col}")

            # 计算 new_table_widget 的行数和列数
            new_row_count = max(name_end_row - name_start_row + 1,
                                xuehao_end_row - xuehao_start_row + 1,
                                score_end_row - score_start_row + 1)
            new_col_count = 3  # 有三列：姓名、学号、分数

            # 设置 new_table_widget 的行数和列数
            new_table_widget.setRowCount(new_row_count)
            new_table_widget.setColumnCount(new_col_count)

            # 设置列标题
            new_table_widget.setHorizontalHeaderLabels(["姓名", "学号", "分数"])  # 复制数据到 new_table_widget
            for i in range(new_row_count):
                # 复制姓名
                if name_start_row + i <= name_end_row:
                    item = table_widget.item(name_start_row + i, name_start_col)
                    if item:
                        new_table_widget.setItem(i, 0, QTableWidgetItem(item.text()))

                # 复制学号
                if xuehao_start_row + i <= xuehao_end_row:
                    item = table_widget.item(xuehao_start_row + i, xuehao_start_col)
                    if item:
                        new_table_widget.setItem(i, 1, QTableWidgetItem(item.text()))

                # 复制分数
                if score_start_row + i <= score_end_row:
                    item = table_widget.item(score_start_row + i, score_start_col)
                    if item:
                        new_table_widget.setItem(i, 2, QTableWidgetItem(item.text()))

            show_message(1, "自定义", "数据复制成功", "ic_fluent_emoji_edit_filled")
        else:
            new_table_widget.clear()
            new_table_widget.setRowCount(table_widget.rowCount())
            new_table_widget.setColumnCount(3)
            new_table_widget.setHorizontalHeaderLabels(["姓名", "学号", "分数"])
            # 第5列是姓名
            for i in range(8, table_widget.rowCount()):
                item = table_widget.item(i, 4)
                if item:
                    new_table_widget.setItem(i - 8, 0, QTableWidgetItem(item.text()))
            # 第6列是学号
            for i in range(8, table_widget.rowCount()):
                item = table_widget.item(i, 5)
                if item:
                    new_table_widget.setItem(i - 8, 1, QTableWidgetItem(item.text()))
            # 第7列是分数
            for i in range(8, table_widget.rowCount()):
                item = table_widget.item(i, 6)
                if item:
                    new_table_widget.setItem(i - 8, 2, QTableWidgetItem(item.text()))

        for i in range(new_table_widget.rowCount() - 1, -1, -1):
            if (new_table_widget.item(i, 0) is None and
                    new_table_widget.item(i, 1) is None and
                    new_table_widget.item(i, 2) is None):

                new_table_widget.removeRow(i)

        save_table_data_to_json(new_table_widget)

        show_message(1, "默认数据", "数据复制成功", "ic_fluent_emoji_edit_filled")
    except Exception as e:
        show_message(3, "默认数据", f"数据复制失败{e}", "ic_fluent_emoji_edit_filled")
def save_table_data_to_json(table_widget):
    """
    保存表格中的数据到json
    :param table_widget: 表格
    :return: None
    """
    data_list = []
    unique_ids = set()
    to_remove = []

    # 获取表格数据
    widget = table_widget
    row_count = widget.rowCount()
    names = [widget.item(i, 0).text() if widget.item(i, 0) else None for i in
             range(row_count)]
    xuehaos = [widget.item(i, 1).text() if widget.item(i, 1) else None for i in
               range(row_count)]
    scores = [widget.item(i, 2).text() if widget.item(i, 2) else None for i in
              range(row_count)]

    # 构建数据列表
    for name, xuehao, score in zip(names, xuehaos, scores):
        if name is not None and xuehao is not None and score is not None:
            data = {
                "unique_id": names.index(name),
                "name": name,
                "stu_id": xuehao,
                "score": score
            }
            data_list.append(data)

    # 检查重复项并处理
    for data in data_list:
        if data['unique_id'] in unique_ids:
            if Settings.duplicate_filter:
                to_remove.append(data)
                widget.removeRow(data_list.index(data))
                show_message(1, "提示", f"已删除重复项: {data}", "ic_fluent_search_filled")
            else:
                pass

        else:
            unique_ids.add(data['unique_id'])

    # 统计数据中所有数据的个数
    Logger.info(f"数据中包含 {len(data_list)} 个数据")
    show_message(1, "提示", f"数据中包含 {len(data_list)} 个数据", "ic_fluent_task_list_ltr_filled")

    # 删除重复项
    for data in to_remove:
        data_list.remove(data)
        Logger.info(f"已删除: {data}")

    # 重新为数据列表中的内容生成唯一编号
    for idx, data in enumerate(data_list):
        data['unique_id'] = idx

    # 保存数据到 JSON 文件
    Logger.info(f"数据已保存到 {file_path}")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)

    Logger.info("数据已保存")

def read_json_data() ->list:
    """
    从指定的JSON文件中读取数据并返回一个列表
    :return: 包含JSON数据的列表
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        Logger.error(f"文件未找到: {file_path}")
        return []
    except json.JSONDecodeError:
        Logger.error(f"JSON解码错误: {file_path}")
        return []

def get_data_by_order(data, order) -> list:
    """
    根据指定的order值筛选数据
    :param data: 包含JSON数据的列表
    :param order: 要筛选的order值
    :return: 筛选出的数据列表
    """
    filtered_data = [item for item in data if item.get('unique_id') == order]
    return filtered_data

def del_data_for_new_table(new_table_widget):
    """
    删除选中的当前行数据，可以多选删除
    """
    selected_rows = new_table_widget.selectionModel().selectedRows()
    if not selected_rows:
        show_message(3, "提示", "没有选中任何行", "ic_fluent_task_list_ltr_filled")
        return

    for row in sorted(selected_rows, reverse=True):
        new_table_widget.removeRow(row.row())
        Logger.info(f"已删除: {row.row()}")

    # 使用最后一个删除的行来显示消息
    last_deleted_row = selected_rows[-1]
    show_message(3, "提示", f"已删除: {last_deleted_row.row() + 1}", "ic_fluent_task_list_ltr_filled")
    save_table_data_to_json(new_table_widget)
def insert_data_for_new_table(new_table_widget,  # 新表格对象
                              data1_input,  # 数据输入框对象1
                              data2_input,  # 数据输入框对象2
                              data3_input):  # 数据输入框对象3
    """
    将数据插入到新表格中
    """

    name = data1_input.text()
    xuehao = data2_input.text()
    score = data3_input.text()
    # 插入到新表格中
    new_table_widget.insertRow(new_table_widget.rowCount())
    new_table_widget.setItem(new_table_widget.rowCount() - 1, 0, QTableWidgetItem(name))
    new_table_widget.setItem(new_table_widget.rowCount() - 1, 1, QTableWidgetItem(xuehao))
    new_table_widget.setItem(new_table_widget.rowCount() - 1, 2, QTableWidgetItem(score))
    show_message(1, "提示", f"已添加: {name}, {xuehao}, {score}", "ic_fluent_task_list_ltr_filled")
    save_table_data_to_json(new_table_widget)

def import_file_for_table_widget(table_widget):
    file_path = QFileDialog.getOpenFileName(table_widget, "选择文件", "", "Excel Files (*.xlsx)")[0]
    if file_path:
        load_data_for_table_widget(table_widget,file_path)
        show_message(2, "成功", "表格数据已导入", "ic_fluent_emoji_meme_filled")

def load_data_for_table_widget(table_widget, file_path):
    try:
        workbook = load_workbook(file_path)
        sheet = workbook.active
        rows = sheet.max_row
        cols = sheet.max_column

        table_widget.setRowCount(rows)
        table_widget.setColumnCount(cols)
        for row in range(rows):
            for col in range(cols):
                cell_value = sheet.cell(row=row + 1, column=col + 1).value
                item = QTableWidgetItem(str(cell_value))
                table_widget.setItem(row, col, item)
    except Exception as e:
        Logger.info(f"load_data_for_table_widget:{e}")
def delete_data_for_table_widget(table_widget, new_table_widget):
    table_widget.clear()
    table_widget.setRowCount(0)
    table_widget.setColumnCount(0)
    new_table_widget.clear()
    new_table_widget.setRowCount(0)
    new_table_widget.setColumnCount(0)

    show_message(2, "成功", "表格数据已清空", "ic_fluent_eraser_medium_filled")