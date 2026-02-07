# src/ui_components.py
import customtkinter as ctk
import sys
from datetime import datetime
from .config import config_manager
from .core import task_service, history_service


class MiniFloatWindow(ctk.CTkToplevel):
    def __init__(self, master, time_var, current_tag, callbacks):
        super().__init__(master)
        self.callbacks = callbacks
        self.overrideredirect(True)
        self.attributes('-topmost', True)

        bg_color = config_manager.get("COLOR_BG_MINI")
        primary_color = config_manager.get("COLOR_PRIMARY")

        if sys.platform.startswith("darwin"):
            self.attributes('-transparent', True)
            self.configure(fg_color='systemTransparent')
        else:
            self.attributes('-alpha', 0.9)
            self.configure(fg_color=bg_color)

        sw, w, h = self.winfo_screenwidth(), 360, 110
        self.geometry(f"{w}x{h}+{sw - w - 30}+{30}")

        self.main_frame = ctk.CTkFrame(self, fg_color=bg_color, border_width=2,
                                       border_color=primary_color, corner_radius=18)
        self.main_frame.pack(fill="both", expand=True)

        self._bind_drag(self.main_frame)

        content_box = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content_box.pack(fill="x", padx=25, pady=(15, 5))
        self._bind_drag(content_box)

        self.lbl_time = ctk.CTkLabel(content_box, textvariable=time_var, width=125, anchor="w",
                                     font=config_manager.get("MINI_TIME_FONT"), text_color=primary_color)
        self.lbl_time.pack(side="left")
        self._bind_drag(self.lbl_time)

        right_frame = ctk.CTkFrame(content_box, fg_color="transparent")
        right_frame.pack(side="right")
        ctk.CTkLabel(right_frame, text=f" {current_tag} ", font=("SF Pro Text", 12, "bold"),
                     text_color="white", fg_color=config_manager.get("COLOR_TAG_SELECTED"), corner_radius=6,
                     height=22, width=120, anchor="center").pack(anchor="center", pady=(0, 8))

        btn_box = ctk.CTkFrame(right_frame, fg_color="transparent")
        btn_box.pack(anchor="center")
        self.btn_toggle = ctk.CTkButton(btn_box, text="⏸", width=32, height=32, font=("Arial", 14),
                                        fg_color=config_manager.get("COLOR_PAUSE"), corner_radius=16,
                                        command=self.callbacks['toggle'])
        self.btn_toggle.pack(side="left", padx=4)
        ctk.CTkButton(btn_box, text="↺", width=32, height=32, font=("Arial", 14), fg_color="#dfe6e9",
                      text_color="gray", corner_radius=16, command=self.callbacks['reset']).pack(side="left", padx=4)
        ctk.CTkButton(btn_box, text="⏹", width=32, height=32, font=("Arial", 12), fg_color="#ff7675",
                      corner_radius=16, command=self.callbacks['stop']).pack(side="left", padx=4)

        self.lbl_status = ctk.CTkLabel(self.main_frame, text="准备...", font=config_manager.get("MINI_TEXT_FONT"),
                                       text_color=config_manager.get("COLOR_TEXT_SUB"), height=15)
        self.lbl_status.pack(anchor="w", padx=28, pady=(0, 2))
        self.progress_bar = ctk.CTkProgressBar(self.main_frame, height=4, corner_radius=2,
                                               progress_color=primary_color, fg_color="#F0F2F5", width=300)
        self.progress_bar.pack(fill="x", padx=25, pady=(2, 12))
        self.progress_bar.set(0)

    def _bind_drag(self, widget):
        widget.bind("<Button-1>", self.start_move)
        widget.bind("<B1-Motion>", self.do_move)

    def update_progress(self, percent, message):
        self.progress_bar.set(percent)
        self.lbl_status.configure(text=message)
        self.progress_bar.configure(progress_color="#00cec9" if percent > 0.9 else config_manager.get("COLOR_PRIMARY"))

    def update_state(self, is_paused):
        pause_col = config_manager.get("COLOR_PAUSE")
        prim_col = config_manager.get("COLOR_PRIMARY")
        if is_paused:
            self.main_frame.configure(border_color=pause_col)
            self.lbl_time.configure(text_color=pause_col)
            self.progress_bar.configure(progress_color=pause_col)
            self.lbl_status.configure(text="⏸ 暂停")
            self.btn_toggle.configure(text="▶", fg_color=prim_col)
        else:
            self.main_frame.configure(border_color=prim_col)
            self.lbl_time.configure(text_color=prim_col)
            self.progress_bar.configure(progress_color=prim_col)
            self.btn_toggle.configure(text="⏸", fg_color=pause_col)

    def start_move(self, event):
        self.x, self.y = event.x, event.y

    def do_move(self, event):
        self.geometry(f"+{self.winfo_x() + event.x - self.x}+{self.winfo_y() + event.y - self.y}")


class TaskFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.tasks = []
        self._setup_ui()
        self.refresh_list()

    def _setup_ui(self):
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", padx=40, pady=(30, 20))
        ctk.CTkLabel(top_bar, text="待办清单", font=("SF Pro Display", 26, "bold"),
                     text_color=config_manager.get("COLOR_TEXT_MAIN")).pack(side="left")
        self.lbl_count = ctk.CTkLabel(top_bar, text="0 个待办", font=("SF Pro Text", 14),
                                      text_color=config_manager.get("COLOR_PRIMARY"))
        self.lbl_count.pack(side="right")

        card = ctk.CTkFrame(self, fg_color=config_manager.get("COLOR_CARD_BG"), corner_radius=20, border_width=1,
                            border_color=config_manager.get("COLOR_BORDER"))
        card.pack(fill="both", expand=True, padx=40, pady=(0, 40))

        add_box = ctk.CTkFrame(card, fg_color="transparent")
        add_box.pack(fill="x", padx=20, pady=20)
        self.entry_task = ctk.CTkEntry(add_box, placeholder_text="新任务...", height=45, border_width=0,
                                       fg_color="#F0F2F5", text_color="black", corner_radius=10)
        self.entry_task.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_task.bind("<Return>", self.add_new_task)
        self.entry_date = ctk.CTkEntry(add_box, placeholder_text="日期 (2023-10-01)", width=160, height=45,
                                       border_width=0, fg_color="#F0F2F5", text_color="black", corner_radius=10)
        self.entry_date.pack(side="left", padx=(0, 10))
        self.entry_date.bind("<Return>", self.add_new_task)
        ctk.CTkButton(add_box, text="+", width=45, height=45, font=("Arial", 22),
                      fg_color=config_manager.get("COLOR_PRIMARY"), command=self.add_new_task).pack(side="right")

        self.scroll_tasks = ctk.CTkScrollableFrame(card, fg_color="transparent")
        self.scroll_tasks.pack(fill="both", expand=True, padx=10, pady=(0, 20))

    def refresh_list(self):
        self.tasks = task_service.get_tasks()
        self.lbl_count.configure(text=f"{sum(1 for t in self.tasks if not t['completed'])} 个待办")
        for w in self.scroll_tasks.winfo_children(): w.destroy()
        if not self.tasks:
            ctk.CTkLabel(self.scroll_tasks, text="🍃 全部完成", font=("Arial", 20), text_color="gray").pack(pady=50)
            return
        for task in self.tasks: self._render_single_task(task)

    def _render_single_task(self, task):
        row = ctk.CTkFrame(self.scroll_tasks, fg_color="transparent")
        row.pack(fill="x", pady=2)
        is_done = task["completed"]
        color = config_manager.get("TASK_DONE_COLOR") if is_done else config_manager.get("COLOR_TEXT_MAIN")

        chk = ctk.CTkCheckBox(row, text="", width=22, height=22, fg_color=config_manager.get("COLOR_PRIMARY"),
                              command=lambda t=task["id"]: self.toggle_task(t))
        if is_done: chk.select()
        chk.pack(side="left", padx=10)
        ctk.CTkLabel(row, text=task["title"], font=config_manager.get("TASK_FONT"), text_color=color, anchor="w").pack(
            side="left", fill="x", expand=True)
        if task.get("due_date"):
            ctk.CTkLabel(row, text=task["due_date"], font=("SF Pro Text", 12), text_color="gray").pack(side="left",
                                                                                                       padx=10)
        ctk.CTkButton(row, text="✕", width=30, fg_color="transparent", text_color="gray", hover_color="#ffeaa7",
                      command=lambda t=task["id"]: self.delete_task(t)).pack(side="right")

    def add_new_task(self, event=None):
        if self.entry_task.get().strip():
            task_service.add_task(self.entry_task.get().strip(), self.entry_date.get().strip())
            self.entry_task.delete(0, "end");
            self.entry_date.delete(0, "end");
            self.refresh_list()

    def toggle_task(self, tid):
        task_service.toggle_task(tid); self.refresh_list()

    def delete_task(self, tid):
        task_service.delete_task(tid); self.refresh_list()


# [请修改 src/ui_components.py 中的 StatsFrame 类]

class StatsFrame(ctk.CTkFrame):
    def __init__(self, master, stat_vars, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.stat_vars = stat_vars  # 保留引用，虽然主要数据通过 Service 获取
        self._setup_ui()

    def _setup_ui(self):
        # 顶部标题
        ctk.CTkLabel(self, text="数据看板", font=("SF Pro Display", 26, "bold"),
                     text_color=config_manager.get("COLOR_TEXT_MAIN")).pack(pady=(30, 20), anchor="w", padx=40)

        # === 核心：整个页面可滚动 ===
        self.main_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # 1. KPI 卡片区域
        self._setup_kpi_cards()

        # 2. 图表区域容器 (左右布局或上下布局，这里用上下布局更清晰)
        self.charts_container = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        self.charts_container.pack(fill="x", pady=10)

        # 3. 近7天趋势模块
        self._setup_trend_section()

        # 4. 最近记录模块
        self._setup_history_section()

        # 底部刷新按钮
        ctk.CTkButton(self, text="刷新数据", command=self.refresh_data, fg_color="transparent",
                      text_color="gray", height=20, font=("Arial", 12)).pack(pady=5)

    def _setup_kpi_cards(self):
        kpi_box = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        kpi_box.pack(fill="x", pady=(0, 20))

        self.kpi_day = self._create_card(kpi_box, "今日专注", config_manager.get("COLOR_PRIMARY"))
        self.kpi_day.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.kpi_week = self._create_card(kpi_box, "本周时长", "#0984e3")
        self.kpi_week.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.kpi_month = self._create_card(kpi_box, "本月累计", "#6c5ce7")
        self.kpi_month.pack(side="left", fill="x", expand=True)

    def _create_card(self, parent, title, color):
        card = ctk.CTkFrame(parent, fg_color=config_manager.get("COLOR_CARD_BG"), corner_radius=16,
                            border_width=1, border_color=config_manager.get("COLOR_BORDER"))
        ctk.CTkLabel(card, text=title, font=("SF Pro Text", 13), text_color="#b2bec3").pack(pady=(15, 5), padx=20,
                                                                                            anchor="w")
        lbl = ctk.CTkLabel(card, text="0", font=("SF Pro Display", 32), text_color=color)
        lbl.pack(pady=(0, 15), padx=20, anchor="w")
        card.value_label = lbl  # 绑定引用以便更新
        return card

    def _setup_trend_section(self):
        # 外框
        self.trend_frame = ctk.CTkFrame(self.charts_container, fg_color=config_manager.get("COLOR_CARD_BG"),
                                        corner_radius=16, border_width=1,
                                        border_color=config_manager.get("COLOR_BORDER"))
        self.trend_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(self.trend_frame, text="📈 近7天专注趋势", font=("SF Pro Text", 15, "bold"),
                     text_color=config_manager.get("COLOR_TEXT_MAIN")).pack(pady=15, padx=20, anchor="w")

        # 柱状图容器
        self.bar_container = ctk.CTkFrame(self.trend_frame, fg_color="transparent")
        self.bar_container.pack(fill="x", padx=20, pady=(0, 20))

    def _setup_history_section(self):
        # 外框
        self.history_frame = ctk.CTkFrame(self.charts_container, fg_color=config_manager.get("COLOR_CARD_BG"),
                                          corner_radius=16, border_width=1,
                                          border_color=config_manager.get("COLOR_BORDER"))
        self.history_frame.pack(fill="x")

        ctk.CTkLabel(self.history_frame, text="📝 最近专注记录", font=("SF Pro Text", 15, "bold"),
                     text_color=config_manager.get("COLOR_TEXT_MAIN")).pack(pady=15, padx=20, anchor="w")

        # 列表容器
        self.list_container = ctk.CTkFrame(self.history_frame, fg_color="transparent")
        self.list_container.pack(fill="x", padx=20, pady=(0, 20))

    def refresh_data(self):
        # 1. 更新 KPI (旧接口)
        stats = history_service.get_stats()
        self.kpi_day.value_label.configure(text=f"{stats['day']}")
        self.kpi_week.value_label.configure(text=f"{stats['week']}")
        self.kpi_month.value_label.configure(text=f"{stats['month']}")

        # 2. 更新图表 (新接口)
        chart_data = history_service.get_chart_data()
        self._render_trend_chart(chart_data['trend'])
        self._render_recent_history(chart_data['recent'])

    def _render_trend_chart(self, trend_data):
        # 清空旧图表
        for widget in self.bar_container.winfo_children():
            widget.destroy()

        if not trend_data:
            return

        for day in trend_data:
            row = ctk.CTkFrame(self.bar_container, fg_color="transparent")
            row.pack(fill="x", pady=6)

            # 日期标签 (09-21)
            ctk.CTkLabel(row, text=day['date_label'], width=50, anchor="w",
                         font=("SF Pro Text", 12), text_color="#636e72").pack(side="left")

            # 进度条
            bar = ctk.CTkProgressBar(row, height=8, corner_radius=4, fg_color="#F0F2F5",
                                     progress_color=config_manager.get("COLOR_PRIMARY"))
            bar.pack(side="left", fill="x", expand=True, padx=10)
            bar.set(day['percent'])

            # 数值标签 (45分)
            val_text = f"{day['minutes']}分" if day['minutes'] > 0 else "-"
            ctk.CTkLabel(row, text=val_text, width=50, anchor="e",
                         font=("SF Pro Text", 12, "bold"), text_color=config_manager.get("COLOR_PRIMARY")).pack(
                side="right")

    def _render_recent_history(self, recent_data):
        for widget in self.list_container.winfo_children():
            widget.destroy()

        if not recent_data:
            ctk.CTkLabel(self.list_container, text="暂无记录", text_color="gray").pack(pady=10)
            return

        # 表头
        header = ctk.CTkFrame(self.list_container, fg_color="transparent")
        header.pack(fill="x", pady=(0, 5))
        ctk.CTkLabel(header, text="时间", width=120, anchor="w", font=("Arial", 12, "bold"), text_color="#b2bec3").pack(
            side="left")
        ctk.CTkLabel(header, text="标签", width=80, anchor="center", font=("Arial", 12, "bold"),
                     text_color="#b2bec3").pack(side="left")
        ctk.CTkLabel(header, text="时长", width=60, anchor="e", font=("Arial", 12, "bold"), text_color="#b2bec3").pack(
            side="right")

        for rec in recent_data:
            row = ctk.CTkFrame(self.list_container, fg_color="transparent")
            row.pack(fill="x", pady=4)

            # 时间格式化
            dt = datetime.fromtimestamp(rec.get("timestamp", 0))
            time_str = dt.strftime("%m-%d %H:%M")

            ctk.CTkLabel(row, text=time_str, width=120, anchor="w", font=("SF Pro Text", 13),
                         text_color=config_manager.get("COLOR_TEXT_MAIN")).pack(side="left")

            tag = rec.get("tag", "默认")
            ctk.CTkLabel(row, text=tag, width=80, anchor="center", font=("SF Pro Text", 12),
                         fg_color="#F0F2F5", corner_radius=6, text_color="#636e72").pack(side="left", padx=5)

            dur = rec.get("duration", 0)
            ctk.CTkLabel(row, text=f"{dur} min", width=60, anchor="e", font=("SF Pro Text", 13, "bold"),
                         text_color=config_manager.get("COLOR_PRIMARY")).pack(side="right")

            # 分隔线
            ctk.CTkFrame(self.list_container, height=1, fg_color="#F0F2F5").pack(fill="x", pady=(2, 0))