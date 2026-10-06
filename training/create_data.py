import os
import random
import cv2
import numpy as np

# Cấu hình thư mục lưu ảnh
OUTPUT_DIR = "generated_samples/images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

NUM_IMAGES = 50
IMG_W, IMG_H = 640, 480

def create_base_sample():
    """Tạo mẫu phôi chuẩn: Vật thể chữ nhật đen + chữ SAMSUNG trắng"""
    # Nền bàn thao tác (xám sáng hơn bên ngoài)
    img = np.full((IMG_H, IMG_W, 3), 60, dtype=np.uint8)

    # 1. Vẽ vật thể hình chữ nhật màu đen (tọa độ căn giữa)
    rect_x1, rect_y1 = 80, 100
    rect_x2, rect_y2 = 560, 380
    
    # Màu đen thực tế có dao động nhẹ (khoảng 15-25) kèm nhiễu hạt nhẹ
    rect_color = random.randint(18, 25)
    cv2.rectangle(img, (rect_x1, rect_y1), (rect_x2, rect_y2), (rect_color, rect_color, rect_color), -1)

    # Thêm một chút nhiễu texture thực tế cho bề mặt đen
    noise = np.random.normal(0, 3, (rect_y2 - rect_y1, rect_x2 - rect_x1, 3))
    patch = img[rect_y1:rect_y2, rect_x1:rect_x2].astype(np.float32) + noise
    img[rect_y1:rect_y2, rect_x1:rect_x2] = np.clip(patch, 0, 255).astype(np.uint8)

    # 2. In chữ "SAMSUNG" màu trắng ở chính giữa
    text = "SAMSUNG"
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 2.2
    thickness = 5
    
    # Lấy kích thước text để căn đúng tâm
    text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
    text_w, text_h = text_size
    text_x = (IMG_W - text_w) // 2
    text_y = (IMG_H + text_h) // 2

    # Vẽ chữ màu trắng sáng (240-255)
    text_color = (250, 250, 250)
    cv2.putText(img, text, (text_x, text_y), font, font_scale, text_color, thickness, cv2.LINE_AA)

    # Vùng chứa text để phục vụ tạo lỗi đúng chỗ
    text_box = (text_x - 10, text_y - text_h - 10, text_w + 20, text_h + 20)
    body_box = (rect_x1 + 10, rect_y1 + 10, (rect_x2 - rect_x1) - 20, (rect_y2 - rect_y1) - 20)

    return img, body_box, text_box

def add_gray_spot_defect(img, body_box, text_box):
    """Class 1: Đốm xám trên nền đen (ngoài vùng chữ)"""
    bx, by, bw, bh = body_box
    tx, ty, tw, th = text_box

    # Chọn tọa độ trên nền đen không trùng vùng chữ
    for _ in range(30):
        cx = random.randint(bx + 15, bx + bw - 15)
        cy = random.randint(by + 15, by + bh - 15)
        # Kiểm tra không nằm trong text box
        if not (tx <= cx <= tx + tw and ty <= cy <= ty + th):
            break

    # Độ sáng đốm xám (từ 90 đến 160)
    gray_val = random.randint(90, 160)
    r_x = random.randint(4, 14)
    r_y = random.randint(4, 14)
    angle = random.randint(0, 180)

    # Vẽ đốm xám dạng elip và làm mờ viền
    overlay = img.copy()
    cv2.ellipse(overlay, (cx, cy), (r_x, r_y), angle, 0, 360, (gray_val, gray_val, gray_val), -1)
    cv2.addWeighted(overlay, 0.85, img, 0.15, 0, img)
    return (cx, cy)

def add_text_defect(img, text_box):
    """Class 2: Lỗi chữ SAMSUNG (mất nét, xước đứt đoạn hoặc lem nhòe mực)"""
    tx, ty, tw, th = text_box
    # Tọa độ bên trong chữ SAMSUNG
    cx = random.randint(tx + 20, tx + tw - 20)
    cy = random.randint(ty + 10, ty + th - 10)

    defect_type = random.choice(["scratch", "blur"])

    if defect_type == "scratch":
        # Vết cào / mất nét: vẽ vệt đen cắt ngang nét chữ trắng
        dx = random.randint(10, 20)
        dy = random.randint(-15, 15)
        scratch_color = (random.randint(18, 25), random.randint(18, 25), random.randint(18, 25))
        cv2.line(img, (cx - dx, cy - dy), (cx + dx, cy + dy), scratch_color, thickness=random.randint(3, 5))
    else:
        # Vết nhòe mực / lem mực: vệt trắng lan ra mép chữ
        blur_r = random.randint(6, 12)
        cv2.circle(img, (cx, cy), blur_r, (235, 235, 235), -1)
        # Làm nhòe vùng lem
        x1 = max(0, cx - blur_r - 4)
        y1 = max(0, cy - blur_r - 4)
        x2 = min(img.shape[1], cx + blur_r + 4)
        y2 = min(img.shape[0], cy + blur_r + 4)
        img[y1:y2, x1:x2] = cv2.GaussianBlur(img[y1:y2, x1:x2], (7, 7), 2.5)

    return (cx, cy)

def generate_all_samples():
    print(f"Đang sinh {NUM_IMAGES} ảnh mẫu kiểm tra...")
    
    for i in range(1, NUM_IMAGES + 1):
        img, body_box, text_box = create_base_sample()

        # Số lỗi trong 1 ảnh: ngẫu nhiên 0, 1 hoặc 2 (dưới 3 điểm)
        num_defects = random.choices([0, 1, 2], weights=[0.1, 0.5, 0.4])[0]
        defects_info = []

        for _ in range(num_defects):
            # Chọn ngẫu nhiên class lỗi
            defect_class = random.choice(["gray_spot", "text_defect"])
            
            if defect_class == "gray_spot":
                pos = add_gray_spot_defect(img, body_box, text_box)
                defects_info.append(f"Đốm xám @ {pos}")
            else:
                pos = add_text_defect(img, text_box)
                defects_info.append(f"Lỗi chữ @ {pos}")

        filename = f"sample_{i:03d}.png"
        filepath = os.path.join(OUTPUT_DIR, filename)
        cv2.imwrite(filepath, img)

        info_str = ", ".join(defects_info) if defects_info else "OK (Không có lỗi)"
        print(f"[{i:02d}/{NUM_IMAGES}] {filename} -> {info_str}")

    print(f"\n--> Đã tạo thành công {NUM_IMAGES} ảnh trong thư mục: {OUTPUT_DIR}")

if __name__ == "__main__":
    generate_all_samples()