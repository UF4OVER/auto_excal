import requests
import os
import json

# 获取API提供的仓库
base_dir = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(os.path.dirname(base_dir), 'config')

user_config_info_path = os.path.join(CONFIG_DIR, 'copy_user_info.json')

user_repo_info_login_path = os.path.join(CONFIG_DIR, 'user_repo_info_login.json')
user_repo_info_unlogin_path = os.path.join(CONFIG_DIR, 'user_repo_info_unlogin.json')


def get_repo_list():
    """
    获取用户配置信息的仓库地址API，发起请求并记录为json
    未成功则写入默认配置
    :return:
    """
    try:
        with open(user_config_info_path, "r") as f:
            try:
                content = json.load(f)["repos_url"]
                response = requests.get(content)
                response.raise_for_status()  # 检查请求是否成功
                repo_data = response.json()  # 提取JSON数据
                with open(user_repo_info_login_path, "w") as f:
                    json.dump(repo_data, f, indent=4)  # 写入成功时的JSON数据
            except requests.exceptions.RequestException as e:
                print(f"HTTP Request failed: {e}")
            except Exception as e:
                with open(user_repo_info_unlogin_path, "w") as f:
                    json.dump(repo_data, f, indent=4)  # 写入失败时的JSON数据
                print(f"Error: {e}")
    except FileNotFoundError:
        print("File not found.")


def get_repo_sum() -> int: return len(json.load(open(user_repo_info_login_path, "r"))) - 1


class load_github_repo:
    def __init__(self, num):
        self.number = num
        if self.number > get_repo_sum():
            self.number = 0
        with open(user_repo_info_login_path, "r") as f:
            self.repo_data = json.load(f)[self.number]

    def get_repo_name(self):
        return self.repo_data["name"]

    def get_repo_url(self):
        return self.repo_data["html_url"]

    def get_repo_description(self):
        return self.repo_data["description"]


def try_to_get_repo_list():
    try:
        get_repo_sum()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    REPO = load_github_repo(0)
    print(REPO.get_repo_url())
