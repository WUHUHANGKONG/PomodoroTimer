############################################################
# 📘 文件说明：
# 本文件实现的功能：核心业务逻辑处理，包括数据计算、状态管理及资源调度。
#
# 📋 程序整体伪代码（中文）：
# 1. 接收 UI 或外部指令
# 2. 执行复杂业务算法（如计时、计算）
# 3. 操作数据持久化层
# 4. 返回执行结果或触发信号
#
# 🔄 程序流程图（逻辑流）：
# ┌──────────┐
# │  输入数据 │
# └─────┬────┘
#       ↓
# ┌────────────┐
# │  核心处理逻辑 │
# └─────┬──────┘
#       ↓
# ┌──────────┐
# │  输出结果 │
# └──────────┘
#
# 📊 数据管道说明：
# 数据流向：UI 指令 → 业务逻辑层 → 数据处理/文件读写 → 状态反馈
#
# 🧩 文件结构：
# - 依赖库：platform, threading, sys, os, datetime...
# - 类 (Class)：ResourceManager - (封装核心对象)
#   └─ 核心方法：get_path
# - 类 (Class)：SoundManager - (封装核心对象)
#   └─ 核心方法：play_finish
# - 类 (Class)：DataManager - (封装核心对象)
#   └─ 核心方法：save_record, get_stats
#
# 🕒 创建时间：2026-02-06
############################################################

# src/core.py
import os
import sys
import json
import platform
import threading
from datetime import datetime, timedelta


class ResourceManager:
    @staticmethod
    def get_path(relative_path):
        """获取资源绝对路径"""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


class SoundManager:
    @staticmethod
    def play_finish():
        """播放结束音效 (跨平台)"""

        def _play():
            system = platform.system()
            if system == "Windows":
                import winsound
                winsound.Beep(1000, 500)
                winsound.Beep(1500, 500)
            elif system == "Darwin":  # macOS
                os.system("afplay /System/Library/Sounds/Glass.aiff")

        threading.Thread(target=_play, daemon=True).start()


class DataManager:
    FILE_PATH = os.path.join(os.getcwd(), "focus_history.json")

    @classmethod
    def save_record(cls, minutes):
        """保存记录"""
        record = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "timestamp": datetime.now().timestamp(),
            "duration": minutes
        }
        data = cls._load_data()
        data.append(record)
        cls._write_data(data)

    @classmethod
    def get_stats(cls):
        """获取 日/周/月 统计数据"""
        data = cls._load_data()
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")

        # 时间界限
        start_week = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        start_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        stats = {"day": 0, "week": 0, "month": 0}

        for rec in data:
            rec_time = datetime.fromtimestamp(rec["timestamp"])
            dur = rec["duration"]

            if rec["date"] == today:
                stats["day"] += dur
            if rec_time >= start_week:
                stats["week"] += dur
            if rec_time >= start_month:
                stats["month"] += dur

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

    @classmethod
    def _write_data(cls, data):
        with open(cls.FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)