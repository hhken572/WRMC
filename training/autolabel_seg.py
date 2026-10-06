import glob
import json
import os
import albumentations as A
from albumentations.pytorch import ToTensorV2
import cv2
import numpy as np
import segmentation_models_pytorch as smp
import torch
import torch.nn.functional as F
from tqdm import tqdm

# ==========================================
# 1. CẤU HÌNH ĐƯỜNG DẪN & THÔNG SỐ
# ==========================================
IMAGE_DIR = "datasetc1_v3/draf/pic_new"  # Thư mục ảnh cần auto-label
MODEL_WEIGHTS = "resnet50_unet_4cls_c1_v2.pth"  # File weights model đã train

CLASS_NAMES = {
    1: "NG_ThieuSon",
    2: "NG_LemSon",
    3: "NG_HoaChat",
}

# Ngưỡng Confidence lọc lỗi
CONF_THRESHOLDS = {
    1: 0.60,
    2: 0.50,
    3: 0.60,
}
DEFAULT_CONF = 0.50

MIN_AREA_NOISE = 10  # Bỏ qua các đốm nhiễu nhỏ hơn N pixel
EPSILON_FACTOR = 0.025  # Hệ số làm mượt polygon (approxPolyDP). Càng lớn số điểm càng ít.

# Ghi đè file JSON nếu đã tồn tại hay bỏ qua?
OVERWRITE_EXISTING = True

# ==========================================
# 2. PIPELINE TIỀN XỬ LÝ
# ==========================================
transform = A.Compose(
    [
        A.Resize(512, 512),
        A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
        ToTensorV2(),
    ]
)

# ==========================================
# 3. NẠP MODEL
# ==========================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"--> Sử dụng thiết bị: {device}")

model = smp.Unet(
    encoder_name="resnet50",
    in_channels=3,
    classes=4,
).to(device)

if not os.path.exists(MODEL_WEIGHTS):
    raise FileNotFoundError(f"Không tìm thấy checkpoint: {MODEL_WEIGHTS}")

model.load_state_dict(torch.load(MODEL_WEIGHTS, map_location=device))
model.eval()

# ==========================================
# 4. DUYỆT ẢNH & XUẤT JSON LABELME
# ==========================================
valid_exts = ("*.png", "*.jpg", "*.jpeg", "*.bmp")
img_files = []
for ext in valid_exts:
    img_files.extend(glob.glob(os.path.join(IMAGE_DIR, ext)))
img_files = sorted(img_files)

print(f"--> Tìm thấy {len(img_files)} ảnh cần xử lý.")

for img_path in tqdm(img_files, desc="Auto Labeling"):
    base_name = os.path.splitext(img_path)[0]
    json_path = f"{base_name}.json"

    if not OVERWRITE_EXISTING and os.path.exists(json_path):
        continue

    raw_img = cv2.imread(img_path)
    if raw_img is None:
        continue

    h_orig, w_orig = raw_img.shape[:2]
    file_name = os.path.basename(img_path)

    # Tiền xử lý & Model Infer
    rgb_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2RGB)
    augmented = transform(image=rgb_img)
    input_tensor = augmented["image"].unsqueeze(0).to(device)

    with torch.no_grad():
        logits = model(input_tensor)
        probs = F.softmax(logits, dim=1).squeeze(0)
        max_probs, pred_classes = torch.max(probs, dim=0)

    # Lọc ngưỡng xác suất (confidence)
    filtered_mask = torch.zeros_like(pred_classes, dtype=torch.uint8)
    for class_id in [1, 2, 3]:
        conf_thresh = CONF_THRESHOLDS.get(class_id, DEFAULT_CONF)
        mask_condition = (pred_classes == class_id) & (max_probs >= conf_thresh)
        filtered_mask[mask_condition] = class_id

    # Đưa mask về kích thước gốc
    pred_mask = filtered_mask.cpu().numpy()
    pred_mask = cv2.resize(
        pred_mask, (w_orig, h_orig), interpolation=cv2.INTER_NEAREST
    )

    shapes = []

    # Trích xuất polygon từng class
    for class_id, label_name in CLASS_NAMES.items():
        binary_mask = (pred_mask == class_id).astype(np.uint8) * 255
        contours, _ = cv2.findContours(
            binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for cnt in contours:
            if cv2.contourArea(cnt) < MIN_AREA_NOISE:
                continue

            # Làm mượt đa giác: giảm tải điểm giúp LabelMe chạy nhẹ
            epsilon = EPSILON_FACTOR * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            # LabelMe yêu cầu polygon phải có tối thiểu 3 điểm
            if len(approx) < 3:
                continue

            # Chuyển đổi tọa độ sang định dạng float [[x1, y1], [x2, y2], ...]
            points = approx.reshape(-1, 2).astype(float).tolist()

            shape_dict = {
                "label": label_name,
                "points": points,
                "group_id": None,
                "description": "",
                "shape_type": "polygon",
                "flags": {},
                "mask": None,
            }
            shapes.append(shape_dict)

    # Khung cấu trúc dữ liệu chuẩn của LabelMe
    labelme_data = {
        "version": "6.3.1",
        "flags": {},
        "shapes": shapes,
        "imagePath": file_name,
        "imageData": None,  # Để None để file nhẹ, LabelMe sẽ tự đọc từ imagePath
        "imageHeight": int(h_orig),
        "imageWidth": int(w_orig),
    }

    # Ghi file json
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(labelme_data, f, ensure_ascii=False, indent=2)

print("\n--> Hoàn tất! Bạn có thể mở LabelMe và trỏ vào thư mục ảnh để review.")

