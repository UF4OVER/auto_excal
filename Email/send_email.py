import configparser

import requests
from PyQt5.QtCore import pyqtSignal, QObject

import config.CONFIG

PATH_CONFIG = config.CONFIG.CONFIG_PATH

print(PATH_CONFIG)


class Email(QObject):
    started = pyqtSignal()
    finished = pyqtSignal(str)

    def __init__(self, isTEXT: bool = False):
        super().__init__()
        self.isTextContent = isTEXT
        self.config = self.load_config()
        self._data: dict = {
            "ColaKey": self.config['EMAIL_API_KEY'],
            "tomail": None,
            "fromTitle": None,
            "subject": None,
            "smtpCode": self.config['EMAIL_API_SMTP_CODE'],
            "smtpEmail": self.config['EMAIL_API_SMTP_EMAIL'],
            "smtpCodeType": "163",
            "isTextContent": self.isTextContent,
            "content": None,
        }

    def load_config(self):
        config = configparser.ConfigParser()
        config.read(PATH_CONFIG)
        if 'Email' not in config:
            raise ValueError("config.ini 中缺少 [Email] 部分")
        return config['Email']

    def setInitData(self):
        """
        初始化字符串
        :return:
        """
        self._data: dict = {
            "ColaKey": self.config['EMAIL_API_KEY'],
            "tomail": None,
            "fromTitle": None,
            "subject": None,
            "smtpCode": self.config['EMAIL_API_SMTP_CODE'],
            "smtpEmail": self.config['EMAIL_API_SMTP_EMAIL'],
            "smtpCodeType": "163",
            "isTextContent": self.isTextContent,
            "content": None,
        }

    def setTextContent(self, isTextContent: bool):
        """
        修改是否显示纯文本，False 显示富文本
        :param isTextContent:
        :return:
        """
        if isinstance(isTextContent, bool):
            raise ValueError("isTextContent 必须是布尔值")
        self.isTextContent = isTextContent

    def setSubject(self, subject: str):
        """
        修改主题
        :param subject:
        :return:
        """
        if not isinstance(subject, str):
            raise ValueError("subject 必须是字符串")
        self._data["subject"] = subject

    def setFromTitle(self, title: str):
        """
        修改标题
        :param title:
        :return:
        """
        if not isinstance(title, str):
            raise ValueError("title 必须是字符串")
        self._data["fromTitle"] = title

    def setContent(self, content: str):
        """
        修改文本
        :param content:
        :return:
        """
        if not isinstance(content, str):
            raise ValueError("content 必须是字符串")
        self._data["content"] = content

    def setToEmail(self, toemail: str):
        """
        修改邮箱
        :param toemail:
        :return:
        """
        if not isinstance(toemail, str):
            raise ValueError("toemail 必须是字符串")
        self._data["tomail"] = toemail

    def setDate(self, data):
        """
        传入的data的格式是固定的
        :param data: {
         "tomail": str,
         "fromTitle": str,
         "subject": str,
          "content": str,
        }
        :return:
        """
        expected_keys = {"tomail", "fromTitle", "subject", "content"}

        if set(data.keys()) != expected_keys:
            raise ValueError(f"数据格式错误，预期的键为: {expected_keys}, 实际的键为: {set(data.keys())}")

        if data["tomail"] is None or data["fromTitle"] is None or data["subject"] is None or data["content"] is None:
            raise ValueError("存在数据为空")

        self._data.update(data)

    def setText(self, toemail: str, title: str, subject: str, content: str):
        """

        :param toemail: 到哪一个邮箱
        :param title: 标题
        :param subject: 主题
        :param content: 内容
        :return:
        """
        self._data.update({
            "tomail": toemail,
            "fromTitle": title,
            "subject": subject,
            "content": content,
        })

    def sendEmail(self):
        """
        发送邮件
        :return:
        """
        if self._data["tomail"] is None or self._data["fromTitle"] is None or self._data["subject"] is None or \
                self._data[
                    "content"] is None:
            raise ValueError("存在数据为空")
        _data = self._Data
        # 发送 POST 请求
        self.started.emit(True)
        try:
            # 检查响应
            response = requests.post(self.config['EMAIL_API_URL'], data=_data)
            if response.status_code == 200:
                print("邮件发送成功！")
                self.finished.emit("发送成功")
            else:
                print(f"邮件发送失败: {response.status_code}")
                print(response.text)
                self.finished.emit("发送失败")
        except Exception as e:
            print(f"邮件发送失败: {e}")
            self.finished.emit(f"发送失败\r\n{e}")

    def Data(self) -> dict:
        """

        :return: 返回要发送的字典
        """
        return self._data
