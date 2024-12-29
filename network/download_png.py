import json
import os
import requests

# 使用绝对路径

base_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(base_dir, '..'))
png_folder_path = os.path.join(project_root, 'pic')
user_info_folder_path = os.path.join(project_root, 'config', 'user_info.json')


def get_png_urls() -> str:
    """
    获取用户配置文件中的头像的网址
    :return: 返回网址
    """
    try:
        with open(user_info_folder_path, "r") as f:
            content = f.read()
            print(json.loads(content).get("avatar_url"))
        return json.loads(content).get("avatar_url")
    except FileNotFoundError:
        print(f"Error: The file {user_info_folder_path} was not found.")
        return ""
    except json.JSONDecodeError:
        print(f"Error: The file {user_info_folder_path} is not a valid JSON file.")
        return ""


def download_png_for_pic(path=png_folder_path) -> None:
    """
    并发起请求，获得头像后保存到pic文件夹中
    若url为空，则不写入文件，其他函数中会判断是否存在用户头像
    有的话则返回用户头像，没有的话，返回默认头像路径
    :param path: 文件路径
    :param url: png_folder_path中获取用户配置信息中的头像网址
    :return: 不返回，直接写入图片
    """
    url = get_png_urls()
    if url == "" or url is None:
        print("没有找到头像的地址")
        return
    else:
        url = get_png_urls()
    # 构建完整的文件路径
    file_path = os.path.join(path, "avatar.png")
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {url} to {file_path}")
    else:
        print(f"Error downloading {url}: {response.status_code}")


if __name__ == "__main__":
    download_png_for_pic()
