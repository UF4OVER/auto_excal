import json
import os
import threading
import requests
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

# GitHub OAuth 应用的配置
CLIENT_ID = "Ov23liihJAbtWX6zyXr9"
CLIENT_SECRET = "22c66bfe6d83d341c787eadc5ca0a0218b3b6a75"
REDIRECT_URI = "http://localhost:8080/callback"
AUTH_URL = "https://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"
USER_API_URL = "https://api.github.com/user"

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
            base_dir = os.path.dirname(os.path.abspath(__file__))
            config_dir = os.path.join(os.path.dirname(base_dir), 'config')
            html_path = os.path.join(config_dir, 'auth_success.html')
            with open(html_path, 'rb') as file:
                self.wfile.write(file.read())

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # 从 HTML 文件中读取内容并写入响应
            base_dir = os.path.dirname(os.path.abspath(__file__))
            config_dir = os.path.join(os.path.dirname(base_dir), 'config')
            html_path = os.path.join(config_dir, 'auth_failed.html')
            with open(html_path, 'rb') as file:
                self.wfile.write(file.read())


def main(callback=None):
    global auth_code

    # 1. 构建 GitHub 授权 URL
    auth_url = f"{AUTH_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=user"

    # 2. 打开默认浏览器，跳转到 GitHub 授权页面
    print(f"Opening GitHub login page: {auth_url}")
    webbrowser.open(auth_url)

    # 3. 创建一个 HTTP 服务器以捕获 GitHub 的回调
    server = HTTPServer(("localhost", 8080), OAuthHandler)
    print("Waiting for authorization response...")
    try:
        server.handle_request()
        server.server_close()
    except Exception as e:
        print(e)
        return False


    if not auth_code:
        print("Error: No authorization code received.")
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
        print("login on!!!!!!!!")
        # 将 user_data 保存为 JSON 文件
        base_dir = os.path.dirname(os.path.abspath(__file__))
        config_dir = os.path.join(os.path.dirname(base_dir), 'config')
        user_info_path = os.path.join(config_dir, 'user_info.json')
        user_info_path_copy = os.path.join(config_dir, 'copy_user_info.json')
        with open(user_info_path, 'w') as json_file:
            json.dump(user_data, json_file, indent=4)
        with open(user_info_path_copy, 'w') as json_file:
            json.dump(user_data, json_file, indent=4)


            # 设置事件
        if callback:
            callback()

        return True
    else:
        print(f"Error fetching user info: {user_response.text}")
        return False

if __name__ == "__main__":
    main()
