import requests


def get_file_content():
    url = "https://raw.githubusercontent.com/UF4OVER/auto_excal/siui/version"
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        content = response.text
        print("文件内容:")
        print(content)
        return content
    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}")
        return None


if __name__ == "__main__":
    get_file_content()
