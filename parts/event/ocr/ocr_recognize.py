# -*- coding: utf-8 -*-

#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

# -------------------------------
#  @Project : 11.py
#  @Time    : 2025 - 02-15 16:57
#  @FileName: ocr_recognize.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------

# encoding:utf-8

import requests
import base64

'''
手写文字识别
'''

# request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
# # 二进制方式打开图片文件



#
# params = {"image": img}
# access_token = '24.729fa8c3f778f790ea9bc2da30b5dd5e.2592000.1742201918.282335-117532117'
# request_url = request_url + "?access_token=" + access_token
# headers = {'content-type': 'application/x-www-form-urlencoded'}
# response = requests.post(request_url, data=params, headers=headers)
# if response:
#     print(response.json())


def get_rand_code(base64_img) -> str | None:
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/handwriting"
    params = {"image": base64_img}
    access_token = '24.729fa8c3f778f790ea9bc2da30b5dd5e.2592000.1742201918.282335-117532117'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print(response.json())
        a: dict = response.json()
        if 'words_result' in a:
            words_result = a['words_result']
            if isinstance(words_result, list) and len(words_result) > 0:
                for result in words_result:
                    print(f"识别结果：{result['words']}")
                    return result['words']
            else:
                print('识别结果格式不正确')
                return None
        else:
            print('识别失败')
            return None


if __name__ == '__main__':
    f = open('rand_code.gif', 'rb')
    img = base64.b64encode(f.read())
    get_rand_code(img)
