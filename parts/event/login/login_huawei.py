# -*- coding: utf-8 -*-
#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

import json
import os
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlencode, urlparse, parse_qs

import jwt
import requests
from PyQt5.QtCore import QThread, pyqtSignal

from parts.event.send_message import show_message
import config.CONFIG as F

# 使用环境变量来存储敏感信息
CLIENT_ID = os.getenv('HUWEI_CLIENT_ID', '113510305')
CLIENT_SECRET = os.getenv('HUWEI_CLIENT_SECRET', '4ed759edd6d080efbbac96bbaaf30cd82aa76575a34078274f4da961dcdcc3ae')
REDIRECT_URI = os.getenv('HUWEI_REDIRECT_URI', 'http://localhost:8080/callback')

AUTH_URL = "https://oauth-login.cloud.huawei.com/oauth2/v3/authorize"
TOKEN_URL = "https://oauth-login.cloud.huawei.com/oauth2/v3/token"
USER_API_URL = "https://account-sdk.cloud.huawei.com/v1/users/getUserInfo"

# 全局变量存储授权码
auth_code = None


class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        if self.path.startswith("/callback"):
            query = urlparse(self.path).query
            params = parse_qs(query)
            # parse_qs 返回的值为列表，所以取第一个值
            auth_code = params.get("code", [None])[0]
            print(f"Received authorization code: {auth_code}")
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # 从 HTML 文件中读取内容并写入响应
            html_path = os.path.join(F.HTML_PATH, "auth_success.html")
            with open(html_path, 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            html_path = os.path.join(F.HTML_PATH, "auth_failed.html")
            with open(html_path, 'rb') as file:
                self.wfile.write(file.read())


def generate_auth_url():
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': 'openid profile email'  # 添加所需的 scope
    }
    auth_url = f"{AUTH_URL}?{urlencode(params)}"
    return auth_url


def main():
    global auth_code
    try:
        # 1. 构建授权 URL
        auth_url = generate_auth_url()

        # 2. 打开默认浏览器跳转到授权页面
        print(f"Opening authorization page: {auth_url}")
        webbrowser.open(auth_url)

        # 3. 创建 HTTP 服务器以捕获回调
        server = HTTPServer(("localhost", 8080), OAuthHandler)
        server.socket.settimeout(60)
        print("Waiting for authorization response...")
        try:
            server.handle_request()
            server.server_close()
        except Exception as e:
            show_message(4, "Error", "错误：未收到授权码或登陆失败！！请重试", "ic_fluent_error_circle_regular")
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
                "grant_type": "authorization_code",
                "code": auth_code,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
            },
        )
        token_data = token_response.json()
        if "id_token" in token_data:
            id_token = token_data["id_token"]
            try:
                decoded_id_token = jwt.decode(id_token, options={"verify_signature": False})
                print(f"Decoded ID Token: {decoded_id_token}")

                user_info_path = os.path.join(F.USER_INFO_PATH, 'user_info.json')
                with open(user_info_path, 'w') as json_file:
                    json.dump(decoded_id_token, json_file, indent=4)

                # 提取 picture URL
                picture_url = decoded_id_token.get('picture')
                if picture_url:
                    print(f"Picture URL: {picture_url}")
                    picture_response = requests.get(picture_url)
                    picture_response.raise_for_status()
                    picture_path = os.path.join(F.PNG_PATH, 'avatar.png')
                    with open(picture_path, 'wb') as picture_file:
                        picture_file.write(picture_response.content)
                    print(f"Picture saved to: {picture_path}")
                else:
                    print("No picture URL found in ID token")
            except jwt.ExpiredSignatureError:
                show_message(4, "Error", "ID Token 已过期", "ic_fluent_error_circle_regular")
                print("ID Token 已过期")
                return False
            except jwt.InvalidTokenError:
                show_message(4, "Error", "无效的 ID Token", "ic_fluent_error_circle_regular")
                print("无效的 ID Token")
                return False
        else:
            show_message(4, "Error", "错误：未收到授权码或登陆失败！！请重试", "ic_fluent_error_circle_regular")
            return False

        return True

    except Exception as E:
        show_message(4, "Error", "错误：未收到授权码或登陆失败！！请重试", "ic_fluent_error_circle_regular")
        print(E)
        return False


if __name__ == "__main__":
    # 如果单独运行，直接调用 main() 测试流程
    main()
