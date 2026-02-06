# src/config.py

class AppConfig:
    # ... (保留头部所有配置) ...
    TITLE = "番茄钟"
    SIZE_MAIN = "1000x650"

    # --- 颜色定义 ---
    COLOR_BG = "#FFFFFF"
    COLOR_SIDEBAR = "#FAFAFA"
    COLOR_SECONDARY_BG = "#F0F0F0"

    # 主色调 (绿色 - 用于时间)
    COLOR_PRIMARY = "#00B894"
    COLOR_PRIMARY_HOVER = "#00A383"

    # ✨ 新增：标签专用色 (静谧蓝 - 用于任务类型)
    COLOR_TAG_SELECTED = "#74b9ff"  # 选中时的清爽蓝
    COLOR_TAG_HOVER = "#0984e3"  # 悬停时的深蓝

    # 警告色
    COLOR_RED = "#FF7675"
    COLOR_RED_HOVER = "#D63031"

    # 文字颜色
    COLOR_TEXT_MAIN = "#2D3436"
    COLOR_TEXT_SUB = "#636E72"

    # 兼容别名 (保持不变)
    COLOR_GREEN = COLOR_PRIMARY
    COLOR_GREEN_HOVER = COLOR_PRIMARY_HOVER
    COLOR_TEXT_GRAY = COLOR_TEXT_SUB
    COLOR_BG_MINI = "#FFFFFF"
    COLOR_BTN_SELECTED = "#E8F8F5"

    # --- UI 字体与尺寸 ---
    SIDEBAR_TITLE_FONT = ("微软雅黑", 18, "bold")
    SIDEBAR_BTN_FONT = ("微软雅黑", 13)
    SIDEBAR_BTN_HEIGHT = 45

    GREETING_FONT = ("微软雅黑", 22, "bold")
    DISPLAY_TIME_FONT = ("Roboto Medium", 160)

    # 时间预设 (保持不变)
    PRESET_FONT = ("微软雅黑", 14)
    PRESET_HEIGHT = 50

    # ✨ 优化：标签配置
    FOCUS_TAGS = ["💻 工作", "📚 学习", "🏃 运动", "📖 阅读", "☕ 摸鱼"]
    TAG_FONT = ("微软雅黑", 13)
    TAG_HEIGHT = 36  # 稍微改矮一点，显得更精致

    # 开始按钮
    BTN_START_FONT = ("微软雅黑", 18, "bold")
    BTN_START_HEIGHT = 70
    BTN_CORNER_RADIUS = 35

    # 悬浮窗
    MINI_SIZE = "220x70"
    MINI_TIME_FONT = ("Roboto Medium", 40)
    MINI_TEXT_FONT = ("微软雅黑", 12)