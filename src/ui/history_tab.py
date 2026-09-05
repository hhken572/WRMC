from PySide6.QtWidgets import QWidget
from UI_g.history import Ui_Form as HistoryUi

class HistoryTab(QWidget, HistoryUi):
    def __init__(self):
        super().__init__()
        self.ui = HistoryUi()
        self.ui.setupUi(self)

    def b(self):
        pass