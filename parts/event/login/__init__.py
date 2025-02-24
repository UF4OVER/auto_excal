from PyQt5.QtCore import QThread, pyqtSignal
import importlib.util


class Login(QThread):  # 登录线程的基类
    loginStarted = pyqtSignal()
    loginFinished = pyqtSignal()
    loginErrored = pyqtSignal(str)

    def __init__(self, parent=None, main=None):
        super().__init__(parent)
        self.main_login = main

    def run(self):
        self.loginStarted.emit()
        try:
            print("Login_start")
            success = self.main_login()
            if success:
                self.loginFinished.emit()
            else:
                self.loginErrored.emit("登录失败，请重试")
        except Exception as e:
            self.loginErrored.emit(str(e))
        finally:
            print("Login_end")


class LoginGithub(Login):
    def __init__(self, parent=None):
        print("LoginGithub")
        main = self._import_main('login_github')
        super().__init__(parent, main)

    def _import_main(self, module_name):
        spec = importlib.util.spec_from_file_location(module_name, f"./parts/event/login/{module_name}.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.main


class LoginHuawei(Login):
    def __init__(self, parent=None):
        print("LoginHuawei")
        main = self._import_main('login_huawei')
        super().__init__(parent, main)

    def _import_main(self, module_name):
        spec = importlib.util.spec_from_file_location(module_name, f"./parts/event/login/{module_name}.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.main


if __name__ == "__main__":
    login = LoginGithub()
    login.start()
