# -*- coding: utf-8 -*-
#  Copyright (c) 2025 UF4OVER
#   All rights reserved.
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDesktopWidget, QApplication, QLabel
from siui.components import SiLineEditWithItemName, SiPushButton
from siui.components.container import SiTriSectionPanelCard, SiDenseContainer
from siui.components.button import SiSwitchRefactor
from siui.components.combobox import SiComboBox
from siui.components.page import SiPage
from siui.components.titled_widget_group import SiTitledWidgetGroup
from siui.components.widgets import (
    SiLabel,
)
from siui.core import Si, SiColor, SiGlobal
from siui.templates.application.application import SiliconApplication


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
        rule_card_plane = SiTriSectionPanelCard(self)  # 创建选项卡
        rule_card_plane.setTitle("自定义规则")

        def add_rule_card_plane_body_widget():
            info_label = QLabel("添加到-->的元素", self)
            self.info_labels.append(info_label)
            rule_card_plane.body().addWidget(info_label)
            rule_card_plane.adjustSize()
            group.adjustSize()

        def remove_rule_card_plane_body_widget():
            if self.info_labels:
                label_to_remove = self.info_labels.pop()  # 获取并移除最后一个标签
                label_to_remove.deleteLater()  # 删除标签实例
                rule_card_plane.adjustSize()
                group.adjustSize()

        with self.titled_widgets_group as group:
            group.addTitle("规则")
            self.rule_card_plane_h = SiDenseContainer(self)

            self.addrule_btu = SiPushButton(self)
            self.addrule_btu.attachment().setText("添加规则")
            self.addrule_btu.setFixedSize(128, 32)
            self.addrule_btu.clicked.connect(add_rule_card_plane_body_widget)

            self.remove_rule_btu = SiPushButton(self)
            self.remove_rule_btu.attachment().setText("删除规则")
            self.remove_rule_btu.setFixedSize(128, 32)
            self.remove_rule_btu.clicked.connect(remove_rule_card_plane_body_widget)

            info_ = QLabel("元素默认后缀自增", self)

            rule_card_plane.body().addWidget(self.rule_card_plane_h)
            rule_card_plane.footer().addWidget(info_)
            rule_card_plane.footer().addWidget(self.addrule_btu, Qt.RightEdge)
            rule_card_plane.footer().addWidget(self.remove_rule_btu, Qt.RightEdge)
            rule_card_plane.footer().setFixedHeight(40)
            # rule_card_plane.footer().layout().setSpacing(12)
            rule_card_plane.adjustSize()
            group.addWidget(rule_card_plane)


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
