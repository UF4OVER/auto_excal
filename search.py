# -*- coding: utf-8 -*-
# -------------------------------
#  @Project : PyQt-SiliconUI
#  @Time    : 2025 - 01-19 22:24
#  @FileName: search.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------


# 在指定的目录下搜索py文件中的指定文字


import os
import re
from tqdm import tqdm


def search_text_in_files(directory, search_text):
    # 遍历指定目录及其子目录中的所有文件
    for root, dirs, files in tqdm(os.walk(directory), desc="Searching directories"):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        # 使用正则表达式搜索指定文字
                        if re.search(search_text, content):
                            print(f'Found in {file_path}')
                except Exception as e:
                    print(f'Error reading {file_path}: {e}')


# 使用示例
directory_to_search = r'E:\python\PyQt-SiliconUI\siui'
text_to_search = 'Toast'
search_text_in_files(directory_to_search, text_to_search)
