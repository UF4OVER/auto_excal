# -*- coding: utf-8 -*-

#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

# -------------------------------
#  @Project : 11.py
#  @Time    : 2025 - 02-20 17:45
#  @FileName: login_baidu.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------


import json
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests

import config.CONFIG as F
from parts.event.send_message import show_message

PATH_CONFIG = F.CONFIG_PATH
HTML_PATH = F.HTML_PATH

# 百度 OAuth 应用的配置
CLIENT_ID = "Ov23liihJAbtWX6zyXr9"
CLIENT_SECRET = "22c66bfe6d83d341c787eadc5ca0a0218b3b6a75"

REDIRECT_URI = F.READ_CONFIG("login", "REDIRECT_URI")
AUTH_URL = F.READ_CONFIG("login", "AUTH_URL")
TOKEN_URL = F.READ_CONFIG("login", "TOKEN_URL")
USER_API_URL = F.READ_CONFIG("login", "USER_API_URL")

# 全局变量存储授权码
auth_code = None


class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code

        # 解析 URL 的查询参数
        if self.path.startswith("/callback"):
            query = self.path.split("?")[1]
            params = dict(qc.split("=") for qc in query.split("&"))

            # 提取授权码
            auth_code = params.get("code")
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # 从 HTML 文件中读取内容并写入响应
            html_path = HTML_PATH / "auth_success.html"
            with open(html_path, 'rb') as file:
                self.wfile.write(file.read())

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # 从 HTML 文件中读取内容并写入响应
            html_path = F.CONFIG_PATH / "auth_fail.html"
            with open(html_path, 'rb') as file:
                self.wfile.write(file.read())


def main():
    global auth_code
    try:
        # 1. 构建 GitHub 授权 URL
        auth_url = f"{AUTH_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=user"

        # 2. 打开默认浏览器，跳转到 GitHub 授权页面
        print(f"Opening GitHub login page: {auth_url}")
        webbrowser.open(auth_url)

        # 3. 创建一个 HTTP 服务器以捕获 GitHub 的回调
        server = HTTPServer(("localhost", 8080), OAuthHandler)
        server.socket.settimeout(10)
        print("Waiting for authorization response...")
        try:
            server.handle_request()
            server.server_close()
        except Exception as e:
            show_message(4, "Error", "错误，回调出错！！请重试", "ic_fluent_error_circle_regular")
            print(e)
            return False

        if not auth_code:
            show_message(4, "Error", "错误：未收到授权码！请重试", "ic_fluent_error_circle_regular")
            print("错误：未收到授权码！请重试")
            return False

        # 4. 用授权码交换访问令牌
        print("Exchanging authorization code for access token...")
        token_response = requests.post(
            TOKEN_URL,
            headers={"Accept": "application/json"},
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": auth_code,
                "redirect_uri": REDIRECT_URI,
            },
        )
        token_data = token_response.json()

        if "access_token" not in token_data:
            print(f"Error fetching access token: {token_data.get('error_description')}")
            show_message(4, "Error", f"Error: {token_data.get('error_description')}", "ic_fluent_error_circle_regular")
            return False

        access_token = token_data["access_token"]
        print(f"Access Token: {access_token}")

        # 5. 使用访问令牌获取用户信息
        print("Fetching user information...")
        user_response = requests.get(
            USER_API_URL, headers={"Authorization": f"Bearer {access_token}"}
        )
        user_data = user_response.json()

        if user_response.status_code == 200:
            print("登录成功")
            # 将 user_data 保存为 JSON 文件
            user_info_path = F.USER_INFO_PATH / "user_info.json"
            with open(user_info_path, 'w') as json_file:
                json.dump(user_data, json_file, indent=4)
            return True
        else:
            show_message(4, "Error", "错误：获取用户信息错误！请重试", "ic_fluent_error_circle_regular")
            print(f"Error fetching user info: {user_response.text}")
            return False
    except Exception as E:
        show_message(4, "Error", "错误：登陆失败！！请重试", "ic_fluent_error_circle_regular")
        print(E)
        return False



if __name__ == "__main__":
    print(CLIENT_ID)
