import os
import sys
import platform
import datetime
from datetime import datetime as dt

# ================= 配置区域 =================
PROJECT_NAME = "PomodoroTimer"
OUTPUT_FILENAME = f"代码使用全景图_按时间轴_{dt.now().strftime('%Y%m%d')}.md"


# ================= 核心逻辑 =================

def get_python_version():
    return sys.version.split()[0]


def get_os_info():
    return f"{platform.system()} {platform.release()}"


def scan_core_files(root_dir):
    """扫描 src 目录下的核心文件"""
    core_files = []
    src_path = os.path.join(root_dir, 'src')
    if os.path.exists(src_path):
        for f in os.listdir(src_path):
            if f.endswith('.py') and f != '__init__.py':
                core_files.append(f)
    return core_files


def generate_markdown_content(root_dir):
    date_str = dt.now().strftime('%Y-%m-%d')
    py_ver = get_python_version()

    # 动态获取文件列表
    core_files = scan_core_files(root_dir)
    file_list_str = "\n".join([f"- `src/{f}`" for f in core_files])

    # 使用列表构建内容，避免 f-string 大括号冲突
    lines = []

    # --- 头部信息 ---
    lines.append(f"# 📘 代码使用全景图文档")
    lines.append(f"")
    lines.append(f"> **项目名称**：{PROJECT_NAME}")
    lines.append(f"> **生成日期**：{date_str}")
    lines.append(f"> **文档说明**：本文档展示了系统的完整技术栈、运行流程及数据流转全景。")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")

    # --- 第一部分 ---
    lines.append(f"## 第一部分：项目环境与技术栈")
    lines.append(f"")
    lines.append(f"### 📦 项目依赖环境")
    lines.append(f"- **Python版本要求**：Python 3.9+ (当前检测: {py_ver})")
    lines.append(f"- **操作系统支持**：Windows / macOS / Linux (跨平台)")
    lines.append(f"- **核心依赖库列表**：")
    lines.append(f"")
    lines.append(f"| 分类 | 库名称 | 说明 |")
    lines.append(f"| :--- | :--- | :--- |")
    lines.append(f"| **GUI 核心框架** | `customtkinter` | 现代化 UI 组件库，提供圆角与深色模式支持 |")
    lines.append(f"| **标准库** | `tkinter` | Python 内置 GUI 基础库 |")
    lines.append(f"| **并发处理** | `threading` | 用于倒计时后台线程，防止界面卡顿 |")
    lines.append(f"| **数据存储** | `json` | 专注记录的轻量级持久化存储 |")
    lines.append(f"| **系统交互** | `os`, `sys`, `platform` | 路径处理与跨平台音频播放策略 |")
    lines.append(f"| **多媒体** | `winsound` (Win) / `os.system` (Mac) | 结束提示音播放 |")
    lines.append(f"")

    lines.append(f"### 🔧 技术栈与核心库详解")
    lines.append(f"#### 1. CustomTkinter (UI 层)")
    lines.append(f"- **版本要求**: 5.0+")
    lines.append(f"- **用途**: 构建主窗口、悬浮窗、按钮及进度条。")
    lines.append(f"- **核心组件**: `CTk`, `CTkToplevel`, `CTkButton`, `CTkLabel`。")
    lines.append(f"- **关键场景**: 用户设置时间、显示倒计时、切换统计面板。")
    lines.append(f"")

    lines.append(f"#### 2. Threading (并发层)")
    lines.append(f"- **版本要求**: 内置")
    lines.append(f"- **用途**: 分离 UI 渲染与计时逻辑。")
    lines.append(f"- **核心组件**: `Thread(daemon=True)`。")
    lines.append(f"- **关键场景**: 点击“开始专注”后，启动后台线程执行 `while` 循环倒计时。")
    lines.append(f"")

    lines.append(f"### 🚀 环境安装指南")
    lines.append(f"#### 快速安装命令")
    lines.append(f"```bash")
    lines.append(f"# 1. 创建虚拟环境 (推荐)")
    lines.append(f"python -m venv venv")
    lines.append(f"# Windows 激活")
    lines.append(f"venv\\Scripts\\activate")
    lines.append(f"# macOS/Linux 激活")
    lines.append(f"source venv/bin/activate")
    lines.append(f"")
    lines.append(f"# 2. 安装核心依赖")
    lines.append(f"pip install customtkinter")
    lines.append(f"```")
    lines.append(f"")
    lines.append(f"#### 验证安装")
    lines.append(f"运行以下命令，若弹出窗口且无报错即为成功：")
    lines.append(f"```bash")
    lines.append(f"python main.py")
    lines.append(f"```")
    lines.append(f"")
    lines.append(f"### 💻 系统要求")
    lines.append(f"- **硬件**: 任意支持 Python 的 PC/Mac。")
    lines.append(f"- **显示**: 支持 1000x650 分辨率及以上。")
    lines.append(f"- **音频**: 需配备扬声器以播放结束提示音。")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")

    # --- 第二部分 ---
    lines.append(f"## 第二部分：代码使用全景图")
    lines.append(f"")
    lines.append(f"### 1. ⚡ 极简版总览（完整流程）")
    lines.append(f"```mermaid")
    lines.append(f"graph LR")
    lines.append(f"    A[启动程序] --> B[UI初始化]")
    lines.append(f"    B --> C{{用户操作}}")
    lines.append(f"    C -- 设置时间 --> D[开始专注]")
    lines.append(f"    D --> E[后台倒计时]")
    lines.append(f"    E -- 时间归零 --> F[播放提示音]")
    lines.append(f"    F --> G[写入历史数据]")
    lines.append(f"    G --> B")
    lines.append(f"    C -- 查看统计 --> H[读取JSON数据]")
    lines.append(f"    H --> I[渲染图表]")
    lines.append(f"```")
    lines.append(f"")

    lines.append(f"### 2. 按时间轴展开详细流程")
    lines.append(f"")
    lines.append(f"#### 🕒 阶段一：系统启动与初始化")
    lines.append(f"- **📊 数据管道流程图**：")
    lines.append(f"```text")
    lines.append(f"┌──────────────┐       ┌──────────────┐       ┌──────────────┐")
    lines.append(f"│   main.py    │ ───→  │  src/ui.py   │ ───→  │ src/config.py│")
    lines.append(f"└──────┬───────┘       └──────┬───────┘       └──────┬───────┘")
    lines.append(f"       │                      │                      │")
    lines.append(f"       ↓                      ↓                      ↓")
    lines.append(f" [程序入口实例化]      [加载窗口与组件]       [读取全局配色/字体]")
    lines.append(f"```")
    lines.append(f"- **📂 核心脚本**：`main.py`, `src/ui.py`, `src/config.py`")
    lines.append(f"- **⏱️ 预估耗时**：< 1秒")
    lines.append(f"- **🎯 功能说明**：初始化 `PomodoroApp` 类，设置窗口居中、置顶策略及主题颜色。")
    lines.append(f"- **⚠️ 重要提醒**：若缺少 `assets/icon.ico`，图标加载通过 try-except 自动忽略。")
    lines.append(f"")

    lines.append(f"#### 🕒 阶段二：专注任务执行 (核心循环)")
    lines.append(f"- **📊 数据管道流程图**：")
    lines.append(f"```text")
    lines.append(f"┌──────────────┐       ┌──────────────┐       ┌──────────────┐")
    lines.append(f"│ 用户点击开始  │ ───→  │ src/core.py  │ ───→  │  GUI 更新    │")
    lines.append(f"└──────┬───────┘       └──────┬───────┘       └──────┬───────┘")
    lines.append(f"       │                  (线程启动)                 │")
    lines.append(f"       ↓                      ↓                      ↓")
    lines.append(f" [获取输入时间]        [While循环倒计时]       [实时刷新 00:00]")
    lines.append(f"```")
    lines.append(f"- **📂 核心脚本**：`src/ui.py` (事件绑定), `src/core.py` (无直接逻辑，逻辑在UI类中)")
    lines.append(f"- **🎯 功能说明**：")
    lines.append(f"    1. UI 线程挂起，开启悬浮窗。")
    lines.append(f"    2. 子线程每秒 `sleep(1)` 并递减 `time_left`。")
    lines.append(f"    3. 实时更新 `StringVar` 变量以刷新界面。")
    lines.append(f"- **📥 输入数据**：用户在 GUI 选择的分钟数 (int)。")
    lines.append(f"- **📤 输出状态**：界面倒计时数字变化。")
    lines.append(f"")

    lines.append(f"#### 🕒 阶段三：任务结束与数据归档")
    lines.append(f"- **📊 数据管道流程图**：")
    lines.append(f"```text")
    lines.append(f"┌──────────────┐       ┌──────────────┐       ┌──────────────┐")
    lines.append(f"│  倒计时结束   │ ───→  │  播放音效     │ ───→  │ 数据持久化    │")
    lines.append(f"└──────┬───────┘       └──────┬───────┘       └──────┬───────┘")
    lines.append(f"       │                      │                      │")
    lines.append(f"       ↓                      ↓                      ↓")
    lines.append(f" [触发完成事件]        [SoundManager]        [focus_history.json]")
    lines.append(f"```")
    lines.append(f"- **📂 核心脚本**：`src/ui.py` -> `src/core.py` (DataManager)")
    lines.append(f"- **🎯 功能说明**：")
    lines.append(f"    1. 播放跨平台提示音 (Windows Beep / Mac afplay)。")
    lines.append(f"    2. 生成当前时间戳记录。")
    lines.append(f"    3. 将 `{{date, timestamp, duration}}` 追加到 JSON 文件。")
    lines.append(f"- **📥 输入数据**：本次专注时长 (minutes)。")
    lines.append(f"- **📤 输出数据**：`focus_history.json` (追加写入)。")
    lines.append(f"- **⚠️ 重要提醒**：文件读写采用 `r+` 模式，确保并发安全。")
    lines.append(f"")

    # --- 核心清单 ---
    lines.append(f"### 3. 📁 核心文件清单")
    lines.append(f"")
    lines.append(f"| 功能模块 | 文件路径 | 核心类/函数 | 作用描述 |")
    lines.append(f"| :--- | :--- | :--- | :--- |")
    lines.append(f"| **🚀 入口** | `main.py` | `main()` | 程序启动入口 |")
    lines.append(f"| **🎨 界面** | `src/ui.py` | `PomodoroApp` | 主窗口、侧边栏及交互逻辑 |")
    lines.append(f"| **🎨 界面** | `src/ui.py` | `MiniFloatWindow` | 专注时的极简悬浮窗 |")
    lines.append(f"| **⚙️ 配置** | `src/config.py` | `AppConfig` | 颜色常量、字体大小、窗口尺寸 |")
    lines.append(f"| **🧠 内核** | `src/core.py` | `DataManager` | JSON 文件的读写与统计计算 |")
    lines.append(f"| **🔊 媒体** | `src/core.py` | `SoundManager` | 跨平台声音播放封装 |")
    lines.append(f"| **🛠️ 工具** | `src/core.py` | `ResourceManager` | 资源路径处理 (兼容打包后) |")
    lines.append(f"")

    # --- 流转图 ---
    lines.append(f"### 4. 🎯 关键数据文件流转图")
    lines.append(f"")
    lines.append(f"```text")
    lines.append(f"       [用户交互]")
    lines.append(f"           │")
    lines.append(f"           ▼")
    lines.append(f"    ┌─────────────┐")
    lines.append(f"    │  src/ui.py  │  <── (读取配置) ──  src/config.py")
    lines.append(f"    └──────┬──────┘")
    lines.append(f"           │ (产生专注记录)")
    lines.append(f"           ▼")
    lines.append(f"    ┌─────────────┐                                ┌──────────────────┐")
    lines.append(f"    │ src/core.py │  ──(序列化 JSON)──> [写入] ──→ │ focus_history.json │")
    lines.append(f"    │ DataManager │                                └─────────┬────────┘")
    lines.append(f"    └──────┬──────┘                                          │")
    lines.append(f"           │                                                 │")
    lines.append(f"           └────────────────── (读取统计) ────────────────────┘")
    lines.append(f"                              (反序列化)")
    lines.append(f"                                  │")
    lines.append(f"                                  ▼")
    lines.append(f"                            [UI 统计面板展示]")
    lines.append(f"```")
    lines.append(f"")

    # --- 说明 ---
    lines.append(f"### 5. 📌 使用说明")
    lines.append(f"")
    lines.append(f"#### 如何查找特定功能？")
    lines.append(f"- **想改颜色/字体**：直接修改 `src/config.py`，无需动逻辑代码。")
    lines.append(f"- **想改倒计时逻辑**：查看 `src/ui.py` 中的 `_run_countdown` 方法。")
    lines.append(f"- **想改数据存储格式**：修改 `src/core.py` 中的 `DataManager` 类。")
    lines.append(f"")
    lines.append(f"#### 如何追踪数据流向？")
    lines.append(f"打开 `focus_history.json`，每条记录格式如下：")
    lines.append(f"```json")
    lines.append(f"{{")
    lines.append(f"    \"date\": \"2023-10-27\",")
    lines.append(f"    \"timestamp\": 1698391200.5,")
    lines.append(f"    \"duration\": 25")
    lines.append(f"}}")
    lines.append(f"```")
    lines.append(f"系统通过计算 `date` 字段来匹配“今日”数据，通过 `timestamp` 计算“本周/本月”数据。")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"**文档自动生成于**：{dt.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return "\n".join(lines)


def save_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ 全景图文档已生成：{filename}")


if __name__ == "__main__":
    root_dir = os.getcwd()
    markdown_content = generate_markdown_content(root_dir)
    save_file(OUTPUT_FILENAME, markdown_content)