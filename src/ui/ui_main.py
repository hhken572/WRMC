#src/ui/ui_main.py
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Signal, QThread
from UI_g.MW import Ui_MainWindow as MainUi
from src.ui.home_tab import HomeTab
from src.ui.history_tab import HistoryTab
from src.ui.setting_tab import SettingTab
from src.utils.ng_image_manager import AsyncNGImageSaver

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
            except Exception:
                continue

class UiMainWindow(QMainWindow):
    def __init__(self, stop_event, res_queue, rule_queue=None):
        super().__init__()
        self.ui = MainUi()
        self.ui.setupUi(self)

        self.stop_event = stop_event

        self.setWindowTitle("ELENTEC-WRMC-VISION SYSTEM V1.0")

        # Bộ đệm giữ 4 ảnh trong 1 chu kỳ kiểm tra
        self.current_step1_images = None
        self.current_step2_image = None

        self.home_tab = HomeTab()
        self.setting_tab = SettingTab(rule_queue=rule_queue)
        self.history_tab = HistoryTab()

        self.ui.tabWidget.addTab(self.home_tab, "Nhà")
        self.ui.tabWidget.addTab(self.setting_tab, "Cài đặt")
        self.ui.tabWidget.addTab(self.history_tab, "Lịch sử")

        # Khởi động Thread nhận tín hiệu từ hàng đợi
        self.worker_thread = QueueWorkerThread(res_queue, self.stop_event)
        self.worker_thread.data_received.connect(self.handle_incoming_data)
        self.worker_thread.start()

    def handle_incoming_data(self, packet):
        p_type = packet.get("type")

        # Pha 1: Nhận kết quả chụp Cam 1 (AI 1 + Binarize trực quan + Đo góc deskew)
        if p_type == "FRAME_STEP1":
            ai_img = packet.get("ai_image")
            bin_img = packet.get("bin_vis_image")
            deskew_img = packet.get("deskew_image")

            self.current_step1_images = (ai_img, bin_img, deskew_img)

            self.home_tab.update_step1_display(
                ai_image=ai_img,
                bin_vis_image=bin_img,
                deskew_image=deskew_img
            )

        # Pha 2: Nhận kết quả chụp Cam 2 (AI 3)
        elif p_type == "FRAME_STEP2":
            ai_cam2_img = packet.get("image")
            self.current_step2_image = ai_cam2_img

            self.home_tab.update_step2_display(
                ai_image=ai_cam2_img
            )

        # Tổng kết chu kỳ kiểm tra
        elif p_type == "RESULT":
            status = packet.get("status", "NG")
            self.home_tab.update_summary(status=status)

            # Nếu kết quả là NG -> Lưu ghép 4 hình vào folder trong background thread (Zero latency to inference)
            if status != "OK":
                img1, img2, img3 = self.current_step1_images if self.current_step1_images else (None, None, None)
                img4 = self.current_step2_image

                AsyncNGImageSaver.get_instance().save_ng(
                    img1=img1,
                    img2=img2,
                    img3=img3,
                    img4=img4,
                    status=status,
                    on_saved_callback=self.history_tab.handle_new_ng_saved
                )

            # Đặt lại bộ đệm cho chu kỳ mới
            self.current_step1_images = None
            self.current_step2_image = None

    def closeEvent(self, event):
        self.stop_event.set()
        self.worker_thread.wait()
        event.accept()