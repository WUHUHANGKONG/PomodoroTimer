# src/core.py
import os
import sys
import json
import uuid
import platform
import threading
from datetime import datetime, timedelta
from abc import ABC, abstractmethod


# ===================================================
# 核心计时引擎 (TimerEngine - SRP)
# ===================================================
class TimerEngine:
    def __init__(self, duration_minutes):
        self.total_seconds = int(duration_minutes * 60)
        self.time_left = self.total_seconds
        self.is_running = False
        self.is_paused = False

    def start(self):
        self.is_running = True; self.is_paused = False

    def stop(self):
        self.is_running = False; self.is_paused = False

    def pause_toggle(self):
        if self.is_running: self.is_paused = not self.is_paused

    def reset(self):
        self.time_left = self.total_seconds;
        self.is_paused = True;
        self.is_running = True

    def tick(self):
        """返回 (是否完成, 进度0-1)"""
        if not self.is_running: return False, 0.0
        if self.is_paused: return False, self._get_progress()

        if self.time_left > 0:
            self.time_left -= 1
            return False, self._get_progress()
        else:
            self.is_running = False
            return True, 1.0

    def _get_progress(self):
        if self.total_seconds == 0: return 1.0
        return 1 - (self.time_left / self.total_seconds)

    def get_time_str(self):
        m, s = divmod(self.time_left, 60)
        return f"{m:02d}:{s:02d}"


# ===================================================
# Infrastructure / Utils
# ===================================================
class ResourceManager:
    @staticmethod
    def get_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


class SoundManager:
    @staticmethod
    def play_finish():
        def _play():
            try:
                system = platform.system()
                if system == "Windows":
                    import winsound; winsound.Beep(1000, 500)
                elif system == "Darwin":
                    os.system("afplay /System/Library/Sounds/Glass.aiff")
            except:
                pass

        threading.Thread(target=_play, daemon=True).start()


# ===================================================
# Repository Pattern
# ===================================================
class IRepository(ABC):
    @abstractmethod
    def load_all(self): pass

    @abstractmethod
    def save_all(self, data): pass


class JsonRepository(IRepository):
    def __init__(self, filename):
        self.file_path = os.path.join(os.getcwd(), filename)

    def load_all(self):
        if not os.path.exists(self.file_path): return []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []

    def save_all(self, data):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Save error: {e}")


# ===================================================
# Service Layer
# ===================================================
class TaskService:
    def __init__(self, repository: IRepository):
        self.repo = repository

    def get_tasks(self):
        tasks = self.repo.load_all()

        def sort_key(x):
            return (1 if x.get('completed') else 0, 0 if x.get('due_date') else 1, x.get('due_date', ""),
                    -x.get('created_at', 0))

        return sorted(tasks, key=sort_key)

    def add_task(self, title, due_date=""):
        tasks = self.repo.load_all()
        new_task = {
            "id": str(uuid.uuid4()), "title": title, "due_date": due_date, "completed": False,
            "created_at": datetime.now().timestamp(), "updated_at": datetime.now().timestamp()
        }
        tasks.append(new_task)
        self.repo.save_all(tasks)

    def toggle_task(self, task_id):
        tasks = self.repo.load_all()
        for t in tasks:
            if t["id"] == task_id:
                t["completed"] = not t["completed"]
                t["updated_at"] = datetime.now().timestamp()
                break
        self.repo.save_all(tasks)

    def delete_task(self, task_id):
        tasks = self.repo.load_all()
        tasks = [t for t in tasks if t["id"] != task_id]
        self.repo.save_all(tasks)


# [请修改 src/core.py 中的 HistoryService 类]

class HistoryService:
    def __init__(self, repository: IRepository):
        self.repo = repository

    def record_focus(self, minutes, tag):
        record = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "timestamp": datetime.now().timestamp(),
            "duration": minutes,
            "tag": tag
        }
        data = self.repo.load_all()
        data.append(record)
        self.repo.save_all(data)

    def get_stats(self):
        """获取基础 KPI 数据"""
        data = self.repo.load_all()
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        start_week = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        start_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        stats = {"day": 0, "week": 0, "month": 0, "tag_dist": {}}
        for rec in data:
            try:
                rec_time = datetime.fromtimestamp(rec["timestamp"])
                dur = rec["duration"]
                tag = rec.get("tag", "未分类")

                if rec["date"] == today: stats["day"] += dur
                if rec_time >= start_week:
                    stats["week"] += dur
                    stats["tag_dist"][tag] = stats["tag_dist"].get(tag, 0) + dur
                if rec_time >= start_month: stats["month"] += dur
            except:
                continue
        return stats

    def get_chart_data(self):
        """
        ✨ 新增：获取图表分析数据
        返回:
        - trend: 近7天每天的专注时长及百分比
        - recent: 最近 10 条详细记录
        """
        data = self.repo.load_all()

        # 1. 准备近7天的日期骨架
        dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
        trend_map = {d: 0 for d in dates}

        # 2. 聚合数据 & 提取最近记录
        # 按时间戳倒序排列
        sorted_data = sorted(data, key=lambda x: x.get("timestamp", 0), reverse=True)
        recent_records = sorted_data[:10]

        for rec in data:
            d = rec.get("date")
            if d in trend_map:
                trend_map[d] += rec.get("duration", 0)

        # 3. 格式化为 UI 易用的结构
        trend_list = []
        max_val = max(trend_map.values()) if trend_map.values() and max(trend_map.values()) > 0 else 1

        for d in dates:
            val = trend_map[d]
            trend_list.append({
                "date_label": d[5:],  # 只显示 MM-DD
                "full_date": d,
                "minutes": val,
                "percent": val / max_val  # 用于进度条长度
            })

        return {
            "trend": trend_list,
            "recent": recent_records
        }


# 依赖注入
task_service = TaskService(JsonRepository("tasks.json"))
history_service = HistoryService(JsonRepository("focus_history.json"))