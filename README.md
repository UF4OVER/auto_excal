# Auto_Excal —— 主要代码逻辑与实现说明

> **项目别名**：Loot Hearts 系列 / Wedding Invitation  
> **版本**：1.2.1  
> **技术栈**：Python 3.10 · PyQt5 · DrissionPage · openpyxl · Baidu OCR API

---

## 一、项目概述

Auto_Excal 是一个基于 PyQt5 的 **Windows 桌面自动化工具**，核心功能是将 Excel 表格中的学生信息（姓名、学号、分数）批量自动填入高校教务系统的网页表单，从而替代手动逐条录入的繁琐操作。

主要解决的痛点：

| 场景 | 传统做法 | 本工具 |
|------|----------|--------|
| 批量录入操行成绩 | 手动复制粘贴，逐条填写 | 一键自动填入，每批最多 49 条 |
| 验证码登录 | 人工识别输入 | Baidu OCR 自动识别 |
| 数据去重 | 手动比对 | 程序自动过滤重复学号 |

---

## 二、整体架构

```
auto_excal/
├── start.py                  # 程序入口
├── ui.py                     # 主窗口（SiliconApplication 子类）
├── sys_stdio.py              # 全局日志与异常处理
├── config/
│   ├── CONFIG.py             # 配置读写管理器
│   ├── config.ini            # 用户配置文件（VPN账号、OCR Token 等）
│   └── qss.py                # 表格 QSS 样式表
├── parts/
│   ├── page/
│   │   ├── page_autoexcalpage.py   # ★ 核心页面：数据处理 + 浏览器自动化
│   │   ├── page_homepage.py        # 主页（项目介绍 + 链接卡片）
│   │   └── page_aboutpage.py       # 关于页面
│   ├── component/
│   │   ├── DynamicIsland.py        # 顶部状态栏（时间、电量、作者名）
│   │   └── GlobalLeftWindow.py     # 左侧抽屉（音量、亮度控制）
│   └── event/
│       ├── ocr/ocr_recognize.py    # Baidu OCR 验证码识别
│       └── send/send_message.py    # 消息通知组件
└── docs/readme.md            # 编译与环境搭建说明
```

---

## 三、程序启动流程

```
start.py
  │
  ├─ setup_logging()          # 初始化日志（输出到 app.log）
  ├─ QApplication()           # 创建 Qt 应用实例
  ├─ MySiliconApp()           # 构建主窗口
  │     ├─ DynamicIsland      # 顶部动态岛状态栏
  │     ├─ LayerLeftGlobalDrawer  # 左侧系统控制抽屉
  │     └─ 三个页面（主页 / 表单页 / 关于页）
  ├─ window.show()            # 显示窗口
  └─ send_custom_message()    # 弹出欢迎通知
```

**全局异常捕获**：`start.py` 中用 `try/except` 包裹整个初始化过程，一旦出现未预期异常，会弹出提示框引导用户截图或发送 `app.log` 给开发者。

---

## 四、核心页面：AutoFormPage（page_autoexcalpage.py）

这是整个项目最重要的文件（约 889 行），承载了所有数据处理与自动化逻辑。

### 4.1 页面初始化

```python
class Autoexcal(SiPage):
    def __init__(self):
        self.index_current_data = 0   # 当前批次起始索引
        self.browser = None           # Chromium 浏览器实例
        self.sheet = None             # openpyxl 工作表对象
        self.main_loop_thread = None  # 后台填表线程
        self.setup_set_widgets()      # 构建"设置"区域（去重开关）
        self.setup_function_widgets() # 构建"表格数据"区域（核心 UI）
```

### 4.2 UI 布局（四张表格 + 操作按钮）

| 表格 | 名称 | 说明 |
|------|------|------|
| `table_widget` | 表格1：原始表格数据 | 直接从 Excel 读入的原始数据，列数与 Excel 一致 |
| `insert_table_widget` | 表格2：待插入原始表格 | 第二个 Excel 文件的原始数据（补充录入用） |
| `new_table_widget` | 表格3：自定义表格数据（左） | 标准化后的三列数据（姓名 / 学号 / 分数），也是提交给自动化的最终数据 |
| `new_insert_table_widget` | 表格4：待插入表（右） | 从表格2提取的标准化数据，可选行后插入表格3 |

---

## 五、核心数据流

```
① 导入 Excel 文件
        ↓  import_file_for_table_widget()
        ↓  openpyxl.load_workbook() 读取单元格
② 填充到表格1（原始数据）

③ 点击"加载数据"
        ↓  reload_data_for_new_table_widget()
        ↓  若未启用自定义输入框：默认取第5~7列（姓名/学号/分数），从第9行开始
        ↓  若启用自定义输入框：按用户指定的 (行,列) 范围提取
④ 填充到表格3（标准三列）

⑤ 去重 + 清理空行
        ↓  save_to_json()
        ↓  构建 [{unique_id, name, stu_id, score}, ...] 列表
        ↓  若"去重"开关开启：用 unique_id 集合过滤重复项
⑥ 写入 data.json（与 page_autoexcalpage.py 同目录）

⑦ 点击"打开浏览器"
        ↓  open_broswer()
        ↓  DrissionPage 启动/连接 Chromium（Edge）
        ↓  自动完成 VPN 登录 + OCR 验证码 + 门户登录 + 教务系统导航

⑧ 点击"开始"
        ↓  start_main_loop_in_thread()
        ↓  创建 MainLoopThread，传入 browser 和 index_current_data
        ↓  后台线程读取 data.json，按批次（每批最多49条）填入网页表单
        ↓  填完后点击"查询"按钮提交，更新 index_current_data
⑨ 本批完成后 finished 信号触发 on_main_loop_finished()，可继续下一批
```

---

## 六、关键实现详解

### 6.1 Excel 数据导入

```python
def import_file_for_table_widget(self):
    file_path = QFileDialog.getOpenFileName(...)[0]   # 弹出文件选择对话框
    workbook = load_workbook(file_path)               # openpyxl 读取 xlsx
    self.sheet = workbook.active                      # 取活跃工作表
    # 遍历所有单元格，逐一写入 QTableWidget
    for row in range(rows):
        for col in range(cols):
            cell_value = self.sheet.cell(row+1, col+1).value
            self.table_widget.setItem(row, col, QTableWidgetItem(str(cell_value)))
```

### 6.2 自定义列范围解析

用户可在 UI 输入框中指定 `(行,列)` 格式的起止坐标（例如姓名起始 `(9,5)`，结束 `(200,5)`）：

```python
# 解析形如 "(9,5)" 的字符串
row_str, col_str = "(9,5)".strip("()").split(',')
start_row = int(row_str) - 1   # 转为 0-indexed
start_col = int(col_str) - 1
```

若未启用自定义模式，则使用硬编码默认值：**第 9 行起，第 5/6/7 列**（分别对应姓名/学号/分数）。

### 6.3 数据序列化与去重（save_to_json）

```python
def save_to_json(self):
    data_list = []
    unique_ids = set()

    # 从表格3读取所有行，构建字典列表
    # 注意：unique_id 使用 names.index(name) 取姓名首次出现的行号，
    # 若存在同名学生，其 unique_id 相同，后续去重逻辑会将同名行识别为重复项。
    for name, xuehao, score in zip(names, xuehaos, scores):
        if name and xuehao and score:
            data_list.append({
                "unique_id": names.index(name),
                "name": name,
                "stu_id": xuehao,
                "score": score
            })

    # 去重：若 unique_id 已存在且开关打开，则标记删除
    for data in data_list:
        if data['unique_id'] in unique_ids and self.duplicate_filter_btu.isChecked():
            to_remove.append(data)
        else:
            unique_ids.add(data['unique_id'])

    # 重新分配连续的 unique_id，写入 JSON 文件
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)
```

### 6.4 浏览器自动化登录（open_broswer）

使用 **DrissionPage** 驱动 Chromium（微软 Edge），按顺序执行：

```
1. Chromium(co).latest_tab.get(vpn_url)        → 打开 VPN 登录页
2. ele("@tabindex=1").input(name)               → 输入 VPN 用户名
3. ele("@id=loginPwd").input(pwrd)              → 输入 VPN 密码
4. get_rand_code(captcha_img.get_screenshot())  → OCR 识别验证码
5. ele("@tabindex=3").input(result)             → 输入验证码
6. ele("@class=button button--normal").click()  → 点击登录
7. ele("@title=综合信息门户").click()            → 进入门户
8. ele("@id=User_ID").input(info_name)          → 输入门户账号
9. ele("@id=btnLogin").click()                  → 门户登录
10. ele("教务系统").click()                      → 进入教务系统
11. ele("新增操行成绩").click()                  → 定位成绩录入表单
```

每一步通过元素的 `@id`、`@class`、`@tabindex`、`@title` 等属性精准定位 DOM 节点。

### 6.5 OCR 验证码识别（ocr_recognize.py）

```python
def get_rand_code(base64_img: str) -> Optional[str]:
    # 向百度 OCR API 发送 base64 编码的验证码截图
    response = requests.post(ocr_api_url, data={"image": base64_img}, ...)
    words_result = response.json()['words_result']

    # 提取纯数字，不足4位在右侧补0；若完全无数字则返回 None（由调用方处理）
    digits = ''.join(c for c in words_result[0]['words'] if c.isdigit())
    if not digits:
        return None           # 识别结果中无数字，调用方应提示用户手动输入
    return digits.ljust(4, '0')
```

验证码图片由 DrissionPage 的 `.get_screenshot(as_base64="jpg")` 直接截取为 base64 字符串，无需落盘。

### 6.6 批量填表（MainLoopThread）

后台线程继承 `QThread`，避免长时间填表操作阻塞 UI 主线程：

```python
class MainLoopThread(QThread):
    finished = pyqtSignal()          # 本批完成时通知主线程

    def run(self):
        start_index = self.index_current_data
        end_index = min(start_index + 49, len(self.data))  # 每批最多 49 条

        for i in range(start_index, end_index):
            # 网页中表单字段 ID 规则：txtstu1~txtstu49 / txtpoint1~txtpoint49
            xuehao_ele = self.last_tab.ele(f"@id=txtstu{(i % 49) + 1}")
            score_ele  = self.last_tab.ele(f"@id=txtpoint{(i % 49) + 1}")
            xuehao_ele.input(data[i]['stu_id'])
            score_ele.input(data[i]['score'])

        # 点击所有"查询"按钮触发保存
        for btn in self.last_tab.eles("@value=查询"):
            btn.click()

        self.parent.index_current_data = end_index  # 更新批次指针
```

**断点续传**：`index_current_data` 记录上次结束的位置，点击"开始"按钮时从该位置继续，支持分批多次提交。

---

## 七、配置系统（config/CONFIG.py）

通过 `configparser` 读写 `config.ini`，统一管理所有可配置项：

```python
READ_CONFIG("vpn", "vpn_name")        # 读取 VPN 用户名
WRITE_CONFIG("date", "today", "2025") # 写入今日日期
```

`config.ini` 主要区段：

| 区段 | 内容 |
|------|------|
| `[vpn]` | VPN 登录地址、账号、密码 |
| `[info]` | 综合信息门户账号、密码 |
| `[ocr]` | Baidu OCR API 地址与 Token |
| `[chromium_options]` | 浏览器路径与调试端口地址 |
| `[version]` | 应用版本号与代码仓库地址 |

---

## 八、其他模块说明

### DynamicIsland（顶部状态栏）

- 每 60 秒刷新一次当前时间（`HH:MM:SS`）
- 每 5 分钟通过 `psutil` 查询电池电量
- 作者名字带颜色动画效果

### GlobalLeftWindow（左侧抽屉）

- 音量控制：通过 `pycaw`（Windows Core Audio API）获取/设置系统音量
- 亮度控制：通过 `wmi`（Windows Management Instrumentation）读写屏幕亮度
- 快捷键：`Ctrl + A` 打开/关闭左侧抽屉

### 消息通知（send_message.py）

统一封装通知弹窗，支持 5 种类型（错误 / 信息 / 成功 / 警告 / 严重），通过 `SiGlobal` 获取主窗口引用后在右下角弹出。

---

## 九、完整数据流示意图

```
┌─────────────┐
│  Excel 文件  │
└──────┬──────┘
       │ openpyxl.load_workbook()
       ▼
┌─────────────────┐
│  表格1（原始）   │  ← 全量列，包含表头等无关行
└──────┬──────────┘
       │ reload_data_for_new_table_widget()
       │ 按列范围提取 (行,列) → 三列标准化
       ▼
┌─────────────────┐
│  表格3（标准化） │  ← 姓名 / 学号 / 分数，三列
└──────┬──────────┘
       │ save_to_json()  去重 + 序号重排
       ▼
┌──────────────┐
│  data.json   │
└──────┬───────┘
       │ MainLoopThread.run()  每批最多49条
       ▼
┌────────────────────────┐
│  Chromium（Edge）浏览器 │
│  txtstu1~txtstu49      │  ← 学号输入框
│  txtpoint1~txtpoint49  │  ← 分数输入框
└────────────────────────┘
       │ eles("@value=查询").click()
       ▼
   教务系统保存成功
```

---

## 十、环境配置与运行

详见 [docs/readme.md](docs/readme.md)，核心步骤：

```bash
pip install -r requirements.txt
# 另需手动安装 siui（PyQt-SiliconUI）
python start.py
```

使用前需在 `config/config.ini` 中填写：
- `[vpn]` 区段的 VPN 账号密码
- `[info]` 区段的门户账号密码
- `[ocr]` 区段的 Baidu OCR access_token
