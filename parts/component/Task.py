# -*- coding: utf-8 -*-
#  Copyright (c) 2025 UF4OVER
#   All rights reserved.
from PyQt5.QtCore import QEvent, QRect, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont
from siui.core import SiGlobal
from siui.components import SiLabel, SiWidget
from siui.components.widgets import SiSimpleButton
from siui.core import SiColor
from siui.gui import SiFont


class Task:
    def __init__(self, name, description, back_name, back_description, due_time_stamp, color):
        self.name = name
        self.description = description
        self.back_name = back_name
        self.back_description = back_description
        self.due_time_stamp = due_time_stamp
        self.color = color


class TaskCardLinear(SiWidget):
    def __init__(self, task, parent=None):
        super().__init__(parent)
        self.task = None

        self.theme_color_indicator = SiLabel(self)
        self.theme_color_indicator.setFixedStyleSheet("border-radius: 8px")

        self.original_panel = SiLabel(self)
        self.original_panel.setFixedStyleSheet("border-radius: 8px")
        self.original_panel.setColor(self.getColor(SiColor.INTERFACE_BG_C))

        self.panel = SiLabel(self)
        self.panel.setFixedStyleSheet("border-radius: 8px; border-top-left-radius: 6px; border-bottom-left-radius: 6px")

        self.title = SiLabel(self)
        self.title.setFont(SiFont.getFont(size=18, weight=QFont.Weight.Bold))

        self.description = SiLabel(self)
        self.description.setFont(SiFont.getFont(size=14, weight=QFont.Weight.Normal))

        self.back_title = SiLabel(self.original_panel)
        self.back_title.setFont(SiFont.getFont(size=18, weight=QFont.Weight.Bold))

        self.back_description = SiLabel(self.original_panel)
        self.back_description.setFont(SiFont.getFont(size=14, weight=QFont.Weight.Normal))

        self.button = SiSimpleButton(self)
        self.button.resize(60, 80)
        self.button.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_virtual_network_filled"))
        self.button.clicked.connect(self.label_animation)
        self.loadTask(task)
        self.button.installEventFilter(self)

        # 创建动画对象
        self.panel_animation = QPropertyAnimation(self.panel, b"geometry")
        self.panel_animation.setDuration(500)  # 动画持续时间，单位为毫秒
        self.panel_animation.setEasingCurve(QEasingCurve.InOutExpo)  # 动画缓动曲线

    def eventFilter(self, obj, event):
        if obj == self.button:
            if event.type() == QEvent.Enter:
                self.on_button_enter()
            elif event.type() == QEvent.Leave:
                self.on_button_leave()
        return super().eventFilter(obj, event)

    def on_button_enter(self):
        start_rect = self.panel.geometry()
        end_rect = QRect(24, 0, 360, self.size().height())
        self.panel_animation.setStartValue(start_rect)
        self.panel_animation.setEndValue(end_rect)
        self.panel_animation.start()

    def on_button_leave(self):
        start_rect = self.panel.geometry()
        end_rect = QRect(24, 0, self.size().width() - 24 - 60, self.size().height())
        self.panel_animation.setStartValue(start_rect)
        self.panel_animation.setEndValue(end_rect)
        self.panel_animation.start()

    def loadTask(self, task: Task):
        self.task = task

        # 设置颜色
        self.theme_color_indicator.setColor(task.color)
        self.panel.setColor(SiColor.mix(self.getColor(SiColor.INTERFACE_BG_C), task.color, weight=0.9))
        self.title.setTextColor(self.getColor(SiColor.TEXT_B))
        self.description.setTextColor(SiColor.mix(self.getColor(SiColor.TEXT_B), task.color))
        self.back_title.setTextColor(self.getColor(SiColor.TEXT_B))
        self.back_description.setTextColor(SiColor.mix(self.getColor(SiColor.TEXT_B), self.getColor(SiColor.TEXT_B)))

        # 设置文本
        self.title.setText(task.name)
        self.description.setText(task.description)
        self.back_title.setText(task.back_name)
        self.back_description.setText(task.back_description)

    def getTask(self):
        return self.task

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.theme_color_indicator.resize(48, event.size().height())
        self.original_panel.setGeometry(24, 0, event.size().width() - 24, event.size().height())
        self.panel.setGeometry(24, 0, event.size().width() - 24 - 60, event.size().height())
        self.title.move(40, 15)
        self.description.move(40, 21 + 24)

        self.back_title.move(event.size().width() - 500, 15)
        self.back_description.move(event.size().width() - 500, 21 + 24)
        self.button.move(event.size().width() - 60, 0)

    def label_animation(self):
        pass
