from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Signal, QThread


from UI_g.MW import Ui_MainWindow as MainUi
from src.ui.home_tab import HomeTab
from src.ui.history_tab import HistoryTab
from src.ui.setting_tab import SettingTab

class QueueWorkerThread(QThread):
    data_received = Signal(dict)

    def __init__(self, res_queue, stop_event):
        super().__init__()
        self.res_queue = res_queue
        self.stop_event = stop_event


    def run(self):
        while not self.stop_event.is_set():
            try:
                data = self.res_queue.get(timeout=0.05)
                self.data_received.emit(data)
            except:
                continue

class UiMainWindow(QMainWindow):
    def __init__(self, stop_event, res_queue):
        super().__init__()
        self.ui = MainUi()
        self.ui.setupUi(self)

        self.stop_event = stop_event

        self.setWindowTitle("ELENTEC-WRMC-VISION SYSTEM V1.0")
        
        self.home_tab = HomeTab()
        self.setting_tab = SettingTab()
        self.history_tab = HistoryTab()

        self.ui.tabWidget.addTab(self.home_tab, "Nhà")
        self.ui.tabWidget.addTab(self.setting_tab, "Cài đặt")
        self.ui.tabWidget.addTab(self.history_tab, "Lịch sử")

        # Khởi động Thread nhận tín hiệu
        self.worker_thread = QueueWorkerThread(res_queue, self.stop_event)
        self.worker_thread.data_received.connect(self.handle_incoming_data)
        self.worker_thread.start()

    def handle_incoming_data(self, packet):
        p_type = packet.get("type")
        if p_type == "FRAME":
            self.home_tab.update_frame(
                step=packet.get("step"),
                bgr_image=packet.get("image"),
                thresh_image=packet.get("thresh_image", None),
                is_ok=packet.get("ok", True)
            )
        elif p_type == "RESULT":
            self.home_tab.update_summary(status=packet["status"])

    def closeEvent(self, event):
        self.stop_event.set()
        self.worker_thread.wait()
        event.accept()