# src/ui.py
import customtkinter as ctk
from .config import config_manager
from .core import ResourceManager, SoundManager, TimerEngine, history_service
from .ui_components import MiniFloatWindow, TaskFrame, StatsFrame

class PomodoroApp:
    def __init__(self):
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("green")

        self.root = ctk.CTk()
        self.root.title(config_manager.get("TITLE"))
        self._set_window_center(config_manager.get("SIZE_MAIN"))

        self.root.attributes('-alpha', config_manager.get("GLASS_ALPHA"))
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after(10, lambda: self.root.attributes('-topmost', False))
        self.root.focus_force()
        self.root.minsize(900, 600)
        self.root.configure(fg_color=config_manager.get("COLOR_BG"))

        try:
            self.root.iconbitmap(ResourceManager.get_path("assets/icon.ico"))
        except: pass

        # === 核心状态 ===
        self.timer_engine = None
        self.in_focus_mode = False
        self.current_duration = 25
        self.current_tag = config_manager.get("FOCUS_TAGS")[0]

        self.time_str_var = ctk.StringVar(value="25:00")
        self.greeting_var = ctk.StringVar(value="准备好进入心流状态了吗？🌱")
        self.stat_vars = {"day": ctk.StringVar(value="0"), "week": ctk.StringVar(value="0"), "month": ctk.StringVar(value="0")}
        self.mini_window = None

        self._setup_ui()
        self._refresh_all_data()
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
            w, h = map(int, size_str.split('x'))
            x = (self.root.winfo_screenwidth() - w) // 2
            y = (self.root.winfo_screenheight() - h) // 2
            self.root.geometry(f"{w}x{h}+{x}+{y}")
        except: self.root.geometry(size_str)

    def _setup_ui(self):
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # 侧边栏
        self.sidebar_frame = ctk.CTkFrame(self.root, width=220, corner_radius=0,
                                          fg_color=config_manager.get("COLOR_SIDEBAR"))
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(self.sidebar_frame, text="专注·极简", font=config_manager.get("SIDEBAR_TITLE_FONT"),
                     text_color=config_manager.get("COLOR_PRIMARY")).pack(pady=(50, 40))

        self.btn_nav_timer = self._create_nav_btn("⏱  专注计时", lambda: self.select_frame("timer"))
        self.btn_nav_timer.pack(pady=8, padx=20, fill="x")
        self.btn_nav_tasks = self._create_nav_btn("✅  待办清单", lambda: self.select_frame("tasks"))
        self.btn_nav_tasks.pack(pady=8, padx=20, fill="x")
        self.btn_nav_stats = self._create_nav_btn("📊  数据统计", lambda: self.select_frame("stats"))
        self.btn_nav_stats.pack(pady=8, padx=20, fill="x")

        # 内容区
        self.content_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        self.frame_timer = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self._setup_timer_frame()
        self.frame_tasks = TaskFrame(self.content_frame)
        self.frame_stats = StatsFrame(self.content_frame, self.stat_vars)

    def _setup_timer_frame(self):
        card = ctk.CTkFrame(self.frame_timer, fg_color=config_manager.get("COLOR_CARD_BG"),
                            corner_radius=20, border_width=1, border_color=config_manager.get("COLOR_BORDER"))
        card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7, relheight=0.85)

        ctk.CTkLabel(card, textvariable=self.greeting_var, font=config_manager.get("GREETING_FONT"),
                     text_color=config_manager.get("COLOR_TEXT_MAIN")).pack(pady=(30, 5))

        ctk.CTkLabel(card, textvariable=self.time_str_var, font=config_manager.get("DISPLAY_TIME_FONT"),
                     text_color=config_manager.get("COLOR_PRIMARY")).pack(pady=5)

        control_panel = ctk.CTkFrame(card, fg_color="transparent")
        control_panel.pack(pady=5)

        self.seg_button = ctk.CTkSegmentedButton(
            control_panel, values=["15 分钟", "25 分钟", "45 分钟", "60 分钟"],
            command=self.on_preset_click, font=config_manager.get("PRESET_FONT"),
            height=config_manager.get("PRESET_HEIGHT"),
            fg_color=config_manager.get("COLOR_SIDEBAR"), selected_color=config_manager.get("COLOR_PRIMARY"),
            selected_hover_color=config_manager.get("COLOR_PRIMARY_HOVER"), corner_radius=20
        )
        self.seg_button.set("25 分钟")
        self.seg_button.pack(pady=10)

        self.slider = ctk.CTkSlider(control_panel, from_=5, to=120, number_of_steps=115, command=self.on_slider_drag,
                                    width=260, height=18, progress_color=config_manager.get("COLOR_PRIMARY"),
                                    button_color=config_manager.get("COLOR_PRIMARY"), button_hover_color=config_manager.get("COLOR_PRIMARY_HOVER"))
        self.slider.set(25)
        self.slider.pack(pady=10)

        tag_box = ctk.CTkFrame(control_panel, fg_color="transparent")
        tag_box.pack(pady=(5, 0))
        self.tag_seg = ctk.CTkSegmentedButton(tag_box, values=config_manager.get("FOCUS_TAGS"), command=self.on_tag_change,
                                              font=config_manager.get("TAG_FONT"), height=config_manager.get("TAG_HEIGHT"),
                                              fg_color=config_manager.get("COLOR_SIDEBAR"), selected_color=config_manager.get("COLOR_TAG_SELECTED"))
        self.tag_seg.set(config_manager.get("FOCUS_TAGS")[0])
        self.tag_seg.pack()

        ctk.CTkButton(card, text="开始专注", command=self.start_focus, width=220,
                      height=config_manager.get("BTN_START_HEIGHT"), corner_radius=config_manager.get("BTN_CORNER_RADIUS"),
                      font=config_manager.get("BTN_START_FONT"), fg_color=config_manager.get("COLOR_PRIMARY"),
                      hover_color=config_manager.get("COLOR_PRIMARY_HOVER")).pack(side="bottom", pady=40)

    def _create_nav_btn(self, text, command):
        # 修复：使用 get() 并提供默认值 45
        return ctk.CTkButton(
            self.sidebar_frame, text=text, command=command, fg_color="transparent",
            text_color=config_manager.get("COLOR_TEXT_MAIN"), hover_color="#FFFFFF", anchor="w", corner_radius=10,
            font=config_manager.get("SIDEBAR_BTN_FONT"),
            height=config_manager.get("SIDEBAR_BTN_HEIGHT", 45)
        )

    def select_frame(self, name):
        self.frame_timer.pack_forget()
        self.frame_tasks.pack_forget()
        self.frame_stats.pack_forget()
        self.btn_nav_timer.configure(fg_color="transparent")
        self.btn_nav_tasks.configure(fg_color="transparent")
        self.btn_nav_stats.configure(fg_color="transparent")

        btn_color = config_manager.get("COLOR_BTN_SELECTED")
        if name == "timer": self.frame_timer.pack(fill="both", expand=True); self.btn_nav_timer.configure(fg_color=btn_color)
        elif name == "tasks": self.frame_tasks.pack(fill="both", expand=True); self.btn_nav_tasks.configure(fg_color=btn_color); self.frame_tasks.refresh_list()
        elif name == "stats": self.frame_stats.pack(fill="both", expand=True); self.btn_nav_stats.configure(fg_color=btn_color); self.frame_stats.refresh_data()

    def _refresh_all_data(self): self.frame_stats.refresh_data()

    # --- 专注逻辑 ---
    def on_preset_click(self, value):
        if self.in_focus_mode: return
        mins = int(value.split(" ")[0])
        self.current_duration = mins
        self.slider.set(mins)
        self.update_display_time(mins)

    def on_slider_drag(self, value):
        if self.in_focus_mode: return
        mins = int(value)
        self.current_duration = mins
        if mins in [15, 25, 45, 60]: self.seg_button.set(f"{mins} 分钟")
        else: self.seg_button.set("")
        self.update_display_time(mins)

    def on_tag_change(self, value): self.current_tag = value
    def update_display_time(self, mins): self.time_str_var.set(f"{mins:02d}:00")

    def start_focus(self):
        if self.in_focus_mode: return
        try:
            mins = self.current_duration
            if mins <= 0: return
        except: return

        self.timer_engine = TimerEngine(mins)
        self.timer_engine.start()
        self.in_focus_mode = True
        self.greeting_var.set(f"正在进行 [{self.current_tag}]，保持专注...")
        self.root.withdraw()

        callbacks = {'toggle': self.toggle_pause, 'reset': self.reset_timer, 'stop': self.stop_focus}
        self.mini_window = MiniFloatWindow(self.root, self.time_str_var, self.current_tag, callbacks)
        self._on_timer_tick()

    def _on_timer_tick(self):
        if not self.in_focus_mode or not self.timer_engine: return
        is_finished, progress = self.timer_engine.tick()
        self.time_str_var.set(self.timer_engine.get_time_str())

        if self.mini_window:
            zen_msgs = config_manager.get("ZEN_MESSAGES")
            msg = zen_msgs['start'] if progress < 0.1 else (zen_msgs['end'] if progress > 0.9 else zen_msgs['focus'])
            self.mini_window.update_progress(progress, msg)
            self.mini_window.update_state(self.timer_engine.is_paused)

        if is_finished:
            self.mini_window.update_progress(1.0, "✨ 已完成")
            self._handle_finish()
        else:
            self.root.after(1000, self._on_timer_tick)

    def toggle_pause(self):
        if self.timer_engine:
            self.timer_engine.pause_toggle()
            if self.mini_window: self.mini_window.update_state(self.timer_engine.is_paused)

    def reset_timer(self):
        if self.timer_engine:
            self.timer_engine.reset()
            self.time_str_var.set(self.timer_engine.get_time_str())
            if self.mini_window:
                self.mini_window.update_progress(0, config_manager.get("ZEN_MESSAGES")['start'])
                self.mini_window.update_state(True)

    def stop_focus(self):
        self.in_focus_mode = False
        if self.timer_engine: self.timer_engine.stop(); self.timer_engine = None
        if self.mini_window: self.mini_window.destroy(); self.mini_window = None
        self.root.deiconify()
        self.greeting_var.set("欢迎回来，休息一下吧。")
        self.update_display_time(self.current_duration)
        self._bring_to_front()

    def _handle_finish(self):
        self.in_focus_mode = False
        SoundManager.play_finish()
        history_service.record_focus(self.current_duration, self.current_tag)
        if self.mini_window: self.mini_window.destroy(); self.mini_window = None
        self.root.deiconify()
        self.frame_stats.refresh_data()
        self.greeting_var.set(f"🎉 恭喜！本次 [{self.current_tag}] 已完成！")
        self.update_display_time(self.current_duration)
        self._bring_to_front()

    def run(self): self.root.mainloop()