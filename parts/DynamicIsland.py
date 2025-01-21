#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

import psutil
from PyQt5.QtCore import QTimer, QRect, Qt, pyqtProperty
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPainter, QFontMetrics
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from siui.components import SiDenseHContainer, SiLabel, SiSvgLabel
from siui.components.widgets.expands import SiVExpandWidget
from siui.core import Si
from siui.core import SiColor, SiExpAccelerateAnimation, SiGlobal
from siui.gui import SiFont
from siui.templates.application.components.layer.layer import SiLayer


class ScrollingLabel(SiLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._offset = 0
        self._timer = QTimer(self)
        self._timer.setInterval(300)  # 设置定时器间隔
        self._timer.timeout.connect(self.updateTextPosition)
        self.setColor(self.getColor(SiColor.TEXT_B))
        self._is_scrolling = False

    def setText(self, text):
        super().setText(text)  # 调用父类的 setText 方法
        self._text = text
        self._offset = 0
        text_width = QFontMetrics(self.font()).horizontalAdvance(text)
        if text_width > self.width():
            self._is_scrolling = True
            self._timer.start()
        else:
            self._is_scrolling = False
            self.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self._timer.stop()
            self.update()

    def updateTextPosition(self):
        current_text = self.text()
        scroll_text = current_text[1:] + current_text[0]
        self.setText(scroll_text)

    def paintEvent(self, event):
        painter = QPainter(self)
        text_width = QFontMetrics(self.font()).horizontalAdvance(self._text)
        if self._is_scrolling:
            painter.drawText(QRect(self._offset, 0, self.width(), self.height()), Qt.AlignLeft | Qt.AlignVCenter,
                             self._text)
            painter.drawText(QRect(self._offset + text_width, 0, self.width(), self.height()),
                             Qt.AlignLeft | Qt.AlignVCenter, self._text)
        else:
            painter.drawText(QRect(0, 0, self.width(), self.height()), Qt.AlignCenter | Qt.AlignVCenter, self._text)

    def startScrolling(self):
        if self._is_scrolling:
            self._timer.start()

    def stopScrolling(self):
        self._timer.stop()

    def setOffset(self, offset):
        self._offset = offset
        self.update()

    offset = pyqtProperty(int, lambda self: self._offset, setOffset)


class DenseVContainerBG(SiDenseHContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.background = SiLabel(self)
        self.background.setFixedStyleSheet("border-radius: 15px")
        self.background.setColor(SiColor.trans(self.getColor(SiColor.INTERFACE_BG_E), 1))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.background.resize(event.size())


class TopStateOverlay(SiVExpandWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.container = DenseVContainerBG(self)

        self.title = ScrollingLabel(self)
        self.title.setFont(SiFont.getFont(size=15, weight=QFont.Weight.Normal))
        self.title.setTextColor(self.getColor(SiColor.TEXT_B))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFixedHeight(24)
        self.title.setFixedWidth(170)
        self.title.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.title.startScrolling()

        self.led = SiLabel(self)
        self.led.setFixedSize(4, 4)
        self.led.setFixedStyleSheet("border-radius: 2px")
        self.led.setColor(self.getColor(SiColor.BUTTON_LONG_PRESS_PROGRESS))

        self.subtitle = ScrollingLabel(self)
        self.subtitle.setFont(SiFont.getFont(size=12, weight=QFont.Weight.DemiBold))
        self.subtitle.setTextColor(self.getColor(SiColor.TEXT_THEME))
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setFixedHeight(15)
        self.subtitle.setFixedWidth(70)
        self.subtitle.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.subtitle.startScrolling()

        self.tip = ScrollingLabel(self)
        self.tip.setFont(SiFont.getFont(size=12, weight=QFont.Weight.Normal))
        self.tip.setTextColor(self.getColor(SiColor.TEXT_C))
        self.tip.setAlignment(Qt.AlignCenter)
        self.tip.setFixedHeight(16)
        self.tip.setFixedWidth(70)
        self.tip.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.tip.startScrolling()

        self.container.setSpacing(0)
        self.container.setAlignment(Qt.AlignCenter)
        self.container.addPlaceholder(8)
        self.container.addWidget(self.led)
        self.container.addPlaceholder(8)
        self.container.addWidget(self.title)
        self.container.addPlaceholder(4)
        self.container.addWidget(self.subtitle)
        self.container.addPlaceholder(10)
        self.container.addWidget(self.tip)

        self.container.adjustSize()

        self.setAttachment(self.container)

        self.animationGroup().fromToken("expand").setAccelerateFunction(lambda x: (x / 10) ** 5)
        self.animation_opacity = SiExpAccelerateAnimation(self)
        self.animation_opacity.setAccelerateFunction(lambda x: (x / 10) ** 3)
        self.animation_opacity.setFactor(1 / 2)
        self.animation_opacity.setBias(0.01)
        self.animation_opacity.setCurrent(1)
        self.animation_opacity.setTarget(1)
        self.animation_opacity.ticked.connect(self.on_opacity_changed)

        self.update_battery()

        battery_timer = QTimer()
        battery_timer.timeout.connect(self.update_battery)
        battery_timer.start(30_0000)  # 5分钟 = 300000毫秒

    def setLedColor(self, color):
        self.led.setColor(color)
        self.led.update()

    def update_battery(self):

        battery = psutil.sensors_battery()

        self.battery_label = SiSvgLabel(self)  # 电量图标
        self.container.addWidget(self.battery_label)
        self.container.addPlaceholder(10)

        battery_level = battery.percent // 10

        if 0 <= battery_level <= 10:
            icon_name = f"ic_fluent_battery_{battery_level}_regular"
        else:
            icon_name = "ic_fluent_battery_warning_filled"

        self.battery_label.load(SiGlobal.siui.iconpack.get(icon_name))

    def on_opacity_changed(self, opacity):
        effect = QGraphicsOpacityEffect()
        effect.setOpacity(opacity)
        self.setGraphicsEffect(effect)

    def emerge(self):
        self.expandTo(1)
        self.setOpacityTo(1)
        self.animation_opacity.start()
        # self.fade_out_timer.start()

    def resizeEvent(self, event):
        super().resizeEvent(event)

    def setContent(self, title, subtitle, tip, emerge=True):
        self.title.setText(title)
        self.subtitle.setText(subtitle)
        self.tip.setText(tip)
        if emerge:
            self.emerge()


class TopLayerOverLays(SiLayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.state_change_overlay = TopStateOverlay(self)
        self.state_change_overlay.adjustSize()

        self.send()

    def send(self):
        self.state_change_overlay.setOpacityTo(1)
        self.state_change_overlay.setContent("Wedding Invitation", "",
                                                                            "UF4OVER")

    def setContent(self, title, artist, album):
        self.state_change_overlay.setContent(
            title, artist, album)

        self.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.state_change_overlay.move(self.width() // 2 - self.state_change_overlay.width() // 2, 20)
