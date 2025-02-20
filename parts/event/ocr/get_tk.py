# -*- coding: utf-8 -*-

#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

# -------------------------------
#  @Project : 11.py
#  @Time    : 2025 - 02-20 17:55
#  @FileName: get_tk.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------

import requests
import json


def main():

    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=6Qa8DitF5RcX9hPVcSFheget&client_secret=VkzzzzGw6f8h1X4jygEIWiEDI9SUTrAl"

    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


if __name__ == '__main__':
    main()
