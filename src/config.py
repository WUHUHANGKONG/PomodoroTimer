# src/config.py
import os
import json
import threading


class AppConfig:
    """
    默认配置模板 (静态常量)。
    作为 ConfigManager 的默认值来源。
    """
    TITLE = "极简番茄"
    SIZE_MAIN = "1000x650"
    GLASS_ALPHA = 0.92

    # --- 颜色定义 ---
    COLOR_BG = "#F7F9FC"
    COLOR_SIDEBAR = "#EDF1F5"
    COLOR_CARD_BG = "#FFFFFF"
    COLOR_BORDER = "#E1E5EB"

    COLOR_PRIMARY = "#00B894"
    COLOR_PRIMARY_HOVER = "#55EFC4"

    COLOR_TAG_SELECTED = "#74b9ff"
    COLOR_TAG_HOVER = "#0984e3"

    COLOR_PAUSE = "#fdcb6e"
    COLOR_PAUSE_HOVER = "#ffeaa7"
    COLOR_RED = "#FF7675"
    COLOR_RED_HOVER = "#ff7675"

    COLOR_TEXT_MAIN = "#2d3436"
    COLOR_TEXT_SUB = "#636e72"

    # 兼容别名
    COLOR_GREEN = COLOR_PRIMARY
    COLOR_GREEN_HOVER = COLOR_PRIMARY_HOVER
    COLOR_TEXT_GRAY = COLOR_TEXT_SUB
    COLOR_BG_MINI = "#FFFFFF"
    COLOR_BTN_SELECTED = "#FFFFFF"

    # --- UI 字体与尺寸 ---
    SIDEBAR_TITLE_FONT = ("SF Pro Display", 20, "bold")
    SIDEBAR_BTN_FONT = ("SF Pro Text", 13)
    SIDEBAR_BTN_HEIGHT = 45  # 确保这里是整数

    GREETING_FONT = ("SF Pro Display", 24, "bold")
    DISPLAY_TIME_FONT = ("SF Pro Display", 120)

    PRESET_FONT = ("SF Pro Text", 13)
    PRESET_HEIGHT = 45

    FOCUS_TAGS = ["💻 工作", "📚 学习", "🏃 运动", "📖 阅读", "☕ 摸鱼"]
    TAG_FONT = ("SF Pro Text", 12)
    TAG_HEIGHT = 32

    TASK_FONT = ("SF Pro Text", 14)
    TASK_DONE_COLOR = "#b2bec3"

    BTN_START_FONT = ("SF Pro Display", 16, "bold")
    BTN_START_HEIGHT = 60
    BTN_CORNER_RADIUS = 30

    MINI_SIZE = "260x90"
    MINI_TIME_FONT = ("SF Pro Display", 46)
    MINI_TEXT_FONT = ("SF Pro Text", 12)

    ZEN_MESSAGES = {
        "start": "🍃 调整呼吸，进入状态...",
        "focus": "🌊 保持心流，沉浸当下...",
        "end": "✨ 即将完成，完美收官..."
    }


class ConfigManager:
    """
    配置管理器 (单例模式)。
    支持从 config.json 加载配置，支持运行时修改并保存。
    """
    _instance = None
    _lock = threading.Lock()
    CONFIG_FILE = "config.json"

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._config = {}
            self._load_defaults()
            self.load_from_file()
            self._initialized = True

    def _load_defaults(self):
        """从 AppConfig 加载默认值"""
        for key in dir(AppConfig):
            if key.isupper():  # 只加载大写常量
                self._config[key] = getattr(AppConfig, key)

    def load_from_file(self):
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    self._config.update(user_config)
            except Exception as e:
                print(f"Config load error: {e}")

    def save_to_file(self):
        try:
            # 简单过滤不可序列化对象
            serializable_config = {k: v for k, v in self._config.items()
                                   if isinstance(v, (str, int, float, bool, dict, list))}
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(serializable_config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Config save error: {e}")

    def get(self, key, default=None):
        return self._config.get(key, default)

    def set(self, key, value):
        self._config[key] = value
        self.save_to_file()


# 全局实例
config_manager = ConfigManager()