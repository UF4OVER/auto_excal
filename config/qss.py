# -*- coding: utf-8 -*-

#  Copyright (c) 2025. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

# -------------------------------
#  @Project : siui
#  @Time    : 2025 - 01-05 20:20
#  @FileName: qss.py
#  @Software: PyCharm 2024.1.6 (Professional Edition)
#  @System  : Windows 11 23H2
#  @Author  : 33974
#  @Contact : 
#  @Python  : 3.10
# -------------------------------
TabelQss = """
QTableWidget {
    background-color: rgba(44, 49, 60, 0.9);
    border: 1px solid #44475a;
    color: #f8f8f2;
    gridline-color: #44475a;
    selection-background-color: #6272a4;
    selection-color: #f8f8f2;
    border-radius: 8px;
}

QTableWidget::item:selected {
    background-color: #6272a4;
    color: #f8f8f2;
}

QTableWidget::item:hover {
    background-color: #44475a;
    color: #f8f8f2;
}

QTableWidget::item {
    padding: 5px;
    border-bottom: 1px solid #44475a;
}

QTableWidget::item:alternate {
    background-color: #3b4252;
}

QHeaderView::section {
    background-color: rgba(68, 71, 90, 0.9);
    color: #f8f8f2;
    padding: 5px;
    border: 1px solid #44475a;
    border-right: 1px solid #44475a;
    border-radius: 8px;
}

QHeaderView::section:last {
    border-right: none;
}

QHeaderView::section:horizontal {
    border-bottom: 1px solid #44475a;
}

QHeaderView::section:vertical {
    border-right: 1px solid #44475a;
}
"""