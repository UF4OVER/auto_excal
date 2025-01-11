1.安装虚拟环境

```bash
pip3 install virtualenv 
```

2.创建一个空的虚拟环境，不指定版本则解释器与当前项目使用的版本相同

```bash
virtualenv [virutalenv name]
```

3.指定虚拟环境的解释器

```bash
virtualenv -p XXX\python.exe [virutalenv name]
```

4.在解释器中切换解释器

5.在pip安装其他的包

6.qt项目需要设置环境变量来确保你的项目中的qt是来自虚拟环境的
QT_PLUGIN_PATH=siui\[virutalenv name]\Lib\site-packages\PyQt5\Qt5\plugins