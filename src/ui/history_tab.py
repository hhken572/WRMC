import os
import subprocess
from datetime import datetime
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QListWidgetItem, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QImage, QKeySequence, QShortcut
from UI_g.history import Ui_Form as HistoryUi
from src.utils.ng_image_manager import DEFAULT_NG_DIR


class ImageViewerDialog(QDialog):
    """Cửa sổ xem chi tiết ảnh ghép NG: hỗ trợ nút Qua/Về, phím mũi tên ⬅ ➡, phóng to co giãn theo cửa sổ."""
    def __init__(self, image_paths: list, current_index: int = 0, parent=None):
        super().__init__(parent)
        self.image_paths = image_paths
        self.current_index = max(0, min(current_index, len(image_paths) - 1)) if image_paths else 0
        self.current_pixmap = None

        self.setWindowTitle("CHI TIẾT HÌNH ẢNH SẢN PHẨM NG (GHÉP 4 KHUNG)")
        self.resize(1100, 720)
        self.setMinimumSize(800, 500)

        # Style giao diện tối hiện đại
        self.setStyleSheet("""
            QDialog {
                background-color: #1E272E;
                color: #FFFFFF;
            }
            QLabel {
                color: #FFFFFF;
                font-family: Arial;
            }
            QPushButton {
                background-color: #2F3640;
                color: #F5F6FA;
                border: 1px solid #718093;
                border-radius: 6px;
                padding: 8px 18px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #353B48;
                border-color: #00A8FF;
                color: #00A8FF;
            }
            QPushButton:pressed {
                background-color: #192A56;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(10)

        # 1. Thanh tiêu đề thông tin ảnh
        header_layout = QHBoxLayout()
        self.lbl_title = QLabel("Đang tải ảnh...")
        self.lbl_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #E74C3C;")
        header_layout.addWidget(self.lbl_title)

        header_layout.addStretch()

        self.lbl_counter = QLabel("")
        self.lbl_counter.setStyleSheet("font-size: 14px; color: #FBC531; font-weight: bold;")
        header_layout.addWidget(self.lbl_counter)
        layout.addLayout(header_layout)

        # 2. Khung hiển thị ảnh chính
        self.lbl_image = QLabel()
        self.lbl_image.setAlignment(Qt.AlignCenter)
        self.lbl_image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lbl_image.setStyleSheet("background-color: #0C1013; border: 1px solid #353B48; border-radius: 4px;")
        layout.addWidget(self.lbl_image, stretch=1)

        # 3. Thanh điều hướng nút bấm bên dưới
        nav_layout = QHBoxLayout()
        self.btn_prev = QPushButton("◀ Ảnh trước (Phím ⬅)")
        self.btn_prev.clicked.connect(self.show_prev)
        nav_layout.addWidget(self.btn_prev)

        self.btn_next = QPushButton("Ảnh sau ▶ (Phím ➡)")
        self.btn_next.clicked.connect(self.show_next)
        nav_layout.addWidget(self.btn_next)

        nav_layout.addStretch()

        self.btn_open_folder = QPushButton("📁 Mở thư mục")
        self.btn_open_folder.clicked.connect(self.open_current_folder)
        nav_layout.addWidget(self.btn_open_folder)

        self.btn_close = QPushButton("✕ Đóng (Esc)")
        self.btn_close.clicked.connect(self.close)
        nav_layout.addWidget(self.btn_close)

        layout.addLayout(nav_layout)

        # Phím tắt bàn phím
        QShortcut(QKeySequence(Qt.Key_Left), self, self.show_prev)
        QShortcut(QKeySequence(Qt.Key_Right), self, self.show_next)
        QShortcut(QKeySequence(Qt.Key_Escape), self, self.close)

        self.load_current_image()

    def load_current_image(self):
        if not self.image_paths or self.current_index >= len(self.image_paths):
            self.lbl_title.setText("Không có hình ảnh để hiển thị")
            self.lbl_counter.setText("0 / 0")
            self.lbl_image.clear()
            self.current_pixmap = None
            return

        file_path = self.image_paths[self.current_index]
        if file_path and os.path.exists(file_path):
            self.current_pixmap = QPixmap(file_path)
            self._render_pixmap()

            filename = os.path.basename(file_path)
            time_display = filename.replace(".jpg", "").replace(".png", "").replace("_", ":")
            parent_day = os.path.basename(os.path.dirname(file_path))

            self.lbl_title.setText(f"LỖI NG | Ngày: {parent_day} - Giờ: {time_display}")
            self.lbl_counter.setText(f"Ảnh {self.current_index + 1} / {len(self.image_paths)}")
        else:
            self.lbl_title.setText(f"File không tồn tại: {file_path}")
            self.lbl_image.clear()
            self.current_pixmap = None

        self.btn_prev.setEnabled(self.current_index > 0)
        self.btn_next.setEnabled(self.current_index < len(self.image_paths) - 1)

    def _render_pixmap(self):
        if self.current_pixmap and not self.current_pixmap.isNull():
            target_size = self.lbl_image.size()
            scaled = self.current_pixmap.scaled(
                target_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.lbl_image.setPixmap(scaled)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._render_pixmap()

    def show_prev(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_current_image()

    def show_next(self):
        if self.current_index < len(self.image_paths) - 1:
            self.current_index += 1
            self.load_current_image()

    def open_current_folder(self):
        if self.image_paths and self.current_index < len(self.image_paths):
            folder = os.path.dirname(self.image_paths[self.current_index])
            if os.path.exists(folder):
                subprocess.Popen(f'explorer "{os.path.abspath(folder)}"')


class HistoryTab(QWidget, HistoryUi):
    # Signal kết nối an toàn từ background thread sang GUI thread khi có ảnh NG mới được lưu
    ng_saved_signal = Signal(str, object)

    def __init__(self, base_dir=DEFAULT_NG_DIR):
        super().__init__()
        self.ui = HistoryUi()
        self.ui.setupUi(self)
        self.base_dir = base_dir

        self.ng_saved_signal.connect(self._on_ng_saved_in_gui)

        # Style ListWidget hiển thị danh sách ảnh NG đẹp mắt
        if hasattr(self.ui, 'lw_hinhanhNG'):
            self.ui.lw_hinhanhNG.setStyleSheet("""
                QListWidget {
                    background-color: #F8F9FA;
                    border: 1px solid #CED4DA;
                    border-radius: 6px;
                    font-size: 14px;
                    padding: 5px;
                }
                QListWidget::item {
                    height: 38px;
                    margin: 3px 0;
                    padding-left: 10px;
                    border-radius: 4px;
                    background-color: #FFFFFF;
                    border: 1px solid #E9ECEF;
                    color: #2D3436;
                    font-weight: bold;
                }
                QListWidget::item:hover {
                    background-color: #FFF3CD;
                    border-color: #FFEBAA;
                    color: #856404;
                }
                QListWidget::item:selected {
                    background-color: #E74C3C;
                    color: #FFFFFF;
                    border-color: #C0392B;
                }
            """)

        # Kết nối sự kiện tương tác
        if hasattr(self.ui, 'cb_sp_thang'):
            self.ui.cb_sp_thang.currentTextChanged.connect(self.on_month_changed)

        if hasattr(self.ui, 'cb_sp_ngay'):
            self.ui.cb_sp_ngay.currentTextChanged.connect(self.on_day_changed)

        if hasattr(self.ui, 'lw_hinhanhNG'):
            self.ui.lw_hinhanhNG.itemClicked.connect(self.on_image_item_clicked)
            self.ui.lw_hinhanhNG.itemDoubleClicked.connect(self.on_image_item_clicked)

        # Nạp dữ liệu ban đầu
        self.refresh_months()

    def handle_new_ng_saved(self, file_path: str, timestamp: datetime):
        """Được gọi từ background thread của AsyncNGImageSaver, phát tín hiệu sang GUI"""
        self.ng_saved_signal.emit(file_path, timestamp)

    def _on_ng_saved_in_gui(self, file_path: str, timestamp: datetime):
        """Xử lý trên GUI thread khi có ảnh NG mới được lưu"""
        month_str = timestamp.strftime("%Y-%m")
        day_str = timestamp.strftime("%Y-%m-%d")

        # Kiểm tra nếu tháng mới chưa có trong combobox thì thêm vào
        if hasattr(self.ui, 'cb_sp_thang'):
            months = [self.ui.cb_sp_thang.itemText(i) for i in range(self.ui.cb_sp_thang.count())]
            if month_str not in months:
                self.ui.cb_sp_thang.insertItem(0, month_str)

        # Nếu đang chọn đúng tháng và ngày hôm nay thì nạp lại danh sách ảnh
        cur_month = self.ui.cb_sp_thang.currentText().strip() if hasattr(self.ui, 'cb_sp_thang') else ""
        cur_day = self.ui.cb_sp_ngay.currentText().strip() if hasattr(self.ui, 'cb_sp_ngay') else ""

        if cur_month == month_str:
            if cur_day == day_str:
                self.load_images_for_day(cur_month, cur_day)
            else:
                self.on_month_changed(cur_month)

    def refresh_months(self):
        """Quét các thư mục tháng (YYYY-MM) trong data/ng_images/"""
        if not hasattr(self.ui, 'cb_sp_thang'):
            return

        self.ui.cb_sp_thang.blockSignals(True)
        self.ui.cb_sp_thang.clear()

        months = []
        if os.path.exists(self.base_dir):
            for entry in os.listdir(self.base_dir):
                full_p = os.path.join(self.base_dir, entry)
                if os.path.isdir(full_p) and len(entry) == 7 and "-" in entry:
                    months.append(entry)

        # Sắp xếp mới nhất lên đầu
        months.sort(reverse=True)

        current_month = datetime.now().strftime("%Y-%m")
        if current_month not in months:
            months.insert(0, current_month)

        for m in months:
            self.ui.cb_sp_thang.addItem(m)

        self.ui.cb_sp_thang.blockSignals(False)

        # Kích hoạt cập nhật ngày theo tháng đầu tiên
        self.on_month_changed(self.ui.cb_sp_thang.currentText())

    def on_month_changed(self, month_str: str):
        """Khi chọn tháng, quét các ngày (YYYY-MM-DD) trong thư mục tháng đó"""
        if not hasattr(self.ui, 'cb_sp_ngay') or not month_str:
            return

        self.ui.cb_sp_ngay.blockSignals(True)
        self.ui.cb_sp_ngay.clear()

        month_folder = os.path.join(self.base_dir, month_str)
        days = []
        if os.path.exists(month_folder):
            for entry in os.listdir(month_folder):
                full_p = os.path.join(month_folder, entry)
                if os.path.isdir(full_p):
                    days.append(entry)

        # Sắp xếp ngày mới nhất lên đầu
        days.sort(reverse=True)

        today_str = datetime.now().strftime("%Y-%m-%d")
        if today_str.startswith(month_str) and today_str not in days:
            days.insert(0, today_str)

        for d in days:
            self.ui.cb_sp_ngay.addItem(d)

        self.ui.cb_sp_ngay.blockSignals(False)

        # Kích hoạt cập nhật ảnh theo ngày đầu tiên
        self.on_day_changed(self.ui.cb_sp_ngay.currentText())

    def on_day_changed(self, day_str: str):
        """Khi chọn ngày, hiển thị danh sách các file ảnh NG trong thư mục ngày"""
        month_str = self.ui.cb_sp_thang.currentText().strip() if hasattr(self.ui, 'cb_sp_thang') else ""
        if not month_str or not day_str:
            return
        self.load_images_for_day(month_str, day_str)

    def load_images_for_day(self, month_str: str, day_str: str):
        if not hasattr(self.ui, 'lw_hinhanhNG'):
            return

        self.ui.lw_hinhanhNG.clear()
        target_dir = os.path.join(self.base_dir, month_str, day_str)

        if not os.path.exists(target_dir):
            item = QListWidgetItem("Chưa có ảnh NG nào trong ngày này")
            item.setFlags(Qt.NoItemFlags)
            self.ui.lw_hinhanhNG.addItem(item)
            return

        # Quét các file .jpg, .png
        valid_exts = (".jpg", ".jpeg", ".png")
        files = [f for f in os.listdir(target_dir) if f.lower().endswith(valid_exts)]
        files.sort(reverse=True)  # Ảnh mới chụp lên đầu danh sách

        if not files:
            item = QListWidgetItem("Chưa có ảnh NG nào trong ngày này")
            item.setFlags(Qt.NoItemFlags)
            self.ui.lw_hinhanhNG.addItem(item)
            return

        for fname in files:
            full_path = os.path.join(target_dir, fname)
            # Định dạng tên hiển thị: Giờ, phút, giây (VD: 14:35:10)
            raw_time = os.path.splitext(fname)[0].replace("_", ":")
            display_title = f"{raw_time} (NG)"

            item = QListWidgetItem(display_title)
            item.setData(Qt.UserRole, full_path)
            self.ui.lw_hinhanhNG.addItem(item)

    def on_image_item_clicked(self, item: QListWidgetItem):
        file_path = item.data(Qt.UserRole)
        if not file_path or not os.path.exists(file_path):
            return

        # Lấy toàn bộ danh sách đường dẫn ảnh hợp lệ trong ngày đang chọn
        all_paths = []
        clicked_index = 0
        for i in range(self.ui.lw_hinhanhNG.count()):
            p = self.ui.lw_hinhanhNG.item(i).data(Qt.UserRole)
            if p and os.path.exists(p):
                if p == file_path:
                    clicked_index = len(all_paths)
                all_paths.append(p)

        if not all_paths:
            return

        # Mở cửa sổ xem ảnh (modeless để không block infer hay UI)
        self.viewer = ImageViewerDialog(all_paths, clicked_index, parent=self)
        self.viewer.show()
        self.viewer.activateWindow()