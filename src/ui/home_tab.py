from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QSizePolicy
import cv2
from UI_g.home import Ui_Form as HomeUi
from src.utils.stats_manager import StatsManager

class HomeTab(QWidget, HomeUi):
    def __init__(self):
        super().__init__()
        self.ui = HomeUi()
        self.ui.setupUi(self)

        self.stats_mgr = StatsManager()

        # Kết nối sự kiện đổi mã hàng trên Combobox
        if hasattr(self.ui, 'cb_recipe'):
            self.ui.cb_recipe.currentTextChanged.connect(self.on_recipe_changed)

        # Khởi tạo dữ liệu hiển thị theo mã hàng đang chọn ban đầu
        self.on_recipe_changed()


        # --- 2. Khởi tạo biến đếm trong __init__ ---
        self.total_count = 0
        self.ok_count = 0
        self.ng_count = 0

        for lbl in [self.ui.lbl_step0, self.ui.lbl_step1_raw, self.ui.lbl_step1_bin, self.ui.lbl_step2]:
            # Cho phép label tự co giãn theo layout mà không ép bung kích thước cửa sổ
            lbl.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
            lbl.setScaledContents(False)

        # Khởi tạo trạng thái mặc định ban đầu: hiển thị dấu "-" cho cả 5 label
        self.reset_all_labels()

    def _mat_to_pixmap(self, cv_img):
        """Hàm phụ trợ chuyển đổi numpy mảng 2D (Gray) hoặc 3D (BGR) sang QPixmap an toàn"""
        if cv_img is None:
            return None
            
        if len(cv_img.shape) == 2:  # Ảnh nhị phân / xám (1 channel)
            h, w = cv_img.shape
            bytes_per_line = w
            q_img = QImage(cv_img.data, w, h, bytes_per_line, QImage.Format_Grayscale8).copy()
        else:  # Ảnh màu BGR (3 channels)
            rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_img.shape
            bytes_per_line = ch * w
            q_img = QImage(rgb_img.data, w, h, bytes_per_line, QImage.Format_RGB888).copy()
            
        return QPixmap.fromImage(q_img)

    def _render_to_label(self, label, pixmap):
        if pixmap and not pixmap.isNull():
            scaled = pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(scaled)

    def update_frame(self, step: int, bgr_image, thresh_image=None, is_ok=True):
        """Phân phối hiển thị lên 4 QLabel tùy theo step"""
        pix_main = self._mat_to_pixmap(bgr_image)

        # Step 0: Cam 1 - Đèn 1
        if step == 0:
            self._render_to_label(self.ui.lbl_step0, pix_main)
            print(1)

        # Step 1: Cam 1 - Đèn 2 (Hiển thị cùng lúc 2 Label: Ảnh gốc và Ảnh nhị phân)
        elif step == 1:
            self._render_to_label(self.ui.lbl_step1_raw, pix_main)
            if thresh_image is not None:
                pix_thresh = self._mat_to_pixmap(thresh_image)
                self._render_to_label(self.ui.lbl_step1_bin, pix_thresh)
            print(2)

        # Step 2: Cam 2 - Đèn 3
        elif step == 2:
            self._render_to_label(self.ui.lbl_step2, pix_main)
            print(3)

        print(f"✅ Đã hiển thị ảnh cho Step {step}")

    def update_summary(self, status: str):
        """
        Cập nhật số lượng và đổi màu trạng thái:
        - OK: Nền xanh lá (#4CAF50 hoặc #2ECC71), chữ màu ĐEN.
        - NG / TIMEOUT_NG: Nền đỏ (#F44336 hoặc #E74C3C), chữ màu ĐEN.
        """
        """Cập nhật kết quả: Lưu vào stats.json theo mã hàng hiện tại và cập nhật UI"""
        is_ok = (status == "OK")
        recipe = self.get_current_recipe()

        # 1. Cập nhật vào file stats.json
        updated_stats = self.stats_mgr.update_record(recipe, is_ok)

        # 2. Cập nhật số lượng đếm lên UI
        if hasattr(self.ui, 'lbl_total_count'):
            self.ui.lbl_total_count.setText(str(updated_stats["total_count"]))
        if hasattr(self.ui, 'lbl_ok'):
            self.ui.lbl_ok.setText(str(updated_stats["ok_count"]))
        if hasattr(self.ui, 'lbl_ng'):
            self.ui.lbl_ng.setText(str(updated_stats["ng_count"]))

        # Cập nhật hiển thị lên lbl_total (Nền màu + Chữ Đen)
        if hasattr(self.ui, 'lbl_total'):
            # Text hiển thị (Bạn có thể để chỉ "OK" / "NG" hoặc kèm số lượng)
            display_text = "OK" if is_ok else "NG"
            self.ui.lbl_total.setText(display_text)

            # Thiết lập màu nền & màu chữ đen (#000000)
            if is_ok:
                style = """
                    QLabel {
                        background-color: #2ECC71;
                        color: #000000;
                        font-weight: bold;
                        font-size: 28px;
                        border-radius: 8px;
                        border: 2px solid #27AE60;
                    }
                """
            else:
                style = """
                    QLabel {
                        background-color: #E74C3C;
                        color: #000000;
                        font-weight: bold;
                        font-size: 28px;
                        border-radius: 8px;
                        border: 2px solid #C0392B;
                    }
                """
            
            self.ui.lbl_total.setStyleSheet(style)

            # HẸN GIỜ ĐÚNG 2 GIÂY (2000ms) SAU ĐỂ RESET VÙNG HIỂN THỊ
            QTimer.singleShot(5000, self.reset_all_labels)
    
    def reset_all_labels(self):
        """Đưa 4 label ảnh và 1 label kết quả về trạng thái hiển thị dấu '-'."""
        
        # Style hiển thị dấu "-" cho 4 khung ảnh
        image_placeholder_style = """
            QLabel {
                background-color: #D1D8E0;
                color: #808E9B;
                font-size: 36px;
                font-weight: bold;
                border: 1px dashed #485460;
                border-radius: 4px;
            }
        """

        # 1. Reset 4 QLabel ảnh
        labels = ['lbl_step0', 'lbl_step1_raw', 'lbl_step1_bin', 'lbl_step2']
        for name in labels:
            if hasattr(self.ui, name):
                lbl = getattr(self.ui, name)
                if hasattr(lbl, 'original_pixmap'):
                    lbl.original_pixmap = None
                lbl.clear()
                lbl.setText("-")
                lbl.setAlignment(Qt.AlignCenter)
                lbl.setStyleSheet(image_placeholder_style)

        # 2. Reset lbl_total về dấu "-"
        if hasattr(self.ui, 'lbl_total'):
            self.ui.lbl_total.setText("-")
            self.ui.lbl_total.setAlignment(Qt.AlignCenter)
            self.ui.lbl_total.setStyleSheet("""
                QLabel {
                    background-color: #2C3E50;
                    color: #BDC3C7;
                    font-weight: bold;
                    font-size: 28px;
                    border-radius: 8px;
                    border: 2px solid #34495E;
                }
            """)

    def get_current_recipe(self) -> str:
        """Lấy tên/mã hàng đang chọn trên Combobox"""
        if hasattr(self.ui, 'cb_recipe'):
            return self.ui.cb_recipe.currentText().strip()
        return "1"

    def on_recipe_changed(self):
        """Khi đổi Combobox: Load lại số lượng OK/NG từ JSON lên UI"""
        recipe = self.get_current_recipe()
        if not recipe:
            return

        stats = self.stats_mgr.get_stats_for_recipe(recipe)

        if hasattr(self.ui, 'lbl_total_count'):
            self.ui.lbl_total_count.setText(str(stats["total_count"]))
        if hasattr(self.ui, 'lbl_ok'):
            self.ui.lbl_ok.setText(str(stats["ok_count"]))
        if hasattr(self.ui, 'lbl_ng'):
            self.ui.lbl_ng.setText(str(stats["ng_count"]))