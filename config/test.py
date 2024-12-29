# -*- coding: utf-8 -*-
# -------------------------------
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

with open("data.json","r") as f:
    data_json = f.read()

data_list = json.loads(data_json)

def find_duplicates(data, field):
    """
    查找列表中指定字段的重复数据

    :param data: 列表，包含字典数据
    :param field: 字符串，要查找重复的字段名
    :return: 集合，包含所有重复的数据
    """
    seen = set()
    duplicates = set()
    for item in data:
        value = item.get(field)
        if value in seen:
            duplicates.add(value)
        else:
            seen.add(value)
    return duplicates

# 查找name字段的重复数据
name_duplicates = find_duplicates(data_list, 'name')
print("name字段重复的数据:", name_duplicates)

# 查找stu_id字段的重复数据
stu_id_duplicates = find_duplicates(data_list, 'stu_id')
print("stu_id字段重复的数据:", stu_id_duplicates)