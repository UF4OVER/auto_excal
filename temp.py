import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDesktopWidget, QApplication, QVBoxLayout
from siui.components import SiLineEditWithItemName, SiDenseVContainer, SiOptionCardPlane, SiDenseHContainer, \
    SiSimpleButton, SiPixLabel
from siui.components.button import SiSwitchRefactor, SiPushButtonRefactor
from siui.components.option_card import SiOptionCardLinear
from siui.components.page import SiPage
from siui.components.spinbox.spinbox import SiIntSpinBox
from siui.components.titled_widget_group import SiTitledWidgetGroup
from siui.components.widgets import (
    SiLabel,
    SiLongPressButton,
)
from siui.core import Si, SiColor, SiGlobal, GlobalFont
from siui.gui import SiFont
from siui.templates.application.application import SiliconApplication
from siui.templates.application.components.message.box import SiSideMessageBox


def send_custom_message(type_, png_path: str, name: str, auto_close_duration=3000):
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

    button_2 = SiSimpleButton()
    button_2.setFixedHeight(22)
    button_2.attachment().setText("退出账号")
    button_2.colorGroup().assign(SiColor.TEXT_B, button_2.getColor(SiColor.TITLE_INDICATOR))
    button_2.adjustSize()
    button_2.reloadStyleSheet()

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
class Autoexcal(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPadding(64)
        self.setScrollMaximumWidth(1000)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("AUTOEXCAL")
        # 创建控件组
        self.titled_widgets_group = SiTitledWidgetGroup(self)
        self.titled_widgets_group.setSiliconWidgetFlag(Si.EnableAnimationSignals)


class MySiliconApp(SiliconApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        screen_geo = QDesktopWidget().screenGeometry()
        self.setMinimumSize(1024, 380)
        self.resize(1366, 916)
        self.move((screen_geo.width() - self.width()) // 2, (screen_geo.height() - self.height()) // 2)
        self.layerMain().setTitle("111")
        self.setWindowTitle("111")

        self.layerMain().addPage(Autoexcal(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_home_filled"),
                                 hint="test", side="top")
        self.layerMain().setPage(0)

        SiGlobal.siui.reloadAllWindowsStyleSheet()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MySiliconApp()
    window.show()
    png_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pic', 'avatar.jpg')
    print(png_dir)
    # E:\python\upper_computer\pic\avatar.jpg
    # E:\python\upper_computer\pic\avatar.png
    # send_custom_message(1, rf"{png_dir}", "user_data['login']")有问题
    send_custom_message(1, r"E:\python\upper_computer\pic\avatar.jpg","user_data['login']")
    # 路径必须是 r"E:\python\upper_computer\pic\avatar.jpg"格式

    sys.exit(app.exec_())
