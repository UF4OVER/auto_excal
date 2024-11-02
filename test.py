import threading
import time
from tkinter import Tk, Button
from pynput import mouse

class mouse_detection_threads(threading.Thread):
    """
    处理鼠标双击的子线程
    """

    def __init__(self, parent=None):
        super().__init__()
        self.running = False
        self.paused = False
        self.double_click_count = 0
        self.double_click_threshold = 0.3  # 双击时间阈值（秒）
        self.last_click_time = 0
        self.parent = parent
        self.listener = None

    def on_click(self, x, y, button, pressed):
        """处理鼠标点击事件"""
        if pressed and button == mouse.Button.left:
            current_time = time.time()
            if current_time - self.last_click_time < self.double_click_threshold:
                self.double_click_count += 1
                self.last_click_time = current_time
                if self.double_click_count >= 2:
                    self.parent.on_double_click()
                    self.double_click_count = 0
            else:
                self.double_click_count = 1
                self.last_click_time = current_time

    def run(self):
        self.running = True
        while self.running:
            if not self.paused:
                if self.listener is None:
                    self.listener = mouse.Listener(on_click=self.on_click)
                    self.listener.start()
                self.listener.join(1)
            else:
                if self.listener is not None:
                    self.listener.stop()
                    self.listener = None
                time.sleep(0.1)

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.running = False
        if self.listener:
            self.listener.stop()


class MouseDetectionApp:
    def __init__(self, root):
        self.root = root
        self.thread = mouse_detection_threads(parent=self)
        self.button_used = False

        # 创建按钮
        self.button = Button(root, text="Start/Stop Detection", command=self.toggle_detection)
        self.button.pack()

    def toggle_detection(self):
        if self.button_used:
            return

        if self.thread.is_alive():
            self.thread.pause()
            self.button.config(text="Resume Detection")
        else:
            self.thread = mouse_detection_threads(parent=self)  # 重新初始化线程
            self.thread.start()
            self.button.config(text="Pause Detection")
            self.button_used = True
            self.button.config(state="disabled")  # 禁用按钮

    def on_double_click(self):
        print("Double click detected!")


# 主程序入口
if __name__ == "__main__":
    root = Tk()
    app = MouseDetectionApp(root)
    root.mainloop()
