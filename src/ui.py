# src/ui.py
import customtkinter as ctk
import time
import threading
from .config import AppConfig
from .core import ResourceManager, SoundManager, DataManager


# --- 悬浮窗 (MiniFloatWindow) ---
class MiniFloatWindow(ctk.CTkToplevel):
    def __init__(self, master, time_var, stop_callback):
        super().__init__(master)
        self.stop_callback = stop_callback

        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.configure(fg_color=AppConfig.COLOR_BG_MINI)
        self.grid_columnconfigure(0, weight=1)

        sw = self.winfo_screenwidth()
        w, h = 220, 70
        x = sw - w - 20
        y = 20
        self.geometry(f"{w}x{h}+{x}+{y}")

        self.lbl_time = ctk.CTkLabel(
            self, textvariable=time_var,
            font=AppConfig.MINI_TIME_FONT,
            text_color=AppConfig.COLOR_PRIMARY
        )
        self.lbl_time.pack(side="left", padx=(20, 10))

        right_frame = ctk.CTkFrame(self, fg_color="transparent")
        right_frame.pack(side="left", pady=5)

        ctk.CTkLabel(right_frame, text="保持专注", font=AppConfig.MINI_TEXT_FONT,
                     text_color=AppConfig.COLOR_TEXT_MAIN).pack()

        self.btn_stop = ctk.CTkButton(
            right_frame, text="⏹", width=30, height=20,
            fg_color=AppConfig.COLOR_RED, hover_color=AppConfig.COLOR_RED_HOVER,
            command=self.stop_callback
        )
        self.btn_stop.pack(pady=2)


# --- 主程序 (PomodoroApp) ---
class PomodoroApp:
    def __init__(self):
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("green")

        self.root = ctk.CTk()
        self.root.title(AppConfig.TITLE)

        self._set_window_center(AppConfig.SIZE_MAIN)
        self.root.minsize(900, 600)

        try:
            self.root.iconbitmap(ResourceManager.get_path("assets/icon.ico"))
        except:
            pass

        # 核心变量
        self.is_running = False
        self.time_left = 0
        self.current_duration = 25
        self.current_tag = AppConfig.FOCUS_TAGS[0]

        self.time_str_var = ctk.StringVar(value="25:00")
        self.greeting_var = ctk.StringVar(value="准备好进入心流状态了吗？🌱")

        # 统计变量
        self.stat_vars = {
            "day": ctk.StringVar(value="0"),
            "week": ctk.StringVar(value="0"),
            "month": ctk.StringVar(value="0")
        }

        self.mini_window = None

        self._setup_ui()
        self._refresh_stats()
        self.select_frame("timer")

        self._bring_to_front()

    def _bring_to_front(self):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self.root.attributes('-topmost', True)
        self.root.after(200, lambda: self.root.attributes('-topmost', False))

    def _set_window_center(self, size_str):
        try:
            w_str, h_str = size_str.split('x')
            window_width = int(w_str)
            window_height = int(h_str)
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        except:
            self.root.geometry(size_str)

    def _create_nav_btn(self, text, command):
        return ctk.CTkButton(
            self.sidebar_frame, text=text, command=command,
            fg_color="transparent", text_color=AppConfig.COLOR_TEXT_MAIN,
            hover_color=AppConfig.COLOR_BTN_SELECTED,
            anchor="w",
            font=AppConfig.SIDEBAR_BTN_FONT,
            height=AppConfig.SIDEBAR_BTN_HEIGHT
        )

    def select_frame(self, name):
        self.frame_timer.pack_forget()
        self.frame_stats.pack_forget()

        self.btn_nav_timer.configure(fg_color="transparent")
        self.btn_nav_stats.configure(fg_color="transparent")

        if name == "timer":
            self.frame_timer.pack(fill="both", expand=True)
            self.btn_nav_timer.configure(fg_color=AppConfig.COLOR_BTN_SELECTED)
        elif name == "stats":
            self.frame_stats.pack(fill="both", expand=True)
            self.btn_nav_stats.configure(fg_color=AppConfig.COLOR_BTN_SELECTED)

    def _create_stat_row(self, parent, title, var):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=15, padx=100)
        ctk.CTkLabel(row, text=title, font=("微软雅黑", 18), text_color=AppConfig.COLOR_TEXT_MAIN).pack(side="left")
        ctk.CTkLabel(row, textvariable=var, font=("Roboto Medium", 24),
                     text_color=AppConfig.COLOR_PRIMARY).pack(side="right")

    def _refresh_stats(self):
        stats = DataManager.get_stats()
        self.stat_vars["day"].set(str(stats['day']))
        self.stat_vars["week"].set(str(stats['week']))
        self.stat_vars["month"].set(str(stats['month']))

    # --- 界面构建 ---
    def _setup_ui(self):
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # === 左侧侧边栏 ===
        self.sidebar_frame = ctk.CTkFrame(self.root, width=220, corner_radius=0, fg_color=AppConfig.COLOR_SIDEBAR)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(self.sidebar_frame, text="🍅 番茄钟", font=AppConfig.SIDEBAR_TITLE_FONT,
                     text_color=AppConfig.COLOR_PRIMARY).pack(pady=(40, 30))

        self.btn_nav_timer = self._create_nav_btn("⏱  专注模式", lambda: self.select_frame("timer"))
        self.btn_nav_timer.pack(pady=5, padx=15, fill="x")
        self.btn_nav_stats = self._create_nav_btn("📊  数据统计", lambda: self.select_frame("stats"))
        self.btn_nav_stats.pack(pady=5, padx=15, fill="x")

        # === 右侧内容区 ===
        self.content_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # ---------------------------------------------------------
        # 页面 A: 专注计时
        # ---------------------------------------------------------
        self.frame_timer = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.center_box = ctk.CTkFrame(self.frame_timer, fg_color="transparent")
        self.center_box.place(relx=0.5, rely=0.5, anchor="center")

        # 1. 暖心问候语
        ctk.CTkLabel(self.center_box, textvariable=self.greeting_var,
                     font=AppConfig.GREETING_FONT, text_color=AppConfig.COLOR_TEXT_MAIN).pack(pady=(0, 20))

        # 2. 超大时间显示
        self.lbl_big_time = ctk.CTkLabel(self.center_box, textvariable=self.time_str_var,
                                         font=AppConfig.DISPLAY_TIME_FONT,
                                         text_color=AppConfig.COLOR_PRIMARY)
        self.lbl_big_time.pack(pady=5)

        # 3. 智能选择区 (容器)
        self.control_panel = ctk.CTkFrame(self.center_box, fg_color="transparent")
        self.control_panel.pack(pady=20)

        # 3.1 时间预设 (绿色系)
        self.seg_button = ctk.CTkSegmentedButton(
            self.control_panel,
            values=["15 分钟", "25 分钟", "45 分钟", "60 分钟"],
            command=self.on_preset_click,
            font=AppConfig.PRESET_FONT,
            height=AppConfig.PRESET_HEIGHT,
            fg_color=AppConfig.COLOR_SECONDARY_BG,
            selected_color=AppConfig.COLOR_PRIMARY,
            selected_hover_color=AppConfig.COLOR_PRIMARY_HOVER,
            unselected_color=AppConfig.COLOR_SECONDARY_BG,
            unselected_hover_color="#E0E0E0"
        )
        self.seg_button.set("25 分钟")
        self.seg_button.pack(pady=10)

        # 3.2 滑块 (绿色系)
        self.slider = ctk.CTkSlider(
            self.control_panel,
            from_=5, to=120, number_of_steps=115,
            command=self.on_slider_drag,
            width=300, height=20,
            progress_color=AppConfig.COLOR_PRIMARY,
            button_color=AppConfig.COLOR_PRIMARY,
            button_hover_color=AppConfig.COLOR_PRIMARY_HOVER
        )
        self.slider.set(25)
        self.slider.pack(pady=10)

        # --- ✨ 优化后的标签选择区 ---

        # 增加一个视觉分隔和提示
        tag_frame = ctk.CTkFrame(self.control_panel, fg_color="transparent")
        tag_frame.pack(pady=(25, 0))  # 增加上方间距，与时间选择区隔开

        ctk.CTkLabel(tag_frame, text="🔖 当前专注类型",
                     font=("微软雅黑", 12, "bold"),
                     text_color=AppConfig.COLOR_TEXT_SUB).pack(pady=(0, 8))

        # 标签选择器 (蓝色系)
        self.tag_seg = ctk.CTkSegmentedButton(
            tag_frame,
            values=AppConfig.FOCUS_TAGS,
            command=self.on_tag_change,
            font=AppConfig.TAG_FONT,
            height=AppConfig.TAG_HEIGHT,
            fg_color=AppConfig.COLOR_SECONDARY_BG,
            # ✨ 使用我们定义的新蓝色
            selected_color=AppConfig.COLOR_TAG_SELECTED,
            selected_hover_color=AppConfig.COLOR_TAG_HOVER,
            unselected_color=AppConfig.COLOR_SECONDARY_BG,
            unselected_hover_color="#E0E0E0"
        )
        self.tag_seg.set(AppConfig.FOCUS_TAGS[0])
        self.tag_seg.pack()

        # 4. 开始按钮
        self.btn_start = ctk.CTkButton(
            self.center_box,
            text="🚀 开启专注",
            command=self.start_focus,
            width=280,
            height=AppConfig.BTN_START_HEIGHT,
            corner_radius=AppConfig.BTN_CORNER_RADIUS,
            font=AppConfig.BTN_START_FONT,
            fg_color=AppConfig.COLOR_PRIMARY,
            hover_color=AppConfig.COLOR_PRIMARY_HOVER
        )
        self.btn_start.pack(pady=40)

        # ---------------------------------------------------------
        # 页面 B: 统计页面
        # ---------------------------------------------------------
        self.frame_stats = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.center_box_stats = ctk.CTkFrame(self.frame_stats, fg_color="transparent")
        self.center_box_stats.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self.center_box_stats, text="📅 你的专注足迹", font=("微软雅黑", 28, "bold"),
                     text_color=AppConfig.COLOR_TEXT_MAIN).pack(pady=(0, 50))
        self._create_stat_row(self.center_box_stats, "今日", self.stat_vars["day"])
        self._create_stat_row(self.center_box_stats, "本周", self.stat_vars["week"])
        self._create_stat_row(self.center_box_stats, "本月", self.stat_vars["month"])

        ctk.CTkButton(self.center_box_stats, text="🔄 刷新数据", command=self._refresh_stats, fg_color="gray", width=120,
                      height=40).pack(pady=60)

    # --- 交互逻辑 ---

    def on_preset_click(self, value):
        if self.is_running: return
        mins = int(value.split(" ")[0])
        self.current_duration = mins
        self.slider.set(mins)
        self.update_display_time(mins)

    def on_slider_drag(self, value):
        if self.is_running: return
        mins = int(value)
        self.current_duration = mins
        if mins in [15, 25, 45, 60]:
            self.seg_button.set(f"{mins} 分钟")
        else:
            self.seg_button.set("")
        self.update_display_time(mins)

    def on_tag_change(self, value):
        self.current_tag = value

    def update_display_time(self, mins):
        self.time_str_var.set(f"{mins:02d}:00")

    def start_focus(self):
        if self.is_running: return

        mins = self.current_duration
        self.work_time = mins * 60
        self.time_left = self.work_time
        self.is_running = True

        self.greeting_var.set(f"正在进行 [{self.current_tag}]，保持专注...")

        self.root.withdraw()
        self.mini_window = MiniFloatWindow(self.root, self.time_str_var, self.stop_focus)

        threading.Thread(target=self._run_countdown, daemon=True).start()

    def _run_countdown(self):
        while self.is_running and self.time_left > 0:
            m, s = divmod(self.time_left, 60)
            self.time_str_var.set(f"{m:02d}:{s:02d}")
            time.sleep(1)
            self.time_left -= 1

        if self.is_running and self.time_left == 0:
            self.time_str_var.set("00:00")
            self.is_running = False
            SoundManager.play_finish()
            DataManager.save_record(self.current_duration, self.current_tag)
            self.root.after(0, self._restore_finish_ui)

    def _restore_finish_ui(self):
        if self.mini_window:
            self.mini_window.destroy()
            self.mini_window = None
        self.root.deiconify()

        self.greeting_var.set(f"🎉 [{self.current_tag}] 任务完成！休息一下吧！")
        self._refresh_stats()
        self.update_display_time(self.current_duration)

        self._bring_to_front()

    def stop_focus(self):
        self.is_running = False
        if self.mini_window:
            self.mini_window.destroy()
            self.mini_window = None
        self.root.deiconify()

        self.greeting_var.set("没关系，休息是为了走更远的路。")
        self.update_display_time(self.current_duration)

        self._bring_to_front()

    def run(self):
        self.root.mainloop()