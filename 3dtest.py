from PyQt5.Qt3DRender import QObjectPicker
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.Qt3DCore import QEntity, QTransform
from PyQt5.Qt3DExtras import (
    Qt3DWindow, QCuboidMesh, QPhongMaterial, QOrbitCameraController
)
from PyQt5.QtGui import QColor, QVector3D

import os
import sys

# 设置插件路径（根据实际路径修改）
os.environ[
    "QT_QPA_PLATFORM_PLUGIN_PATH"] = r"C:\Users\33974\.conda\envs\PyQt5\Lib\site-packages\PyQt5\Qt5\plugins\platforms"


class Rotatable3DApp(Qt3DWindow):
    def __init__(self):
        super().__init__()

        # 初始化场景
        self.rootEntity = QEntity()
        self.setRootEntity(self.rootEntity)

        # 创建模型
        self.models = []
        self.create_model(QVector3D(-2, 0, 0), QColor(255, 0, 0))  # 红色立方体
        self.create_model(QVector3D(2, 0, 0), QColor(0, 0, 255))  # 蓝色立方体

        # 初始化相机
        self.setup_camera()

        # 初始化选中对象
        self.selected_model = None

    def create_model(self, position, color):
        """创建一个立方体模型"""
        modelEntity = QEntity(self.rootEntity)

        # 创建立方体网格
        mesh = QCuboidMesh()

        # 创建材质
        material = QPhongMaterial()
        material.setDiffuse(color)

        # 设置模型变换
        transform = QTransform()
        transform.setTranslation(position)

        # 添加鼠标拾取功能
        picker = QObjectPicker(modelEntity)
        picker.clicked.connect(self.on_model_clicked)

        # 组装模型
        modelEntity.addComponent(mesh)
        modelEntity.addComponent(material)
        modelEntity.addComponent(transform)
        modelEntity.addComponent(picker)

        # 保存模型及其变换
        self.models.append({"entity": modelEntity, "transform": transform})

    def setup_camera(self):
        """设置相机和控制器"""
        camera = self.camera()
        camera.lens().setPerspectiveProjection(45.0, 16.0 / 9.0, 0.1, 1000.0)
        camera.setPosition(QVector3D(0, 5, 15))
        camera.setViewCenter(QVector3D(0, 0, 0))

        # 添加相机轨道控制器
        camController = QOrbitCameraController(self.rootEntity)
        camController.setCamera(camera)

    def on_model_clicked(self, event):
        """处理模型的单击事件"""
        for model in self.models:
            if model["entity"] == event.entity():
                self.selected_model = model
                print("Model selected:", model["entity"].objectName)
                break

    def rotate_selected_model(self, axis, angle):
        """旋转选中的模型"""
        if self.selected_model:
            transform = self.selected_model["transform"]
            rotation = transform.rotation()
            transform.setRotation(rotation * QVector3D(axis) * angle)

    def keyPressEvent(self, event):
        """处理键盘事件，实现旋转"""
        if self.selected_model:
            if event.key() == Qt.Key_Left:
                self.rotate_selected_model(QVector3D(0, 1, 0), 10)  # 左转
            elif event.key() == Qt.Key_Right:
                self.rotate_selected_model(QVector3D(0, 1, 0), -10)  # 右转
            elif event.key() == Qt.Key_Up:
                self.rotate_selected_model(QVector3D(1, 0, 0), 10)  # 向上转
            elif event.key() == Qt.Key_Down:
                self.rotate_selected_model(QVector3D(1, 0, 0), -10)  # 向下转


def main():
    app = QApplication(sys.argv)
    window = Rotatable3DApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
