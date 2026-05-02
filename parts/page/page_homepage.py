#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from siui.components import SiOptionCardLinear, SiPixLabel
from siui.components.page import SiPage
from siui.components.titled_widget_group import SiTitledWidgetGroup
from siui.components.widgets import SiDenseVContainer, SiLabel, SiSimpleButton
from siui.core import GlobalFont, SiColor, SiGlobal
from siui.gui import SiFont

import config.CONFIG as F

PATH_PNG = F.PNG_PATH


class Homepage(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPadding(64)
        self.setScrollMaximumWidth(960)
        self.setTitle("主页")

        self.scroll_container = SiTitledWidgetGroup(self)
        self.scroll_container.setSpacing(16)

        self.hero_container = SiDenseVContainer(self)
        self.hero_container.setAdjustWidgetsSize(True)
        self.hero_container.setSpacing(12)
        self.hero_container.setAlignment(Qt.AlignCenter)

        self.hero_image = SiPixLabel(self)
        self.hero_image.setFixedSize(900, 260)
        self.hero_image.setBorderRadius(12)
        self.hero_image.load(f"{PATH_PNG}\\back.jpg")

        self.title = SiLabel(self)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setText("Auto Excal")
        self.title.setFont(SiFont.tokenized(GlobalFont.XL_MEDIUM))

        self.subtitle = SiLabel(self)
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setText("导入 Excel 数据，整理成标准三列表，并批量填入网页表单。")
        self.subtitle.setFont(SiFont.tokenized(GlobalFont.S_MEDIUM))

        self.hero_container.addWidget(self.hero_image)
        self.hero_container.addWidget(self.title)
        self.hero_container.addWidget(self.subtitle)
        self.scroll_container.addWidget(self.hero_container)

        with self.scroll_container as group:
            group.addTitle("核心流程")

            import_card = SiOptionCardLinear(self)
            import_card.setTitle("1. 导入表格", "选择 Excel 文件，加载原始成绩数据。")
            import_card.load(SiGlobal.siui.iconpack.get("ic_fluent_table_stack_right_filled"))

            normalize_card = SiOptionCardLinear(self)
            normalize_card.setTitle("2. 整理数据", "按默认列或自定义区间提取姓名、学号、分数。")
            normalize_card.load(SiGlobal.siui.iconpack.get("ic_fluent_data_trending_regular"))

            browser_card = SiOptionCardLinear(self)
            browser_card.setTitle("3. 打开浏览器并批量填表", "程序仅启动浏览器，后续由你控制目标页面与录入时机。")
            browser_card.load(SiGlobal.siui.iconpack.get("ic_fluent_open_regular"))

            group.addWidget(import_card)
            group.addWidget(normalize_card)
            group.addWidget(browser_card)

        with self.scroll_container as group:
            group.addTitle("使用建议")

            tips_card = SiOptionCardLinear(self)
            tips_card.setTitle("浏览器准备", "请提前确认 Chromium/Edge 路径和调试地址配置正确。")
            tips_card.load(SiGlobal.siui.iconpack.get("ic_fluent_wrench_settings_filled"))

            duplicate_card = SiOptionCardLinear(self)
            duplicate_card.setTitle("数据检查", "加载完成后先检查去重结果，再执行批量输入。")
            duplicate_card.load(SiGlobal.siui.iconpack.get("ic_fluent_task_list_ltr_filled"))

            group.addWidget(tips_card)
            group.addWidget(duplicate_card)

        with self.scroll_container as group:
            group.addTitle("项目链接")

            repo_card = SiOptionCardLinear(self)
            repo_card.setTitle("项目仓库", "查看 Auto Excal 的源码与更新说明。")
            repo_card.load(SiGlobal.siui.iconpack.get("ic_fluent_home_database_regular"))

            repo_button = SiSimpleButton(self)
            repo_button.resize(32, 32)
            repo_button.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_open_regular"))
            repo_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(F.REPO_URL)))
            repo_card.addWidget(repo_button)

            release_card = SiOptionCardLinear(self)
            release_card.setTitle("发布页", "保留版本发布入口，后续用户可在这里继续下载更新。")
            release_card.load(SiGlobal.siui.iconpack.get("ic_fluent_arrow_download_regular"))

            release_button = SiSimpleButton(self)
            release_button.resize(32, 32)
            release_button.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_open_regular"))
            release_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(F.RELEASES_URL)))
            release_card.addWidget(release_button)

            latest_card = SiOptionCardLinear(self)
            latest_card.setTitle("下载最新版", f"当前版本 {F.VERSION}，点击跳转到 latest 发布页面。")
            latest_card.load(SiGlobal.siui.iconpack.get("ic_fluent_arrow_download_regular"))

            latest_button = SiSimpleButton(self)
            latest_button.resize(32, 32)
            latest_button.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_open_regular"))
            latest_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(F.LATEST_RELEASE_URL)))
            latest_card.addWidget(latest_button)

            ui_card = SiOptionCardLinear(self)
            ui_card.setTitle("Silicon UI", "当前界面依赖 PyQt-SiliconUI。")
            ui_card.load(SiGlobal.siui.iconpack.get("ic_fluent_box_regular"))

            ui_button = SiSimpleButton(self)
            ui_button.resize(32, 32)
            ui_button.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_open_regular"))
            ui_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/ChinaIceF/PyQt-SiliconUI")))
            ui_card.addWidget(ui_button)

            group.addWidget(repo_card)
            group.addWidget(release_card)
            group.addWidget(latest_card)
            group.addWidget(ui_card)

        self.scroll_container.addPlaceholder(64)
        self.setAttachment(self.scroll_container)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.title.setStyleSheet(f"color: {SiGlobal.siui.colors['TEXT_A']}")
        self.subtitle.setStyleSheet(f"color: {SiColor.trans(SiGlobal.siui.colors['TEXT_B'], 0.9)}")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.hero_image.setFixedWidth(min(event.size().width() - 128, 900))
