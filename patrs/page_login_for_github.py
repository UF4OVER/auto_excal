import os

from PyQt5.QtCore import Qt

from siui.components import SiPixLabel
from siui.components.button import SiPushButtonRefactor, SiFlatButton
from siui.components.option_card import SiOptionCardLinear, SiOptionCardPlane
from siui.components.page import SiPage
from siui.components.titled_widget_group import SiTitledWidgetGroup
from siui.components.widgets import (
    SiDenseHContainer, SiDenseVContainer, SiLabel, )
from siui.core import Si, SiColor, SiGlobal
from network.load_user_info import load_user_info
from network import login_github

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(BASE_PATH)
user_info_path = os.path.join(project_root, 'config', 'user_info.json')

try:
    if os.path.exists(user_info_path):
        USER_INFO = load_user_info(1)

    else:
        USER_INFO = load_user_info(0)

except Exception as e:
    USER_INFO = load_user_info(0)
    print(e)
print(USER_INFO.ini())


class Label(SiLabel):
    def __init__(self, parent, text):
        super().__init__(parent)

        self.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(32)

        # self.setFixedStyleSheet("border-radius: 4px")
        self.setText(text)
        self.adjustSize()
        self.resize(self.width() + 24, self.height())

    def reloadStyleSheet(self):
        self.setStyleSheet(f"color: {self.getColor(SiColor.TEXT_B)};")
        # f"background-color: {self.getColor(SiColor.INTERFACE_BG_D)}")


class login_for_github(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPadding(64)
        self.setScrollMaximumWidth(1000)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("个人信息")

        # 创建控件组
        self.titled_widgets_group = SiTitledWidgetGroup(self)
        self.titled_widgets_group.setSiliconWidgetFlag(Si.EnableAnimationSignals)
        if USER_INFO.ini() == 0:
            self.setup_login_groups(True)
        else:
            self.setup_user_groups()
        self.update()
        # self.titled_widgets_group.show()
        self.titled_widgets_group.addPlaceholder(64)
        # 设置控件组为页面对象
        self.setAttachment(self.titled_widgets_group)

    def login_page(self):
        if login_github.main():
            self.setup_login_groups(False)  # 登录成功后移除登录页面
            self.setup_user_groups()
            self.titled_widgets_group.update()

        else:
            self.setup_login_groups(True)
            self.titled_widgets_group.update()
        self.titled_widgets_group.update()
        self.update()

    def setup_login_groups(self, bool_):
        """
        根据传递的bool值判断添加或者移除窗口
        :param bool_: 如果为 True，则添加登录窗口；如果为 False，则移除登录窗口
        :return:
        """
        with self.titled_widgets_group as group:
            if bool_:
                # 添加登录窗口
                self.login_top = SiOptionCardLinear(self)
                self.login_top.load(SiGlobal.siui.iconpack.get("ic_fluent_globe_star_regular"))

                self.login_top.adjustSize()
                self.login_top.setTitle("登录您的GitHub账号", "点击按钮来登录到github账户")
                login_btu = SiPushButtonRefactor(self)
                login_btu.setText("登录")
                login_btu.setFixedSize(120, 40)

                login_btu.clicked.connect(self.login_page)
                self.login_top.addWidget(login_btu)
                group.addWidget(self.login_top)
            else:
                # 移除登录窗口
                if hasattr(self, 'login_top') and self.login_top in group.widgets():
                    group.removeWidget(self.login_top)
                    self.login_top.deleteLater()  # 删除不再使用的部件以释放资源

    def setup_user_groups(self):
        with self.titled_widgets_group as group:
            user_pix = SiOptionCardPlane(self)
            user_pix.adjustSize()
            user_pix.setTitle("您的基本信息")
            user_pix.setFixedHeight(190)
            user_pix.header().setFixedHeight(70)
            user_pix.header().addPlaceholder(12)
            user_pix.body().setFixedHeight(110)
            user_pix.body().adjustSize()
            user_pix.footer().setFixedHeight(30)
            user_pix.footer().adjustSize()

            # 创建修改照片按钮
            change_pix_btu = SiFlatButton(self)
            change_pix_btu.setText("更换头像")

            # 创建用户信息标签
            pix_info_label = Label(self, "添加照片，个性化你的账户。")

            # 创建照片标签
            user_pix_png = SiPixLabel(self)
            user_pix_png.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
            user_pix_png.setFixedSize(80, 80)
            user_pix_png.setBorderRadius(40)
            user_pix_png.load(USER_INFO.get_user_png_path())
            # 用户名标签
            user_name_label = Label(self, "全名")
            user_name_label_1 = Label(self, USER_INFO.get_user_name())

            # 创建修改全名按钮
            charge_name_btu = SiFlatButton(self)
            charge_name_btu.setText("编辑名称")

            user_pix.body().addWidget(user_pix_png)
            user_pix.header().addWidget(pix_info_label, side="left")
            user_pix.header().addWidget(change_pix_btu, side="right")
            user_pix.footer().addWidget(user_name_label, side="left")
            user_pix.footer().addWidget(user_name_label_1, side="left")
            user_pix.footer().addWidget(charge_name_btu, side="right")

            group.addWidget(user_pix)

        with self.titled_widgets_group as group:
            group.addTitle("个人资料信息")
            user_info_card = SiOptionCardPlane(self)
            user_info_card.adjustSize()
            user_info_card.setFixedHeight(250)
            user_info_card.header().setFixedHeight(50)
            user_info_card.header().addPlaceholder(6)

            user_info_card.body().setFixedHeight(180)
            user_info_card.body().adjustSize()

            user_info_card.footer().setFixedHeight(30)
            user_info_card.footer().adjustSize()

            user_info_card.setTitle("您的个人资料信息")
            chargr_info_btu = SiFlatButton(self)
            chargr_info_btu.setText("编辑资料")

            commany_label = Label(self, "公司")
            nationality_label = Label(self, "国籍")
            language_label = Label(self, "语言")
            district_label = Label(self, "地区")
            # 创建三个垂直容器
            temp_vbox1 = SiDenseVContainer(self)
            temp_vbox1.setFixedWidth(150)
            temp_vbox1.addWidget(commany_label)
            temp_vbox1.addWidget(nationality_label)
            temp_vbox1.addWidget(language_label)
            temp_vbox1.addWidget(district_label)

            commany_label_1 = Label(self, USER_INFO.get_user_company())
            nationality_label_1 = Label(self, "中国")
            language_label_1 = Label(self, "中文（中国）")
            district_label_1 = Label(self, USER_INFO.get_user_location())

            temp_vbox2 = SiDenseVContainer(self)
            temp_vbox2.setFixedWidth(150)
            temp_vbox2.addWidget(commany_label_1)
            temp_vbox2.addWidget(nationality_label_1)
            temp_vbox2.addWidget(language_label_1)
            temp_vbox2.addWidget(district_label_1)

            commany_label_2 = Label(self, "您所在的公司或者学校")
            nationality_label_1 = Label(self, "您的国籍（中国不可更改）")
            language_label_1 = Label(self, "您使用的语言（中文不可更改）")
            district_label_1 = Label(self, "您所在的地区")

            temp_vbox3 = SiDenseVContainer(self)
            temp_vbox3.addWidget(commany_label_2)
            temp_vbox3.addWidget(nationality_label_1)
            temp_vbox3.addWidget(language_label_1)
            temp_vbox3.addWidget(district_label_1)

            temp_hbox = SiDenseHContainer(self)
            temp_hbox.addWidget(temp_vbox1)
            temp_hbox.addWidget(temp_vbox2)
            temp_hbox.addWidget(temp_vbox3)
            user_info_card.body().addWidget(temp_hbox)

            user_info_card.header().addWidget(chargr_info_btu, side="right")
            group.addWidget(user_info_card)

        with self.titled_widgets_group as group:
            group.addTitle("账户信息")
            account_card = SiOptionCardPlane(self)
            account_card.adjustSize()
            account_card.setFixedHeight(350)
            account_card.header().setFixedHeight(50)
            account_card.header().addPlaceholder(6)
            account_card.body().setFixedHeight(270)
            account_card.body().adjustSize()
            account_card.footer().setFixedHeight(30)
            account_card.footer().adjustSize()
            account_card.setTitle("您的账户信息")
            change_account_btu = SiFlatButton(self)
            change_account_btu.setText("编辑账户")
            account_email_label = Label(self, USER_INFO.get_user_email())
            account_email_label_1 = Label(self, "您的电子邮箱")
            account_login_label = Label(self, USER_INFO.get_user_login())
            account_login_label_1 = Label(self, "您的用户名")
            account_id_label = Label(self, USER_INFO.get_user_id())
            account_id_label_1 = Label(self, "您的用户编号")
            account_blog_label = Label(self, USER_INFO.get_user_blog())
            account_blog_label_1 = Label(self, "您的博客")
            account_bio_label = Label(self, "")
            account_bio_label_1 = Label(self, "您的个人简介")

            temp_vbox1 = SiDenseVContainer(self)
            temp_vbox1.setFixedWidth(150)
            temp_vbox1.addWidget(account_email_label)
            temp_vbox1.addWidget(account_login_label)
            temp_vbox1.addWidget(account_id_label)
            temp_vbox1.addWidget(account_blog_label)
            temp_vbox1.addWidget(account_bio_label)

            temp_vbox2 = SiDenseVContainer(self)
            temp_vbox2.setFixedWidth(150)
            temp_vbox2.addWidget(account_email_label_1)
            temp_vbox2.addWidget(account_login_label_1)
            temp_vbox2.addWidget(account_id_label_1)
            temp_vbox2.addWidget(account_blog_label_1)
            temp_vbox2.addWidget(account_bio_label_1)

            temp_vbox3 = SiDenseVContainer(self)

            account_email_label_2 = Label(self, "您的电子邮箱，不会用于隐私提取")
            account_login_label_2 = Label(self, "您的昵称，是您账户的昵称")
            account_id_label_2 = Label(self, "您的用户编号，唯一编号，不可更改")
            account_blog_label_2 = Label(self, "您的博客信息，若没有设置，为空")
            account_bio_label_2 = Label(self, "您的个人简介,设置为空，不可更改")

            temp_vbox3.addWidget(account_email_label_2)
            temp_vbox3.addWidget(account_login_label_2)
            temp_vbox3.addWidget(account_id_label_2)
            temp_vbox3.addWidget(account_blog_label_2)
            temp_vbox3.addWidget(account_bio_label_2)

            temp_hbox = SiDenseHContainer(self)

            temp_hbox.addWidget(temp_vbox2)
            temp_hbox.addWidget(temp_vbox1)
            temp_hbox.addWidget(temp_vbox3)

            account_card.body().addWidget(temp_hbox)
            account_card.header().addWidget(change_account_btu, side="right")
            group.addWidget(account_card)
