############################################################
# 📘 文件说明：
# 本文件实现的功能：全局配置管理，定义应用程序的常量、参数及样式标准。
#
# 📋 程序整体伪代码（中文）：
# 1. 定义配置类或字典
# 2. 设置颜色、字体、路径等静态常量
# 3. 提供配置获取接口
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
# 数据流向：硬编码常量 → 应用程序读取 → 全局样式/行为控制
#
# 🧩 文件结构：
# - 类 (Class)：AppConfig - (封装核心对象)
#
# 🕒 创建时间：2026-02-06
############################################################

# src/config.py

class AppConfig:
    # --- 窗口基础 ---
    TITLE = "番茄钟"
    SIZE_MAIN = "1000x650"

    # --- 核心颜色定义 (人性化配色) ---
    COLOR_BG = "#FFFFFF"  # 背景白
    COLOR_SIDEBAR = "#FAFAFA"  # 侧边栏极浅灰
    COLOR_SECONDARY_BG = "#F0F0F0"  # 次级背景

    # 主色调 (绿色系)
    COLOR_PRIMARY = "#00B894"
    COLOR_PRIMARY_HOVER = "#00A383"

    # 警告/停止色 (红色系)
    COLOR_RED = "#FF7675"
    COLOR_RED_HOVER = "#D63031"

    # 文字颜色
    COLOR_TEXT_MAIN = "#2D3436"  # 深黑
    COLOR_TEXT_SUB = "#636E72"  # 深灰

    # --- 关键修复：兼容旧代码的别名 ---
    # ui.py 中有些地方还在用 COLOR_GREEN，这里做个映射，防止报错
    COLOR_GREEN = COLOR_PRIMARY
    COLOR_GREEN_HOVER = COLOR_PRIMARY_HOVER
    COLOR_TEXT_GRAY = COLOR_TEXT_SUB

    # 悬浮窗背景
    COLOR_BG_MINI = "#FFFFFF"
    # 侧边栏选中颜色
    COLOR_BTN_SELECTED = "#E8F8F5"

    # --- UI 字体与尺寸参数 ---

    # 侧边栏
    SIDEBAR_TITLE_FONT = ("微软雅黑", 18, "bold")
    SIDEBAR_BTN_FONT = ("微软雅黑", 13)
    SIDEBAR_BTN_HEIGHT = 45

    # 顶部问候语
    GREETING_FONT = ("微软雅黑", 22, "bold")

    # 巨大的数字展示
    DISPLAY_TIME_FONT = ("Roboto Medium", 160)

    # 时间预设胶囊
    PRESET_FONT = ("微软雅黑", 14)
    PRESET_HEIGHT = 50

    # 开始按钮
    BTN_START_FONT = ("微软雅黑", 18, "bold")
    BTN_START_HEIGHT = 70
    BTN_CORNER_RADIUS = 35

    # 悬浮窗
    MINI_SIZE = "220x70"
    MINI_TIME_FONT = ("Roboto Medium", 40)
    MINI_TEXT_FONT = ("微软雅黑", 12)