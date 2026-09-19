import cv2
import numpy as np

def nothing(x):
    pass

def run_standalone_test(image_path: str):
    frame_orig = cv2.imread(image_path)
    if frame_orig is None:
        print(f"❌ Lỗi: Không thể tải ảnh từ đường dẫn: {image_path}")
        return

    ctrl_win = "Controls"
    cv2.namedWindow(ctrl_win, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(ctrl_win, 540, 420)

    # Khởi tạo các thanh kéo Trackbar
    cv2.createTrackbar("Thresh 1: Rot (0=Otsu)", ctrl_win, 85, 255, nothing)
    cv2.createTrackbar("Blur Size", ctrl_win, 5, 21, nothing)
    cv2.createTrackbar("Line Spacing (px)", ctrl_win, 170, 400, nothing)
    cv2.createTrackbar("Scan: 0=Top->Bot, 1=Bot->Top", ctrl_win, 1, 1, nothing)

    cv2.createTrackbar("Thresh 2: Letters (0=Otsu)", ctrl_win, 130, 255, nothing)
    cv2.createTrackbar("Min Letter Area", ctrl_win, 250, 5000, nothing)
    cv2.createTrackbar("Max Letter Area", ctrl_win, 8000, 50000, nothing)  # 👉 Thêm giới hạn diện tích MAX
    cv2.createTrackbar("Min Letter Height", ctrl_win, 15, 100, nothing)
    cv2.createTrackbar("Max Ratio (x10 %)", ctrl_win, 12, 50, nothing)

    print("---------------------------------------------------------")
    print("-> Điều chỉnh thanh trượt 'Min/Max Letter Area' để lọc đúng chữ")
    print("-> Nhấn 'q' hoặc 'ESC' để THOÁT")
    print("---------------------------------------------------------")

    h_img, w_img = frame_orig.shape[:2]

    while True:
        frame = frame_orig.copy()

        # ==========================================
        # ĐỌC GIÁ TRỊ TỪ TRACKBAR
        # ==========================================
        thresh_rotate = cv2.getTrackbarPos("Thresh 1: Rot (0=Otsu)", ctrl_win)
        blur_k = cv2.getTrackbarPos("Blur Size", ctrl_win)
        spacing = cv2.getTrackbarPos("Line Spacing (px)", ctrl_win)
        scan_dir = cv2.getTrackbarPos("Scan: 0=Top->Bot, 1=Bot->Top", ctrl_win)

        thresh_letters = cv2.getTrackbarPos("Thresh 2: Letters (0=Otsu)", ctrl_win)
        min_char_area = cv2.getTrackbarPos("Min Letter Area", ctrl_win)
        max_char_area = cv2.getTrackbarPos("Max Letter Area", ctrl_win)  # 👉 Lấy giá trị MAX
        min_char_h = cv2.getTrackbarPos("Min Letter Height", ctrl_win)
        max_ratio_limit = cv2.getTrackbarPos("Max Ratio (x10 %)", ctrl_win) / 10.0

        blur_k = max(1, blur_k if blur_k % 2 != 0 else blur_k + 1)
        spacing = max(10, spacing)
        max_char_area = max(min_char_area + 50, max_char_area)

        # ==========================================
        # 1. BƯỚC 1: QUÉT TIA & XOAY PHẲNG ẢNH
        # ==========================================
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
        win2_scan = frame.copy()

        for x in x_lines:
            cv2.line(win2_scan, (x, 0), (x, h_img), (255, 100, 0), 1)
            col_pixels = binary_rot[:, x]
            hit_y = None

            if scan_dir == 0:
                indices = np.where(col_pixels == 255)[0]
                if len(indices) > 0:
                    hit_y = indices[0]
            else:
                indices = np.where(col_pixels == 255)[0]
                if len(indices) > 0:
                    hit_y = indices[-1]

            if hit_y is not None:
                detected_points.append((x, hit_y))
                cv2.circle(win2_scan, (x, hit_y), 5, (0, 0, 255), -1)

        angle = 0.0
        rotated_img = frame.copy()

        if len(detected_points) >= 2:
            pts = np.array(detected_points, dtype=np.int32)
            [vx, vy, x0, y0] = cv2.fitLine(pts, cv2.DIST_L2, 0, 0.01, 0.01)
            vx, vy, x0, y0 = float(vx[0]), float(vy[0]), float(x0[0]), float(y0[0])

            angle_rad = np.arctan2(vy, vx)
            angle = float(np.degrees(angle_rad))

            pt1 = (int(x0 - vx * 600), int(y0 - vy * 600))
            pt2 = (int(x0 + vx * 600), int(y0 + vy * 600))
            cv2.line(win2_scan, pt1, pt2, (0, 255, 0), 2)

            cv2.putText(win2_scan, f"Points: {len(detected_points)}/5 | Angle: {angle:.3f} deg", 
                        (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            M = cv2.getRotationMatrix2D((center_x, h_img // 2), angle, 1.0)
            rotated_img = cv2.warpAffine(frame, M, (w_img, h_img), 
                                         flags=cv2.INTER_CUBIC, 
                                         borderMode=cv2.BORDER_REPLICATE)

        # ==========================================
        # 2. BƯỚC 2: PHÂN NGƯỠNG & LỌC MIN / MAX AREA
        # ==========================================
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
            # 👉 Điều kiện lọc: diện tích nằm giữa min và max
            if min_char_area <= area <= max_char_area and h > min_char_h:
                valid_chars.append((x, y, w, h, area, c))

        # Sắp xếp các ký tự từ TRÁI sang PHẢI theo tọa độ x
        valid_chars = sorted(valid_chars, key=lambda item: item[0])
        win4_result = rotated_img.copy()

        # ==========================================
        # 3. BƯỚC 3: ĐO KHOẢNG CÁCH L, h & HIỂN THỊ
        # ==========================================
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
            is_ok = ratio_percent <= max_ratio_limit

            judge_color = (0, 255, 0) if is_ok else (0, 0, 255)

            # Vẽ bounding box và ghi diện tích (Area) trực tiếp lên từng chữ để dễ căn chỉnh
            cv2.rectangle(win4_result, (x_s, y_s), (x_s + w_s, bottom_y_s), (255, 255, 0), 2)
            cv2.putText(win4_result, f"A:{int(area_s)}", (x_s, y_s - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)

            cv2.rectangle(win4_result, (x_g, y_g), (x_g + w_g, bottom_y_g), (255, 255, 0), 2)
            cv2.putText(win4_result, f"A:{int(area_g)}", (x_g, y_g - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)

            # Thước đo L
            meas_y_L = max(30, min(y_s, y_g) - 25)
            cv2.line(win4_result, (x_left_s, meas_y_L), (x_right_g, meas_y_L), (0, 255, 255), 2)
            cv2.line(win4_result, (x_left_s, meas_y_L - 6), (x_left_s, meas_y_L + 6), (0, 255, 255), 2)
            cv2.line(win4_result, (x_right_g, meas_y_L - 6), (x_right_g, meas_y_L + 6), (0, 255, 255), 2)
            cv2.putText(win4_result, f"L = {L:.1f}px", (int(x_left_s + L / 2 - 50), meas_y_L - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            # Gióng chân chữ
            cv2.line(win4_result, (x_left_s, bottom_y_s), (x_right_g + 55, bottom_y_s), (255, 0, 255), 1)
            cv2.line(win4_result, (x_left_s, bottom_y_g), (x_right_g + 55, bottom_y_g), (0, 165, 255), 1)

            # Đoạn chênh lệch h
            h_line_x = x_right_g + 40
            cv2.line(win4_result, (h_line_x, bottom_y_s), (h_line_x, bottom_y_g), (0, 0, 255), 2)
            cv2.putText(win4_result, f"h={h:.1f}px", (h_line_x + 8, int((bottom_y_s + bottom_y_g) / 2) + 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            status_text = f"RESULT: {'OK' if is_ok else 'NG'} | (h/L)*100 = {ratio_percent:.2f}% (Limit <= {max_ratio_limit:.2f}%)"
            cv2.putText(win4_result, status_text, (30, h_img - 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.85, judge_color, 2)
        else:
            cv2.putText(win4_result, f"Searching chars... (Found: {len(valid_chars)})",
                        (30, h_img - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)

        scale = 0.3 if w_img > 1920 else 0.5
        cv2.imshow("1. Rotate Mask (Scanlines)", cv2.resize(binary_rot, None, fx=scale, fy=scale))
        cv2.imshow("2. 5-Line Scan & Fit Line", cv2.resize(win2_scan, None, fx=scale, fy=scale))
        cv2.imshow("3. Rotated Letters Mask", cv2.resize(binary_letters, None, fx=scale, fy=scale))
        cv2.imshow("4. Final Measurement & Result", cv2.resize(win4_result, None, fx=scale, fy=scale))

        key = cv2.waitKey(30) & 0xFF
        if key == ord('q') or key == 27:
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    TEST_IMAGE = r"D:\WRMC\saved_images\Image_20260905171644614.jpg"
    run_standalone_test(TEST_IMAGE)