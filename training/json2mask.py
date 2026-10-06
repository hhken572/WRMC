import os
import json
import glob
import cv2
import numpy as np

# 1. Định nghĩa nhãn tương ứng với ID class (phải khớp chính xác tên bạn đặt trên Labelme)
LABEL_MAPPING = {
    "background": 0,
    "NG_H": 1,    # Thay bằng nhãn bạn gán cho đốm xám trên Labelme
    "NG_S": 2   # Thay bằng nhãn bạn gán cho lỗi chữ trên Labelme
}

def convert_labelme_json_to_mask(json_dir, output_mask_dir):
    os.makedirs(output_mask_dir, exist_ok=True)
    json_files = glob.glob(os.path.join(json_dir, "*.json"))
    
    print(f"Tìm thấy {len(json_files)} file JSON cần chuyển đổi...")

    for json_path in json_files:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        img_h = data.get("imageHeight")
        img_w = data.get("imageWidth")
        
        # Nếu file json không lưu kích thước ảnh, đọc trực tiếp từ file ảnh tương ứng
        if img_h is None or img_w is None:
            image_name = data.get("imagePath")
            img_real_path = os.path.join(json_dir, os.path.basename(image_name))
            img_temp = cv2.imread(img_real_path)
            img_h, img_w = img_temp.shape[:2]

        # Khởi tạo mask toàn số 0 (nền đen)
        mask = np.zeros((img_h, img_w), dtype=np.uint8)

        # Vẽ từng polygon lên mask
        for shape in data.get("shapes", []):
            label_name = shape.get("label")
            points = shape.get("points")

            if label_name not in LABEL_MAPPING:
                print(f"Cảnh báo: Bỏ qua nhãn lạ '{label_name}' trong file {os.path.basename(json_path)}")
                continue

            class_id = LABEL_MAPPING[label_name]
            # Đổi tọa độ sang dạng integer của OpenCV
            pts = np.array(points, dtype=np.int32).reshape((-1, 1, 2))
            
            # cv2.fillPoly tô kín vùng polygon với giá trị pixel = class_id
            cv2.fillPoly(mask, [pts], color=class_id)
        
        # Đoạn code kiểm tra trực quan
        view_mask = mask * 100  # class 1 thành 100, class 2 thành 200
        cv2.imshow("Check Mask", view_mask)
        cv2.waitKey(0)

        # Lưu file mask với tên trùng tên ảnh gốc (đuôi .png để tránh nén mất mát pixel)
        base_name = os.path.splitext(os.path.basename(json_path))[0]
        save_path = os.path.join(output_mask_dir, f"{base_name}.png")
        cv2.imwrite(save_path, mask)

    print("Hoàn tất chuyển đổi toàn bộ file JSON sang Mask PNG!")

# Chạy chuyển đổi
if __name__ == "__main__":
    # Đường dẫn thư mục chứa ảnh + file .json bạn vừa gắn nhãn
    INPUT_DIR = "raw_data" 
    # Thư mục xuất ra mask
    OUTPUT_MASK_DIR = "masks1" 
    
    convert_labelme_json_to_mask(INPUT_DIR, OUTPUT_MASK_DIR)