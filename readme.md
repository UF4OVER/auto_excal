AUTO
========
Auto is a tool for automatically filling in data in Excel files. It can automatically fill in data based on the position of the mouse cursor, and also supports manual input of data. It can also automatically save data to a JSON file.

> <b>if you have any questions, please contact me.<br><br><br>
> <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>联系方式</title>
  <style>
    .contact-container {
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
      background-color: rgba(60,116,129,0.55);
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      max-width: 600px;
      margin: 0 auto;
    }

    .contact-title {
      font-size: 24px;
      color: #333;
      margin-bottom: 10px;
    }

    .contact-info {
      display: flex;
      justify-content: space-around;
      width: 100%;
    }

    .contact-item {
      text-align: center;
    }

    .contact-item img {
      width: 50px;
      height: 50px;
      margin-bottom: 10px;
    }

    .contact-item p {
      margin: 0;
    }

    .contact-item p.title {
      font-size: 18px;
      color: #555;
    }

    .contact-item p.content {
      font-size: 16px;
      color: #777;
    }
  </style>
</head>
<body>
  <div class="contact-container">
    <div class="contact-title">
      <b>联系方式</b>
    </div>
    <div class="contact-info">
      <div class="contact-item">
        <img src="docs/邮箱登录.png" alt="Email Icon">
        <p class="title">邮箱</p>
        <p class="content">uf4hp
                    @foxmail.com</p>
      </div>
      <div class="contact-item">
        <img src="docs/手机登录.png" alt="Phone Icon">
        <p class="title">电话</p>
        <p class="content">+86 155 8406 5081(假)</p>
      </div>
      <div class="contact-item">
        <img src="docs/img_4.png" alt="Address Icon">
        <p class="title">地址</p>
        <p class="content">China NEEPU</p>
      </div>
    </div>
  </div>
</body>
</html>

> Author: [HePing](https://github.com/UF4OVER) `click green to see more information`. <br>
> Contact Me: [WeChat](https://github.com/UF4OVER/auto_excal/blob/master/docs/img_1.png) `cilck the green to add me.`<br>

## The First: Usage
- Run the application.
    - Windows: Double-click `原神.exe`
    - macOS: not Available At This Time
  - and you can see the following window:
  -![img.png](docs/img.png)
  - then select the Excel file you want to fill in data.
  -![GIF1.gif](docs/GIF1.gif)
  - if you want to add data, you can click the `添加` button，of course, you can also add author information hhhhhh....
  - then you can push the `开始` button to start monitoring.:
  - open the website you need to input data, then click the left mouse button, if a double click is detected, then the data will be automatically populated, and the data will be automatically saved to a JSON file.
  - if you want to creat a new table, you can click the `结束` button，this button will only pause the double-click thread and will not stop the entire program.
- Theme：
  - you can change the theme of the application by clicking the following button.
  - ![GIF2.gif](docs/GIF2.gif)
- small window:
  - you can click the `小窗` button to open a small window and the small window will be displayed on the <b>TOP</b> of the other window.
  - ![GIF3.gif](docs/GIF3.gif)

## The End

### 控制流图
#### 1.主窗口控制流图
```mermaid
flowchart TD
    A[启动应用] --> B[初始化主窗口]
    B --> C[设置UI和信号槽]
    C --> D[等待用户操作]
    D -->|选择文件| E[加载Excel文件]
    E --> F[解析文件并显示数据]
    D -->|开始监控| G[启动鼠标双击线程]
    G --> H{是否检测到双击?}
    H -->|是| I[处理双击事件]
    I --> J[自动填充数据]
    J --> K[更新UI]
    H -->|否| L[继续监控]
    D -->|停止监控| M[停止鼠标双击线程]
    M --> N[更新UI]
    D -->|添加数据| O[弹出输入框]
    O --> P[添加数据到表格]
    P --> Q[保存数据]
    D -->|保存数据| R[保存表格数据到JSON文件]
    R --> S[更新UI]
    D -->|打开小窗口| T[初始化小窗口]
    T --> U[显示小窗口]
    U --> V[更新小窗口数据]
    V --> W[等待小窗口操作]
    W -->|关闭小窗口| X[隐藏小窗口]
    X --> Y[更新主窗口数据]
    D -->|关闭应用| Z[退出应用]
```

#### 2.小窗口控制流图

```mermaid
flowchart TD
    A[初始化小窗口] --> B[设置UI和信号槽]
    B --> C[等待用户操作]
    C -->|关闭窗口| D[隐藏小窗口]
    C -->|清除表格| E[清空表格内容]
    C -->|更新数据| F[接收主窗口数据]
    F --> G[更新表格显示]
    G --> H[高亮行]
    H --> I[更新UI]

```


#### 3.鼠标双击监控线程控制流图
```mermaid
flowchart TD
    A[启动线程] --> B[初始化变量]
    B --> C{是否运行?}
    C -->|否| D[停止线程]
    C -->|是| E{是否暂停?}
    E -->|是| F[等待恢复]
    F --> C
    E -->|否| G[监听鼠标点击事件]
    G --> H{是否双击?}
    H -->|否| I[记录点击时间]
    I --> G
    H -->|是| J[处理双击事件]
    J --> K[通知主窗口]
    K --> G

```

#### 4.单元格点击线程控制流图
```mermaid

flowchart TD
    A[启动线程] --> B[获取单元格位置]
    B --> C[发送点击信号]
    C --> D[结束线程]

```
