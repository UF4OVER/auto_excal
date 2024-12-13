from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from qfluentwidgets import TableWidget, FluentStyleSheet
from siui.components import SiLineEditWithItemName, SiDenseVContainer, SiOptionCardPlane, SiDenseHContainer, \
    SiPushButton
from siui.components.button import SiSwitchRefactor, SiPushButtonRefactor
from siui.components.combobox import SiComboBox
from siui.components.option_card import SiOptionCardLinear
from siui.components.page import SiPage
from siui.components.spinbox.spinbox import SiIntSpinBox
from siui.components.titled_widget_group import SiTitledWidgetGroup
from siui.components.widgets import SiLabel, SiLongPressButton
from siui.core import Si, SiColor, SiGlobal


class Label(SiLabel):
    def __init__(self, parent, text):
        super().__init__(parent)

        self.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(32)

        # self.setFixedStyleSheet("border-radius: 4px")
        self.setText(text)
        self.adjustSize()
        self.resize(self.width() + 24, self.height())
        self.setVisible(True)
        self.update()

#
# class testLabel(QLabel):
#     def __init__(self, parent, text):
#         super().__init__(parent)
#         # self.setAlignment(Qt.AlignCenter)
#         self.setFixedHeight(32)
#         self.setText(text)
#         self.setVisible(True)
#         self.update()

    def reloadStyleSheet(self):
        self.setStyleSheet(f"color: {self.getColor(SiColor.TEXT_B)};")
        # f"background-color: {self.getColor(SiColor.INTERFACE_BG_D)}")


class Autoexcal(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPadding(64)
        self.setScrollMaximumWidth(1000)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("AUTOEXCAL")

        self.data_for_combox: str = "数据1"
        self.ele_name_for_combox: str = "@id="
        self.info_labels = []  # 存储添加的标签

        # 创建控件组
        self.titled_widgets_group = SiTitledWidgetGroup(self)
        self.titled_widgets_group.setSiliconWidgetFlag(Si.EnableAnimationSignals)
        self.setup_set_widgets()
        self.setup_rules_groups()
        self.setup_function_widgets()

        SiGlobal.siui.reloadStyleSheetRecursively(self)

        # 添加页脚的空白以增加美观性
        self.titled_widgets_group.addPlaceholder(64)
        # 设置控件组为页面对象
        self.setAttachment(self.titled_widgets_group)

    def setup_set_widgets(self):
        # 密堆积容器
        with self.titled_widgets_group as group:
            group.addTitle("设置")
            choose_boswer_btu = SiLongPressButton(self)
            choose_boswer_btu.resize(128, 32)
            choose_boswer_btu.setHint("长按选择文件夹")
            choose_boswer_btu.attachment().setText("选择文件夹")

            choose_boswer_sw = SiSwitchRefactor(self)
            choose_boswer_sw.toggled.connect(lambda checked: choose_boswer_btu.setEnabled(checked))

            self.boswer_filter = SiOptionCardLinear(self)
            self.boswer_filter.setTitle("浏览器所在文件夹", "启用以自定义选择浏览器")
            self.boswer_filter.load(SiGlobal.siui.iconpack.get("ic_fluent_folder_add_filled"))
            self.boswer_filter.addWidget(choose_boswer_sw)
            self.boswer_filter.addWidget(choose_boswer_btu)

            self.port_int_spin_box = SiIntSpinBox(self)
            self.port_int_spin_box.resize(128, 32)
            self.port_int_spin_box.setMaximum(65535)
            self.port_int_spin_box.setMinimum(1024)
            self.port_int_spin_box.setValue(9002)

            choose_port_sw = SiSwitchRefactor(self)
            choose_port_sw.toggled.connect(lambda checked: self.port_int_spin_box.setEnabled(checked))

            self.choose_port_card = SiOptionCardLinear(self)
            self.choose_port_card.setTitle("端口号", "启用以自定义端口号")
            self.choose_port_card.load(SiGlobal.siui.iconpack.get("ic_fluent_plug_connected_filled"))
            self.choose_port_card.addWidget(choose_port_sw)
            self.choose_port_card.addWidget(self.port_int_spin_box)

            duplicate_filter_btu = SiSwitchRefactor(self)
            self.duplicate_filter_card = SiOptionCardLinear(self)
            self.duplicate_filter_card.setTitle("去重", "启用以数据去重")
            self.duplicate_filter_card.load(SiGlobal.siui.iconpack.get("ic_fluent_poll_off_filled"))
            self.duplicate_filter_card.addWidget(duplicate_filter_btu)

        group.addWidget(self.boswer_filter)
        group.addWidget(self.choose_port_card)
        group.addWidget(self.duplicate_filter_card)

    def setup_function_widgets(self):
        with self.titled_widgets_group as group:
            choose_switch = SiSwitchRefactor(self)
            add_weights_btu = SiPushButtonRefactor(self)
            add_weights_btu.setText("添加数据流")
            add_weights_btu.resize(128, 32)

            remove_weights_btu = SiPushButtonRefactor(self)
            remove_weights_btu.setText("移除数据流")
            remove_weights_btu.resize(128, 32)
            self.data_stream_list = []
            self.data_stream_num = 1

            self.data_stream_container = SiDenseHContainer(self)
            self.data_stream_container_v1 = SiDenseVContainer(self)
            self.data_stream_container_v2 = SiDenseVContainer(self)

            start_input = SiLineEditWithItemName(self)
            start_input.setName("数据1起始")
            start_input.lineEdit().setText("(0,0)")
            start_input.resize(350, 32)

            finish_input = SiLineEditWithItemName(self)
            finish_input.setName("数据1结束")
            finish_input.lineEdit().setText("(0,0)")
            finish_input.resize(350, 32)

            start_input1 = SiLineEditWithItemName(self)
            start_input1.setName("数据2起始")
            start_input1.lineEdit().setText("(0,0)")
            start_input1.resize(350, 32)

            finish_input1 = SiLineEditWithItemName(self)
            finish_input1.setName("数据2结束")
            finish_input1.lineEdit().setText("(0,0)")
            finish_input1.resize(350, 32)

            start_input2 = SiLineEditWithItemName(self)
            start_input2.setName("数据3起始")
            start_input2.lineEdit().setText("(0,0)")
            start_input2.resize(350, 32)

            finish_input2 = SiLineEditWithItemName(self)
            finish_input2.setName("数据3结束")
            finish_input2.lineEdit().setText("(0,0)")
            finish_input2.resize(350, 32)

            self.data_stream_container_v1.addWidget(start_input)
            self.data_stream_container_v2.addWidget(finish_input)
            self.data_stream_container_v1.addWidget(start_input1)
            self.data_stream_container_v2.addWidget(finish_input1)
            self.data_stream_container_v1.addWidget(start_input2)
            self.data_stream_container_v2.addWidget(finish_input2)

            self.data_stream_container.addWidget(self.data_stream_container_v1)
            self.data_stream_container.addWidget(self.data_stream_container_v2)

            info_ = Label(self, "启用以自定义添加数据")

            customize_the_input_box = SiOptionCardPlane(self)
            customize_the_input_box.setTitle("自定义输入框")
            customize_the_input_box.header().addWidget(choose_switch, "right")
            customize_the_input_box.body().addWidget(self.data_stream_container)
            customize_the_input_box.footer().addWidget(info_)
            customize_the_input_box.footer().addWidget(add_weights_btu, "right")
            customize_the_input_box.footer().addWidget(remove_weights_btu, "right")
            customize_the_input_box.footer().setFixedHeight(40)
            customize_the_input_box.body().addPlaceholder(12)
            customize_the_input_box.adjustSize()

            # group.addWidget(customize_the_input_box)

            choose_switch.toggled.connect(lambda checked: customize_the_input_box.body().setEnabled(checked))
            choose_switch.toggled.connect(lambda checked: customize_the_input_box.footer().setEnabled(checked))
            group.addWidget(customize_the_input_box)

        with self.titled_widgets_group as group:
            table_widget_height = 900
            table_widget_width = 500
            group.addTitle("表格数据")

            self.auto_input_widget_box = SiOptionCardPlane(self)
            self.auto_input_widget_box.adjustSize()
            self.auto_input_widget_box.setTitle("原始表格数据")
            self.auto_input_widget_box.body().setFixedSize(table_widget_height + 40, table_widget_width + 40)
            self.auto_input_widget_box.footer().setFixedHeight(40)

            self.table_widget = TableWidget(self)
            # self.table_widget.setStyleSheet("""
            #                                     QTableWidget::item {
            #                                     color: white;
            #                                     background-color: transparent;}""")
            self.table_widget.setFixedSize(table_widget_height, table_widget_width)
            self.table_widget.setColumnCount(40)
            self.table_widget.setRowCount(140)

            clear_data_btu = SiLongPressButton(self)
            clear_data_btu.setFixedHeight(32)
            clear_data_btu.attachment().setText("清除数据")
            clear_data_btu.longPressed.connect(lambda: print("clear_data"))
            clear_data_btu.setFixedHeight(32)

            choose_file_btu = SiPushButtonRefactor(self)
            choose_file_btu.setText("选择文件")

            self.auto_input_widget_box.header().addWidget(choose_file_btu, "right")
            self.auto_input_widget_box.body().addWidget(self.table_widget)
            self.auto_input_widget_box.footer().addWidget(Label(self, "使用表格数据时，请确保表格数据与输入框对应"))
            self.auto_input_widget_box.footer().addWidget(clear_data_btu, "right")

            self.new_input_widget_box = SiOptionCardPlane(self)
            self.new_input_widget_box.adjustSize()
            self.new_input_widget_box.setTitle("自定义表格数据")
            self.new_input_widget_box.body().setFixedSize(table_widget_height + 40, table_widget_width + 70)
            self.new_input_widget_box.footer().setFixedHeight(40)

            self.new_table_widget = TableWidget(self)
            # self.new_table_widget.setStyleSheet("""
            #                                     QTableWidget::item {
            #                                     color: white;
            #                                     background-color: transparent;}""")
            self.new_table_widget.setFixedSize(int(table_widget_height * 0.7), table_widget_width)
            self.new_table_widget.setColumnCount(40)
            self.new_table_widget.setRowCount(140)

            # 此容器左侧用于放置表格数据，右侧放置按钮
            self.operate_the_container_h = SiDenseHContainer(self)
            # 此容器用于放置表格数据
            self.vertical_container_for_tabular_data = SiDenseVContainer(self)

            self.vertical_container_for_tabular_data.addWidget(self.new_table_widget)
            # 此容器用于放置按钮
            self.btu_container_for_vertical_container = SiDenseVContainer(self)

            open_web_btu = SiPushButton(self)
            open_web_btu.setUseTransition(True)
            open_web_btu.attachment().setText("打开浏览器")
            open_web_btu.setFixedSize(128, 32)

            start_btu = SiPushButton(self)
            start_btu.setUseTransition(True)
            start_btu.attachment().setText("开始")
            start_btu.setFixedSize(128, 32)

            restart_btu = SiLongPressButton(self)
            # restart_btu.setUseTransition(True)
            restart_btu.attachment().setText("清除数据")
            restart_btu.setFixedSize(128, 32)

            delete_btu = SiPushButton(self)
            delete_btu.attachment().setText("删除")
            delete_btu.setFixedSize(128, 32)

            insert_btu = SiPushButton(self)
            insert_btu.attachment().setText("插入")
            insert_btu.setFixedSize(128, 32)

            # 创建控件组
            # self.named_input_box_group = SiTitledWidgetGroup(self)
            # self.named_input_box_group.setSiliconWidgetFlag(Si.EnableAnimationSignals)

            data1_input = SiLineEditWithItemName(self)
            data1_input.setName("数据1")
            data1_input.lineEdit().setText("(0,0)")
            data1_input.resize(210, 32)

            data2_input = SiLineEditWithItemName(self)
            data2_input.setName("数据2")
            data2_input.lineEdit().setText("(0,0)")
            data2_input.resize(210, 32)

            data3_input = SiLineEditWithItemName(self)
            data3_input.setName("数据3")
            data3_input.lineEdit().setText("(0,0)")
            data3_input.resize(210, 32)
            self.btu_container_for_vertical_container.addWidget(data1_input)
            self.btu_container_for_vertical_container.addWidget(data2_input)
            self.btu_container_for_vertical_container.addWidget(data3_input)
            # self.named_input_box_group.addWidget(data1_input)
            # self.named_input_box_group.addWidget(data2_input)
            # self.named_input_box_group.addWidget(data3_input)

            # SiGlobal.siui.reloadStyleSheetRecursively(self)
            # self.named_input_box_group.addPlaceholder(64)
            # self.setAttachment(self.named_input_box_group)

            temp_h = SiDenseHContainer(self)

            temp_h.addWidget(open_web_btu)
            temp_h.addWidget(start_btu)
            temp_h.addWidget(restart_btu)
            temp_h.addWidget(delete_btu)
            temp_h.addWidget(insert_btu)

            # self.btu_container_for_vertical_container.addWidget(self.named_input_box_group)
            self.vertical_container_for_tabular_data.addWidget(temp_h)

            self.operate_the_container_h.addWidget(self.vertical_container_for_tabular_data)
            self.operate_the_container_h.addWidget(self.btu_container_for_vertical_container)

            self.new_input_widget_box.body().addWidget(self.operate_the_container_h)
            self.new_input_widget_box.footer().addWidget(Label(self, "使用表格数据时，请确保表格数据与输入框对应"))

            group.addWidget(self.auto_input_widget_box)
            group.addWidget(self.new_input_widget_box)

            # 确保所有部件都可见
            self.table_widget.setVisible(True)
            self.new_table_widget.setVisible(True)
            clear_data_btu.setVisible(True)
            choose_file_btu.setVisible(True)

            # 调整父部件大小
            self.auto_input_widget_box.adjustSize()
            self.new_input_widget_box.adjustSize()
            group.adjustSize()
            self.adjustSize()

    def setup_rules_groups(self):
        rule_card_plane = SiOptionCardPlane(self)
        rule_card_plane.setTitle("自定义规则")

        def add_rule_card_plane_body_widget():
            info_label = Label(self,
                                   f"{self.data_for_combox}添加到-->{self.ele_name_for_combox}的{self.ele_name_input.getText()}元素")
            info_label.setVisible(True)
            print(f"{self.data_for_combox}添加到-->{self.ele_name_for_combox}的{self.ele_name_input.getText()}元素")
            rule_card_plane.body().addWidget(info_label)
            rule_card_plane.body().adjustSize()
            rule_card_plane.body().update()
            rule_card_plane.adjustSize()
            self.info_labels.append(info_label)  # 存储标签引用
            group.adjustSize()
            group.update()

        def remove_rule_card_plane_body_widget():
            if self.info_labels:
                label_to_remove = self.info_labels.pop()  # 获取并移除最后一个标签
                rule_card_plane.body().removeWidget(label_to_remove)
                label_to_remove.deleteLater()  # 删除标签实例
                rule_card_plane.body().adjustSize()
                rule_card_plane.body().update()
                rule_card_plane.adjustSize()
                group.adjustSize()

        with self.titled_widgets_group as group:
            group.addTitle("规则")
            self.rule_card_plane_h = SiDenseHContainer(self)

            self.custom_rule_tu = SiSwitchRefactor(self)
            self.custom_rule_tu.toggled.connect(lambda :rule_card_plane.body().setEnabled(False))
            self.custom_rule_tu.toggled.connect(lambda :rule_card_plane.footer().setEnabled(False))

            self.choose_data_flu = SiComboBox(self)
            self.choose_data_flu.resize(128, 32)
            self.choose_data_flu.addOption("数据1", value="数据1")
            self.choose_data_flu.addOption("数据2", value="数据2")
            self.choose_data_flu.addOption("数据3", value="数据3")
            self.choose_data_flu.menu().setShowIcon(False)
            self.choose_data_flu.menu().setIndex(0)
            self.choose_data_flu.menu().valueChanged.connect(self.get_ele_name_for_combox)

            self.choose_ele = SiComboBox(self)
            self.choose_ele.resize(128, 32)
            self.choose_ele.addOption("@id=", value="@id=")
            self.choose_ele.addOption("@tag()=", value="@tag()=")
            self.choose_ele.addOption("@text()=", value="@text()=")
            self.choose_ele.menu().setShowIcon(False)
            self.choose_ele.menu().setIndex(0)
            self.choose_data_flu.menu().valueChanged.connect(self.get_data_for_combox)

            self.ele_name_input = SiLineEditWithItemName(self)
            self.ele_name_input.setName("元素名称")
            self.ele_name_input.lineEdit().setText("txtpoint")
            self.ele_name_input.resize(350, 32)

            self.addrule_btu = SiPushButton(self)
            self.addrule_btu.attachment().setText("添加规则")
            self.addrule_btu.setFixedSize(128, 32)
            self.addrule_btu.clicked.connect(add_rule_card_plane_body_widget)

            self.remove_rule_btu = SiPushButton(self)
            self.remove_rule_btu.attachment().setText("删除规则")
            self.remove_rule_btu.setFixedSize(128, 32)
            self.remove_rule_btu.clicked.connect(remove_rule_card_plane_body_widget)

            self.rule_card_plane_h.addWidget(self.choose_data_flu)
            self.rule_card_plane_h.addWidget(Label(self, "定义到---->"))
            self.rule_card_plane_h.addWidget(self.choose_ele)
            self.rule_card_plane_h.addWidget(self.ele_name_input)

            info_ = Label(self, "元素默认后缀自增")

            rule_card_plane.header().addWidget(self.custom_rule_tu, "right")
            rule_card_plane.body().addWidget(self.rule_card_plane_h)
            rule_card_plane.footer().addWidget(info_)
            rule_card_plane.footer().addWidget(self.addrule_btu, "right")
            rule_card_plane.footer().addWidget(self.remove_rule_btu, "right")
            rule_card_plane.footer().setFixedHeight(40)
            rule_card_plane.body().addPlaceholder(12)
            rule_card_plane.adjustSize()

            # group.addWidget(customize_the_input_box)

            group.addWidget(rule_card_plane)

    def get_data_for_combox(self, data_name):
        self.data_for_combox = data_name

    def get_ele_name_for_combox(self, data_name):
        self.ele_name_for_combox = data_name
