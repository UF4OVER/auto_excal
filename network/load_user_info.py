import json
import os


class load_user_info:
    def __init__(self, _type):
        self._type = _type
        # 获取项目根目录
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.png_folder_path = os.path.join(project_root, 'pic')

        if self._type == 0:
            # 使用默认配置
            self.user_info = {
                "name": "默认",
                "Email": "默认",
                "login": "默认",
                "id": 10086,
                "company": "默认",
                "blog": "默认",
                "location": "中国",
                "bio": "默认",
            }
        else:
            path = os.path.join(project_root, 'config', 'user_info.json')
            with open(path, 'r') as f:
                self.user_info = json.load(f)
                # print(self.user_info)

    def ini(self):
        """
        初始化用户信息
        :return:
        """
        return self._type

    def get_user_name(self):
        """
        :return: 姓名
        """
        return self.user_info.get("name")

    def get_user_email(self):
        """
        :return: 邮箱
        """
        return str(self.user_info.get("Email"))

    def get_user_login(self):
        """
        :return: 登录昵称
        """
        return self.user_info.get("login")

    def get_user_id(self):
        """
        :return: id
        """
        return str(self.user_info.get("id"))

    def get_user_company(self):
        """
        :return: 公司
        """
        return self.user_info.get("company")

    def get_user_blog(self):
        """
        :return: 博客
        """
        return self.user_info.get("blog")

    def get_user_location(self):
        """
        :return: 位置
        """
        return self.user_info.get("location")

    def get_user_bio(self):
        """
        :return: 简介
        """
        return self.user_info.get("bio")

    def get_user_png_path(self):
        """
        如果有用户头像，则返回
        否则返回默认路径
        :return: 头像
        """
        avatar_path = os.path.join(self.png_folder_path, "avatar.png")
        default_path = os.path.join(self.png_folder_path, "default.jpg")

        if os.path.exists(avatar_path):
            return avatar_path
        else:
            return default_path


if __name__ == "__main__":
    print(load_user_info().get_user_png_path())
