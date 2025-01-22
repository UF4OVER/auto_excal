import psutil
from PyQt5.QtCore import QTimer, QRect, Qt, pyqtProperty, QPropertyAnimation, QEasingCurve, QSize, QPoint
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtGui import QPainter, QFontMetrics
from siui.components import SiDenseHContainer, SiLabel, SiSvgLabel
from siui.core import Si
from siui.core import SiColor, SiGlobal
from siui.gui import SiFont
from siui.components.widgets.expands import SiHExpandWidget


class DenseVContainerBG(SiDenseHContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.background = SiLabel(self)
        self.background.setFixedStyleSheet("border-radius: 15px")
        self.background.setColor(SiColor.trans(self.getColor(SiColor.INTERFACE_BG_E), 0.6))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.background.resize(event.size())


class ScrollingLabel(SiLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._offset = 0
        self._timer = QTimer(self)
        self._timer.setInterval(300)  # 设置定时器间隔
        self._timer.timeout.connect(self.updateTextPosition)
        # self.setColor(self.getColor(SiColor.TEXT_B))
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


class DynamicIsland(SiHExpandWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.setFixedSize(350, 30)

        self.container = DenseVContainerBG(self)
        self.container.setFixedSize(350, 30)
        self.adjustSize()

        self.title = ScrollingLabel(self)
        self.title.setFixedSize(150, 30)
        self.title.setColor("#0af00f")
        self.title.setFont(SiFont.getFont(size=15, weight=QFont.Weight.Normal))
        self.title.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.title.setTextColor(self.getColor(SiColor.TEXT_B))
        self.title.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.title.startScrolling()

        self.subtitle = ScrollingLabel(self)
        self.subtitle.setFixedSize(70, 30)
        self.subtitle.setFont(SiFont.getFont(size=12, weight=QFont.Weight.DemiBold))
        self.subtitle.setTextColor(self.getColor(SiColor.TEXT_THEME))
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.resize(int(self.size().width() / (6 / 1) - 1), self.size().height())
        self.subtitle.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.subtitle.startScrolling()

        self.tip = ScrollingLabel(self)
        self.tip.setFixedSize(70, 30)
        self.tip.setFont(SiFont.getFont(size=12, weight=QFont.Weight.Normal))
        self.tip.setTextColor(self.getColor(SiColor.TEXT_C))
        self.tip.setAlignment(Qt.AlignCenter)
        self.tip.resize(int(self.size().width() / (6 / 1) - 1), self.size().height())
        self.tip.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.tip.startScrolling()

        self.container.setSpacing(0)
        self.container.addPlaceholder(10)
        self.container.addWidget(self.title)
        self.container.addPlaceholder(5)
        self.container.addWidget(self.subtitle)
        self.container.addPlaceholder(3)
        self.container.addWidget(self.tip)
        self.container.addPlaceholder(5)

        self.send_default()

        self.update_battery()

        battery_timer = QTimer()
        battery_timer.timeout.connect(self.update_battery)
        battery_timer.start(30_0000)  # 5分钟 = 300000毫秒

        self._color = QColor(255, 255, 255)  # 初始颜色为白色
        self.tip_color_animation = QPropertyAnimation(self, b"tipColor")
        self.tip_color_animation.setDuration(300)
        self.tip_color_animation.setEasingCurve(QEasingCurve.InOutQuad)


    @pyqtProperty(QColor)
    def tipColor(self):
        return self._color

    @tipColor.setter
    def tipColor(self, value):
        self._color = value
        palette = self.tip.palette()
        palette.setColor(QPalette.WindowText, self._color)
        self.tip.setPalette(palette)

    def enterEvent(self, a0):
        super().enterEvent(a0)
        self.tip.setText("UF4OVER")
        self.tip_color_animation.setStartValue(self.tipColor)
        self.tip_color_animation.setEndValue(QColor(255, 0, 0))  # 鼠标进入时颜色变为红色
        self.tip_color_animation.start()

    def leaveEvent(self, a0):
        super().leaveEvent(a0)
        self.tip.setText("UF4OVER")
        self.tip_color_animation.setStartValue(self.tipColor)
        self.tip_color_animation.setEndValue(QColor(255, 255, 255))  # 鼠标离开时颜色变为白色
        self.tip_color_animation.start()

    def send_default(self):
        self.title.setText("Loot Hearts")
        self.subtitle.setText("")
        self.tip.setText("UF4OVER")

    def send(self, title, subtitle, tip):
        self.title.setText(title)
        self.subtitle.setText(subtitle)
        self.tip.setText(tip)

    def update_battery(self):

        battery = psutil.sensors_battery()
        self.battery_label = SiSvgLabel(self)  # 电量图标
        battery_level = battery.percent // 10

        if 0 <= battery_level <= 10:
            icon_name = f"ic_fluent_battery_{battery_level}_regular"
        else:
            icon_name = "ic_fluent_battery_warning_filled"

        self.battery_label.load(SiGlobal.siui.iconpack.get(icon_name))
        self.container.addWidget(self.battery_label)
        self.battery_label.setFixedSize(20, 30)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # self.title.move(10, 0)


def Send_DynamicIsland_Message(title, subtitle, tip):
    SiGlobal.siui.windows["MAIN_WINDOW"].Dynamic_Island().send(title, subtitle, tip)
