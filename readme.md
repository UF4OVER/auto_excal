# Wedding Invitation 自动化工具

## 简介
Wedding Invitation 是一个基于 PyQt5 和自定义 UI 框架 `siui` 的桌面应用程序，主要用于自动化 Excel 数据输入到网页表单中。

## 主要功能
- 从 Excel 文件中读取数据。
- 自定义数据输入框和表格数据。
- 打开浏览器并自动填充网页表单。
- 提供关于页面，展示项目信息和第三方资源。

## 安装与运行
1. 确保已安装 Python 3.10 及以上版本。
2. 安装项目依赖：
3. 运行项目：


## 配置
项目配置文件位于 `siui/config/config.ini`，可以调整以下配置项：
- `dpi_policy`: 高 DPI 缩放策略。
- `enable_hdpi_scaling`: 是否启用高 DPI 缩放。
- `use_hdpi_pixmaps`: 是否使用高 DPI 图片。
- `enable_switch`: 是否启用关闭确认对话框。
- `download_path`: 下载路径。
- `tmp_path`: 临时文件路径。
- `chromium_options`: Chromium 浏览器相关配置。
- `session_options`: 会话相关配置。
- `timeouts`: 各类超时时间。
- `proxies`: 代理设置。
- `others`: 其他配置，如重试次数和间隔。

## 目录结构
```python
auto_excal_new/ 
├── siui/ 
│ ├── components/ 
│ ├── config/ 
│ │ └── config.ini 
│ ├── core/ 
│ ├── gui/ 
│ ├── parts/ 
│ │ ├── layer_left_global.py 
│ │ ├── page_aboutpage.py 
│ │ ├── page_autoexcalpage.py 
│ │ ├── page_homepage.py 
│ │ └── page_settingpage.py 
│ ├── templates/ 
│ ├── ui.py 
│ └── start.py 
└── requirements.txt
```
## 贡献
欢迎提交问题和拉取请求。请确保遵循项目代码规范。

## 许可证
本项目遵循 MIT 许可证。
