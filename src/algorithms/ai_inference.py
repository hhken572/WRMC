# #ai_inference.py
# import os
# import time
# import cv2
# import numpy as np
# import torch
# import albumentations as A
# from albumentations.pytorch import ToTensorV2
# import segmentation_models_pytorch as smp


# class AIInferenceEngine:
#     def __init__(
#         self,
#         model_ai1_path=r"resnet50_unet_4cls_c1_v2.pth",
#         model_ai2_path=None,
#         model_ai3_path=r"resnet50_unet_4cls_c2.pth",
#         num_classes=4,
#         img_size=(512, 512),
#         min_area=5,
#         mm_per_pixel=0.05
#     ):
#         print("AI Inference Engine khởi tạo...")
#         self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#         self.num_classes = num_classes
#         self.min_area = min_area
#         self.mm_per_pixel = mm_per_pixel
#         print(f"[AI Engine] Chạy trên thiết bị: {self.device}")

#         # 1. Bảng nhãn lỗi riêng biệt cho từng model
#         self.class_names_ai1 = {
#             1: "NG_ThieuSon",
#             2: "NG_LemSon",
#             3: "NG_HoaChat"
#         }
#         self.class_names_ai3 = {
#             1: "NG_ChamDen",
#             2: "NG_OVang",
#             3: "NG_Can"
#         }

#         # Bảng màu BGR đánh dấu lỗi
#         self.class_colors = {
#             1: (0, 165, 255),  # Cam
#             2: (0, 0, 255),    # Đỏ
#             3: (0, 255, 255)   # Vàng
#         }

#         # Pipeline tiền xử lý chuẩn
#         self.transform = A.Compose([
#             A.Resize(img_size[0], img_size[1]),
#             A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
#             ToTensorV2(),
#         ])

#         # Nạp Model AI 1
#         self.model1 = None
#         if model_ai1_path and os.path.exists(model_ai1_path):
#             print(f"[AI 1] Tải trọng số: {model_ai1_path}")
#             self.model1 = self._load_smp_model(model_ai1_path)
#             self._warmup(self.model1, "AI 1", img_size)

#         # Nạp Model AI 3
#         self.model3 = None
#         if model_ai3_path and os.path.exists(model_ai3_path):
#             print(f"[AI 3] Tải trọng số: {model_ai3_path}")
#             self.model3 = self._load_smp_model(model_ai3_path)
#             self._warmup(self.model3, "AI 3", img_size)

#     def _load_smp_model(self, weight_path):
#         model = smp.Unet(
#             encoder_name="resnet50",
#             in_channels=3,
#             classes=self.num_classes
#         ).to(self.device)

#         state_dict = torch.load(weight_path, map_location=self.device)
#         if "model_state_dict" in state_dict:
#             state_dict = state_dict["model_state_dict"]
#         elif "state_dict" in state_dict:
#             state_dict = state_dict["state_dict"]

#         model.load_state_dict(state_dict)
#         model.eval()
#         return model

#     def _warmup(self, model, name: str, img_size):
#         dummy_tensor = torch.zeros((1, 3, img_size[0], img_size[1]), device=self.device)
#         with torch.no_grad():
#             _ = model(dummy_tensor)
#         print(f"[{name}] Warm-up hoàn tất.")

#     def _infer_and_draw(self, model, image, class_names: dict, cam_prefix="AI1"):
#         h_orig, w_orig = image.shape[:2]

#         # Tiền xử lý RGB + Albumentations
#         rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         augmented = self.transform(image=rgb_img)
#         input_tensor = augmented["image"].unsqueeze(0).to(self.device)

#         with torch.no_grad():
#             logits = model(input_tensor)
#             pred_mask = torch.argmax(logits, dim=1).squeeze(0).cpu().numpy().astype(np.uint8)

#         pred_mask = cv2.resize(pred_mask, (w_orig, h_orig), interpolation=cv2.INTER_NEAREST)

#         overlay = image.copy()
#         display_img = image.copy()
#         ng_count = 0

#         for class_id in [1, 2, 3]:
#             binary_mask = (pred_mask == class_id).astype(np.uint8) * 255
#             contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#             color = self.class_colors.get(class_id, (0, 0, 255))
#             cls_name = class_names.get(class_id, f"Defect_{class_id}")

#             for cnt in contours:
#                 area_pixels = cv2.contourArea(cnt)
#                 if area_pixels < self.min_area:
#                     continue

#                 ng_count += 1
#                 area_mm2 = area_pixels * (self.mm_per_pixel ** 2)

#                 # Vẽ vùng lỗi & viền
#                 # cv2.drawContours(overlay, [cnt], -1, color, thickness=cv2.FILLED)
#                 cv2.drawContours(display_img, [cnt], -1, color, thickness=2)

#                 # Vẽ nhãn text theo tên class tương ứng
#                 x, y, w, h = cv2.boundingRect(cnt)
#                 label_text = f"{cls_name}: {int(area_pixels)}px"
#                 cv2.putText(
#                     display_img,
#                     label_text,
#                     (x, max(18, y - 5)),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     1,
#                     color,
#                     2,
#                     cv2.LINE_AA
#                 )

#         # # Trộn màu overlay 30%
#         # cv2.addWeighted(overlay, 0.3, display_img, 0.7, 0, display_img)

#         if ng_count > 0:
#             is_ok = False
#             msg = f"{cam_prefix}_NG ({ng_count})"
#             cv2.putText(display_img, f"STATUS: NG ({ng_count})", (30, 50),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2, cv2.LINE_AA)
#         else:
#             is_ok = True
#             msg = f"{cam_prefix}_OK"
#             cv2.putText(display_img, "STATUS: OK", (30, 50),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv2.LINE_AA)

#         return is_ok, msg, display_img

#     def run_ai_1(self, image):
#         if self.model1 is None:
#             return True, "AI1_SKIP", image
#         return self._infer_and_draw(self.model1, image, self.class_names_ai1, cam_prefix="AI1")

#     def run_ai_2(self, image):
#         time.sleep(0.03)
#         return True, "AI2_OK", image

#     def run_ai_3(self, image):
#         if self.model3 is None:
#             return True, "AI3_SKIP", image
#         return self._infer_and_draw(self.model3, image, self.class_names_ai3, cam_prefix="AI3")




















# ai_inference.py
from pathlib import Path
import os
import time
import cv2
import numpy as np
import torch
import torch.nn.functional as F
import albumentations as A
from albumentations.pytorch import ToTensorV2
import segmentation_models_pytorch as smp
import json


class AIInferenceEngine:
    def __init__(
        self,
        model_ai1_path=r"resnet50_unet_4cls_c1_v5.pth",
        model_ai2_path=None,
        model_ai3_path=r"resnet50_unet_4cls_c2_v4.pth",
        num_classes=4,
        img_size=(512, 512),
        min_area=5,
        mm_per_pixel=0.05
    ):
        print("AI Inference Engine khởi tạo...")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.num_classes = num_classes
        self.min_area = min_area
        self.mm_per_pixel = mm_per_pixel
        print(f"[AI Engine] Chạy trên thiết bị: {self.device}")

        # 1. Bảng nhãn lỗi riêng biệt cho từng model
        self.class_names_ai1 = {
            1: "NG_ThieuSon",
            2: "NG_LemSon",
            3: "NG_HoaChat"
        }
        self.class_names_ai3 = {
            1: "NG_ChamDen",
            2: "NG_OVang",
            3: "NG_Can"
        }

        # Bảng màu BGR đánh dấu viền lỗi
        self.class_colors = {
            1: (0, 165, 255),  # Cam
            2: (0, 0, 255),    # Đỏ
            3: (0, 255, 255)   # Vàng
        }

        # ==============================================================
        # 2. TÁCH RIÊNG BIỆT 6 QUY LUẬT PHÁN ĐỊNH CHO AI 1 VÀ AI 3
        # - Area <= x: Luôn OK
        # - x < Area <= y: NG nếu Conf >= conf_mid
        # - Area > y: NG nếu Conf >= conf_large (giảm phụ thuộc vào conf)
        # ==============================================================

        # --- 3 QUY LUẬT CHO MODEL AI 1 ---
        self.rules_ai1 = {
            1: {"x": 250, "y": 500, "conf_mid": 0.85, "conf_large": 0.50},  # 1. NG_ThieuSon
            2: {"x": 250, "y": 500, "conf_mid": 0.85, "conf_large": 0.50},  # 2. NG_LemSon
            3: {"x": 400, "y": 800, "conf_mid": 0.85, "conf_large": 0.50},  # 3. NG_HoaChat
        }

        # --- 3 QUY LUẬT CHO MODEL AI 3 ---
        self.rules_ai3 = {
            1: {"x": 100, "y": 500, "conf_mid": 0.80, "conf_large": 0.50},  # 4. NG_ChamDen (đốm nhỏ cần khắt khe)
            2: {"x": 700, "y": 1500, "conf_mid": 0.80, "conf_large": 0.50}, # 5. NG_OVang (vết loang mờ)
            3: {"x": 250, "y": 500, "conf_mid": 0.80, "conf_large": 0.50},  # 6. NG_Can
        }

        self.default_rule = {"x": 30, "y": 80, "conf_mid": 0.60, "conf_large": 0.40}

        # Pipeline tiền xử lý chuẩn
        self.transform = A.Compose([
            A.Resize(img_size[0], img_size[1]),
            A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
            ToTensorV2(),
        ])

        # Nạp Model AI 1
        self.model1 = None
        if model_ai1_path and os.path.exists(model_ai1_path):
            print(f"[AI 1] Tải trọng số: {model_ai1_path}")
            self.model1 = self._load_smp_model(model_ai1_path)
            self._warmup(self.model1, "AI 1", img_size)

        # Nạp Model AI 3
        self.model3 = None
        if model_ai3_path and os.path.exists(model_ai3_path):
            print(f"[AI 3] Tải trọng số: {model_ai3_path}")
            self.model3 = self._load_smp_model(model_ai3_path)
            self._warmup(self.model3, "AI 3", img_size)

        
        # Trong hàm __init__:
        project_root = Path(__file__).resolve().parents[2]  # Lùi 2 cấp từ src/algorithms về WRMC
        config_path = str(project_root / "data" / "rules_config.json")
        self.load_rules_from_file(config_path)

    def _load_smp_model(self, weight_path):
        model = smp.Unet(
            encoder_name="resnet50",
            in_channels=3,
            classes=self.num_classes
        ).to(self.device)

        state_dict = torch.load(weight_path, map_location=self.device)
        if "model_state_dict" in state_dict:
            state_dict = state_dict["model_state_dict"]
        elif "state_dict" in state_dict:
            state_dict = state_dict["state_dict"]

        model.load_state_dict(state_dict)
        model.eval()
        return model

    def _warmup(self, model, name: str, img_size):
        dummy_tensor = torch.zeros((1, 3, img_size[0], img_size[1]), device=self.device)
        with torch.no_grad():
            _ = model(dummy_tensor)
        print(f"[{name}] Warm-up hoàn tất.")

    def _infer_and_draw(self, model, image, class_names: dict, rules: dict, cam_prefix="AI1"):
        h_orig, w_orig = image.shape[:2]

        # Tiền xử lý RGB + Albumentations
        rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        augmented = self.transform(image=rgb_img)
        input_tensor = augmented["image"].unsqueeze(0).to(self.device)

        # Inference và tính ma trận Softmax xác suất
        with torch.no_grad():
            logits = model(input_tensor)
            probs = F.softmax(logits, dim=1).squeeze(0)          # [4, 512, 512]
            max_probs, pred_classes = torch.max(probs, dim=0)   # [512, 512]

        # Đưa kết quả về kích thước ảnh gốc
        pred_mask = pred_classes.cpu().numpy().astype(np.uint8)
        pred_mask = cv2.resize(pred_mask, (w_orig, h_orig), interpolation=cv2.INTER_NEAREST)

        prob_map = max_probs.cpu().numpy()
        prob_map = cv2.resize(prob_map, (w_orig, h_orig), interpolation=cv2.INTER_LINEAR)

        display_img = image.copy()
        ng_count = 0

        for class_id in [1, 2, 3]:
            binary_mask = (pred_mask == class_id).astype(np.uint8) * 255
            contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            color = self.class_colors.get(class_id, (0, 0, 255))
            cls_name = class_names.get(class_id, f"Defect_{class_id}")

            # Lấy bộ quy luật riêng của class đó theo model đang chạy
            rule = rules.get(class_id, self.default_rule)
            x_limit = rule["x"]
            y_limit = rule["y"]
            conf_mid = rule["conf_mid"]
            conf_large = rule["conf_large"]

            for cnt in contours:
                area_pixels = cv2.contourArea(cnt)
                if area_pixels < self.min_area:
                    continue

                # Tạo mask cục bộ để tính Confidence trung bình của vùng contour
                single_cnt_mask = np.zeros((h_orig, w_orig), dtype=np.uint8)
                cv2.drawContours(single_cnt_mask, [cnt], -1, 255, thickness=cv2.FILLED)
                mean_conf = cv2.mean(prob_map, mask=single_cnt_mask)[0]

                # 2. Logic phán định NG theo 3 tầng diện tích:
                is_defect_ng = False
                reason = ""

                if area_pixels <= x_limit:
                    # Mức 1: 0 -> x (Quá nhỏ, coi là OK)
                    is_defect_ng = False
                    reason = f"Area({int(area_pixels)}) <= x({x_limit}) -> Chấp nhận (OK)"
                elif area_pixels <= y_limit:
                    # Mức 2: x -> y (Trung bình, cần conf cao mới tính NG)
                    if mean_conf >= conf_mid:
                        is_defect_ng = True
                        reason = f"x({x_limit}) < Area({int(area_pixels)}) <= y({y_limit}) & Conf({mean_conf*100:.1f}%) >= conf_mid({conf_mid*100:.1f}%) -> NG"
                    else:
                        is_defect_ng = False
                        reason = f"x({x_limit}) < Area({int(area_pixels)}) <= y({y_limit}) & Conf({mean_conf*100:.1f}%) < conf_mid({conf_mid*100:.1f}%) -> Chấp nhận (OK)"
                else:
                    # Mức 3: > y (Lỗi to, giảm phụ thuộc vào conf)
                    if mean_conf >= conf_large:
                        is_defect_ng = True
                        reason = f"Area({int(area_pixels)}) > y({y_limit}) & Conf({mean_conf*100:.1f}%) >= conf_large({conf_large*100:.1f}%) -> NG"
                    else:
                        is_defect_ng = False
                        reason = f"Area({int(area_pixels)}) > y({y_limit}) & Conf({mean_conf*100:.1f}%) < conf_large({conf_large*100:.1f}%) -> Chấp nhận (OK)"

                # In log chi tiết để theo dõi chính xác vì sao bị NG hay OK
                print(f"   [{cam_prefix}] [{cls_name}] {reason}")

                # Đổi màu và trạng thái theo kết quả phán định
                if is_defect_ng:
                    ng_count += 1
                    status_tag = "NG"
                    text_color = (0, 0, 255)  # ĐỎ nếu NG
                    draw_color = color        # Màu riêng của class lỗi
                else:
                    status_tag = "OK"
                    text_color = (0, 255, 0)  # XANH LÁ nếu chấp nhận được
                    draw_color = (0, 255, 0)  # Viền XANH LÁ nếu bỏ qua lỗi

                # 1. Vẽ viền ngoài contour: NG viền màu lỗi, OK viền xanh lá
                cv2.drawContours(display_img, [cnt], -1, draw_color, thickness=2 if is_defect_ng else 1)

                # 3. Vẽ nhãn text: Tên lỗi + Diện tích + Conf + [OK]/[NG] rõ ràng
                x, y, w, h = cv2.boundingRect(cnt)
                label_text = f"{cls_name}: {int(area_pixels)}px-{mean_conf*100:.1f}% [{status_tag}]"
                cv2.putText(
                    display_img,
                    label_text,
                    (max(5, x - 100), max(28, y - 8)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.1,
                    text_color,
                    2,
                    cv2.LINE_AA
                )

        # Trạng thái tổng quát của ảnh
        if ng_count > 0:
            is_ok = False
            msg = f"{cam_prefix}_NG ({ng_count})"
            cv2.putText(display_img, f"STATUS: NG ({ng_count})", (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3, cv2.LINE_AA)
        else:
            is_ok = True
            msg = f"{cam_prefix}_OK"
            cv2.putText(display_img, "STATUS: OK", (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3, cv2.LINE_AA)

        return is_ok, msg, display_img

    def run_ai_1(self, image):
        if self.model1 is None:
            return True, "AI1_SKIP", image
        # Truyền bộ quy luật self.rules_ai1 vào
        return self._infer_and_draw(
            self.model1, 
            image, 
            self.class_names_ai1, 
            rules=self.rules_ai1, 
            cam_prefix="AI1"
        )

    def run_ai_2(self, image):
        time.sleep(0.03)
        return True, "AI2_OK", image

    def run_ai_3(self, image):
        if self.model3 is None:
            return True, "AI3_SKIP", image
        # Truyền bộ quy luật self.rules_ai3 vào
        return self._infer_and_draw(
            self.model3, 
            image, 
            self.class_names_ai3, 
            rules=self.rules_ai3, 
            cam_prefix="AI3"
        )


    def load_rules_from_file(self, config_path):
        """Đọc file rules_config.json khi khởi động AI Engine"""
        if not os.path.exists(config_path) or os.path.getsize(config_path) == 0:
            print(f"[AI Engine] Không tìm thấy file {config_path} hoặc file rỗng. Sử dụng rules mặc định.")
            return

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if "ai1" in data:
                for cls_id_str, vals in data["ai1"].items():
                    cls_id = int(cls_id_str)
                    if cls_id in self.rules_ai1:
                        self.rules_ai1[cls_id].update(vals)

            if "ai3" in data:
                for cls_id_str, vals in data["ai3"].items():
                    cls_id = int(cls_id_str)
                    if cls_id in self.rules_ai3:
                        self.rules_ai3[cls_id].update(vals)

            print(f"[AI Engine] ✅ Đã nạp rules từ file: {config_path}")
            print(f"   -> AI1 rules: {self.rules_ai1}")
            print(f"   -> AI3 rules: {self.rules_ai3}")
        except Exception as e:
            print(f"[AI Engine] Lỗi khi nạp file cấu hình: {e}")

    def update_rules_from_dict(self, data: dict):
        """Cập nhật trực tiếp dictionary rules trên RAM khi nhận gói tin từ Queue"""
        try:
            if "ai1" in data:
                for cls_id_str, vals in data["ai1"].items():
                    cls_id = int(cls_id_str)
                    if cls_id in self.rules_ai1:
                        self.rules_ai1[cls_id].update(vals)

            if "ai3" in data:
                for cls_id_str, vals in data["ai3"].items():
                    cls_id = int(cls_id_str)
                    if cls_id in self.rules_ai3:
                        self.rules_ai3[cls_id].update(vals)

            print("[AI Engine] ✅ Đã cập nhật rules mới từ IPC Queue thành công!")
            print(f"   -> AI1 rules RAM: {self.rules_ai1}")
            print(f"   -> AI3 rules RAM: {self.rules_ai3}")
        except Exception as e:
            print(f"[AI Engine] Lỗi khi update rules từ dict: {e}")