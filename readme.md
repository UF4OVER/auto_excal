## 编译应用
### 1. 编译应用的前提
1. 编译前，请确保已经安装好 **python3.10**
2. 升级pip到最新版本 `pip install --upgrade pip`
3. 安装 virtualenv 管理环境 `pip install virtualenv`
4. 创建一个虚拟环境 `virtualenv [virutalenv name]`
    ```bash
    virtualenv [virutalenv name] # 创建一个虚拟环境
   
    virtualenv -p XXX\python.exe [virutalenv name] # 激活虚拟环境
    ```
5. 切换其他解释器到`[virutalenv name]`的解释器
   ```bash
   (base) (siui_env) PS E:\python\auto_excal_new\siui>conda deactivate  # 退出conda的base环境
   
   (siui_env) PS E:\python\auto_excal_new\siui>
   ```
6. 安装依赖包`pip install -r requirements.txt`
7. 注意，`siui` 的库并不能在 `PyPi` 上安装,你可以克隆这个项目，然后安装到本地<BR>
   ```bash
   git clone https://github.com/ChinaIceF/PyQt-SiliconUI.git  # 克隆项目到本地
   
   cd PyQt-SiliconUI
   
   python setup.py install # 注意安装到虚拟环境
   ```
   
8. 至此，环境搭建完成，可以开始编译了
### 2. 编译应用
1. 进入项目根目录，执行命令 `pytho n setup.py build`
2. 可能有的库缺少，请手动查询安装，或者使用 `pip install -r requirements.txt`
3. 上两部步完成后，会生成 `build` 文件夹，`build` 文件夹下生成一个 `exe.win-amd64-3.10` 文件夹，打开这个文件夹，找到 `Wedding Invitation.exe` 文件，双击运行即可
4. 再将`upx.exe`添加到环境变量中，然后在根目录下执行`python zip.py`,并等待压缩完成
5. 将`ce.nsi`文件移动到`build`文件夹下，执行`makensis.exe ce.nsi`命令或者使用HM NIS Edit打开并编译，等待编译完成
### 3. 运行应用
在`build\exe.win-amd64-3.10`文件夹下找到`setup.exe`文件，双击运行即可