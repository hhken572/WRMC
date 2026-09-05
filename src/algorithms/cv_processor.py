import cv2
import numpy as np

class CVProcessor:
    @staticmethod
    def measure_area(image: np.ndarray, min_area: int = 5, max_area: int = 5000000):
        # 1. Tiền xử lý từ ảnh gốc
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # 2. Tìm contour trên ảnh nhị phân sạch (chưa bị dính chữ AI)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 3. Chuyển ảnh nhị phân sang định dạng 3 kênh màu (BGR) để vẽ chữ/contour có màu lên đó
        thresh_annotated = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
        
        total_area = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > min_area:
                total_area += area
                # Vẽ viền màu xanh lá lên ảnh nhị phân
                cv2.drawContours(thresh_annotated, [cnt], -1, (0, 255, 0), 2)

        # 4. Phán định diện tích
        is_ok = (min_area <= total_area <= max_area)

        # 5. Ghi thông số kết quả OpenCV lên ảnh nhị phân
        color = (0, 255, 0) if is_ok else (0, 0, 255)
        status_text = f"CV: {'OK' if is_ok else 'NG'} | Area: {int(total_area)}"
        cv2.putText(thresh_annotated, status_text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        return is_ok, total_area, thresh_annotated