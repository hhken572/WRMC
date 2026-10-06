import cv2
import numpy as np
# Chạy thử 1 dòng này với ảnh mask nghi ngờ
mask_test = cv2.imread("dataset/a/masks/Image_20260905135621719.png", cv2.IMREAD_GRAYSCALE)
print("Các giá trị pixel trong mask gốc:", np.unique(mask_test))