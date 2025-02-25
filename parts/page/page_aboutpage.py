#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

import os

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from siui.components import (
    SiOptionCardLinear,
    SiPixLabel,
    SiTitledWidgetGroup,
)
from siui.components.page import SiPage
from siui.components.widgets import (
    SiDenseVContainer,
    SiLabel,
    SiSimpleButton,
)
from siui.core import GlobalFont, Si, SiColor, SiGlobal, SiQuickEffect
from siui.gui import SiFont


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

        self.titled_widget_group.addPlaceholder(64)
        self.setAttachment(self.titled_widget_group)
