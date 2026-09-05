from PySide6.QtWidgets import QWidget
from UI_g.setting import Ui_Form as SettingUi

class SettingTab(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = SettingUi()
        self.ui.setupUi(self)

    def c(self):
        pass