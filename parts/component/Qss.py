# -*- coding: utf-8 -*-

#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

# -------------------------------
#  @Project : siui_refacter
#  @Time    : 2025 - 01-05 20:20
#  @FileName: Qss.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Python  : 3.10
# -------------------------------
TabelQss = """
QTableWidget {
    background-color: #332e38;
    color: white;
    gridline-color: #39333e;
    font-size: 14px;
    border: none;
    selection-background-color: #1c191f;
    selection-color: #89539d;
    alternate-background-color: #2d2931;
}

QHeaderView::section {
    background-color: #25222a;
    color: white;
    padding: 6px;
    border: 1px solid #39333e;
    font-weight: bold;
    border-radius: 8px;
}

QTableView QTableCornerButton::section {
    background-color: transparent;
    border: none;
}

QTableView QHeaderView::section {
    background-color: #25222a;
    color: white;
    padding: 6px;
    border: 1px solid #39333e;
    font-weight: bold;
    border-radius: 8px;
}

QHeaderView::section:pressed {
    background-color: #1c191f;
}

QTableWidget::item {
    padding: 6px;
    border: none;
    border-radius: 8px;
}

QTableWidget::item:selected {
    background-color: #1c191f;
    color: #89539d;
    border-radius: 8px;
}

QTableWidget::item:hover {
    background-color: #2a2730;
    border-radius: 8px;
}

QScrollBar:vertical {
    border: none;
    background: #25222a;
    width: 12px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #39333e;
    min-height: 20px;
    border-radius: 6px;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: none;
}

QScrollBar:horizontal {
    border: none;
    background: #25222a;
    height: 12px;
    margin: 0px;
}

QScrollBar::handle:horizontal {
    background: #39333e;
    min-width: 20px;
    border-radius: 6px;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0px;
}

QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {
    background: none;
}

"""