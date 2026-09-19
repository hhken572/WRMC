# import time
# # pyrefly: ignore [missing-import]
# import cv2
# # pyrefly: ignore [missing-import]
# import numpy as np
# import time
# from datetime import datetime
# import os


# class AIInferenceEngine:
#     def __init__(self, model_ai1_path=None, model_ai2_path=None, model_ai3_path=None):
#         print("AI Inference Engine khoi tao.")
#         self.save_dir1 = "saved_images/ai_1"
#         os.makedirs(self.save_dir1, exist_ok=True)
    
#     def run_ai_1(self, image):
#         time.sleep(0.03)
#         annotated = image.copy()
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
#         filename = f"{timestamp}.jpg"
#         filepath = os.path.join(self.save_dir1, filename)
#         cv2.imwrite(filepath, annotated)
#         is_ok = True
#         cv2.putText(annotated, "AI1: OK", (10,100), cv2.FONT_HERSHEY_SIMPLEX, 4, (0,255,0), 4)
#         return is_ok, "AI1_OK", annotated
    
#     def run_ai_2(self, image):
#         time.sleep(0.03)
#         annotated = image.copy()
#         is_ok = True
#         cv2.putText(annotated, "AI2: OK", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
#         return is_ok, "AI2_OK", annotated
    
#     def run_ai_3(self, image):
#         time.sleep(0.03)
#         annotated = image.copy()
#         is_ok = True
#         cv2.putText(annotated, "AI3: OK", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
#         return is_ok, "AI3_OK", annotated




import os
import time
from datetime import datetime
import cv2
import numpy as np
from ultralytics import YOLO


class AIInferenceEngine:
    def __init__(self, model_ai1_path=None, model_ai2_path=None, model_ai3_path=None):
        print("AI Inference Engine khoi tao.")
        # self.save_dir1 = r"D:\WRMC\models\cam1_ver2.pt"
        # self.save_dir3 = r"D:\WRMC\models\cam2.pt"
        # os.makedirs(self.save_dir1, exist_ok=True)
        # os.makedirs(self.save_dir3, exist_ok=True)

        # 2. Gán đường dẫn file weights model .pt
        if model_ai1_path is None:
            model_ai1_path = r"D:\WRMC\models\cam1_ver2.pt"
        if model_ai3_path is None:
            model_ai3_path = r"D:\WRMC\models\cam2.pt"

        # 1. Khởi tạo Model AI 1 (Segmentation)
        self.model1 = None
        if model_ai1_path and os.path.exists(model_ai1_path):
            print(f"[AI 1] Dang tai weights: {model_ai1_path}")
            self.model1 = YOLO(model_ai1_path)
            self._warmup(self.model1, "AI 1", imgsz=640)

        # 2. Khởi tạo Model AI 3 (Segmentation)
        self.model3 = None
        if model_ai3_path and os.path.exists(model_ai3_path):
            print(f"[AI 3] Dang tai weights: {model_ai3_path}")
            self.model3 = YOLO(model_ai3_path)
            self._warmup(self.model3, "AI 3", imgsz=640)

    def _warmup(self, model, name: str, imgsz: int = 640):
        dummy_img = np.zeros((imgsz, imgsz, 3), dtype=np.uint8)
        model.predict(source=dummy_img, imgsz=imgsz, verbose=False)
        print(f"[{name}] Warm-up hoan tat.")

    def run_ai_1(self, image):
        annotated = image.copy()
        
        # # Lưu ảnh gốc trước khi vẽ kết quả
        # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        # filepath = os.path.join(self.save_dir1, f"{timestamp}.jpg")
        # cv2.imwrite(filepath, image)

        is_ok = True
        ng_count = 0

        if self.model1 is not None:
            results = self.model1.predict(source=image, conf=0.3, imgsz=640, verbose=False)
            res = results[0]

            if res.masks is not None:
                polygons = res.masks.xy
                boxes = res.boxes
                ng_count = len(polygons)

                for i, polygon in enumerate(polygons):
                    pts = np.int32(polygon)
                    # Chỉ vẽ viền đường bao lỗi (màu đỏ)
                    cv2.polylines(annotated, [pts], isClosed=True, color=(0, 0, 255), thickness=3)

                    # Ghi nhãn và score
                    cls_id = int(boxes.cls[i])
                    score = float(boxes.conf[i])
                    class_name = self.model1.names[cls_id]
                    label = f"{class_name}: {score:.2f}"

                    top_pt = tuple(pts[pts[:, 1].argmin()])
                    txt_pos = (max(0, top_pt[0] - 10), max(25, top_pt[1] - 10))
                    cv2.putText(annotated, label, txt_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 4)
                    cv2.putText(annotated, label, txt_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        if ng_count > 0:
            is_ok = False
            msg = f"AI1_NG ({ng_count})"
            cv2.putText(annotated, f"AI1: NG ({ng_count})", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 4)
        else:
            msg = "AI1_OK"
            cv2.putText(annotated, "AI1: OK", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 4)

        return is_ok, msg, annotated

    def run_ai_2(self, image):
        time.sleep(0.03)
        annotated = image.copy()
        is_ok = True
        # cv2.putText(annotated, "AI2: OK", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return is_ok, "AI2_OK", annotated

    def run_ai_3(self, image):
        annotated = image.copy()
        
        # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        # filepath = os.path.join(self.save_dir3, f"{timestamp}.jpg")
        # cv2.imwrite(filepath, image)

        is_ok = True
        ng_count = 0

        if self.model3 is not None:
            results = self.model3.predict(source=image, conf=0.2, imgsz=640, verbose=False)
            res = results[0]

            if res.masks is not None:
                polygons = res.masks.xy
                boxes = res.boxes
                ng_count = len(polygons)

                for i, polygon in enumerate(polygons):
                    pts = np.int32(polygon)
                    cv2.polylines(annotated, [pts], isClosed=True, color=(0, 0, 255), thickness=3)

                    cls_id = int(boxes.cls[i])
                    score = float(boxes.conf[i])
                    class_name = self.model3.names[cls_id]
                    label = f"{class_name}: {score:.2f}"

                    top_pt = tuple(pts[pts[:, 1].argmin()])
                    txt_pos = (max(0, top_pt[0] - 10), max(25, top_pt[1] - 10))
                    cv2.putText(annotated, label, txt_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 4)
                    cv2.putText(annotated, label, txt_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        if ng_count > 0:
            is_ok = False
            msg = f"AI3_NG ({ng_count})"
            cv2.putText(annotated, f"AI3: NG ({ng_count})", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 4)
        else:
            msg = "AI3_OK"
            cv2.putText(annotated, "AI3: OK", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 4)

        return is_ok, msg, annotated