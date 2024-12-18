# -*- coding: utf-8 -*-
# -------------------------------

#  @Project : upper_computer
#  @Time    : 2024 - 12-21 20:44
#  @FileName: email_test.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 3.10

# -------------------------------
from Email.send_email import Email


def p(df):
    print(f"执行了{df}")


e = Email(isTEXT=False)
e.setText("3397499417@qq.com", "标题", "主题", "内容")
e.start_signal.connect(lambda: p("开始发送"))
e.end_signal.connect(lambda b_: p(f"发送结果{b_}"))
# e.sendEmail()
print(e.Data())
