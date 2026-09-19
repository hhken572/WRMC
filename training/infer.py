# import cv2
# import numpy as np
# import torch
# import albumentations as A
# from albumentations.pytorch import ToTensorV2
# import segmentation_models_pytorch as smp

# # Hệ số quy đổi camera: ví dụ 1 pixel = 0.05 mm
# MM_PER_PIXEL = 0.05 
# CLASS_NAMES = {1: "Đốm xám nền", 2: "Lỗi chữ trắng"}

# # Load model
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model = smp.Unet(encoder_name="resnet18", classes=3).to(device)
# model.load_state_dict(torch.load("best_resnet18_unet.pth", map_location=device))
# model.eval()

# # Preprocess ảnh test
# raw_img = cv2.imread("Image_20260905135721869.png")
# h_orig, w_orig = raw_img.shape[:2]
# input_tensor = val_transform(image=cv2.cvtColor(raw_img, cv2.COLOR_BGR2RGB))["image"].unsqueeze(0).to(device)

# with torch.no_grad():
#     logits = model(input_tensor)
#     pred_mask = torch.argmax(logits, dim=1).squeeze(0).cpu().numpy().astype(np.uint8)

# # Resize mask về kích thước ảnh gốc
# pred_mask = cv2.resize(pred_mask, (w_orig, h_orig), interpolation=cv2.INTER_NEAREST)

# # Trích xuất diện tích từng class
# for class_id in [1, 2]:
#     # Tạo mask nhị phân cho từng class
#     binary_mask = (pred_mask == class_id).astype(np.uint8) * 255
    
#     # Tìm các đốm / vùng lỗi độc lập
#     num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_mask, connectivity=8)
    
#     print(f"\n--- Kết quả phát hiện: {CLASS_NAMES[class_id]} ---")
#     defect_count = 0
#     for i in range(1, num_labels):  # Bỏ qua nhãn 0 (nền)
#         area_pixels = stats[i, cv2.CC_STAT_AREA]
        
#         # Bỏ qua nhiễu hạt quá nhỏ
#         if area_pixels < 5:
#             continue
            
#         defect_count += 1
#         x = stats[i, cv2.CC_STAT_LEFT]
#         y = stats[i, cv2.CC_STAT_TOP]
#         w = stats[i, cv2.CC_STAT_WIDTH]
#         h = stats[i, cv2.CC_STAT_HEIGHT]
        
#         area_mm2 = area_pixels * (MM_PER_PIXEL ** 2)
#         print(f"  + Vết #{defect_count}: Tọa độ [X:{x}, Y:{y}, W:{w}, H:{h}] | Diện tích: {area_pixels} px ({area_mm2:.4f} mm²)")
        
#         # Vẽ bbox đánh dấu lỗi lên ảnh
#         color = (0, 165, 255) if class_id == 1 else (0, 0, 255)
#         cv2.rectangle(raw_img, (x, y), (x + w, y + h), color, 2)

# cv2.imwrite("result_detected.jpg", raw_img)









import os
import cv2
import numpy as np
import torch
import albumentations as A
from albumentations.pytorch import ToTensorV2
import segmentation_models_pytorch as smp

# 1. Định nghĩa pipeline tiền xử lý cho ảnh test (giống lúc validation)
val_transform = A.Compose([
    A.Resize(512, 512),
    A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ToTensorV2(),
])

# 2. Cấu hình thông số
IMAGE_PATH = "Image_20260905140454799.png"         # Đường dẫn ảnh cần test
MODEL_WEIGHTS = "resnet18_unet_4cls.pth" # File checkpoint đã train
OUTPUT_PATH = "result_detected.jpg"    # Ảnh xuất ra sau khi vẽ lỗi
MM_PER_PIXEL = 0.05                    # Hệ số camera quy đổi 1 pixel = ? mm (tùy chỉnh)

CLASS_NAMES = {
    1: "NG_S",
    2: "NG_H",
    3: "NG_N"
}
CLASS_COLORS = {
    1: (0, 165, 255),  # Màu cam cho đốm xám (BGR)
    2: (0, 0, 255),     # Màu đỏ cho lỗi chữ (BGR)
    3: (255, 255, 0)
}

# 3. Khởi tạo và nạp Model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"--> Đang sử dụng thiết bị: {device}")

model = smp.Unet(
    encoder_name="resnet18",
    in_channels=3,
    classes=4
).to(device)

if not os.path.exists(MODEL_WEIGHTS):
    raise FileNotFoundError(f"Không tìm thấy file trọng số: {MODEL_WEIGHTS}")

model.load_state_dict(torch.load(MODEL_WEIGHTS, map_location=device))
model.eval()

# 4. Đọc và tiền xử lý ảnh
raw_img = cv2.imread(IMAGE_PATH)
if raw_img is None:
    raise FileNotFoundError(f"Không thể đọc ảnh đầu vào: {IMAGE_PATH}")

h_orig, w_orig = raw_img.shape[:2]

# Chuyển đổi màu và áp dụng transform
rgb_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2RGB)
augmented = val_transform(image=rgb_img)
input_tensor = augmented["image"].unsqueeze(0).to(device)

# 5. Inference
with torch.no_grad():
    logits = model(input_tensor)
    pred_mask = torch.argmax(logits, dim=1).squeeze(0).cpu().numpy().astype(np.uint8)

# Resize mask dự đoán về kích thước ban đầu của ảnh
pred_mask = cv2.resize(pred_mask, (w_orig, h_orig), interpolation=cv2.INTER_NEAREST)

# 6. Trích xuất diện tích và vẽ CONTOUR
print("\n" + "="*50)
print("KẾT QUẢ KIỂM ĐỊNH LỖI NGOẠI QUAN (CONTOUR)")
print("="*50)

# Tạo một bản sao để vẽ lớp phủ màu bán trong suốt (overlay)
overlay = raw_img.copy()
total_defects_found = 0

for class_id in [1, 2, 3]:
    # Tạo mask nhị phân cho class hiện tại
    binary_mask = (pred_mask == class_id).astype(np.uint8) * 255
    
    # Tìm các đường bao contour
    # cv2.RETR_EXTERNAL: chỉ lấy đường bao ngoài cùng
    # cv2.CHAIN_APPROX_SIMPLE: nén các điểm thẳng để tiết kiệm bộ nhớ
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    defect_count = 0
    print(f"\n[Loại lỗi: {CLASS_NAMES[class_id]}]")
    color = CLASS_COLORS[class_id]
    
    for cnt in contours:
        # Tính diện tích chính xác theo contour (tính theo pixel)
        area_pixels = cv2.contourArea(cnt)
        
        # Lọc bỏ nhiễu hạt quá nhỏ (dưới 5 pixel)
        if area_pixels < 5:
            continue
            
        defect_count += 1
        total_defects_found += 1
        area_mm2 = area_pixels * (MM_PER_PIXEL ** 2)
        
        # 1. Tô kín phần ruột của lỗi lên lớp overlay
        cv2.drawContours(overlay, [cnt], -1, color, thickness=cv2.FILLED)
        
        # 2. Vẽ viền nét ngoài contour lên ảnh gốc (độ dày viền = 2)
        cv2.drawContours(raw_img, [cnt], -1, color, thickness=2)
        
        # Lấy tọa độ một điểm trên viền để gắn text tên lỗi
        x, y, w, h = cv2.boundingRect(cnt)
        print(f"  + Vết #{defect_count}: Tọa độ [X:{x}, Y:{y}] | Diện tích: {area_pixels:.1f} px (~{area_mm2:.4f} mm²)")
        
        cv2.putText(raw_img, f"{CLASS_NAMES[class_id]}: {int(area_pixels)}px", 
                    (x, max(15, y - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1, cv2.LINE_AA)

    if defect_count == 0:
        print("  --> Không phát hiện lỗi.")

# Trộn ảnh gốc với overlay để tạo hiệu ứng trong suốt 30% (alpha blending)
alpha = 0.3
cv2.addWeighted(overlay, alpha, raw_img, 1 - alpha, 0, raw_img)

# Lưu kết quả
cv2.imwrite(OUTPUT_PATH, raw_img)
print(f"\n--> Đã lưu ảnh kết quả vào: {OUTPUT_PATH}")
print(f"--> Tổng số lỗi phát hiện: {total_defects_found}")