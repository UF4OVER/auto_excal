# 文件路径：main.py
from PyQt5.QtWidgets import QTableWidget

class HPTableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 设置行高和列宽
        self.horizontalHeader().setDefaultSectionSize(200)  # 默认列宽
        self.verticalHeader().setDefaultSectionSize(40)     # 默认行高

        # 隐藏默认网格线
        self.setShowGrid(False)

        # 启用交替行颜色
        self.setAlternatingRowColors(True)

        # 设置默认透明度（可选）
        self.setWindowOpacity(0)

        # 样式表：修复白色区域
        self.setStyleSheet("""
            QTableWidget, QTableView {
                background-color: #2B2B2B;  /* 表格背景颜色 */
                color: #FFFFFF;  /* 字体颜色 */
                border: none;  /* 去除外边框 */
                gridline-color: #3A3A3A;  /* 设置交替背景行网格线 */
                font-size: 14px;
            }
            QTableWidget::item {
                background-color: #2B2B2B;  /* 单元格背景 */
                border-radius: 6px;  /* 单元格圆角 */
                padding: 5px;
            }
            QTableWidget::item:alternate {
                background-color: #3A3A3A;  /* 交替行背景颜色 */
            }
            QTableWidget::item:selected {
                background-color: #4B89FF;  /* 选中单元格背景 */
                color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #1F1F1F;  /* 表头背景颜色 */
                color: #FFFFFF;  /* 表头字体颜色 */
                padding: 8px;
                border: none;
                font-size: 14px;
                font-weight: bold;
                text-align: center;
            }
            QTableCornerButton::section {
                background-color: #1F1F1F;  /* 左上角按钮背景颜色 */
                border: none;
            }
            QScrollBar:vertical {
                background-color: #2B2B2B;  /* 垂直滚动条背景 */
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #5D5D5D;  /* 滚动条滑块颜色 */
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }
            QScrollBar:horizontal {
                background-color: #2B2B2B;  /* 水平滚动条背景 */
                height: 10px;
                margin: 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:horizontal {
                background-color: #5D5D5D;  /* 滚动条滑块颜色 */
                border-radius: 5px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background: none;
            }
        """)

    def set_opacity(self, opacity):
        """
        设置窗口部件的透明度
        :param opacity: 透明度值，范围为 0.0 到 1.0
        """
        self.setWindowOpacity(opacity)

