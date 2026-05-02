# Auto Excal

> 版本：1.3.0  
> 技术栈：Python 3.10 · PyQt5 · DrissionPage · openpyxl · PyQt-SiliconUI

## 项目简介

Auto Excal 是一个基于 PyQt5 的 Windows 桌面工具，用于：

1. 导入 Excel 成绩表；
2. 提取并整理出姓名、学号、分数三列数据；
3. 将整理后的数据保存为标准 JSON；
4. 打开 Chromium/Edge 浏览器，配合网页表单进行批量填表。

当前版本已经移除了以下历史遗留功能：

- 音乐播放器界面与相关模块
- 左侧侧边栏/系统控制抽屉
- OCR 验证码识别逻辑
- 自动 VPN 登录与门户跳转逻辑

“打开浏览器”按钮现在只负责启动浏览器，不再执行任何自动登录或页面跳转。

## 当前目录结构

```text
auto_excal/
├── main.py
├── ui.py
├── zip.py
├── config/
│   ├── CONFIG.py
│   ├── config.ini
│   └── qss.py
├── parts/
│   ├── component/
│   │   └── DynamicIsland.py
│   ├── event/
│   │   └── send/
│   └── page/
│       ├── page_autoexcalpage.py
│       ├── page_homepage.py
│       ├── page_settingpage.py
│       └── page_aboutpage.py
├── pyproject.toml
├── uv.lock
└── .github/workflows/release.yml
```

## 使用流程

### 1. 导入原始表格

- 在“原始表格数据”区域选择 Excel 文件。
- 程序会把工作表内容加载到表格控件中。

### 2. 生成标准三列表

- 默认模式：从第 9 行开始读取第 5、6、7 列。
- 自定义模式：手动输入起止坐标，例如 `(9,5)`。
- 点击“加载数据”后，生成姓名 / 学号 / 分数三列数据。

### 3. 检查与补充数据

- 可启用“去重”开关。
- 可从第二张表格导入补充数据后插入到主数据表。
- 数据会保存到 `parts/page/data.json`。

### 4. 打开浏览器并执行批量输入

- 点击“打开浏览器”只会启动 `DrissionPage` 配置的浏览器。
- 你需要手动打开目标网页并定位到需要录入的表单页面。
- 点击“开始”后，程序会按每批最多 49 条的方式，将学号与分数填入当前页面表单。

## 运行项目

先安装 uv 并同步依赖：

```powershell
uv sync --group build
```

`pyqt-siliconui` 已经写入 `pyproject.toml`，会由 `uv` 自动从 Git 源拉取。

启动应用：

```powershell
uv run python main.py
```

## 构建与打包

项目已经迁移到 `uv + pyproject.toml + cx_Freeze`：

- 依赖由 `uv` 管理
- 可执行文件打包配置位于 `pyproject.toml` 的 `tool.cxfreeze`
- 最终归档由 `zip.py` 负责

本地构建命令：

```powershell
uv sync --group build
uv run cxfreeze build
uv run python zip.py --build-dir build/AutoExcal --output-dir dist --artifact-name AutoExcal-1.3.0-windows-amd64.zip --upx upx.exe
```

## 更新与下载

- 项目仓库：`https://github.com/UF4OVER/auto_excal`
- 发布页：`https://github.com/UF4OVER/auto_excal/releases`
- 最新版下载入口：`https://github.com/UF4OVER/auto_excal/releases/latest`
- 版本元数据：`version.json`

当前项目已经保留版本元数据和发布页入口，后续用户仍然可以通过 GitHub Releases 持续下载新版本。

## GitHub Actions 自动构建与 Release

已添加工作流文件：

- `.github/workflows/release.yml`

工作流行为：

1. 在推送 tag 时触发
2. 使用 `uv sync --group build` 安装依赖
3. 执行 `uv run cxfreeze build`
4. 执行 `uv run python zip.py ...` 生成 zip 包
5. 使用 tag 对应提交的 commit message 作为 Release 内容
6. 上传 zip 资产到 GitHub Release

本次约定的发布标签：

- tag：`1.3.0`

发布流程：

```powershell
git add .
git commit -m "feat(release): migrate build pipeline to uv and pyproject"
git tag 1.3.0
git push origin HEAD
git push origin 1.3.0
```

当 `1.3.0` tag 被推送到 GitHub 后，Actions 会自动构建、打 zip 并创建 Release。

## 浏览器配置

浏览器路径和调试地址在 `config/config.ini` 中维护：

```ini
[chromium_options]
address = 127.0.0.1:9112
browser_path = C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
```

请确保本机已安装对应的 Chromium/Edge 浏览器。
