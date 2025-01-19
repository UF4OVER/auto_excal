from PyQt5.QtCore import pyqtSignal

from siui.components.widgets.abstracts.widget import SiWidget


class FloatingLabel(SiWidget):
    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
