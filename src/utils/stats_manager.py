import json
import os
from datetime import datetime

class StatsManager:
    def __init__(self, json_path="data/stats.json"):
        self.json_path = json_path
        os.makedirs(os.path.dirname(self.json_path), exist_ok=True)
        if not os.path.exists(self.json_path):
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)

    def _load_all(self):
        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _save_all(self, data):
        try:
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Lỗi ghi file stats.json: {e}")

    def get_stats_for_recipe(self, recipe_name: str, target_date: str = None):
        """Lấy thông số đếm cho mã hàng trong ngày (mặc định là hôm nay)"""
        if target_date is None:
            target_date = datetime.now().strftime("%Y-%m-%d")

        data = self._load_all()
        for item in data:
            if item.get("date") == target_date and str(item.get("recipe")) == str(recipe_name):
                return item

        # Trả về mặc định nếu ngày hôm nay mã này chưa chạy
        return {
            "date": target_date,
            "recipe": str(recipe_name),
            "start_time": datetime.now().strftime("%H:%M:%S"),
            "end_time": datetime.now().strftime("%H:%M:%S"),
            "total_count": 0,
            "ok_count": 0,
            "ng_count": 0
        }

    def update_record(self, recipe_name: str, is_ok: bool):
        """Cộng dồn số lượng và cập nhật thời gian vào file JSON"""
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")

        data = self._load_all()
        target_item = None

        for item in data:
            if item.get("date") == current_date and str(item.get("recipe")) == str(recipe_name):
                target_item = item
                break

        if target_item is None:
            # Tạo mới bản ghi cho mã hàng trong ngày
            target_item = {
                "date": current_date,
                "recipe": str(recipe_name),
                "start_time": current_time,
                "end_time": current_time,
                "total_count": 1,
                "ok_count": 1 if is_ok else 0,
                "ng_count": 0 if is_ok else 1
            }
            data.append(target_item)
        else:
            # Cập nhật bản ghi có sẵn
            target_item["total_count"] += 1
            if is_ok:
                target_item["ok_count"] += 1
            else:
                target_item["ng_count"] += 1
            target_item["end_time"] = current_time

        self._save_all(data)
        return target_item