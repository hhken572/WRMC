

# # cv_processor.py
# import cv2
# import numpy as np

# class CVProcessor:
#     @staticmethod
#     def measure_alignment(
#         frame: np.ndarray,
#         thresh_rotate: int = 50,
#         blur_k: int = 5,
#         spacing: int = 400,
#         scan_dir: int = 1,
#         thresh_letters: int = 150,
#         min_char_area: int = 12500,
#         max_char_area: int = 14000,
#         min_char_h: int = 15,
#         max_ratio_limit: float = 1.2
#     ):
#         """
#         Thuật toán kiểm tra độ nghiêng in chữ, tâm lề ngang và khoảng cách đáy.
#         Returns:
#             is_ok (bool): True nếu đạt toàn bộ tiêu chuẩn
#             ratio_percent (float): Tỉ lệ (h / L) * 100 (%)
#             annotated_img (np.ndarray): Ảnh kết quả trực quan đầy đủ thước đo
#         """
#         h_img, w_img = frame.shape[:2]

#         # Hệ số quy đổi thực tế: 18mm = 1123px
#         MM_PER_PIXEL = 18.0 / 1123.0

#         # 1. Chuẩn hóa tham số
#         blur_k = max(1, blur_k if blur_k % 2 != 0 else blur_k + 1)
#         spacing = max(10, spacing)

#         # 2. Bước 1: Phân ngưỡng quét mép cạnh & Tính góc xoay Deskew
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         blurred = cv2.GaussianBlur(gray, (blur_k, blur_k), 0)

#         if thresh_rotate == 0:
#             _, binary_rot_raw = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#         else:
#             _, binary_rot_raw = cv2.threshold(blurred, thresh_rotate, 255, cv2.THRESH_BINARY_INV)

#         center_x = w_img // 2
#         x_lines = [
#             center_x - 2 * spacing,
#             center_x - 1 * spacing,
#             center_x,
#             center_x + 1 * spacing,
#             center_x + 2 * spacing
#         ]
#         x_lines = [x for x in x_lines if 0 <= x < w_img]

#         # Quét tia dọc từ trên xuống dưới, bắt chuỗi 5 pixel ĐEN liên tiếp
#         detected_points = []
#         for x in x_lines:
#             col_pixels = binary_rot_raw[:, x]
#             hit_y = None
#             consecutive_count = 0
#             for y in range(h_img):
#                 if col_pixels[y] == 0:
#                     consecutive_count += 1
#                     if consecutive_count >= 5:
#                         hit_y = y - 4
#                         break
#                 else:
#                     consecutive_count = 0

#             if hit_y is not None:
#                 detected_points.append((x, hit_y))

#         angle = 0.0
#         rotated_img = frame.copy()
#         binary_rot = binary_rot_raw.copy()

#         if len(detected_points) >= 2:
#             pts = np.array(detected_points, dtype=np.int32)
#             [vx, vy, x0, y0] = cv2.fitLine(pts, cv2.DIST_L2, 0, 0.01, 0.01)
#             vx, vy = float(vx[0]), float(vy[0])
#             angle = float(np.degrees(np.arctan2(vy, vx)))

#             # Xoay toàn bộ ảnh sản phẩm và ảnh binary_rot về phẳng góc 0 độ
#             M = cv2.getRotationMatrix2D((center_x, h_img // 2), angle, 1.0)
#             rotated_img = cv2.warpAffine(
#                 frame, M, (w_img, h_img),
#                 flags=cv2.INTER_CUBIC,
#                 borderMode=cv2.BORDER_REPLICATE
#             )
#             binary_rot = cv2.warpAffine(
#                 binary_rot_raw, M, (w_img, h_img),
#                 flags=cv2.INTER_NEAREST,
#                 borderMode=cv2.BORDER_CONSTANT,
#                 borderValue=0
#             )

#         # 3. Bước 2: Phân ngưỡng ký tự trên ảnh đã xoay phẳng
#         rot_gray = cv2.cvtColor(rotated_img, cv2.COLOR_BGR2GRAY)
#         rot_blur = cv2.GaussianBlur(rot_gray, (3, 3), 0)

#         if thresh_letters == 0:
#             _, binary_letters = cv2.threshold(rot_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#         else:
#             _, binary_letters = cv2.threshold(rot_blur, thresh_letters, 255, cv2.THRESH_BINARY)

#         contours, _ = cv2.findContours(binary_letters, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         valid_chars = []

#         for c in contours:
#             area = cv2.contourArea(c)
#             x, y, w, h = cv2.boundingRect(c)
#             if min_char_area <= area <= max_char_area and h > min_char_h:
#                 valid_chars.append((x, y, w, h, area, c))

#         # Sắp xếp ký tự từ trái qua phải theo trục x
#         valid_chars = sorted(valid_chars, key=lambda item: item[0])
#         result_annotated = rotated_img.copy()

#         # 4. Bước 3: Phân tích và đo các thông số hình học
#         if len(valid_chars) >= 2:
#             x_s, y_s, w_s, h_s, area_s, _ = valid_chars[0]   # Ký tự đầu tiên (bên trái)
#             x_g, y_g, w_g, h_g, area_g, _ = valid_chars[-1]  # Ký tự cuối cùng (bên phải)

#             # --- A. ĐO ĐỘ NGHIÊNG h VÀ CHIỀU DÀI L ---
#             x_left_s = x_s
#             x_right_g = x_g + w_g
#             L = float(x_right_g - x_left_s)

#             bottom_y_s = y_s + h_s
#             bottom_y_g = y_g + h_g
#             h = float(abs(bottom_y_s - bottom_y_g))

#             ratio_percent = (h / L) * 100.0 if L > 0 else 999.0
#             ok_tilt = (ratio_percent <= max_ratio_limit)

#             # --- B. ĐO KHOẢNG CÁCH NGANG A' VÀ B' (CỘNG THÊM 15 PX OFFSET) ---
#             y_scan_A = y_s + (h_s // 2)
#             y_scan_B = y_g + (h_g // 2)

#             # 1. Quét từ x_s sang trái tìm 3 pixel trắng liên tiếp (255) + lùi thêm 15px
#             hit_x_A = 0
#             cnt_white = 0
#             for x in range(x_s - 1, -1, -1):
#                 if binary_rot[y_scan_A, x] == 255:
#                     cnt_white += 1
#                     if cnt_white >= 3:
#                         # Điểm chạm đầu tiên là x + 2, lùi sang trái thêm 15px
#                         hit_x_A = max(0, (x + 2) - 10)
#                         break
#                 else:
#                     cnt_white = 0

#             dist_A_px = float(x_s - hit_x_A)
#             dist_A_mm = dist_A_px * MM_PER_PIXEL

#             # 2. Quét từ (x_g + w_g) sang phải tìm 3 pixel trắng liên tiếp (255) + tiến thêm 15px
#             hit_x_B = w_img - 1
#             cnt_white = 0
#             for x in range(x_right_g, w_img):
#                 if binary_rot[y_scan_B, x] == 255:
#                     cnt_white += 1
#                     if cnt_white >= 3:
#                         # Điểm chạm đầu tiên là x - 2, tiến sang phải thêm 15px
#                         hit_x_B = min(w_img - 1, (x - 2) + 10)
#                         break
#                 else:
#                     cnt_white = 0

#             dist_B_px = float(hit_x_B - x_right_g)
#             dist_B_mm = dist_B_px * MM_PER_PIXEL

#             # Kiểm tra chênh lệch tâm: (A' - B') / 2
#             diff_center_mm = (dist_A_mm - dist_B_mm) / 2.0
#             ok_center = (-0.20 <= diff_center_mm <= 0.20)

#             # --- C. ĐO KHOẢNG CÁCH ĐÁY DƯỚI (CỘNG THÊM 10 PX OFFSET) ---
#             # 1. Quét từ điểm đáy trái chữ đầu: (x_s, bottom_y_s) xuống dưới
#             hit_y_bot_s = h_img - 1
#             cnt_white = 0
#             for y in range(bottom_y_s, h_img):
#                 if binary_rot[y, x_s] == 255:
#                     cnt_white += 1
#                     if cnt_white >= 3:
#                         hit_y_bot_s = min(h_img - 1, (y - 2) + 10)
#                         break
#                 else:
#                     cnt_white = 0

#             dist_bot_s_px = float(hit_y_bot_s - bottom_y_s)
#             dist_bot_s_mm = dist_bot_s_px * MM_PER_PIXEL
#             ok_bot_s = (0.94 <= dist_bot_s_mm <= 1.14)

#             # 2. Quét từ điểm đáy phải chữ cuối: (x_right_g, bottom_y_g) xuống dưới
#             hit_y_bot_g = h_img - 1
#             cnt_white = 0
#             for y in range(bottom_y_g, h_img):
#                 if binary_rot[y, x_right_g] == 255:
#                     cnt_white += 1
#                     if cnt_white >= 3:
#                         hit_y_bot_g = min(h_img - 1, (y - 2) + 10)
#                         break
#                 else:
#                     cnt_white = 0

#             dist_bot_g_px = float(hit_y_bot_g - bottom_y_g)
#             dist_bot_g_mm = dist_bot_g_px * MM_PER_PIXEL
#             ok_bot_g = (0.94 <= dist_bot_g_mm <= 1.14)

#             # Điều kiện đáy tổng thể
#             ok_bot = bool(ok_bot_s and ok_bot_g)

#             # --- D. TỔNG HỢP KẾT QUẢ ĐẠT / KHÔNG ĐẠT ---
#             is_ok = bool(ok_tilt and ok_center and ok_bot)

#             # Bảng màu riêng cho từng dòng trạng thái
#             color_status1 = (0, 255, 0) if is_ok else (0, 0, 255)
#             color_status2 = (0, 255, 0) if ok_tilt else (0, 0, 255)
#             color_status3 = (0, 255, 0) if ok_center else (0, 0, 255)
#             color_status4 = (0, 255, 0) if ok_bot else (0, 0, 255)

#             # ==========================================================
#             # 5. VẼ TRỰC QUAN HÓA THƯỚC ĐO LÊN ẢNH
#             # ==========================================================

#             # 1. Bounding box chữ đầu và chữ cuối
#             cv2.rectangle(result_annotated, (x_s, y_s), (x_s + w_s, bottom_y_s), (255, 255, 0), 3)
#             cv2.rectangle(result_annotated, (x_g, y_g), (x_g + w_g, bottom_y_g), (255, 255, 0), 3)

#             # 2. Thước đo chiều dài L
#             meas_y_L = max(60, min(y_s, y_g) - 45)
#             cv2.line(result_annotated, (x_left_s, meas_y_L), (x_right_g, meas_y_L), (0, 255, 255), 3)
#             cv2.line(result_annotated, (x_left_s, meas_y_L - 10), (x_left_s, meas_y_L + 10), (0, 255, 255), 3)
#             cv2.line(result_annotated, (x_right_g, meas_y_L - 10), (x_right_g, meas_y_L + 10), (0, 255, 255), 3)

#             text_L = f"L={L:.1f}px ({L*MM_PER_PIXEL:.2f}mm)"
#             pos_L = (int(x_left_s + L / 2 - 120), meas_y_L - 12)
#             cv2.putText(result_annotated, text_L, pos_L, cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 6)
#             cv2.putText(result_annotated, text_L, pos_L, cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)

#             # 3. Thước đo độ lệch cao h
#             cv2.line(result_annotated, (x_left_s, bottom_y_s), (x_right_g + 80, bottom_y_s), (255, 0, 255), 2)
#             cv2.line(result_annotated, (x_left_s, bottom_y_g), (x_right_g + 80, bottom_y_g), (0, 165, 255), 2)

#             h_line_x = x_right_g + 60
#             cv2.line(result_annotated, (h_line_x, bottom_y_s), (h_line_x, bottom_y_g), (0, 0, 255), 4)
#             text_h = f"h={h:.1f}px ({(h/L)*100:.2f}%)"
#             pos_h = (h_line_x + 10, int((bottom_y_s + bottom_y_g) / 2) + 5)
#             cv2.putText(result_annotated, text_h, pos_h, cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 5)
#             cv2.putText(result_annotated, text_h, pos_h, cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

#             # 4. Thước đo mép ngang A' và B' (đã bao gồm +15px offset)
#             # Đường kẻ A' sang trái
#             cv2.line(result_annotated, (x_s, y_scan_A), (hit_x_A, y_scan_A), (255, 100, 0), 3)
#             cv2.circle(result_annotated, (hit_x_A, y_scan_A), 5, (0, 255, 255), -1)
#             # Đường kẻ B' sang phải
#             cv2.line(result_annotated, (x_right_g, y_scan_B), (hit_x_B, y_scan_B), (255, 100, 0), 3)
#             cv2.circle(result_annotated, (hit_x_B, y_scan_B), 5, (0, 255, 255), -1)

#             cv2.putText(result_annotated, f"A':{dist_A_mm:.2f}mm", (hit_x_A + 10, y_scan_A - 10),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 5)
#             cv2.putText(result_annotated, f"A':{dist_A_mm:.2f}mm", (hit_x_A + 10, y_scan_A - 10),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

#             cv2.putText(result_annotated, f"B':{dist_B_mm:.2f}mm", (x_right_g + 10, y_scan_B - 10),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 5)
#             cv2.putText(result_annotated, f"B':{dist_B_mm:.2f}mm", (x_right_g + 10, y_scan_B - 10),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

#             # 5. Thước đo khoảng cách mép đáy dưới
#             color_bot_s_draw = (0, 255, 0) if ok_bot_s else (0, 0, 255)
#             cv2.line(result_annotated, (x_s, bottom_y_s), (x_s, hit_y_bot_s), color_bot_s_draw, 3)
#             cv2.circle(result_annotated, (x_s, hit_y_bot_s), 6, (0, 0, 255), -1)
#             cv2.putText(result_annotated, f"BotL: {dist_bot_s_mm:.2f}mm", (x_s - 120, hit_y_bot_s - 30),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 5)
#             cv2.putText(result_annotated, f"BotL: {dist_bot_s_mm:.2f}mm", (x_s - 120, hit_y_bot_s - 30),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.8, color_bot_s_draw, 2)

#             color_bot_g_draw = (0, 255, 0) if ok_bot_g else (0, 0, 255)
#             cv2.line(result_annotated, (x_right_g, bottom_y_g), (x_right_g, hit_y_bot_g), color_bot_g_draw, 3)
#             cv2.circle(result_annotated, (x_right_g, hit_y_bot_g), 6, (0, 0, 255), -1)
#             cv2.putText(result_annotated, f"BotR: {dist_bot_g_mm:.2f}mm", (x_right_g - 40, hit_y_bot_g - 30),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 5)
#             cv2.putText(result_annotated, f"BotR: {dist_bot_g_mm:.2f}mm", (x_right_g - 40, hit_y_bot_g - 30),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.8, color_bot_g_draw, 2)

#             # 6. Bảng hiển thị phán định tổng hợp từng dòng (line nào NG đỏ, OK xanh)
#             status_line1 = f"STATUS: {'OK' if is_ok else 'NG'}"
#             status_line2 = f"Tilt: {ratio_percent:.2f}% (Limit <= {max_ratio_limit:.2f}%)"
#             status_line3 = f"(A'-B')/2: {diff_center_mm:+.2f}mm ([-0.20, 0.20])"
#             status_line4 = f"BotL: {dist_bot_s_mm:.2f}mm | BotR: {dist_bot_g_mm:.2f}mm ([0.94, 1.14])"

#             # Line 1: STATUS
#             cv2.putText(result_annotated, status_line1, (30, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 0), 6)
#             cv2.putText(result_annotated, status_line1, (30, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.1, color_status1, 2)

#             # Line 2: Tilt
#             cv2.putText(result_annotated, status_line2, (30, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 5)
#             cv2.putText(result_annotated, status_line2, (30, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color_status2, 2)

#             # Line 3: (A'-B')/2
#             cv2.putText(result_annotated, status_line3, (30, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 5)
#             cv2.putText(result_annotated, status_line3, (30, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color_status3, 2)

#             # Line 4: BotL / BotR
#             cv2.putText(result_annotated, status_line4, (30, 165), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 5)
#             cv2.putText(result_annotated, status_line4, (30, 165), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color_status4, 2)

#             return is_ok, ratio_percent, result_annotated

#         else:
#             is_ok = False
#             ratio_percent = 999.0
#             err_text = f"CV: NG (Chars found: {len(valid_chars)} < 2)"
#             cv2.putText(result_annotated, err_text, (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 6)
#             cv2.putText(result_annotated, err_text, (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 2)
#             return is_ok, ratio_percent, result_annotated






















# cv_processor.py
import cv2
import numpy as np


class CVProcessor:

    # Cấu hình mặc định ngưỡng pixel trắng cho 7 ký tự (S, A, M, S, U, N, G)
    DEFAULT_CHAR_PIXEL_LIMITS = [
        (12500, 14500),  # Ký tự 1 ('S'): ~13.2k - 14.0k
        (13000, 15000),  # Ký tự 2 ('A'): ~13.6k - 14.2k
        (22500, 25000),  # Ký tự 3 ('M'): ~22.8k - 23.8k
        (13000, 15000),  # Ký tự 4 ('S'): ~13.6k - 14.2k
        (14000, 16000),  # Ký tự 5 ('U'): ~14.2k - 14.9k
        (17000, 19000),  # Ký tự 6 ('N'): ~17.3k (NG lem sơn lên >20k)
        (13000, 15000),  # Ký tự 7 ('G'): ~13.6k - 14.2k
    ]

    @staticmethod
    def measure_alignment(
        frame: np.ndarray,
        thresh_rotate: int = 50,
        blur_k: int = 5,
        spacing: int = 400,
        scan_dir: int = 1,
        thresh_letters: int = 150,
        min_char_area: int = 10000,
        max_char_area: int = 24000,
        min_char_h: int = 15,
        min_char_w: int = 90,   # Giới hạn chiều ngang tối thiểu (px)
        max_char_w: int = 210,  # Giới hạn chiều ngang tối đa (px) để nhận đủ 7 ký tự
        max_ratio_limit: float = 1.2,
        expected_char_count: int = 7,  # Số lượng ký tự mong đợi: 7 ký tự
        char_pixel_limits: list = None,  # Tuỳ chọn giới hạn pixel trắng riêng cho từng ký tự [(min, max), ...]
    ):
        """Thuật toán kiểm tra độ nghiêng in chữ, tâm lề ngang, khoảng cách đáy
        và kiểm tra số lượng contours (đủ 7 ký tự) cùng số pixel trắng từng contour.

        Returns:
            is_ok (bool): True nếu đạt toàn bộ tiêu chuẩn
            ratio_percent (float): Tỉ lệ (h / L) * 100 (%)
            result_annotated (np.ndarray): Ảnh kết quả trực quan đầy đủ thước đo
            char_inspect_annotated (np.ndarray): Ảnh nhị phân trực quan kiểm tra 7 contour và pixel
        """
        h_img, w_img = frame.shape[:2]

        # Hệ số quy đổi thực tế: 18mm = 1123px
        MM_PER_PIXEL = 18.0 / 1123.0

        # 1. Chuẩn hóa tham số
        blur_k = max(1, blur_k if blur_k % 2 != 0 else blur_k + 1)
        spacing = max(10, spacing)

        # 2. Bước 1: Phân ngưỡng quét mép cạnh & Tính góc xoay Deskew
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (blur_k, blur_k), 0)

        if thresh_rotate == 0:
            _, binary_rot_raw = cv2.threshold(
                blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )
        else:
            _, binary_rot_raw = cv2.threshold(
                blurred, thresh_rotate, 255, cv2.THRESH_BINARY_INV
            )

        center_x = w_img // 2
        x_lines = [
            center_x - 2 * spacing,
            center_x - 1 * spacing,
            center_x,
            center_x + 1 * spacing,
            center_x + 2 * spacing,
        ]
        x_lines = [x for x in x_lines if 0 <= x < w_img]

        # Quét tia dọc từ trên xuống dưới, bắt chuỗi 5 pixel ĐEN liên tiếp
        detected_points = []
        for x in x_lines:
            col_pixels = binary_rot_raw[:, x]
            hit_y = None
            consecutive_count = 0
            for y in range(h_img):
                if col_pixels[y] == 0:
                    consecutive_count += 1
                    if consecutive_count >= 5:
                        hit_y = y - 4
                        break
                else:
                    consecutive_count = 0

            if hit_y is not None:
                detected_points.append((x, hit_y))

        angle = 0.0
        rotated_img = frame.copy()
        binary_rot = binary_rot_raw.copy()

        if len(detected_points) >= 2:
            pts = np.array(detected_points, dtype=np.int32)
            [vx, vy, x0, y0] = cv2.fitLine(pts, cv2.DIST_L2, 0, 0.01, 0.01)
            vx, vy = float(vx[0]), float(vy[0])
            angle = float(np.degrees(np.arctan2(vy, vx)))

            # Xoay toàn bộ ảnh sản phẩm và ảnh binary_rot về phẳng góc 0 độ
            M = cv2.getRotationMatrix2D((center_x, h_img // 2), angle, 1.0)
            rotated_img = cv2.warpAffine(
                frame,
                M,
                (w_img, h_img),
                flags=cv2.INTER_CUBIC,
                borderMode=cv2.BORDER_REPLICATE,
            )
            binary_rot = cv2.warpAffine(
                binary_rot_raw,
                M,
                (w_img, h_img),
                flags=cv2.INTER_NEAREST,
                borderMode=cv2.BORDER_CONSTANT,
                borderValue=0,
            )

        # 3. Bước 2: Phân ngưỡng ký tự trên ảnh đã xoay phẳng
        rot_gray = cv2.cvtColor(rotated_img, cv2.COLOR_BGR2GRAY)
        rot_blur = cv2.GaussianBlur(rot_gray, (3, 3), 0)

        if thresh_letters == 0:
            _, binary_letters = cv2.threshold(
                rot_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )
        else:
            _, binary_letters = cv2.threshold(
                rot_blur, thresh_letters, 255, cv2.THRESH_BINARY
            )

        contours, _ = cv2.findContours(
            binary_letters, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        valid_chars = []

        # Lọc các contour thoả mãn điều kiện kích thước ký tự
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if min_char_w <= w <= max_char_w and h > min_char_h:
                # Đếm số lượng pixel trắng thực tế của contour trong ảnh binary_letters
                c_mask = np.zeros(binary_letters.shape, dtype=np.uint8)
                cv2.drawContours(c_mask, [c], -1, 255, -1)
                white_pixels = cv2.countNonZero(cv2.bitwise_and(binary_letters, binary_letters, mask=c_mask))
                valid_chars.append((x, y, w, h, white_pixels, c))

        # Sắp xếp ký tự từ trái qua phải theo trục x
        valid_chars = sorted(valid_chars, key=lambda item: item[0])
        result_annotated = rotated_img.copy()

        # Tạo ảnh trực quan hoá kiểm tra ký tự (thay cho ảnh binarization cũ)
        char_inspect_annotated = cv2.cvtColor(binary_letters, cv2.COLOR_GRAY2BGR)

        # Lấy bảng cấu hình pixel: ưu tiên char_pixel_limits truyền vào, nếu không dùng DEFAULT_CHAR_PIXEL_LIMITS
        active_pixel_limits = char_pixel_limits if char_pixel_limits is not None else CVProcessor.DEFAULT_CHAR_PIXEL_LIMITS

        # Kiểm tra điều kiện số lượng contour: Phải đủ số lượng mong đợi (mặc định 7)
        ok_char_count = (len(valid_chars) == expected_char_count)
        char_pixel_statuses = []

        for idx, (cx, cy, cw, ch, c_px, c_cnt) in enumerate(valid_chars):
            # Xác định ngưỡng pixel cho contour này:
            # 1. Nếu có trong active_pixel_limits theo vị trí idx -> lấy (min, max) của ký tự đó
            # 2. Nếu không -> dùng min_char_area, max_char_area tổng quát
            if active_pixel_limits and idx < len(active_pixel_limits):
                min_p, max_p = active_pixel_limits[idx]
            else:
                min_p, max_p = min_char_area, max_char_area

            is_px_ok = (min_p <= c_px <= max_p)
            char_pixel_statuses.append(is_px_ok)

            # Màu xanh nếu pixel nằm trong khoảng, màu đỏ nếu nằm ngoài
            box_color = (0, 255, 0) if is_px_ok else (0, 0, 255)

            # Vẽ ô vuông và đường bao quanh contour
            cv2.rectangle(char_inspect_annotated, (cx, cy), (cx + cw, cy + ch), box_color, 2)
            cv2.drawContours(char_inspect_annotated, [c_cnt], -1, box_color, 1)

            # Hiển thị số lượng pixel và thông số cài đặt lên ảnh
            lbl_px = f"C{idx + 1}: {c_px}px"
            lbl_cfg = f"[{min_p}-{max_p}]"

            y_lbl1 = cy - 28 if cy - 28 > 40 else cy + ch + 22
            y_lbl2 = cy - 8 if cy - 28 > 40 else cy + ch + 42

            cv2.putText(char_inspect_annotated, lbl_px, (cx - 10, y_lbl1), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 0), 4)
            cv2.putText(char_inspect_annotated, lbl_px, (cx - 10, y_lbl1), cv2.FONT_HERSHEY_SIMPLEX, 0.65, box_color, 2)
            cv2.putText(char_inspect_annotated, lbl_cfg, (cx - 10, y_lbl2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 3)
            cv2.putText(char_inspect_annotated, lbl_cfg, (cx - 10, y_lbl2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

        ok_all_pixels = (ok_char_count and all(char_pixel_statuses))

        # Hiển thị banner tổng kết lên ảnh char_inspect_annotated
        cnt_color = (0, 255, 0) if ok_char_count else (0, 0, 255)
        px_color = (0, 255, 0) if ok_all_pixels else (0, 0, 255)
        banner_cnt = f"CONTOURS: {len(valid_chars)}/{expected_char_count} ({'OK' if ok_char_count else 'NG'})"
        banner_px = f"PIXELS: {'OK' if ok_all_pixels else 'NG'}"

        cv2.putText(char_inspect_annotated, banner_cnt, (30, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 5)
        cv2.putText(char_inspect_annotated, banner_cnt, (30, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.9, cnt_color, 2)
        cv2.putText(char_inspect_annotated, banner_px, (450, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 5)
        cv2.putText(char_inspect_annotated, banner_px, (450, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.9, px_color, 2)

        # 4. Bước 3: Phân tích và đo các thông số hình học
        if len(valid_chars) >= 2:
            x_s, y_s, w_s, h_s, area_s, _ = valid_chars[
                0
            ]  # Ký tự đầu tiên (bên trái)
            x_g, y_g, w_g, h_g, area_g, _ = valid_chars[
                -1
            ]  # Ký tự cuối cùng (bên phải)

            # --- A. ĐO ĐỘ NGHIÊNG h VÀ CHIỀU DÀI L ---
            x_left_s = x_s
            x_right_g = x_g + w_g
            L = float(x_right_g - x_left_s)

            bottom_y_s = y_s + h_s
            bottom_y_g = y_g + h_g
            h = float(abs(bottom_y_s - bottom_y_g))

            ratio_percent = (h / L) * 100.0 if L > 0 else 999.0
            ok_tilt = ratio_percent <= max_ratio_limit

            # --- B. ĐO KHOẢNG CÁCH NGANG A' VÀ B' (CỘNG THÊM 15 PX OFFSET) ---
            y_scan_A = y_s + (h_s // 2)
            y_scan_B = y_g + (h_g // 2)

            # 1. Quét từ x_s sang trái tìm 3 pixel trắng liên tiếp (255) + lùi thêm 10px
            hit_x_A = 0
            cnt_white = 0
            for x in range(x_s - 1, -1, -1):
                if binary_rot[y_scan_A, x] == 255:
                    cnt_white += 1
                    if cnt_white >= 3:
                        hit_x_A = max(0, (x + 2) - 10)
                        break
                else:
                    cnt_white = 0

            dist_A_px = float(x_s - hit_x_A)
            dist_A_mm = dist_A_px * MM_PER_PIXEL

            # 2. Quét từ (x_g + w_g) sang phải tìm 3 pixel trắng liên tiếp (255) + tiến thêm 10px
            hit_x_B = w_img - 1
            cnt_white = 0
            for x in range(x_right_g, w_img):
                if binary_rot[y_scan_B, x] == 255:
                    cnt_white += 1
                    if cnt_white >= 3:
                        hit_x_B = min(w_img - 1, (x - 2) + 10)
                        break
                else:
                    cnt_white = 0

            dist_B_px = float(hit_x_B - x_right_g)
            dist_B_mm = dist_B_px * MM_PER_PIXEL

            # Kiểm tra chênh lệch tâm: (A' - B') / 2
            diff_center_mm = (dist_A_mm - dist_B_mm) / 2.0
            ok_center = -0.24 <= diff_center_mm <= 0.24

            # --- C. ĐO KHOẢNG CÁCH ĐÁY DƯỚI (CỘNG THÊM 10 PX OFFSET) ---
            # 1. Quét từ điểm đáy trái chữ đầu: (x_s, bottom_y_s) xuống dưới
            hit_y_bot_s = h_img - 1
            cnt_white = 0
            for y in range(bottom_y_s, h_img):
                if binary_rot[y, x_s] == 255:
                    cnt_white += 1
                    if cnt_white >= 3:
                        hit_y_bot_s = min(h_img - 1, (y - 2) + 10)
                        break
                else:
                    cnt_white = 0

            dist_bot_s_px = float(hit_y_bot_s - bottom_y_s)
            dist_bot_s_mm = dist_bot_s_px * MM_PER_PIXEL
            ok_bot_s = 0.86 <= dist_bot_s_mm <= 1.17

            # 2. Quét từ điểm đáy phải chữ cuối: (x_right_g, bottom_y_g) xuống dưới
            hit_y_bot_g = h_img - 1
            cnt_white = 0
            for y in range(bottom_y_g, h_img):
                if binary_rot[y, x_right_g] == 255:
                    cnt_white += 1
                    if cnt_white >= 3:
                        hit_y_bot_g = min(h_img - 1, (y - 2) + 10)
                        break
                else:
                    cnt_white = 0

            dist_bot_g_px = float(hit_y_bot_g - bottom_y_g)
            dist_bot_g_mm = dist_bot_g_px * MM_PER_PIXEL
            ok_bot_g = 0.86 <= dist_bot_g_mm <= 1.17

            # Điều kiện đáy tổng thể
            ok_bot = bool(ok_bot_s and ok_bot_g)

            # --- D. TỔNG HỢP KẾT QUẢ ĐẠT / KHÔNG ĐẠT ---
            # Tổng hợp: Độ nghiêng, tâm lề ngang, mép đáy, đủ 6 contours và pixel của từng contour đạt chuẩn
            is_ok = bool(ok_tilt and ok_center and ok_bot and ok_char_count and ok_all_pixels)

            # Bảng màu riêng cho từng dòng trạng thái
            color_status1 = (0, 255, 0) if is_ok else (0, 0, 255)
            color_status2 = (0, 255, 0) if ok_tilt else (0, 0, 255)
            color_status3 = (0, 255, 0) if ok_center else (0, 0, 255)
            color_status4 = (0, 255, 0) if ok_bot else (0, 0, 255)

            # ==========================================================
            # 5. VẼ TRỰC QUAN HÓA THƯỚC ĐO LÊN ẢNH
            # ==========================================================

            # 1. Bounding box chữ đầu và chữ cuối
            cv2.rectangle(
                result_annotated,
                (x_s, y_s),
                (x_s + w_s, bottom_y_s),
                (255, 255, 0),
                3,
            )
            cv2.rectangle(
                result_annotated,
                (x_g, y_g),
                (x_g + w_g, bottom_y_g),
                (255, 255, 0),
                3,
            )

            # 2. Thước đo chiều dài L
            meas_y_L = max(60, min(y_s, y_g) - 45)
            cv2.line(
                result_annotated,
                (x_left_s, meas_y_L),
                (x_right_g, meas_y_L),
                (0, 255, 255),
                3,
            )
            cv2.line(
                result_annotated,
                (x_left_s, meas_y_L - 10),
                (x_left_s, meas_y_L + 10),
                (0, 255, 255),
                3,
            )
            cv2.line(
                result_annotated,
                (x_right_g, meas_y_L - 10),
                (x_right_g, meas_y_L + 10),
                (0, 255, 255),
                3,
            )

            text_L = f"L={L:.1f}px ({L*MM_PER_PIXEL:.2f}mm)"
            pos_L = (int(x_left_s + L / 2 - 120), meas_y_L - 12)
            cv2.putText(
                result_annotated,
                text_L,
                pos_L,
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 0, 0),
                6,
            )
            cv2.putText(
                result_annotated,
                text_L,
                pos_L,
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 255),
                2,
            )

            # 3. Thước đo độ lệch cao h
            cv2.line(
                result_annotated,
                (x_left_s, bottom_y_s),
                (x_right_g + 80, bottom_y_s),
                (255, 0, 255),
                2,
            )
            cv2.line(
                result_annotated,
                (x_left_s, bottom_y_g),
                (x_right_g + 80, bottom_y_g),
                (0, 165, 255),
                2,
            )

            h_line_x = x_right_g + 60
            cv2.line(
                result_annotated,
                (h_line_x, bottom_y_s),
                (h_line_x, bottom_y_g),
                (0, 0, 255),
                4,
            )
            text_h = f"h={h:.1f}px ({(h/L)*100:.2f}%)"
            pos_h = (h_line_x + 10, int((bottom_y_s + bottom_y_g) / 2) + 5)
            cv2.putText(
                result_annotated,
                text_h,
                pos_h,
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 0, 0),
                5,
            )
            cv2.putText(
                result_annotated,
                text_h,
                pos_h,
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 0, 255),
                2,
            )

            # 4. Thước đo mép ngang A' và B'
            cv2.line(
                result_annotated,
                (x_s, y_scan_A),
                (hit_x_A, y_scan_A),
                (255, 100, 0),
                3,
            )
            cv2.circle(
                result_annotated, (hit_x_A, y_scan_A), 5, (0, 255, 255), -1
            )

            cv2.line(
                result_annotated,
                (x_right_g, y_scan_B),
                (hit_x_B, y_scan_B),
                (255, 100, 0),
                3,
            )
            cv2.circle(
                result_annotated, (hit_x_B, y_scan_B), 5, (0, 255, 255), -1
            )

            cv2.putText(
                result_annotated,
                f"A':{dist_A_mm:.2f}mm",
                (hit_x_A + 10, y_scan_A - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 0, 0),
                5,
            )
            cv2.putText(
                result_annotated,
                f"A':{dist_A_mm:.2f}mm",
                (hit_x_A + 10, y_scan_A - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 255),
                2,
            )

            cv2.putText(
                result_annotated,
                f"B':{dist_B_mm:.2f}mm",
                (x_right_g + 10, y_scan_B - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 0, 0),
                5,
            )
            cv2.putText(
                result_annotated,
                f"B':{dist_B_mm:.2f}mm",
                (x_right_g + 10, y_scan_B - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 255),
                2,
            )

            # 5. Thước đo khoảng cách mép đáy dưới
            color_bot_s_draw = (0, 255, 0) if ok_bot_s else (0, 0, 255)
            cv2.line(
                result_annotated,
                (x_s, bottom_y_s),
                (x_s, hit_y_bot_s),
                color_bot_s_draw,
                3,
            )
            cv2.circle(
                result_annotated, (x_s, hit_y_bot_s), 6, (0, 0, 255), -1
            )
            cv2.putText(
                result_annotated,
                f"BotL: {dist_bot_s_mm:.2f}mm",
                (x_s - 120, hit_y_bot_s - 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 0),
                5,
            )
            cv2.putText(
                result_annotated,
                f"BotL: {dist_bot_s_mm:.2f}mm",
                (x_s - 120, hit_y_bot_s - 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color_bot_s_draw,
                2,
            )

            color_bot_g_draw = (0, 255, 0) if ok_bot_g else (0, 0, 255)
            cv2.line(
                result_annotated,
                (x_right_g, bottom_y_g),
                (x_right_g, hit_y_bot_g),
                color_bot_g_draw,
                3,
            )
            cv2.circle(
                result_annotated, (x_right_g, hit_y_bot_g), 6, (0, 0, 255), -1
            )
            cv2.putText(
                result_annotated,
                f"BotR: {dist_bot_g_mm:.2f}mm",
                (x_right_g - 40, hit_y_bot_g - 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 0),
                5,
            )
            cv2.putText(
                result_annotated,
                f"BotR: {dist_bot_g_mm:.2f}mm",
                (x_right_g - 40, hit_y_bot_g - 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color_bot_g_draw,
                2,
            )

            # 6. Bảng hiển thị phán định tổng hợp từng dòng
            status_line1 = f"STATUS: {'OK' if is_ok else 'NG'}"
            status_line2 = (
                f"Tilt: {ratio_percent:.2f}% (Limit <="
                f" {max_ratio_limit:.2f}%)"
            )
            status_line3 = f"(A'-B')/2: {diff_center_mm:+.2f}mm ([-0.20, 0.20])"
            status_line4 = (
                f"BotL: {dist_bot_s_mm:.2f}mm | BotR: {dist_bot_g_mm:.2f}mm"
                " ([0.94, 1.14])"
            )

            # Line 1: STATUS
            cv2.putText(
                result_annotated,
                status_line1,
                (30, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.1,
                (0, 0, 0),
                6,
            )
            cv2.putText(
                result_annotated,
                status_line1,
                (30, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.1,
                color_status1,
                2,
            )

            # Line 2: Tilt
            cv2.putText(
                result_annotated,
                status_line2,
                (30, 85),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 0, 0),
                5,
            )
            cv2.putText(
                result_annotated,
                status_line2,
                (30, 85),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                color_status2,
                2,
            )

            # Line 3: (A'-B')/2
            cv2.putText(
                result_annotated,
                status_line3,
                (30, 125),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 0, 0),
                5,
            )
            cv2.putText(
                result_annotated,
                status_line3,
                (30, 125),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                color_status3,
                2,
            )

            # Line 4: BotL / BotR
            cv2.putText(
                result_annotated,
                status_line4,
                (30, 165),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 0, 0),
                5,
            )
            cv2.putText(
                result_annotated,
                status_line4,
                (30, 165),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                color_status4,
                2,
            )

            return is_ok, ratio_percent, result_annotated, char_inspect_annotated

        else:
            is_ok = False
            ratio_percent = 999.0
            err_text = f"CV: NG (Chars found: {len(valid_chars)} < 2)"
            cv2.putText(
                result_annotated,
                err_text,
                (40, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.3,
                (0, 0, 0),
                6,
            )
            cv2.putText(
                result_annotated,
                err_text,
                (40, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.3,
                (0, 0, 255),
                2,
            )
            return is_ok, ratio_percent, result_annotated, char_inspect_annotated