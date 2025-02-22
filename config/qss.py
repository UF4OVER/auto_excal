# -*- coding: utf-8 -*-

#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

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

LoginBtuQss = """
            AnimatedButton {
                background-color: #FFFFFF;
                border: 1px solid #ccc;
                border-radius: 25px;
                font-size: 16px;
                padding-left: 10px;
            }
            AnimatedButton:hover {
                background-color: #F0F0F0;
            }
        """
