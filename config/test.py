# -*- coding: utf-8 -*-

#  Copyright (c) 2025. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

# -------------------------------
import configparser
import json


#  @Project : siui
#  @Time    : 2024 - 12-29 21:12
#  @FileName: test.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 3.10

# -------------------------------

# with open("data.json","r") as f:
#     data_json = f.read()
#
# data_list = json.loads(data_json)
#
# def find_duplicates(data, field):
#     """
#     查找列表中指定字段的重复数据
#
#     :param data: 列表，包含字典数据
#     :param field: 字符串，要查找重复的字段名
#     :return: 集合，包含所有重复的数据
#     """
#     seen = set()
#     duplicates = set()
#     for item in data:
#         value = item.get(field)
#         if value in seen:
#             duplicates.add(value)
#         else:
#             seen.add(value)
#     return duplicates
#
# # 查找name字段的重复数据
# name_duplicates = find_duplicates(data_list, 'name')
# print("name字段重复的数据:", name_duplicates)
#
# # 查找stu_id字段的重复数据
# stu_id_duplicates = find_duplicates(data_list, 'stu_id')
# print("stu_id字段重复的数据:", stu_id_duplicates)


# def read_to_json() -> list:
#     """
#     从指定的JSON文件中读取数据并返回一个列表
#     :return: 包含JSON数据的列表
#     """
#     file_path = "data.json"
#     try:
#         with open(file_path, 'r') as file:
#             data = json.load(file)
#             return data
#     except FileNotFoundError:
#         print(f"文件未找到: {file_path}")
#         return []
#     except json.JSONDecodeError:
#         print(f"JSON解码错误: {file_path}")
#         return []
#
# a = read_to_json()
# print(len(a))
import config.CONFIG

PATH_CONFIG = config.CONFIG.CONFIG_PATH

try:
    config = configparser.ConfigParser()
    config.read(PATH_CONFIG)
    if 'Broswer' not in config:
        raise ValueError("config.ini 中缺少 [Broswer] 部分")
    config = config["Broswer"]

    BROSWER_PATH = config["BROSWER_PATH"].strip('"').strip("'")
    BROSWER_PORT = int(config["BROSWER_PORT"].strip('"').strip("'"))
except Exception as e:
    print(e)
    print("config.ini 中缺少 [Broswer] 部分")


print(BROSWER_PATH)