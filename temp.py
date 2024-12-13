import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDesktopWidget, QApplication
from siui.components import SiLineEditWithItemName, SiOptionCardPlane, SiDenseHContainer, SiPushButton
from siui.components.button import SiSwitchRefactor
from siui.components.combobox import SiComboBox
from siui.components.page import SiPage
from siui.components.titled_widget_group import SiTitledWidgetGroup
from siui.components.widgets import (
    SiLabel,
)
from siui.core import Si, SiColor, SiGlobal
from siui.templates.application.application import SiliconApplication


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
        self.setVisible(True)
        self.update()

    #
    # class testLabel(QLabel):
    #     def __init__(self, parent, text):
    #         super().__init__(parent)
    #         # self.setAlignment(Qt.AlignCenter)
    #         self.setFixedHeight(32)
    #         self.setText(text)
    #         self.setVisible(True)
    #         self.update()

    def reloadStyleSheet(self):
        self.setStyleSheet(f"color: {self.getColor(SiColor.TEXT_B)};")
        # f"background-color: {self.getColor(SiColor.INTERFACE_BG_D)}")


class Autoexcal(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # -------------------------------start------------------------------------- #
        self.setPadding(64)
        self.setScrollMaximumWidth(1000)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("AUTOEXCAL")
        # 创建控件组
        self.titled_widgets_group = SiTitledWidgetGroup(self)
        self.titled_widgets_group.setSiliconWidgetFlag(Si.EnableAnimationSignals)
        # -------------------------------const------------------------------------- #
        self.info_labels = []
        # -------------------------------widget------------------------------------ #
        self.setup_rules_groups()
        # -------------------------------finish------------------------------------ #
        SiGlobal.siui.reloadStyleSheetRecursively(self)
        # 添加页脚的空白以增加美观性
        self.titled_widgets_group.addPlaceholder(64)
        # 设置控件组为页面对象
        self.setAttachment(self.titled_widgets_group)

    def setup_rules_groups(self):
        rule_card_plane = SiOptionCardPlane(self)  # 创建选项卡
        rule_card_plane.setTitle("自定义规则")

        def add_rule_card_plane_body_widget():
            # 获取下拉框与具名输入框中的数据
            info_label = Label(self,
                               f"{self.get_data_for_combox}添加到-->{self.get_ele_name_for_combox}的{self.ele_name_input.getText()}元素")
            print(info_label)  # 打印正常
            info_label.setVisible(True)  # 确保可视，似乎没什么用
            rule_card_plane.body().addWidget(info_label)  # 添加
            rule_card_plane.body().adjustSize()  # 更新控件大小
            rule_card_plane.body().update()
            rule_card_plane.adjustSize()
            self.info_labels.append(info_label)  # 存储标签引用
            group.adjustSize()  # 更新控件组大小
            group.update()
        def remove_rule_card_plane_body_widget():
            if self.info_labels:
                label_to_remove = self.info_labels.pop()  # 获取并移除最后一个标签
                rule_card_plane.body().removeWidget(label_to_remove)
                label_to_remove.deleteLater()  # 删除标签实例
                rule_card_plane.body().adjustSize()
                rule_card_plane.body().update()
                rule_card_plane.adjustSize()
                group.adjustSize()  # 更新控件组大小

        with self.titled_widgets_group as group:
            group.addTitle("规则")
            self.rule_card_plane_h = SiDenseHContainer(self)

            self.custom_rule_tu = SiSwitchRefactor(self)
            self.custom_rule_tu.toggled.connect(lambda: rule_card_plane.body().setEnabled(False))
            self.custom_rule_tu.toggled.connect(lambda: rule_card_plane.footer().setEnabled(False))

            self.choose_data_flu = SiComboBox(self)
            self.choose_data_flu.resize(128, 32)
            self.choose_data_flu.addOption("数据1", value="数据1")
            self.choose_data_flu.addOption("数据2", value="数据2")
            self.choose_data_flu.addOption("数据3", value="数据3")
            self.choose_data_flu.menu().setShowIcon(False)
            self.choose_data_flu.menu().setIndex(0)
            self.choose_data_flu.menu().valueChanged.connect(self.get_ele_name_for_combox)

            self.choose_ele = SiComboBox(self)
            self.choose_ele.resize(128, 32)
            self.choose_ele.addOption("@id=", value="@id=")
            self.choose_ele.addOption("@tag()=", value="@tag()=")
            self.choose_ele.addOption("@text()=", value="@text()=")
            self.choose_ele.menu().setShowIcon(False)
            self.choose_ele.menu().setIndex(0)
            self.choose_data_flu.menu().valueChanged.connect(self.get_data_for_combox)

            self.ele_name_input = SiLineEditWithItemName(self)
            self.ele_name_input.setName("元素名称")
            self.ele_name_input.lineEdit().setText("txtpoint")
            self.ele_name_input.resize(350, 32)

            self.addrule_btu = SiPushButton(self)
            self.addrule_btu.attachment().setText("添加规则")
            self.addrule_btu.setFixedSize(128, 32)
            self.addrule_btu.clicked.connect(add_rule_card_plane_body_widget)

            self.remove_rule_btu = SiPushButton(self)
            self.remove_rule_btu.attachment().setText("删除规则")
            self.remove_rule_btu.setFixedSize(128, 32)
            self.remove_rule_btu.clicked.connect(remove_rule_card_plane_body_widget)

            self.rule_card_plane_h.addWidget(self.choose_data_flu)
            self.rule_card_plane_h.addWidget(Label(self, "定义到---->"))
            self.rule_card_plane_h.addWidget(self.choose_ele)
            self.rule_card_plane_h.addWidget(self.ele_name_input)

            info_ = Label(self, "元素默认后缀自增")

            rule_card_plane.header().addWidget(self.custom_rule_tu, "right")
            rule_card_plane.body().addWidget(self.rule_card_plane_h)
            rule_card_plane.footer().addWidget(info_)
            rule_card_plane.footer().addWidget(self.addrule_btu, "right")
            rule_card_plane.footer().addWidget(self.remove_rule_btu, "right")
            rule_card_plane.footer().setFixedHeight(40)
            rule_card_plane.body().addPlaceholder(12)
            rule_card_plane.adjustSize()


            group.addWidget(rule_card_plane)

    def get_data_for_combox(self, data_name):  # 获取下拉框数据
        self.data_for_combox = data_name

    def get_ele_name_for_combox(self, data_name):  # 获取下拉框数据
        self.ele_name_for_combox = data_name


class MySiliconApp(SiliconApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        screen_geo = QDesktopWidget().screenGeometry()
        self.setMinimumSize(1024, 380)
        self.resize(1366, 916)
        self.move((screen_geo.width() - self.width()) // 2, (screen_geo.height() - self.height()) // 2)

        self.layerMain().addPage(Autoexcal(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_home_filled"),
                                 hint="test", side="top")
        self.layerMain().setPage(0)

        SiGlobal.siui.reloadAllWindowsStyleSheet()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MySiliconApp()
    window.show()
    sys.exit(app.exec_())
