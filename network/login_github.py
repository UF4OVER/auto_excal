import json
import os


import requests
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

from siui.components import SiSimpleButton, SiLabel, SiDenseVContainer, SiPixLabel, SiDenseHContainer
from siui.core import SiGlobal, SiColor, GlobalFont
from siui.gui import SiFont
from siui.templates.application.components.message.box import SiSideMessageBox

from network import download_png
import configparser

import config.CONFIG
PATH_CONFIG = config.CONFIG.CONFIG_PATH

# GitHub OAuth 应用的配置
CLIENT_ID = "Ov23liihJAbtWX6zyXr9"
CLIENT_SECRET = "22c66bfe6d83d341c787eadc5ca0a0218b3b6a75"
try:
    config = configparser.ConfigParser()
    config.read(PATH_CONFIG)
    if 'Login' not in config:
        raise ValueError("config.ini 中缺少 [Login] 部分")
    config = config["Login"]

    REDIRECT_URI = config["REDIRECT_URI"].strip('"').strip("'")
    AUTH_URL = config["AUTH_URL"].strip('"').strip("'")
    TOKEN_URL = config["TOKEN_URL"].strip('"').strip("'")
    USER_API_URL = config["USER_API_URL"].strip('"').strip("'")

    print(f"Redirect URI: {REDIRECT_URI}")
    print(f"Authorization URL: {AUTH_URL}")
    print(f"Token URL: {TOKEN_URL}")
    print(f"User API URL: {USER_API_URL}")
except Exception as e:
    raise ValueError("config.ini 配置文件错误")

# 全局变量存储授权码
auth_code = None


def send_custom_message(type_, png_path: str, name: str, url :str, auto_close_duration=5000):
    fold_after = auto_close_duration
    container = SiDenseHContainer()
    container.setAdjustWidgetsSize(True)
    container.setFixedHeight(80)
    container.setSpacing(0)

    info_label = SiLabel()
    info_label.setFont(SiFont.tokenized(GlobalFont.S_NORMAL))
    info_label.setStyleSheet(f"color: {info_label.getColor(SiColor.TEXT_D)}; padding-left: 16px")
    info_label.setText("以下账号已成功登录")
    info_label.adjustSize()

    split_line = SiLabel()
    split_line.resize(300, 1)
    split_line.setFixedStyleSheet("margin-left: 20px")
    split_line.setColor(SiColor.trans(split_line.getColor(SiColor.TEXT_D), 0.3))

    avatar = SiPixLabel(container)
    avatar.resize(80, 80)
    avatar.setBorderRadius(40)
    avatar.load(png_path)

    container_v = SiDenseVContainer(container)
    container_v.setFixedWidth(200)
    container_v.setSpacing(0)

    name_label = SiLabel()
    name_label.setFont(SiFont.tokenized(GlobalFont.M_BOLD))
    name_label.setStyleSheet(f"color: {name_label.getColor(SiColor.TEXT_B)}; padding-left:8px")
    name_label.setText(f"{name}")
    name_label.adjustSize()

    button_1 = SiSimpleButton()
    button_1.setFixedHeight(22)
    button_1.attachment().setText("打开我的主页")
    button_1.colorGroup().assign(SiColor.TEXT_B, button_1.getColor(SiColor.TITLE_INDICATOR))
    button_1.adjustSize()
    button_1.reloadStyleSheet()
    button_1.clicked.connect(lambda: webbrowser.open(url))

    button_2 = SiSimpleButton()
    button_2.setFixedHeight(22)
    button_2.attachment().setText("退出应用")
    button_2.colorGroup().assign(SiColor.TEXT_B, button_2.getColor(SiColor.TITLE_INDICATOR))
    button_2.adjustSize()
    button_2.reloadStyleSheet()
    button_2.clicked.connect(lambda: SiGlobal.siui.windows["MAIN_WINDOW"].close())

    container_v.addWidget(name_label)
    container_v.addPlaceholder(8)
    container_v.addWidget(button_1)
    container_v.addWidget(button_2)
    container_v.adjustSize()

    container.addPlaceholder(24)
    container.addWidget(avatar)
    container.addPlaceholder(8)
    container.addWidget(container_v)
    container.adjustSize()

    new_message_box = SiSideMessageBox()
    new_message_box.setMessageType(type_)
    new_message_box.content().container().setSpacing(0)
    new_message_box.content().container().addPlaceholder(16)
    new_message_box.content().container().addWidget(info_label)
    new_message_box.content().container().addPlaceholder(8)
    new_message_box.content().container().addWidget(split_line)
    new_message_box.content().container().addPlaceholder(24)
    new_message_box.content().container().addWidget(container)
    new_message_box.content().container().addPlaceholder(32)
    new_message_box.adjustSize()

    new_message_box.setFoldAfter(fold_after)

    SiGlobal.siui.windows["MAIN_WINDOW"].LayerRightMessageSidebar().sendMessageBox(new_message_box)


def show_message(_type:int,title: str, text: str, icon: str):
    SiGlobal.siui.windows["MAIN_WINDOW"].LayerRightMessageSidebar().send(
        title=title,
        text=text,
        msg_type=_type,
        icon=SiGlobal.siui.iconpack.get(f"{icon}"),
        fold_after=5000)


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


def main():
    global auth_code
    try:
        # 1. 构建 GitHub 授权 URL
        auth_url = AUTH_URL+'?client_id='+CLIENT_ID+'&redirect_uri='+REDIRECT_URI+'&scope=user'
        print(auth_url)

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
            show_message(4,"Error", "错误：未收到授权码或登陆失败！！请重试", "ic_fluent_error_circle_regular")
            print(e)
            return False

        if not auth_code:
            show_message(4,"Error", "错误：未收到授权码或登陆失败！！请重试", "ic_fluent_error_circle_regular")
            print("错误：未收到授权码或登陆失败！！请重试")
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
            show_message(4,"Error", f"Error: {token_data.get('error_description')}", "ic_fluent_error_circle_regular")
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
            print("login scuss!!!!!!!!!!!!!!!!!!!!")
            # 将 user_data 保存为 JSON 文件
            base_dir = os.path.dirname(os.path.abspath(__file__))
            config_dir = os.path.join(os.path.dirname(base_dir), 'config')
            user_info_path = os.path.join(config_dir, 'user_info.json')
            user_info_path_copy = os.path.join(config_dir, 'copy_user_info.json')
            with open(user_info_path, 'w') as json_file:
                json.dump(user_data, json_file, indent=4)
            with open(user_info_path_copy, 'w') as json_file:
                json.dump(user_data, json_file, indent=4)
            try:
                download_png.download_png_for_pic()
                base_dir = os.path.dirname(os.path.abspath(__file__))
                png_dir = os.path.join(os.path.dirname(base_dir), 'pic')
                pic_path = os.path.join(png_dir, 'avatar.png')
                print(pic_path)
                send_custom_message(1, pic_path, user_data['login'], user_data['html_url'])
            except Exception as e:
                show_message(1,"成矣", "可关否？在启？", "ic_fluent_checkmark_filled")

                print(e)

            return True
        else:
            show_message(4,"Error", "错误：未收到授权码或登陆失败！！请重试", "ic_fluent_error_circle_regular")
            print(f"Error fetching user info: {user_response.text}")
            return False
    except Exception as E:
        show_message(4,"Error", "错误：未收到授权码或登陆失败！！请重试", "ic_fluent_error_circle_regular")
        print(E)
        return False


if __name__ == "__main__":
    # webbrowser.open('https://github.com/login/oauth/authorize?client_id=Ov23liihJAbtWX6zyXr9&redirect_uri=http://localhost:8080/callback&scope=user',new=2)
    main()