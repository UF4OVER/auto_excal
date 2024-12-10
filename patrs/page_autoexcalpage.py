from PyQt5.QtCore import Qt
from siui.components import SiLineEditWithItemName, SiDenseVContainer, SiOptionCardPlane, SiDenseHContainer
from siui.components.button import SiSwitchRefactor, SiPushButtonRefactor
from siui.components.option_card import SiOptionCardLinear
from siui.components.page import SiPage
from siui.components.spinbox.spinbox import SiIntSpinBox
from siui.components.titled_widget_group import SiTitledWidgetGroup
from siui.components.widgets import (
    SiLabel,
    SiLongPressButton,
)
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

        # 创建控件组
        self.titled_widgets_group = SiTitledWidgetGroup(self)
        self.titled_widgets_group.setSiliconWidgetFlag(Si.EnableAnimationSignals)
        self.setup_set_widgets()
        self.setup_function_widgets()

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
        group.addWidget(self.boswer_filter)
        group.addWidget(self.choose_port_card)

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
            self.data_stream_container.addWidget(self.data_stream_container_v1)
            self.data_stream_container.addWidget(self.data_stream_container_v2)

            def add_weights_btu_clicked():
                self.data_stream_num += 1
                print(self.data_stream_num)

                data_stream1 = SiLineEditWithItemName(self)
                data_stream1.setName(f"数据{self.data_stream_num}起始")
                data_stream1.lineEdit().setText("(0,0)")

                self.data_stream_container_v1.addWidget(data_stream1)
                self.data_stream_container_v1.update()

                data_stream2 = SiLineEditWithItemName(self)
                data_stream2.setName(f"数据{self.data_stream_num}结束")
                data_stream2.lineEdit().setText("(0,0)")

                self.data_stream_container_v2.addWidget(data_stream2)
                self.data_stream_container_v2.update()

                self.data_stream_list.append((data_stream1, data_stream2))
                group.show()

            def remove_weights_btu_clicked():
                if self.data_stream_num > 1:
                    print(self.data_stream_num)
                    self.data_stream_num -= 1
                    data_stream1, data_stream2 = self.data_stream_list.pop()
                    data_stream1.deleteLater()
                    data_stream2.deleteLater()
                    self.data_stream_container_v1.removeWidget(data_stream1)
                    self.data_stream_container_v2.removeWidget(data_stream2)

                    group.show()

            add_weights_btu.clicked.connect(add_weights_btu_clicked)
            remove_weights_btu.clicked.connect(remove_weights_btu_clicked)
            # start_input = SiLineEditWithItemName(self)
            # start_input.setName("数据1起始")
            # start_input.lineEdit().setText("(0,0)")
            # start_input.resize(350, 32)
            #
            # finish_input = SiLineEditWithItemName(self)
            # finish_input.setName("数据1结束")
            # finish_input.lineEdit().setText("(0,0)")
            # finish_input.resize(350, 32)

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
