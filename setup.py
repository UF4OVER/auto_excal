from cx_Freeze import setup, Executable

pic_path = "E:\\python\\auto_excal_new\\siui\\pic"
build_exe_options = {
    "packages": [
        "PyQt5.QtCore",
        "PyQt5.QtGui",
        "PyQt5.QtWidgets",
        "siui",
        "icons",
        "parts",
        "config",
        "openpyxl",
        "ui",
        "DrissionPage",
        "pygame.mixer",
        "mutagen.mp3",
        "music",
        "pycaw",
        "wmi",
        "comtypes"
    ],
    "include_files": [
        (pic_path, "pic"),
    ],
    "excludes": [
        "scipy",
        "scipy.libs",
        "matplotlib",
        "backports",        # 通常用于兼容旧版 Python，如果您运行的是现代 Python 版本（如 3.8+），可以移除。
        "PIL",
        "lib2to3",
        "setuptools",
        "tkinter",          # 排除 tkinter 以减小体积
        "unittest",         # 排除测试模块
        "email",            # 排除 email 模块
        "pydoc",            # 排除文档模块
    ],
    # "zip_include_packages": ["*"],
    # #
    # "zip_exclude_packages": ["siui",
    #                          "ui",
    #                          "icons",
    #                          "config",
    #                          "music"
    #                          ]
}

# 设置 GUI 基础
base = "Win32GUI"

setup(
    name='Wedding Invitation',
    version='1.1.2',
    url='https://github.com/UF4OVER',
    license='MIT',
    author='UF4',
    author_email='uf4hp@foxmail.com',
    description='Wedding Invitation 系列',
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            script="start.py",
            target_name="Wedding Invitation",
            base=base,
            icon="pic/圆角-default_256x256.ico"
        )
    ]
)
