from siui.components import SiTitledWidgetGroup
from siui.components.page import SiPage


class repopage(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 滚动区域
        self.scroll_container = SiTitledWidgetGroup(self)
        # 整个顶部
