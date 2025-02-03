# -*- coding: utf-8 -*-

#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

# -------------------------------
#  @Project : zip.py
#  @Time    : 2025 - 02-03 10:06
#  @FileName: send_email.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 
# -------------------------------


import requests
from PyQt5.QtCore import pyqtSignal, QObject
import config.CONFIG as F
from event.send_message import show_message

PATH_CONFIG = F.CONFIG_PATH
print(PATH_CONFIG)


class Email(QObject):

    def __init__(self, isTEXT: bool = False):
        super().__init__()
        self.isTextContent = isTEXT
        self._data: dict = {
            "ColaKey": F.READ_CONFIG('Email', 'email_api_key'),
            "tomail": '3397499417@qq.com',
            "fromTitle": None,
            "subject": None,
            "smtpCode": F.READ_CONFIG("Email", "email_api_smtp_code"),
            "smtpEmail": F.READ_CONFIG("Email", "email_api_smtp_email"),
            "smtpCodeType": "163",
            "isTextContent": self.isTextContent,
            "content": None,
        }

    def setInitData(self):
        """
        初始化字符串
        :return:
        """
        self._data: dict = {
            "ColaKey": F.READ_CONFIG('Email', 'email_api_key'),
            "tomail": "3397499417@qq.com",
            "fromTitle": None,
            "subject": None,
            "smtpCode": F.READ_CONFIG("Email", "email_api_smtp_code"),
            "smtpEmail": F.READ_CONFIG("Email", "email_api_smtp_email"),
            "smtpCodeType": "163",
            "isTextContent": self.isTextContent,
            "content": None,
        }

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

    def sendEmail(self):
        """
        发送邮件
        :return:
        """
        _data = self._data
        # 发送 POST 请求
        try:
            # 检查响应
            response = requests.post(F.READ_CONFIG("Email", "email_api_url"), data=_data)
            if response.status_code == 200:
                print("邮件发送成功！")
            else:
                print(f"邮件发送失败: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"邮件发送失败: {e}")
            show_message(1, "发送邮件失败", str(e), "ic_fluent_shield_error_regular")



def Get_Data(self) -> dict:
        """

        :return: 返回要发送的字典
        """
        return self._data


if __name__ == '__main__':
    email = Email(False)
    email.setSubject("测试")
    email.setFromTitle("测试")
    email.setContent('''
        <div id="qm_con_body">
            <div id="mailContentContainer" onclick="getTop().previewContentImage(event, '')" onmousemove="getTop().contentImgMouseOver(event, '')" onmouseout="getTop().contentImgMouseOut(event, '')" class="qmbox qm_con_body_content qqmail_webmail_only" style="opacity: 1;">
                <meta charset="UTF-8">
                <meta http-equiv="Content-Language" content="zh-CN">
                <script>
                    document.addEventListener('DOMContentLoaded', function() {
                        getTop().handleScanContentImage('ZC0001_jJXN6lCMMrMurWcA3aa20f2');
                    })
                </script>
                <style>
                    /* 邮件内部图片支持调起预览。 */
                    img[image-inside-content='1'] {
                        cursor: pointer;
                    }
                </style>
                <style>
                    .qmbox .container {
                        font-family: PingFangSC, PingFang SC,serif;
                        margin: 0 auto;
                        width: 600px;
                        height: auto;
                        background: #ffffff;
                    }
        
                    .qmbox h3 {
                        font-size: 20px;
                        text-align: center;
                        margin-bottom: 20px;
                    }
        
                    .qmbox header {
                        padding: 20px 0;
                        border-bottom: 1px solid #ff585f;
                    }
        
                    .qmbox footer {
                        border-bottom: 1px solid #ff585f;
                    }
        
                    .qmbox span {
                        color: #ff585f;
                    }
        
                    .qmbox .mt20 {
                        margin-top: 20px;
                    }
        
                    .qmbox p {
                        color: #000000;
                        font-weight: bold;
                        font-size: 14px;
                    }
        
                    .qmbox .copyright p {
                        font-size: 12px;
                        color: #888888;
                        text-align: center;
                    }
                </style>
                <div class="container">
                    <header>
                        <h1 style="color: #ff585f;">app应用的修改建议</h1>
                    </header>
                    <h3 class="mt20">开发者你好</h3>
                    <p>经过一段时间的使用，我对你的app应用有一些改进建议，希望能帮助提升用户体验。</p>
                    <h3>具体建议如下：</h3>
                    <ul>
                        <li>优化加载速度：减少不必要的资源加载，提高应用的启动速度。</li>
                        <li>改进用户界面：简化操作流程，使界面更加直观易用。</li>
                        <li>增加功能模块：根据用户反馈，增加一些实用的功能模块。</li>
                        <li>增强安全性：加强数据保护措施，确保用户信息安全。</li>
                    </ul>
                    <p>以上是我的一些初步想法，期待与大家进一步讨论。</p>
                    <p>谢谢！</p>
                    <div class="signature" style="text-align: right; font-weight: bold;">尤金</div>
                    <footer class="mt20"></footer>
                    <div class="copyright mt20">
                        <p>感谢您选择 UF4OVER</p>
                        <p>如果您有任何疑问或建议，请随时与我联系</p>
                        <p>Copyright (c) 2025 UF4OVER，保留所有权利。</p>
                    </div>
                </div>
                <center>
                    <table width="100%" align="center" style="max-width:900px;margin:0 auto;width:100%;">
                        <tbody>
                        <tr align="center"></tr>
                        <tr align="center">
                            <td style="border-top:1px #e5e5e5 solid;padding-top:15px;padding-bottom:15px;" width="560">
                                <table border="0" cellspacing="0" cellpadding="0" align="center">
                                    <tbody>
                                    <tr>
                                        <td style="background-color:#ddd;border:1px #ddd solid;border-radius:4px;padding:3px 15px;text-align:center;"><a style="color:#a6a6a6;background:#ddd;font-size:12px;text-decoration:none;" href="https://track2.sendcloud.net/track/unsubscribe.do?p=eyJ1c2VyX2lkIjogMTA1ODU3LCAidGFza19pZCI6ICIiLCAiZW1haWxfaWQiOiAiMTczODM5ODgwNzIwNF8xMDU4NTdfMjUxMDBfMTkwNy5zZy0xMF8xXzI1M18yNi1pbmJvdW5kMCQzMzk3NDk5NDE3QHFxLmNvbSIsICJwYWdlX2lkIjogLTEsICJzaWduIjogIjdiZWMwNzc5MzFlYWIyNzRiYTBmODhiMjU1M2VmN2QyIiwgInVzZXJfaGVhZGVycyI6IHt9LCAibGFiZWwiOiAwLCAidHJhY2tfZG9tYWluIjogInRyYWNrMi5zZW5kY2xvdWQubmV0IiwgInJlYWxfdHlwZSI6ICIiLCAibmV0ZWFzZSI6ICJmYWxzZSIsICJvdXRfaXAiOiAiNDcuNzQuMTc5LjM1IiwgImNvbnRlbnRfdHlwZSI6ICIiLCAicmVjZWl2ZXIiOiAiMzM5NzQ5OTQxN0BxcS5jb20iLCAibWFpbGxpc3RfaWQiOiAwLCAib3ZlcnNlYXMiOiAiIiwgImNhdGVnb3J5X2lkIjogODAwOTk1LCAib3V0X3Bvb2xfaWQiOiA1NX0%3D" target="_blank" rel="noopener">click to unsubscribe</a></td>
                                    </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </center>
                <style type="text/css">
                    .qmbox style,
                    .qmbox script,
                    .qmbox head,
                    .qmbox link,
                    .qmbox meta {
                        display: none !important;
                    }
                </style>
            </div>
        </div>

    ''')
    email.sendEmail()