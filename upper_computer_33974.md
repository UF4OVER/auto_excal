# 结构

## 组件
- `homepage`类
    - `SiTitledWidgetGroup`实例化滚动区域
        - `SiLabel`顶部标签
            - `SiDenseHContainer(SiLabel)` 添加容器到标签
                - `ThemedOptionCardPlane` 卡片组件
                - `resizeEvent` 方法
        - `SiLabel`身体标签
            - `SiTitledWidgetGroup(SiLabel)` titledWidgetGroups
                - `titled_widget_group.addWidget(WidgetsExamplePanel(self))` 方法
                - `titled_widget_group.addWidget(OptionCardsExamplePanel(self))` 方法
- `WidgetsExamplePanel(SiDenseVContainer)`类
    - `SiDenseHContainer(self)` 容器

- `OptionCardsExamplePanel(SiDenseVContainer)`类
    - `SiDenseHContainer(self)` 容器

