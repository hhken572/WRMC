import os
import glob
import cv2

def convert_jpg_to_png(input_dir, output_dir=None, delete_original=False):
    """
    Chuyển đổi toàn bộ file .jpg / .jpeg trong input_dir sang .png
    - input_dir: Thư mục chứa ảnh JPG
    - output_dir: Thư mục lưu ảnh PNG (nếu None sẽ lưu cùng thư mục với ảnh gốc)
    - delete_original: True nếu muốn xóa file .jpg sau khi chuyển đổi xong
    """
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    else:
        output_dir = input_dir

    # Tìm tất cả file .jpg và .jpeg (không phân biệt hoa/thường)
    jpg_files = glob.glob(os.path.join(input_dir, "*.[jJ][pP][gG]")) + \
                glob.glob(os.path.join(input_dir, "*.[jJ][pP][eE][gG]"))

    print(f"Tìm thấy {len(jpg_files)} file JPG.")

    success_count = 0
    for img_path in jpg_files:
        # Đọc ảnh
        img = cv2.imread(img_path)
        if img is None:
            print(f"Không thể đọc file: {img_path}")
            continue

        # Lấy tên file không kèm đuôi
        base_name = os.path.splitext(os.path.basename(img_path))[0]
        save_path = os.path.join(output_dir, f"{base_name}.png")

        # Lưu ảnh dưới định dạng PNG (nén không mất dữ liệu)
        cv2.imwrite(save_path, img)
        success_count += 1

        # Xóa file cũ nếu cần
        if delete_original:
            os.remove(img_path)

    print(f"Hoàn thành! Đã chuyển đổi {success_count}/{len(jpg_files)} ảnh sang .png")

# --- Hướng dẫn sử dụng ---
if __name__ == "__main__":
    # Thay đổi đường dẫn thư mục tại đây:
    INPUT_FOLDER = "ai_1"
    
    # Lưu sang thư mục riêng (hoặc để output_dir=None nếu muốn lưu đè vào cùng folder)
    OUTPUT_FOLDER = "ai1" 

    convert_jpg_to_png(
        input_dir=INPUT_FOLDER, 
        output_dir=OUTPUT_FOLDER, 
        delete_original=False  # Đổi thành True nếu muốn xóa file .jpg cũ
    )