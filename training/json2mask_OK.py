import os
import json
import glob
import cv2
import numpy as np

# 1. Định nghĩa nhãn tương ứng với ID class (khớp với tên trên Labelme)
LABEL_MAPPING = {
    "background": 0,
    "NG_S": 1,    # Đốm xám nền
    "NG_H": 2,
    "NG_N": 3     # Lỗi chữ
}

# Đặt True nếu muốn hiển thị từng ảnh để kiểm tra, False để chạy tự động lưu hàng loạt
SHOW_PREVIEW = False

def convert_dataset_to_masks(input_dir, output_mask_dir):
    os.makedirs(output_mask_dir, exist_ok=True)
    
    # Quét tất cả các file ảnh trong thư mục (hỗ trợ .png, .jpg, .jpeg)
    image_extensions = ("*.png", "*.jpg", "*.jpeg")
    img_files = []
    for ext in image_extensions:
        img_files.extend(glob.glob(os.path.join(input_dir, ext)))
    
    img_files = sorted(img_files)
    print(f"--> Tìm thấy tổng cộng {len(img_files)} ảnh cần xử lý...")

    ng_count = 0
    ok_count = 0

    for img_path in img_files:
        base_name = os.path.splitext(os.path.basename(img_path))[0]
        json_path = os.path.join(input_dir, f"{base_name}.json")
        save_path = os.path.join(output_mask_dir, f"{base_name}.png")

        # Đọc ảnh để lấy kích thước chiều cao, chiều rộng
        img = cv2.imread(img_path)
        if img is None:
            print(f"Cảnh báo: Không thể đọc ảnh {img_path}")
            continue
            
        img_h, img_w = img.shape[:2]

        # Khởi tạo mask toàn số 0 (nền đen / hoàn toàn không có lỗi)
        mask = np.zeros((img_h, img_w), dtype=np.uint8)

        # Kiểm tra xem có file JSON đi kèm hay không
        if os.path.exists(json_path):
            ng_count += 1
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Vẽ từng polygon lên mask
            for shape in data.get("shapes", []):
                label_name = shape.get("label")
                points = shape.get("points")

                if label_name not in LABEL_MAPPING:
                    print(f"Cảnh báo: Bỏ qua nhãn lạ '{label_name}' trong file {os.path.basename(json_path)}")
                    continue

                class_id = LABEL_MAPPING[label_name]
                pts = np.array(points, dtype=np.int32).reshape((-1, 1, 2))
                cv2.fillPoly(mask, [pts], color=class_id)
        else:
            # Không có file JSON => Ảnh OK
            ok_count += 1

        # Lưu file mask với định dạng .png
        cv2.imwrite(save_path, mask)

        # Tùy chọn xem trước trực quan
        if SHOW_PREVIEW:
            view_mask = mask * 70  # 0: đen, 1: xám, 2: trắng
            cv2.imshow("Check Mask (Nhan phim bat ky de tiep tuc)", view_mask)
            if cv2.waitKey(0) & 0xFF == 27:  # Bấm Esc để thoát preview
                break

    if SHOW_PREVIEW:
        cv2.destroyAllWindows()

    print("\n" + "="*40)
    print(f"Hoàn tất chuyển đổi:")
    print(f" - Tổng số ảnh: {len(img_files)}")
    print(f" - Ảnh có lỗi (NG): {ng_count}")
    print(f" - Ảnh không lỗi (OK - mask toàn đen): {ok_count}")
    print(f" - Đã lưu mask vào thư mục: {output_mask_dir}")
    print("="*40)

# Chạy chuyển đổi
if __name__ == "__main__":
    # Thay đường dẫn thư mục ảnh của bạn ở đây
    INPUT_DIR = "dataset/a/raw_data" 
    OUTPUT_MASK_DIR = "dataset/a/masks" 
    
    convert_dataset_to_masks(INPUT_DIR, OUTPUT_MASK_DIR)