# import os
# import glob
# import cv2
# import numpy as np
# import torch
# import albumentations as A
# from albumentations.pytorch import ToTensorV2
# import segmentation_models_pytorch as smp

# # 1. Cấu hình đường dẫn và thông số
# IMAGE_DIR = "datasetc1_v2/val/images"       # Thư mục chứa ảnh cần test
# MODEL_WEIGHTS = "resnet50_unet_4cls_c1_v2.pth"    # File trọng số model
# MM_PER_PIXEL = 0.05                         # Hệ số quy đổi 1 pixel = ? mm

# # CLASS_NAMES = {
# #     1: "NG_ChamDen",
# #     2: "NG_OVang",
# #     3: "NG_Can"
# # }

# CLASS_NAMES = {
#     1: "NG_ThieuSon",
#     2: "NG_LemSon",
#     3: "NG_HoaChat"
# }

# # Định nghĩa màu BGR cho từng class
# CLASS_COLORS = {
#     0: (0, 0, 0),        # Background: Đen
#     1: (0, 165, 255),    # NG_S: Cam
#     2: (0, 0, 255),      # NG_H: Đỏ
#     3: (0, 255, 255)     # NG_N: Vàng
# }

# # 2. Pipeline tiền xử lý
# val_transform = A.Compose([
#     A.Resize(512, 512),
#     A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
#     ToTensorV2(),
# ])

# # 3. Khởi tạo và nạp Model
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print(f"--> Khởi động thiết bị: {device}")

# model = smp.Unet(
#     encoder_name="resnet50",
#     in_channels=3,
#     classes=4
# ).to(device)

# if not os.path.exists(MODEL_WEIGHTS):
#     raise FileNotFoundError(f"Không tìm thấy file trọng số: {MODEL_WEIGHTS}")

# model.load_state_dict(torch.load(MODEL_WEIGHTS, map_location=device))
# model.eval()

# # 4. Quét danh sách ảnh trong thư mục
# valid_exts = ("*.png", "*.jpg", "*.jpeg", "*.bmp")
# img_files = []
# for ext in valid_exts:
#     img_files.extend(glob.glob(os.path.join(IMAGE_DIR, ext)))
# img_files = sorted(img_files)

# if not img_files:
#     print(f"Không tìm thấy ảnh nào trong thư mục: {IMAGE_DIR}")
#     exit()

# print(f"--> Tìm thấy {len(img_files)} ảnh. Bắt đầu hiển thị...")
# print("  [Điều khiển]: Nhấn phím 'q' (hoặc Space) để sang ảnh tiếp theo | Nhấn 'Esc' để thoát.\n")

# # Đặt vị trí cửa sổ cố định để không bị đè lên nhau
# win_mask = "1. Mask Raw - Model Output"
# win_result = "2. Defect Detection & Area"

# cv2.namedWindow(win_mask, cv2.WINDOW_NORMAL)
# cv2.namedWindow(win_result, cv2.WINDOW_NORMAL)
# cv2.resizeWindow(win_mask, 1280, 720)
# cv2.resizeWindow(win_result, 1280, 720)
# cv2.moveWindow(win_mask, 100, 100)
# cv2.moveWindow(win_result, 760, 100)

# # 5. Duyệt qua từng ảnh
# for idx, img_path in enumerate(img_files):
#     raw_img = cv2.imread(img_path)
#     if raw_img is None:
#         continue

#     file_name = os.path.basename(img_path)
#     h_orig, w_orig = raw_img.shape[:2]

#     # Preprocessing & Inference
#     rgb_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2RGB)
#     augmented = val_transform(image=rgb_img)
#     input_tensor = augmented["image"].unsqueeze(0).to(device)

#     with torch.no_grad():
#         logits = model(input_tensor)
#         pred_mask = torch.argmax(logits, dim=1).squeeze(0).cpu().numpy().astype(np.uint8)

#     pred_mask = cv2.resize(pred_mask, (w_orig, h_orig), interpolation=cv2.INTER_NEAREST)

#     # --- TẠO CỬA SỔ 1: ẢNH MASK MÀU TRẢ RA TỪ PIXEL MODEL ---
#     color_mask = np.zeros((h_orig, w_orig, 3), dtype=np.uint8)
#     for c_id, color in CLASS_COLORS.items():
#         color_mask[pred_mask == c_id] = color

#     # --- TẠO CỬA SỔ 2: TÍNH DIỆN TÍCH VÀ VẼ CONTOUR TRÊN ẢNH GỐC ---
#     overlay = raw_img.copy()
#     display_img = raw_img.copy()

#     print(f"[{idx+1}/{len(img_files)}] Đang kiểm tra: {file_name}")
#     has_defect = False

#     for class_id in [1, 2, 3]:
#         binary_mask = (pred_mask == class_id).astype(np.uint8) * 255
#         contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         color = CLASS_COLORS[class_id]

#         for cnt in contours:
#             area_pixels = cv2.contourArea(cnt)
#             if area_pixels < 5:  # Lọc nhiễu dưới 5 pixel
#                 continue

#             has_defect = True
#             area_mm2 = area_pixels * (MM_PER_PIXEL ** 2)

#             # Vẽ ruột lên overlay và viền lên display_img
#             cv2.drawContours(overlay, [cnt], -1, color, thickness=cv2.FILLED)
#             cv2.drawContours(display_img, [cnt], -1, color, thickness=2)

#             # Gắn nhãn text kèm diện tích
#             x, y, w, h = cv2.boundingRect(cnt)
#             label_text = f"{CLASS_NAMES[class_id]}: {int(area_pixels)}px"
#             cv2.putText(display_img, label_text, (x, max(18, y - 5)),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1, cv2.LINE_AA)

#             print(f"  + [{CLASS_NAMES[class_id]}] Tọa độ: ({x},{y}) | Diện tích: {area_pixels:.1f} px ({area_mm2:.4f} mm²)")

#     if not has_defect:
#         print("  --> OK (Không phát hiện lỗi)")
#         cv2.putText(display_img, "STATUS: OK", (30, 50),
#                     cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv2.LINE_AA)
#     else:
#         cv2.putText(display_img, "STATUS: NG", (30, 50),
#                     cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2, cv2.LINE_AA)

#     # Trộn màu overlay 30%
#     cv2.addWeighted(overlay, 0.3, display_img, 0.7, 0, display_img)

#     # Hiển thị 2 cửa sổ
#     cv2.imshow(win_mask, color_mask)
#     cv2.imshow(win_result, display_img)

#     # Bắt sự kiện phím bấm
#     while True:
#         key = cv2.waitKey(0) & 0xFF
#         if key in (ord('q'), ord('Q'), 32, 13):  # 'q', Space hoặc Enter để next
#             break
#         elif key == 27:  # Phím Esc để thoát hẳn
#             print("\n--> Đã dừng chương trình.")
#             cv2.destroyAllWindows()
#             exit()

# cv2.destroyAllWindows()
# print("\n--> Đã duyệt xong toàn bộ ảnh trong thư mục!")
























import os
import glob
import cv2
import numpy as np
import torch
import torch.nn.functional as F
import albumentations as A
from albumentations.pytorch import ToTensorV2
import segmentation_models_pytorch as smp

# ==========================================
# 1. CẤU HÌNH ĐƯỜNG DẪN & THÔNG SỐ
# ==========================================
IMAGE_DIR = "anh_them_c1/NG"           # Thư mục ảnh cần kiểm tra
MODEL_WEIGHTS = "resnet50_unet_4cls_c1_v5.pth"  # File trọng số model
MM_PER_PIXEL = 0.05                             # Hệ số quy đổi 1 pixel = ? mm

CLASS_NAMES = {
    1: "NG_ThieuSon",
    2: "NG_LemSon",
    3: "NG_HoaChat"
}

# CLASS_NAMES = {
#     1: "NG_ChamDen",
#     2: "NG_OVang",
#     3: "NG_Can"
# }

# Màu viền BGR cho từng loại lỗi
CLASS_COLORS = {
    0: (0, 0, 0),        # Background: Đen
    1: (0, 165, 255),    # NG_ThieuSon: Cam
    2: (0, 0, 255),      # NG_LemSon: Đỏ
    3: (0, 255, 255)     # NG_HoaChat: Vàng
}

# Ngưỡng Confidence (độ tin cậy) cho từng class (0.0 -> 1.0)
CONF_THRESHOLDS = {
    1: 0.60,  # NG_ThieuSon
    2: 0.50,  # NG_LemSon
    3: 0.60   # NG_HoaChat
}
DEFAULT_CONF = 0.50

# Ngưỡng diện tích tối đa cho phép (tính theo Pixel). Vượt quá ngưỡng này chữ sẽ màu ĐỎ.
AREA_THRESHOLDS = {
    1: 50,    # NG_ThieuSon: > 50 px -> chữ Đỏ, <= 50 px -> chữ Xanh lá
    2: 40,    # NG_LemSon:   > 40 px -> chữ Đỏ, <= 40 px -> chữ Xanh lá
    3: 60     # NG_HoaChat:  > 60 px -> chữ Đỏ, <= 60 px -> chữ Xanh lá
}

MIN_AREA_NOISE = 5  # Bỏ qua các hạt nhiễu nhỏ hơn 5 pixel

# ==========================================
# 2. PIPELINE TIỀN XỬ LÝ
# ==========================================
val_transform = A.Compose([
    A.Resize(512, 512),
    A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ToTensorV2(),
])

# ==========================================
# 3. KHỞI TẠO VÀ NẠP MODEL
# ==========================================
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

# ==========================================
# 4. QUÉT DANH SÁCH ẢNH
# ==========================================
valid_exts = ("*.png", "*.jpg", "*.jpeg", "*.bmp")
img_files = []
for ext in valid_exts:
    img_files.extend(glob.glob(os.path.join(IMAGE_DIR, ext)))
img_files = sorted(img_files)

if not img_files:
    print(f"Không tìm thấy ảnh nào trong thư mục: {IMAGE_DIR}")
    exit()

print(f"--> Tìm thấy {len(img_files)} ảnh.")
print("  [Điều khiển]: Nhấn phím 'q' (hoặc Space) để sang ảnh tiếp theo | 'Esc' để thoát.\n")

win_mask = "1. Mask Raw - Model Output"
win_result = "2. Defect Detection & Area"

cv2.namedWindow(win_mask, cv2.WINDOW_NORMAL)
cv2.namedWindow(win_result, cv2.WINDOW_NORMAL)
cv2.resizeWindow(win_mask, 1280, 720)
cv2.resizeWindow(win_result, 1280, 720)
cv2.moveWindow(win_mask, 50, 80)
cv2.moveWindow(win_result, 720, 80)

# ==========================================
# 5. DUYỆT TỪNG ẢNH & INFERENCE
# ==========================================
for idx, img_path in enumerate(img_files):
    raw_img = cv2.imread(img_path)
    if raw_img is None:
        continue

    file_name = os.path.basename(img_path)
    h_orig, w_orig = raw_img.shape[:2]

    # Tiền xử lý
    rgb_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2RGB)
    augmented = val_transform(image=rgb_img)
    input_tensor = augmented["image"].unsqueeze(0).to(device)

    # Dự đoán kèm trích xuất ma trận xác suất (Probabilities)
    with torch.no_grad():
        logits = model(input_tensor)
        probs = F.softmax(logits, dim=1).squeeze(0)          # Shape: [4, 512, 512]
        max_probs, pred_classes = torch.max(probs, dim=0)   # Shape: [512, 512]

    # Lọc ngưỡng Confidence cho từng class
    filtered_mask = torch.zeros_like(pred_classes, dtype=torch.uint8)
    for class_id in [1, 2, 3]:
        conf_thresh = CONF_THRESHOLDS.get(class_id, DEFAULT_CONF)
        mask_condition = (pred_classes == class_id) & (max_probs >= conf_thresh)
        filtered_mask[mask_condition] = class_id

    # Đưa mask và ma trận max_probs về kích thước ảnh gốc
    pred_mask = filtered_mask.cpu().numpy()
    pred_mask = cv2.resize(pred_mask, (w_orig, h_orig), interpolation=cv2.INTER_NEAREST)

    prob_map = max_probs.cpu().numpy()
    prob_map = cv2.resize(prob_map, (w_orig, h_orig), interpolation=cv2.INTER_LINEAR)

    # --- CỬA SỔ 1: MASK RAW COLOR TỪ MODEL ---
    color_mask = np.zeros((h_orig, w_orig, 3), dtype=np.uint8)
    for c_id, color in CLASS_COLORS.items():
        color_mask[pred_mask == c_id] = color

    # --- CỬA SỔ 2: VẼ ĐƯỜNG VIỀN & HIỂN THỊ DIỆN TÍCH + CONF ---
    display_img = raw_img.copy()

    print(f"\n[{idx+1}/{len(img_files)}] Đang kiểm tra: {file_name}")
    is_strictly_ng = False
    has_any_defect = False

    for class_id in [1, 2, 3]:
        binary_mask = (pred_mask == class_id).astype(np.uint8) * 255
        contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        border_color = CLASS_COLORS[class_id]
        limit_area = AREA_THRESHOLDS.get(class_id, 50)

        for cnt in contours:
            area_pixels = cv2.contourArea(cnt)
            if area_pixels < MIN_AREA_NOISE:
                continue

            has_any_defect = True
            area_mm2 = area_pixels * (MM_PER_PIXEL ** 2)

            # Tạo mask đơn lẻ cho riêng contour này để tính conf trung bình bên trong ruột lỗi
            single_cnt_mask = np.zeros((h_orig, w_orig), dtype=np.uint8)
            cv2.drawContours(single_cnt_mask, [cnt], -1, 255, thickness=cv2.FILLED)
            
            # Tính conf trung bình của vùng lỗi (giá trị từ 0.0 -> 1.0)
            mean_conf = cv2.mean(prob_map, mask=single_cnt_mask)[0]

            # 1. Chỉ vẽ viền ngoài contour (thickness = 2)
            cv2.drawContours(display_img, [cnt], -1, border_color, thickness=2)

            # 2. Đổi màu chữ theo độ lớn diện tích:
            # <= ngưỡng -> Xanh lá | > ngưỡng -> Đỏ
            if area_pixels > limit_area:
                text_color = (0, 0, 255)      # Đỏ (Vượt ngưỡng diện tích)
                is_strictly_ng = True
                status_tag = "NG"
            else:
                text_color = (0, 255, 0)      # Xanh lá (Chấp nhận được)
                status_tag = "OK"

            # 3. Ghi text: Tên lỗi + Diện tích + Conf + Trạng thái
            x, y, w, h = cv2.boundingRect(cnt)
            label_text = f"{CLASS_NAMES[class_id]}: {int(area_pixels)}px | Conf: {mean_conf*100:.1f}% [{status_tag}]"
            
            # Tọa độ vẽ text
            text_pos_y = max(20, y - 6)
            cv2.putText(display_img, label_text, (x, text_pos_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, text_color, 1, cv2.LINE_AA)

            print(f"  + [{CLASS_NAMES[class_id]}] Diện tích: {area_pixels:.1f} px | Conf: {mean_conf*100:.1f}% -> {status_tag}")

    # Đánh giá tổng quát toàn sản phẩm
    if is_strictly_ng:
        cv2.putText(display_img, "TOTAL: NG", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3, cv2.LINE_AA)
    elif has_any_defect:
        cv2.putText(display_img, "TOTAL: WARNING (Minor)", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2, cv2.LINE_AA)
    else:
        cv2.putText(display_img, "TOTAL: OK", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3, cv2.LINE_AA)

    # Hiển thị
    cv2.imshow(win_mask, color_mask)
    cv2.imshow(win_result, display_img)

    # Bắt phím điều khiển
    while True:
        key = cv2.waitKey(0) & 0xFF
        if key in (ord('q'), ord('Q'), 32, 13):  # 'q', Space hoặc Enter
            break
        elif key == 27:  # Phím Esc để thoát
            print("\n--> Đã dừng chương trình.")
            cv2.destroyAllWindows()
            exit()

cv2.destroyAllWindows()
print("\n--> Đã duyệt xong toàn bộ ảnh trong thư mục!")