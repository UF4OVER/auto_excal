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
import base64
import config.CONFIG as F
import requests
import logging
from typing import Optional

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def get_rand_code(base64_img: str) -> Optional[str]:
    request_url = F.READ_CONFIG("ocr", "ocr_api_url")
    access_token = F.READ_CONFIG("ocr", "ocr_api_token")
    request_url = f"{request_url}?access_token={access_token}"
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    params = {"image": base64_img}

    try:
        response = requests.post(request_url, data=params, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
    except requests.exceptions.RequestException as e:
        logger.error(f"请求OCR API失败: {e}")
        return None

    response_json = response.json()
    logger.debug(f"OCR API响应: {response_json}")

    if 'words_result' not in response_json:
        logger.error("识别结果格式不正确")
        return None

    words_result = response_json['words_result']
    if not isinstance(words_result, list) or len(words_result) == 0:
        logger.error("识别结果格式不正确")
        return None

    for result in words_result:
        original_words = result.get('words', '')
        logger.debug(f"原始识别结果: {original_words}")

        # 过滤掉非数字字符
        filtered_words = ''.join(char for char in original_words if char.isdigit())
        logger.debug(f"过滤非数字识别结果: {filtered_words}")

        # 补全识别结果至4位
        if len(filtered_words) < 4:
            filtered_words += '0' * (4 - len(filtered_words))
            logger.debug(f"补全识别结果: {filtered_words}")

        return filtered_words

    logger.error("识别结果格式不正确")
    return None


if __name__ == '__main__':
    f = open('LogicVerifyCode.jpg', 'rb')
    img = base64.b64encode(f.read())
    get_rand_code(img)
