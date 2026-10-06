import os
import cv2
import queue
import threading
import numpy as np
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_NG_DIR = str(PROJECT_ROOT / "data_NG" / "ng_images")


def _prepare_sub_image(img, title: str, target_size=(800, 450), title_color=(0, 255, 255)):
    """Chuẩn hóa kích thước và vẽ nhãn tiêu đề cho từng khung ảnh con."""
    tw, th = target_size
    if img is None:
        canvas = np.zeros((th, tw, 3), dtype=np.uint8)
        cv2.putText(canvas, f"NO IMAGE ({title})", (tw // 4, th // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2, cv2.LINE_AA)
        return canvas

    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    resized = cv2.resize(img, (tw, th), interpolation=cv2.INTER_LINEAR)

    # Vẽ thanh tiêu đề mờ ở mép trên
    overlay = resized.copy()
    cv2.rectangle(overlay, (0, 0), (tw, 36), (15, 15, 15), -1)
    cv2.addWeighted(overlay, 0.75, resized, 0.25, 0, resized)

    cv2.putText(resized, title, (14, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, title_color, 2, cv2.LINE_AA)
    return resized


def stitch_4_images(img1, img2, img3, img4, timestamp: datetime = None, status: str = "NG") -> np.ndarray:
    """
    Ghép 4 khung ảnh thành 1 ảnh duy nhất (lưới 2x2):
      [1] Cam 1 - AI 1       |  [2] Cam 1 - Nhị phân trực quan
      [3] Cam 1 - Đo góc CV  |  [4] Cam 2 - AI 3
    """
    if timestamp is None:
        timestamp = datetime.now()

    time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    s1 = _prepare_sub_image(img1, "[1] CAM 1 - AI 1 (KHIEM KHUYET BE MAT)", title_color=(0, 165, 255))
    s2 = _prepare_sub_image(img2, "[2] CAM 1 - NHI PHAN TRUC QUAN (CV)", title_color=(0, 255, 255))
    s3 = _prepare_sub_image(img3, "[3] CAM 1 - KET QUA DO GOC (CV)", title_color=(255, 200, 0))
    s4 = _prepare_sub_image(img4, "[4] CAM 2 - AI 3 (NGOAI QUAN CAM 2)", title_color=(0, 165, 255))

    top_row = np.hstack([s1, s2])
    bot_row = np.hstack([s3, s4])
    grid = np.vstack([top_row, bot_row])

    # Banner trên cùng
    header_h = 46
    header = np.zeros((header_h, grid.shape[1], 3), dtype=np.uint8)
    cv2.rectangle(header, (0, 0), (grid.shape[1], header_h), (25, 25, 30), -1)

    status_color = (0, 0, 255) if "NG" in status else (0, 255, 0)
    title_text = f"ELENTEC WRMC - INSPECTION LOG [{status}]  |  Thoi gian: {time_str}"
    cv2.putText(header, title_text, (20, 31), cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2, cv2.LINE_AA)

    combined = np.vstack([header, grid])
    return combined


class AsyncNGImageSaver:
    """Quản lý lưu ảnh ghép NG bất đồng bộ trong background thread, không block tiến trình infer hay giao diện."""
    _instance = None

    def __init__(self, base_dir=DEFAULT_NG_DIR):
        self.base_dir = base_dir
        self.task_queue = queue.Queue(maxsize=100)
        self.stop_event = threading.Event()
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = AsyncNGImageSaver()
        return cls._instance

    def save_ng(self, img1, img2, img3, img4, status="NG", on_saved_callback=None):
        now = datetime.now()
        task = {
            "img1": img1.copy() if img1 is not None else None,
            "img2": img2.copy() if img2 is not None else None,
            "img3": img3.copy() if img3 is not None else None,
            "img4": img4.copy() if img4 is not None else None,
            "timestamp": now,
            "status": status,
            "callback": on_saved_callback
        }
        try:
            self.task_queue.put_nowait(task)
        except queue.Full:
            print("⚠️ [AsyncNGSaver] Hàng đợi lưu ảnh bị đầy, bỏ qua bản ghi!")

    def _worker_loop(self):
        while not self.stop_event.is_set():
            try:
                task = self.task_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            try:
                ts: datetime = task["timestamp"]
                month_dir = ts.strftime("%Y-%m")
                day_dir = ts.strftime("%Y-%m-%d")
                filename = ts.strftime("%H_%M_%S") + ".jpg"

                target_folder = os.path.join(self.base_dir, month_dir, day_dir)
                os.makedirs(target_folder, exist_ok=True)

                file_path = os.path.join(target_folder, filename)

                stitched = stitch_4_images(
                    task["img1"],
                    task["img2"],
                    task["img3"],
                    task["img4"],
                    timestamp=ts,
                    status=task["status"]
                )

                cv2.imwrite(file_path, stitched, [cv2.IMWRITE_JPEG_QUALITY, 90])
                print(f"[AsyncNGSaver] Da luu anh ghep NG: {file_path}")

                if task.get("callback"):
                    try:
                        task["callback"](file_path, ts)
                    except Exception as cb_err:
                        print(f"[AsyncNGSaver] Loi goi callback: {cb_err}")

            except Exception as e:
                print(f"[AsyncNGSaver] Loi khi luu anh ghep NG: {e}")
            finally:
                self.task_queue.task_done()
