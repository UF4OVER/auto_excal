#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

import os

from PyQt5.QtCore import Qt, QUrl, QThread, pyqtSignal
from PyQt5.QtGui import QDesktopServices
from siui.components import (
    SiOptionCardLinear,
    SiOptionCardPlane,
    SiPixLabel,
    SiTitledWidgetGroup,
)
from siui.components.button import SiPushButtonRefactor
from siui.components.editbox import SiLineEdit
from siui.components.page import SiPage
from siui.components.widgets import (
    SiDenseVContainer,
    SiLabel,
    SiSimpleButton,
)
from siui.core import GlobalFont, Si, SiColor, SiGlobal, SiQuickEffect
from siui.gui import SiFont

import config.CONFIG as F
from parts.event.send_email import Email
from parts.event.send_message import show_message


class About(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPadding(64)
        self.setScrollMaximumWidth(950)
        self.setTitle("关于")

        self.titled_widget_group = SiTitledWidgetGroup(self)
        self.titled_widget_group.setSiliconWidgetFlag(Si.EnableAnimationSignals)

        version_picture_container = SiDenseVContainer(self)
        version_picture_container.setAlignment(Qt.AlignCenter)
        version_picture_container.setFixedHeight(128 + 48)
        SiQuickEffect.applyDropShadowOn(version_picture_container, color=(28, 25, 31, 255), blur_radius=48)

        self.version_picture = SiPixLabel(self)
        self.version_picture.setFixedSize(128, 128)
        self.version_picture.setBorderRadius(64)

        path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "pic", "avatar.png")
        print(path)
        self.version_picture.load(path)

        self.version_label = SiLabel(self)
        self.version_label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.version_label.setFont(SiFont.tokenized(GlobalFont.M_NORMAL))
        self.version_label.setStyleSheet(f"color: {self.getColor(SiColor.TEXT_D)}")
        self.version_label.setText("Wedding Invitation")

        version_picture_container.addWidget(self.version_picture)
        version_picture_container.addWidget(self.version_label)
        self.titled_widget_group.addWidget(version_picture_container)
        with self.titled_widget_group as group:
            group.addTitle("关于")
            self.about_me = SiOptionCardLinear(self)
            self.about_me.setTitle("关于我", "I am an ordinary person, now learning Python.")
            self.about_me.load(SiGlobal.siui.iconpack.get("ic_fluent_share_screen_person_overlay_filled"))

            self.about_me_btu = SiSimpleButton(self)
            self.about_me_btu.resize(32, 32)
            self.about_me_btu.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_open_regular"))
            self.about_me_btu.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/UF4OVER")))
            self.about_me.addWidget(self.about_me_btu)

            self.button_to_me_repo = SiSimpleButton(self)
            self.button_to_me_repo.resize(32, 32)
            self.button_to_me_repo.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_open_regular"))
            self.button_to_me_repo.clicked.connect(
                lambda: QDesktopServices.openUrl(QUrl("https://github.com/UF4OVER/auto_excal")))

            self.option_card_my_repo = SiOptionCardLinear(self)
            self.option_card_my_repo.setTitle("开源仓库", "在 GitHub 上查看 Wedding Invitation 的项目主页")
            self.option_card_my_repo.load(SiGlobal.siui.iconpack.get("ic_fluent_home_database_regular"))
            self.option_card_my_repo.addWidget(self.button_to_me_repo)

            group.addWidget(self.about_me)
            group.addWidget(self.option_card_my_repo)

        with self.titled_widget_group as group:
            group.addTitle("UI开源库")

            self.button_to_repo = SiSimpleButton(self)
            self.button_to_repo.resize(32, 32)
            self.button_to_repo.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_open_regular"))
            self.button_to_repo.clicked.connect(
                lambda: QDesktopServices.openUrl(QUrl("https://github.com/ChinaIceF/PyQt-SiliconUI")))

            self.option_card_repo = SiOptionCardLinear(self)
            self.option_card_repo.setTitle("开源仓库", "在 GitHub 上查看 Silicon UI 的项目主页")
            self.option_card_repo.load(SiGlobal.siui.iconpack.get("ic_fluent_home_database_regular"))
            self.option_card_repo.addWidget(self.button_to_repo)

            self.option_card_license = SiOptionCardLinear(self)
            self.option_card_license.setTitle("开源许可证", "Silicon UI遵循 GPLv3.0 许可证供非商业使用")
            self.option_card_license.load(SiGlobal.siui.iconpack.get("ic_fluent_certificate_regular"))

            group.addWidget(self.option_card_repo)
            group.addWidget(self.option_card_license)

        with self.titled_widget_group as group:
            group.addTitle("版权")

            self.option_card_copyright = SiOptionCardLinear(self)
            self.option_card_copyright.setTitle("版权声明", "PyQt-SiliconUI 版权所有 © 2024 by ChinaIceF")
            self.option_card_copyright.load(SiGlobal.siui.iconpack.get("ic_fluent_info_regular"))

            group.addWidget(self.option_card_copyright)

        with self.titled_widget_group as group:
            group.addTitle("第三方资源")

            self.option_card_icon_pack = SiOptionCardLinear(self)
            self.option_card_icon_pack.setTitle("Fluent UI 图标库",
                                                "本项目内置了 Fluent UI 图标库，Microsoft 公司保有这些图标的版权")
            self.option_card_icon_pack.load(SiGlobal.siui.iconpack.get("ic_fluent_diversity_regular"))

            group.addWidget(self.option_card_icon_pack)

        with self.titled_widget_group as group:
            group.addTitle("邮件")

            self.title_line_edit = SiLineEdit(self)
            self.title_line_edit.setFixedSize(800, 32)
            self.title_line_edit.setTitle("标题")

            self.subject_line_edit = SiLineEdit(self)
            self.subject_line_edit.setFixedSize(800, 32)
            self.subject_line_edit.setTitle("主题")

            self.content_line_edit = SiLineEdit(self)
            self.content_line_edit.setFixedSize(800, 96)
            self.content_line_edit.setTitle("内容")

            self.send_button = SiPushButtonRefactor(self)
            self.send_button.setFixedSize(128, 32)
            self.send_button.clicked.connect(self.send_email)
            self.send_button.setText("发送邮件")

            explain_label = SiLabel(self)
            explain_label.setText("向开发者提出修改意见")
            explain_label.setTextColor(self.getColor(SiColor.TEXT_B))

            self.email_options = SiOptionCardPlane(self)
            self.email_options.setTitle("发送邮件")
            self.email_options.header().addWidget(self.send_button, "right")
            self.email_options.body().addWidget(self.title_line_edit)
            self.email_options.body().addWidget(self.subject_line_edit)
            self.email_options.body().addWidget(self.content_line_edit)
            self.email_options.body().addPlaceholder(12)
            self.email_options.footer().addWidget(explain_label)
            self.email_options.footer().adjustSize()
            self.email_options.adjustSize()

            group.addWidget(self.email_options)

        self.titled_widget_group.addPlaceholder(64)
        self.setAttachment(self.titled_widget_group)

    def send_email(self):
        self.title = self.title_line_edit.text()
        self.subject = self.subject_line_edit.text()
        self.content = self.content_line_edit.text()

        if self.title == "" or self.subject == "" or self.content == "":
            show_message(2, "错误", "请填写完整信息", "ic_fluent_voicemail_filled")
            print("请填写完整信息")
            return
        if F.READ_CONFIG("Email", "email_send") == 'True':
            print("正在发送邮件...")
            email_thread = Send_Email(self.subject, self.title, self.content)

            email_thread.started.connect(self.start_progress_bar_circular)
            email_thread.finished.connect(self.stop_progress_bar_circular)

            email_thread.started.connect(
                lambda: show_message(3, "邮件", "正在发送邮件...", "ic_fluent_voicemail_filled"))
            email_thread.finished.connect(
                lambda: show_message(1, "邮件", "邮件发送成功！！！", "ic_fluent_voicemail_filled"))
            email_thread.error.connect(
                lambda e: show_message(2, "错误", f"邮件发送失败{e}！", "ic_fluent_voicemail_filled"))
            email_thread.finished.connect(self.write_email_today)
            email_thread.start()
            print("邮件发送成功！！！")
        else:
            show_message(2, "完啦", "一天只能发送一次邮件哦", "ic_fluent_comment_error_filled")
            print("一天只能发送一次邮件哦")

    def write_email_today(self):
        F.WRITE_CONFIG("Email", "email_send", "False")

    def start_progress_bar_circular(self):
        # 确保旧的按钮已经被完全删除
        if self.send_button:
            self.send_button.setText("发送中....")
            self.send_button.setDisabled(True)

    def stop_progress_bar_circular(self):
        # 确保旧的按钮已经被完全删除
        if self.send_button:
            self.send_button.setText("发送邮件")



class Send_Email(QThread):
    started = pyqtSignal()
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, subject, fromTitle, content):
        super().__init__()
        self.email = Email(False)
        self.fromTitle = fromTitle
        self.subject = subject
        self.content = content
        try:
            self.username = os.getlogin()
        except Exception as e:
            self.username = "unknown"

        self.html = f'''
        <div id="qm_con_body">
            <div id="mailContentContainer" onclick="getTop().previewContentImage(event, '')" onmousemove="getTop().contentImgMouseOver(event, '')" onmouseout="getTop().contentImgMouseOut(event, '')" class="qmbox qm_con_body_content qqmail_webmail_only" style="opacity: 1;">
                <meta charset="UTF-8">
                <meta http-equiv="Content-Language" content="zh-CN">
                <script>
                    document.addEventListener('DOMContentLoaded', function() {{
                getTop().handleScanContentImage('ZC0001_jJXN6lCMMrMurWcA3aa20f2');
                }})
                </script>
                <style>
                    .qmbox .container {{
                font-family: PingFangSC, PingFang SC,serif;
                        margin: 0 auto;
                        width: 600px;
                        height: auto;
                        background: #ffffff;
                    }}
        
                    .qmbox h3 {{
                font-size: 20px;
                        text-align: center;
                        margin-bottom: 20px;
                    }}
        
                    .qmbox header {{
                padding: 20px 0;
                        border-bottom: 1px solid #ff585f;
                    }}
        
                    .qmbox footer {{
                border-bottom: 1px solid #ff585f;
                    }}
        
                    .qmbox span{{
                color: #ff585f;
                    }}
        
                    .qmbox .mt20 {{
                margin-top: 20px;
                    }}
        
                    .qmbox p {{
                color: #000000;
                        font-weight: bold;
                        font-size: 14px;
                    }}
        
                    .qmbox .copyright p {{
                font-size: 12px;
                        color: #888888;
                        text-align: center;
                    }}
                </style>
                <div class="container">
                    <header>
                        <h1 style="color: #ff585f;">app应用的修改建议:{self.fromTitle}</h1>
                    </header>
                    <h3 class="mt20">开发者你好</h3>
                    <p>经过一段时间的使用，我对你的app应用有一些改进建议，希望能帮助提升用户体验。</p>
                    <h3>具体建议如下：</h3>
                    <ul>
                        <li>{self.content}</li>
                    </ul>
                    <p>以上是我的一些初步想法，期待与大家进一步讨论。</p>
                    <p>谢谢！</p>
                    <div class="signature" style="text-align: right; font-weight: bold;">{self.username}</div>
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
                    .qmbox meta {{
                display: none !important;
                    }}
                </style>
            </div>
        </div>
        '''

    def run(self):
        try:
            self.started.emit()
            self.email.setSubject(self.subject)
            self.email.setFromTitle(self.fromTitle)
            self.email.setContent(self.html)
            self.email.sendEmail()
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))
            show_message(1, "发送邮件失败", str(e), "ic_fluent_shield_error_regular")
