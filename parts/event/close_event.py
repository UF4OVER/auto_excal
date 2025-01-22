#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

from PyQt5.QtCore import pyqtSignal
from siui.components import SiLabel, SiLongPressButton, SiPushButton
from siui.core import SiColor, SiGlobal
from siui.templates.application.components.dialog.modal import SiModalDialog


class CloseModalDialog(SiModalDialog):
    user_decision = pyqtSignal(bool)  # 定义一个信号

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.callback = callback
        self.setFixedWidth(500)
        self._bool_b: bool = False
        # self.icon().load(SiGlobal.siui.iconpack.get("ic_fluent_save_filled",
        #                                             color_code=SiColor.mix(
        #                                                 self.getColor(SiColor.SVG_NORMAL),
        #                                                 self.getColor(SiColor.INTERFACE_BG_B),
        #                                                 0.05))
        #                  )

        label = SiLabel(self)
        label.setStyleSheet(f"color: {self.getColor(SiColor.TEXT_E)}")
        label.setText(f'<span style="color: {self.getColor(SiColor.TEXT_B)}">是否退出？</span>')
        label.adjustSize()
        self.contentContainer().addWidget(label)

        button2 = SiPushButton(self)
        button2.setFixedHeight(32)
        button2.attachment().setText("取消")
        button2.colorGroup().assign(SiColor.BUTTON_PANEL, self.getColor(SiColor.INTERFACE_BG_D))
        button2.clicked.connect(SiGlobal.siui.windows["MAIN_WINDOW"].layerModalDialog().closeLayer)

        self.button3 = SiLongPressButton(self)
        self.button3.setFixedHeight(32)
        self.button3.attachment().setText("狠心退出")
        # self.button3.longPressed.connect(lambda: self.callback)
        self.button3.longPressed.connect(lambda: self.user_decision.emit(True))
        self.buttonContainer().addWidget(button2)
        self.buttonContainer().addWidget(self.button3)

        SiGlobal.siui.reloadStyleSheetRecursively(self)
        self.adjustSize()

    def deleteLater(self):
        # print("你好")
        self.button3.hold_thread.safe_to_stop = True
        self.button3.hold_thread.wait()
        self.button3.deleteLater()
        SiGlobal.siui.windows["TOOL_TIP"].setNowInsideOf(None)
        SiGlobal.siui.windows["TOOL_TIP"].hide_()
        super().deleteLater()



