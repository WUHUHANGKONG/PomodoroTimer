# 🍅 ZenPomo (Minimalist Pomodoro Timer)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![UI Framework](https://img.shields.io/badge/UI-CustomTkinter-green)](https://github.com/TomSchimansky/CustomTkinter)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> **Focus on what matters. Stay in the flow.**

**ZenPomo** is a sleek, modern, and lightweight Pomodoro timer built with Python. Unlike clunky electron apps, it's native, fast, and designed with a clean architecture. It combines task management, time tracking, and data visualization into one minimalist interface.

---

## ✨ Features

### 🎯 Core Focus
- **Customizable Timer:** Presets (15/25/45/60 min) or drag-to-set slider.
- **Floating Mini-Window:** A tiny, always-on-top widget to keep track of time without distraction.
- **Zen Messages:** Context-aware quotes that guide you through the start, focus, and finish stages.

### ✅ Task Management
- **Integrated To-Do List:** Add tasks with due dates.
- **Smart Sorting:** Tasks are auto-sorted by completion status and due dates.
- **Persistence:** All tasks are saved locally (JSON based).

### 📊 Data & Insights
- **Visual Dashboard:** View your daily, weekly, and monthly focus stats.
- **Trend Analysis:** Weekly bar charts to visualize your productivity consistency.
- **Detailed History:** Review your recent focus sessions.

---

## 📸 Screenshots

| **Main Interface** | **Data Dashboard** |
|:---:|:---:|
| <img src="assets/screenshot_main.png" alt="Main Timer" width="400"/> | <img src="assets/screenshot_stats.png" alt="Statistics" width="400"/> |

| **Task List** | **Floating Mini Mode** |
|:---:|:---:|
| <img src="assets/screenshot_tasks.png" alt="Task List" width="400"/> | <img src="assets/screenshot_mini.png" alt="Mini Mode" width="400"/> |

*(Note: Please replace the image paths above with your actual screenshots)*

---

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
   cd your-repo-name
2. **Install dependencies**
   ```bash
    pip install -r requirements.txt
3. **Run the application**
   ```bash
    python main.py
   
## 🏗️ Architecture

This project is not just a script; it's engineered with scalability in mind, making it a great learning resource for Python GUI development.

- **MV-ish Pattern:** Separation of Logic (Core) and View (UI).
- **Repository Pattern:** Data access logic (JSON) is decoupled from business logic via Service layers (`TaskService`, `HistoryService`).
- **Event-Driven:** Uses Tkinter's main loop (`.after()`) instead of unstable threading for UI updates.
- **Config Management:** Hot-loadable configuration system.

```mermaid
graph TD
    A["UI Layer (View)"] --> B["Service Layer"]
    B --> C["Repository Layer"]
    C --> D[("JSON Files")]
    A --> E["Timer Engine (State Machine)"]
    E --> A

## ⚙️ Configuration

You can customize the look and feel by editing `config.json` (generated after the first run) or modifying `src/config.py`.
- Change theme colors.
- Customize "Zen Messages".
- Adjust default timer durations.

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">
  <sub>Built with ❤️ by <a href="https://github.com/your-username">WUHUHANGKONG</a></sub>
</div>
