import os
import glob
import cv2
import numpy as np
import torch
import albumentations as A
from albumentations.pytorch import ToTensorV2
import segmentation_models_pytorch as smp

# 1. Cấu hình đường dẫn và thông số
IMAGE_DIR = "dataset/val/images"       # Thư mục chứa ảnh cần test
MODEL_WEIGHTS = "resnet50_unet_4cls.pth"    # File trọng số model
MM_PER_PIXEL = 0.05                         # Hệ số quy đổi 1 pixel = ? mm

CLASS_NAMES = {
    1: "NG_S",
    2: "NG_H",
    3: "NG_N"
}

# Định nghĩa màu BGR cho từng class
CLASS_COLORS = {
    0: (0, 0, 0),        # Background: Đen
    1: (0, 165, 255),    # NG_S: Cam
    2: (0, 0, 255),      # NG_H: Đỏ
    3: (0, 255, 255)     # NG_N: Vàng
}

# 2. Pipeline tiền xử lý
val_transform = A.Compose([
    A.Resize(512, 512),
    A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ToTensorV2(),
])

# 3. Khởi tạo và nạp Model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"--> Khởi động thiết bị: {device}")

model = smp.Unet(
    encoder_name="resnet50",
    in_channels=3,
    classes=4
).to(device)

if not os.path.exists(MODEL_WEIGHTS):
    raise FileNotFoundError(f"Không tìm thấy file trọng số: {MODEL_WEIGHTS}")

model.load_state_dict(torch.load(MODEL_WEIGHTS, map_location=device))
model.eval()

# 4. Quét danh sách ảnh trong thư mục
valid_exts = ("*.png", "*.jpg", "*.jpeg", "*.bmp")
img_files = []
for ext in valid_exts:
    img_files.extend(glob.glob(os.path.join(IMAGE_DIR, ext)))
img_files = sorted(img_files)

if not img_files:
    print(f"Không tìm thấy ảnh nào trong thư mục: {IMAGE_DIR}")
    exit()

print(f"--> Tìm thấy {len(img_files)} ảnh. Bắt đầu hiển thị...")
print("  [Điều khiển]: Nhấn phím 'q' (hoặc Space) để sang ảnh tiếp theo | Nhấn 'Esc' để thoát.\n")

# Đặt vị trí cửa sổ cố định để không bị đè lên nhau
win_mask = "1. Mask Raw - Model Output"
win_result = "2. Defect Detection & Area"

cv2.namedWindow(win_mask, cv2.WINDOW_NORMAL)
cv2.namedWindow(win_result, cv2.WINDOW_NORMAL)
cv2.resizeWindow(win_mask, 1280, 720)
cv2.resizeWindow(win_result, 1280, 720)
cv2.moveWindow(win_mask, 100, 100)
cv2.moveWindow(win_result, 760, 100)

# 5. Duyệt qua từng ảnh
for idx, img_path in enumerate(img_files):
    raw_img = cv2.imread(img_path)
    if raw_img is None:
        continue

    file_name = os.path.basename(img_path)
    h_orig, w_orig = raw_img.shape[:2]

    # Preprocessing & Inference
    rgb_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2RGB)
    augmented = val_transform(image=rgb_img)
    input_tensor = augmented["image"].unsqueeze(0).to(device)

    with torch.no_grad():
        logits = model(input_tensor)
        pred_mask = torch.argmax(logits, dim=1).squeeze(0).cpu().numpy().astype(np.uint8)

    pred_mask = cv2.resize(pred_mask, (w_orig, h_orig), interpolation=cv2.INTER_NEAREST)

    # --- TẠO CỬA SỔ 1: ẢNH MASK MÀU TRẢ RA TỪ PIXEL MODEL ---
    color_mask = np.zeros((h_orig, w_orig, 3), dtype=np.uint8)
    for c_id, color in CLASS_COLORS.items():
        color_mask[pred_mask == c_id] = color

    # --- TẠO CỬA SỔ 2: TÍNH DIỆN TÍCH VÀ VẼ CONTOUR TRÊN ẢNH GỐC ---
    overlay = raw_img.copy()
    display_img = raw_img.copy()

    print(f"[{idx+1}/{len(img_files)}] Đang kiểm tra: {file_name}")
    has_defect = False

    for class_id in [1, 2, 3]:
        binary_mask = (pred_mask == class_id).astype(np.uint8) * 255
        contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        color = CLASS_COLORS[class_id]

        for cnt in contours:
            area_pixels = cv2.contourArea(cnt)
            if area_pixels < 5:  # Lọc nhiễu dưới 5 pixel
                continue

            has_defect = True
            area_mm2 = area_pixels * (MM_PER_PIXEL ** 2)

            # Vẽ ruột lên overlay và viền lên display_img
            cv2.drawContours(overlay, [cnt], -1, color, thickness=cv2.FILLED)
            cv2.drawContours(display_img, [cnt], -1, color, thickness=2)

            # Gắn nhãn text kèm diện tích
            x, y, w, h = cv2.boundingRect(cnt)
            label_text = f"{CLASS_NAMES[class_id]}: {int(area_pixels)}px"
            cv2.putText(display_img, label_text, (x, max(18, y - 5)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1, cv2.LINE_AA)

            print(f"  + [{CLASS_NAMES[class_id]}] Tọa độ: ({x},{y}) | Diện tích: {area_pixels:.1f} px ({area_mm2:.4f} mm²)")

    if not has_defect:
        print("  --> OK (Không phát hiện lỗi)")
        cv2.putText(display_img, "STATUS: OK", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv2.LINE_AA)
    else:
        cv2.putText(display_img, "STATUS: NG", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2, cv2.LINE_AA)

    # Trộn màu overlay 30%
    cv2.addWeighted(overlay, 0.3, display_img, 0.7, 0, display_img)

    # Hiển thị 2 cửa sổ
    cv2.imshow(win_mask, color_mask)
    cv2.imshow(win_result, display_img)

    # Bắt sự kiện phím bấm
    while True:
        key = cv2.waitKey(0) & 0xFF
        if key in (ord('q'), ord('Q'), 32, 13):  # 'q', Space hoặc Enter để next
            break
        elif key == 27:  # Phím Esc để thoát hẳn
            print("\n--> Đã dừng chương trình.")
            cv2.destroyAllWindows()
            exit()

cv2.destroyAllWindows()
print("\n--> Đã duyệt xong toàn bộ ảnh trong thư mục!")