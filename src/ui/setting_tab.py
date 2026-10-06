# # src/ui/setting_tab.py

# from PySide6.QtWidgets import QWidget

# from UI_g.setting import Ui_Form as SettingUi
# import os
# import json
# from PySide6.QtWidgets import QWidget
# from UI_g.setting import Ui_Form as SettingUi

# CONFIG_FILE = f"data/rules_config.json"

# class SettingTab(QWidget):
#     def __init__(self, ai_engine=None):
#         super().__init__()
#         self.ui = SettingUi()
#         self.ui.setupUi(self)
#         self.ai_engine = ai_engine

#         # Bản đồ ánh xạ: (model_key, class_id, rule_key) -> widget tương ứng trên UI
#         # Hãy kiểm tra và sửa lại đúng objectName bạn đặt trong Qt Designer
#         self.widget_map = {
#             # --- CAMERA 1 (AI 1) ---
#             ("ai1", 1, "x"): self.ui.sp_area_TS1,
#             ("ai1", 1, "y"): self.ui.sp_area_TS2,
#             ("ai1", 1, "conf_mid"): self.ui.sp_conf_TS1,
#             ("ai1", 1, "conf_large"): self.ui.sp_conf_TS2,

#             ("ai1", 2, "x"): self.ui.sp_area_LS1,
#             ("ai1", 2, "y"): self.ui.sp_area_LS2,
#             ("ai1", 2, "conf_mid"): self.ui.sp_conf_LS1,
#             ("ai1", 2, "conf_large"): self.ui.sp_conf_LS2,

#             ("ai1", 3, "x"): self.ui.sp_area_HC1,
#             ("ai1", 3, "y"): self.ui.sp_area_HC2,
#             ("ai1", 3, "conf_mid"): self.ui.sp_conf_HC1,
#             ("ai1", 3, "conf_large"): self.ui.sp_conf_HC2,

#             # --- CAMERA 2 (AI 3) ---
#             ("ai3", 1, "x"): self.ui.sp_area_CD1,
#             ("ai3", 1, "y"): self.ui.sp_area_CD2,
#             ("ai3", 1, "conf_mid"): self.ui.sp_conf_CD1,
#             ("ai3", 1, "conf_large"): self.ui.sp_conf_CD2,

#             ("ai3", 2, "x"): self.ui.sp_area_OV1,
#             ("ai3", 2, "y"): self.ui.sp_area_OV2,
#             ("ai3", 2, "conf_mid"): self.ui.sp_conf_OV1,
#             ("ai3", 2, "conf_large"): self.ui.sp_conf_OV2,

#             ("ai3", 3, "x"): self.ui.sp_area_C1,
#             ("ai3", 3, "y"): self.ui.sp_area_C2,
#             ("ai3", 3, "conf_mid"): self.ui.sp_conf_C1,
#             ("ai3", 3, "conf_large"): self.ui.sp_conf_C2,
#         }

#         # 1. Nạp cấu hình lên UI
#         self.load_settings()

#         # 2. Kết nối sự kiện mất focus (editingFinished) để tự động lưu
#         for widget in self.widget_map.values():
#             widget.editingFinished.connect(self.save_settings)

#     def load_settings(self):
#         """Đọc file JSON, đưa số liệu lên SpinBox và cập nhật sang AI Engine"""
#         rules_data = {}
#         if os.path.exists(CONFIG_FILE):
#             try:
#                 with open(CONFIG_FILE, "r", encoding="utf-8") as f:
#                     rules_data = json.load(f)
#             except Exception as e:
#                 print(f"[SettingTab] Lỗi đọc file config: {e}")

#         # Block signals tạm thời để tránh kích hoạt save_settings khi đang load
#         for (model_key, class_id, rule_key), widget in self.widget_map.items():
#             widget.blockSignals(True)
#             # Lấy giá trị từ file, nếu chưa có thì lấy giá trị mặc định từ AI Engine
#             val = None
#             if model_key in rules_data and str(class_id) in rules_data[model_key]:
#                 val = rules_data[model_key][str(class_id)].get(rule_key)

#             if val is None and self.ai_engine is not None:
#                 engine_rules = self.ai_engine.rules_ai1 if model_key == "ai1" else self.ai_engine.rules_ai3
#                 val = engine_rules.get(class_id, {}).get(rule_key, 0)

#             if val is not None:
#                 widget.setValue(val)
#             widget.blockSignals(False)

#         # Cập nhật cấu hình sang AI Engine
#         self._sync_to_ai_engine()

#     def save_settings(self):
#         """Hàm được gọi khi người dùng gõ xong và click chuột ra ngoài (mất focus)"""
#         config_to_save = {"ai1": {}, "ai3": {}}

#         for (model_key, class_id, rule_key), widget in self.widget_map.items():
#             cls_str = str(class_id)
#             if cls_str not in config_to_save[model_key]:
#                 config_to_save[model_key][cls_str] = {}

#             val = widget.value()
#             if isinstance(val, float):
#                 val = round(val, 2)
#             config_to_save[model_key][cls_str][rule_key] = val

#         try:
#             with open(CONFIG_FILE, "w", encoding="utf-8") as f:
#                 json.dump(config_to_save, f, indent=4, ensure_ascii=False)
#             print("[SettingTab] Đã tự động lưu cấu hình mới vào rules_config.json")
#         except Exception as e:
#             print(f"[SettingTab] Lỗi ghi file config: {e}")

#         # Đồng bộ giá trị mới ngay lập tức cho AI Engine đang chạy
#         self._sync_to_ai_engine()

#     def _sync_to_ai_engine(self):
#         """Cập nhật trực tiếp dictionary rules_ai1 và rules_ai3 trong AIInferenceEngine"""
#         if self.ai_engine is None:
#             return

#         for (model_key, class_id, rule_key), widget in self.widget_map.items():
#             target_rules = self.ai_engine.rules_ai1 if model_key == "ai1" else self.ai_engine.rules_ai3
#             if class_id not in target_rules:
#                 target_rules[class_id] = {}
#             target_rules[class_id][rule_key] = widget.value()














# src/ui/setting_tab.py
import os
import json
from pathlib import Path
from PySide6.QtWidgets import QWidget
from UI_g.setting import Ui_Form as SettingUi

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_FILE = str(PROJECT_ROOT / "data" / "rules_config.json")

class SettingTab(QWidget):
    def __init__(self, rule_queue=None):
        super().__init__()
        self.ui = SettingUi()
        self.ui.setupUi(self)
        self.rule_queue = rule_queue  # Lưu reference tới Queue

        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)

        self.widget_map = {
            # --- CAMERA 1 (AI 1) ---
            ("ai1", 1, "x"): self.ui.sp_area_TS1,
            ("ai1", 1, "y"): self.ui.sp_area_TS2,
            ("ai1", 1, "conf_mid"): self.ui.sp_conf_TS1,
            ("ai1", 1, "conf_large"): self.ui.sp_conf_TS2,

            ("ai1", 2, "x"): self.ui.sp_area_LS1,
            ("ai1", 2, "y"): self.ui.sp_area_LS2,
            ("ai1", 2, "conf_mid"): self.ui.sp_conf_LS1,
            ("ai1", 2, "conf_large"): self.ui.sp_conf_LS2,

            ("ai1", 3, "x"): self.ui.sp_area_HC1,
            ("ai1", 3, "y"): self.ui.sp_area_HC2,
            ("ai1", 3, "conf_mid"): self.ui.sp_conf_HC1,
            ("ai1", 3, "conf_large"): self.ui.sp_conf_HC2,

            # --- CAMERA 2 (AI 3) ---
            ("ai3", 1, "x"): self.ui.sp_area_CD1,
            ("ai3", 1, "y"): self.ui.sp_area_CD2,
            ("ai3", 1, "conf_mid"): self.ui.sp_conf_CD1,
            ("ai3", 1, "conf_large"): self.ui.sp_conf_CD2,

            ("ai3", 2, "x"): self.ui.sp_area_OV1,
            ("ai3", 2, "y"): self.ui.sp_area_OV2,
            ("ai3", 2, "conf_mid"): self.ui.sp_conf_OV1,
            ("ai3", 2, "conf_large"): self.ui.sp_conf_OV2,

            ("ai3", 3, "x"): self.ui.sp_area_C1,
            ("ai3", 3, "y"): self.ui.sp_area_C2,
            ("ai3", 3, "conf_mid"): self.ui.sp_conf_C1,
            ("ai3", 3, "conf_large"): self.ui.sp_conf_C2,
        }

        self.load_settings()

        for widget in self.widget_map.values():
            widget.editingFinished.connect(self.save_settings)

    def load_settings(self):
        if not os.path.exists(CONFIG_FILE) or os.path.getsize(CONFIG_FILE) == 0:
            return

        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                rules_data = json.load(f)

            for (model_key, class_id, rule_key), widget in self.widget_map.items():
                widget.blockSignals(True)
                if model_key in rules_data and str(class_id) in rules_data[model_key]:
                    val = rules_data[model_key][str(class_id)].get(rule_key)
                    if val is not None:
                        widget.setValue(val)
                widget.blockSignals(False)

            print(f"[SettingTab] Đã nạp cấu hình từ: {CONFIG_FILE}")
        except Exception as e:
            print(f"[SettingTab] Lỗi khi nạp file config: {e}")

    def save_settings(self):
        config_to_save = {"ai1": {}, "ai3": {}}

        for (model_key, class_id, rule_key), widget in self.widget_map.items():
            cls_str = str(class_id)
            if cls_str not in config_to_save[model_key]:
                config_to_save[model_key][cls_str] = {}

            val = widget.value()
            if isinstance(val, float):
                val = round(val, 2)
            config_to_save[model_key][cls_str][rule_key] = val

        # 1. Lưu xuống đĩa để duy trì khi tắt app
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config_to_save, f, indent=4, ensure_ascii=False)
            print("[SettingTab] Đã lưu cấu hình mới vào JSON!")
        except Exception as e:
            print(f"[SettingTab] Lỗi khi ghi file config: {e}")

        # 2. Đẩy vào Queue: Xả hết gói cũ, chỉ giữ lại duy nhất bản tin mới nhất
        if self.rule_queue is not None:
            try:
                # Rút sạch các bản tin chỉnh dở trước đó
                while not self.rule_queue.empty():
                    try:
                        self.rule_queue.get_nowait()
                    except Exception:
                        break
                
                # Đẩy bản tin mới nhất vào (luôn đảm bảo queue chỉ có 1 phần tử)
                self.rule_queue.put_nowait(config_to_save)
                print("[SettingTab] 📡 Đã gửi bản tin thông số mới nhất vào Queue!")
            except Exception as e:
                print(f"[SettingTab] Lỗi đẩy Queue: {e}")