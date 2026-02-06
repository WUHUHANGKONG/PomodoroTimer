# src/core.py
import os
import sys
import json
import platform
import threading
from datetime import datetime, timedelta


# ... (ResourceManager 和 SoundManager 类保持不变) ...
class ResourceManager:
    @staticmethod
    def get_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


class SoundManager:
    @staticmethod
    def play_finish():
        def _play():
            try:
                system = platform.system()
                if system == "Windows":
                    import winsound
                    winsound.Beep(1000, 500)
                    winsound.Beep(1500, 500)
                elif system == "Darwin":  # macOS
                    os.system("afplay /System/Library/Sounds/Glass.aiff")
            except:
                pass

        threading.Thread(target=_play, daemon=True).start()


class DataManager:
    FILE_PATH = os.path.join(os.getcwd(), "focus_history.json")

    @classmethod
    def save_record(cls, minutes, tag="默认"):  # ✨ 修改：增加 tag 参数
        """保存专注记录"""
        try:
            record = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "timestamp": datetime.now().timestamp(),
                "duration": minutes,
                "tag": tag  # ✨ 保存标签
            }
            data = cls._load_data()
            data.append(record)
            with open(cls.FILE_PATH, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)  # ✨ 允许保存中文
        except Exception as e:
            print(f"Save error: {e}")

    @classmethod
    def get_stats(cls):
        """读取统计数据"""
        data = cls._load_data()
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")

        start_week = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        start_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        stats = {"day": 0, "week": 0, "month": 0}

        for rec in data:
            try:
                rec_time = datetime.fromtimestamp(rec["timestamp"])
                dur = rec["duration"]

                if rec["date"] == today:
                    stats["day"] += dur
                if rec_time >= start_week:
                    stats["week"] += dur
                if rec_time >= start_month:
                    stats["month"] += dur
            except:
                continue

        return stats

    @classmethod
    def _load_data(cls):
        if not os.path.exists(cls.FILE_PATH):
            return []
        try:
            with open(cls.FILE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []