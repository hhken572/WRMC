# import cv2
# import numpy as np

# class CVProcessor:
#     @staticmethod
#     def measure_area(image: np.ndarray, min_area: int = 5, max_area: int = 5000000):
#         # 1. Tiền xử lý từ ảnh gốc
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#         _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
#         # 2. Tìm contour trên ảnh nhị phân sạch (chưa bị dính chữ AI)
#         contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
#         # 3. Chuyển ảnh nhị phân sang định dạng 3 kênh màu (BGR) để vẽ chữ/contour có màu lên đó
#         thresh_annotated = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
        
#         total_area = 0
#         for cnt in contours:
#             area = cv2.contourArea(cnt)
#             if area > min_area:
#                 total_area += area
#                 # Vẽ viền màu xanh lá lên ảnh nhị phân
#                 cv2.drawContours(thresh_annotated, [cnt], -1, (0, 255, 0), 2)

#         # 4. Phán định diện tích
#         is_ok = (min_area <= total_area <= max_area)

#         # 5. Ghi thông số kết quả OpenCV lên ảnh nhị phân
#         color = (0, 255, 0) if is_ok else (0, 0, 255)
#         status_text = f"CV: {'OK' if is_ok else 'NG'} | Area: {int(total_area)}"
#         cv2.putText(thresh_annotated, status_text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

#         return is_ok, total_area, thresh_annotated



import cv2
import numpy as np


class CVProcessor:
    @staticmethod
    def measure_alignment(
        frame: np.ndarray,
        thresh_rotate: int = 174,
        blur_k: int = 5,
        spacing: int = 400,
        scan_dir: int = 1,
        thresh_letters: int = 154,
        min_char_area: int = 2180,
        max_char_area: int = 50000,
        min_char_h: int = 15,
        max_ratio_limit: float = 1.2
    ):
        """
        Thuật toán kiểm tra độ nghiêng in chữ (Deskew & Measure h/L).
        Returns:
            is_ok (bool): True nếu đạt chuẩn (ratio <= max_ratio_limit)
            ratio_percent (float): Tỉ lệ (h / L) * 100 (%)
            annotated_img (np.ndarray): Ảnh kết quả đã xoay phẳng và vẽ thước đo
        """
        h_img, w_img = frame.shape[:2]

        # 1. Chuẩn hóa tham số
        blur_k = max(1, blur_k if blur_k % 2 != 0 else blur_k + 1)
        spacing = max(10, spacing)

        # 2. Bước 1: Quét biên cạnh & Tính góc xoay Deskew
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (blur_k, blur_k), 0)

        if thresh_rotate == 0:
            _, binary_rot = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        else:
            _, binary_rot = cv2.threshold(blurred, thresh_rotate, 255, cv2.THRESH_BINARY_INV)

        center_x = w_img // 2
        x_lines = [
            center_x - 2 * spacing,
            center_x - 1 * spacing,
            center_x,
            center_x + 1 * spacing,
            center_x + 2 * spacing
        ]
        x_lines = [x for x in x_lines if 0 <= x < w_img]

        detected_points = []
        for x in x_lines:
            col_pixels = binary_rot[:, x]
            indices = np.where(col_pixels == 255)[0]
            if len(indices) > 0:
                hit_y = indices[-1] if scan_dir == 1 else indices[0]
                detected_points.append((x, hit_y))

        angle = 0.0
        rotated_img = frame.copy()

        if len(detected_points) >= 2:
            pts = np.array(detected_points, dtype=np.int32)
            [vx, vy, x0, y0] = cv2.fitLine(pts, cv2.DIST_L2, 0, 0.01, 0.01)
            vx, vy = float(vx[0]), float(vy[0])
            angle = float(np.degrees(np.arctan2(vy, vx)))

            # Xoay toàn bộ ảnh về góc 0 độ
            M = cv2.getRotationMatrix2D((center_x, h_img // 2), angle, 1.0)
            rotated_img = cv2.warpAffine(
                frame, M, (w_img, h_img),
                flags=cv2.INTER_CUBIC,
                borderMode=cv2.BORDER_REPLICATE
            )

        # 3. Bước 2: Phân ngưỡng ký tự trên ảnh đã xoay phẳng
        rot_gray = cv2.cvtColor(rotated_img, cv2.COLOR_BGR2GRAY)
        rot_blur = cv2.GaussianBlur(rot_gray, (3, 3), 0)

        if thresh_letters == 0:
            _, binary_letters = cv2.threshold(rot_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        else:
            _, binary_letters = cv2.threshold(rot_blur, thresh_letters, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(binary_letters, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        valid_chars = []

        for c in contours:
            area = cv2.contourArea(c)
            x, y, w, h = cv2.boundingRect(c)
            if min_char_area <= area <= max_char_area and h > min_char_h:
                valid_chars.append((x, y, w, h, area, c))

        # Sắp xếp các ký tự từ trái qua phải
        valid_chars = sorted(valid_chars, key=lambda item: item[0])
        result_annotated = rotated_img.copy()

        # 4. Bước 3: Đo khoảng cách L, h và đánh giá
        if len(valid_chars) >= 2:
            x_s, y_s, w_s, h_s, area_s, _ = valid_chars[0]
            x_g, y_g, w_g, h_g, area_g, _ = valid_chars[-1]

            x_left_s = x_s
            x_right_g = x_g + w_g
            L = float(x_right_g - x_left_s)

            bottom_y_s = y_s + h_s
            bottom_y_g = y_g + h_g
            h = float(abs(bottom_y_s - bottom_y_g))

            ratio_percent = (h / L) * 100.0 if L > 0 else 999.0
            is_ok = (ratio_percent <= max_ratio_limit)
            judge_color = (0, 255, 0) if is_ok else (0, 0, 255)

            # 1. Vẽ bounding box chữ đầu và cuối (tăng nét lên thickness=4)
            cv2.rectangle(result_annotated, (x_s, y_s), (x_s + w_s, bottom_y_s), (255, 255, 0), 4)
            cv2.rectangle(result_annotated, (x_g, y_g), (x_g + w_g, bottom_y_g), (255, 255, 0), 4)

            # 2. Thước đo chiều dài L (tăng nét line=4, chữ scale=1.3)
            meas_y_L = max(60, min(y_s, y_g) - 45)
            cv2.line(result_annotated, (x_left_s, meas_y_L), (x_right_g, meas_y_L), (0, 255, 255), 4)
            cv2.line(result_annotated, (x_left_s, meas_y_L - 15), (x_left_s, meas_y_L + 15), (0, 255, 255), 4)
            cv2.line(result_annotated, (x_right_g, meas_y_L - 15), (x_right_g, meas_y_L + 15), (0, 255, 255), 4)

            text_L = f"L = {L:.1f}px"
            pos_L = (int(x_left_s + L / 2 - 100), meas_y_L - 15)
            # Viền đen dày để làm nổi chữ
            cv2.putText(result_annotated, text_L, pos_L, cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 8)
            cv2.putText(result_annotated, text_L, pos_L, cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 255), 3)

            # 3. Gióng chân chữ (tăng nét line=3)
            cv2.line(result_annotated, (x_left_s, bottom_y_s), (x_right_g + 90, bottom_y_s), (255, 0, 255), 3)
            cv2.line(result_annotated, (x_left_s, bottom_y_g), (x_right_g + 90, bottom_y_g), (0, 165, 255), 3)

            # 4. Đoạn chênh lệch h (tăng nét line=5, chữ scale=1.2)
            h_line_x = x_right_g + 70
            cv2.line(result_annotated, (h_line_x, bottom_y_s), (h_line_x, bottom_y_g), (0, 0, 255), 5)

            text_h = f"h={h:.1f}px"
            pos_h = (h_line_x + 15, int((bottom_y_s + bottom_y_g) / 2) + 10)
            cv2.putText(result_annotated, text_h, pos_h, cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 8)
            cv2.putText(result_annotated, text_h, pos_h, cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

            # 5. Dòng chữ phán định tổng thể (tăng scale=1.8 - 2.0, thickness=4 - 5)
            status_text = f"CV: {'OK' if is_ok else 'NG'} | (h/L)*100 = {ratio_percent:.2f}% (Limit <= {max_ratio_limit:.2f}%)"
            pos_status = (40, h_img - 50)
            cv2.putText(result_annotated, status_text, pos_status, cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 0, 0), 10)
            cv2.putText(result_annotated, status_text, pos_status, cv2.FONT_HERSHEY_SIMPLEX, 1.8, judge_color, 4)

            return is_ok, ratio_percent, result_annotated

        else:
            is_ok = False
            ratio_percent = 999.0
            err_text = f"CV: NG (Chars found: {len(valid_chars)} < 2)"
            pos_err = (40, h_img - 50)
            cv2.putText(result_annotated, err_text, pos_err, cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 0, 0), 10)
            cv2.putText(result_annotated, err_text, pos_err, cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 0, 255), 4)
            return is_ok, ratio_percent, result_annotated

    # # Alias tương thích ngược nếu sequence_engine vẫn gọi tên measure_area cũ
    # measure_area = measure_alignment