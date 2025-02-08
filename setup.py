#  Copyright (c) 2025 UF4OVER
#   All rights reserved.


from cx_Freeze import setup, Executable


VERSION_A = "1.1.5"
import config.CONFIG as F
F.WRITE_CONFIG("version", "version", VERSION_A)  # 写入配置文件版本号

# 设置 GUI 基础
base = "Win32GUI"


def build_exe_cx_freeze():
    build_exe_options = {  # 构建选项
        "packages":  # 包
            [
                "PyQt5.QtCore",
                "PyQt5.QtGui",
                "PyQt5.QtWidgets",
                "PyQt5.QtMultimedia",
                "PyQt5.QtNetwork",
                "siui",
                "parts",
                "config",
                "openpyxl",
                "DrissionPage",
                "mutagen.mp3",
                "music",
                "pycaw",
                "wmi",
                "comtypes",
                "pic"
            ],
        "include_files":  # 包含文件
            [
            ],
        "excludes":  # 排除文件/包
            [
                "matplotlib",
                "backports",
                "PIL",
                "lib2to3",
                "cryptography",
                "setuptools",
                "tkinter",
                "unittest",
                "email",
                "pydoc",
            ],
        "optimize": 2  # 优化级别
    }

    setup(
        name='Wedding Invitation',  # 项目名称
        version=VERSION_A,  # 项目版本
        url='https://github.com/UF4OVER',  # 项目地址
        license='MIT',  # 许可证
        author='UF4',  # 作者
        author_email='uf4hp@foxmail.com',  # 邮箱
        description='Loot Hearts 系列',  # 描述
        options={"build_exe": build_exe_options},  # 构建选项
        executables=[  # 构建可执行文件
            Executable(
                script="start.py",  # 起始脚本
                target_name="Wedding Invitation",  # 可执行文件名
                base=base,  # GUI基础
                icon="pic/logo.ico"  # 图标
            )
        ]
    )


if __name__ == '__main__':
    build_exe_cx_freeze()
