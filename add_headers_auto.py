import os
import ast
import datetime
import re

# ================= 配置区域 =================
# 排除的目录
EXCLUDE_DIRS = {'.venv', 'venv', 'site-packages', '__pycache__', '.git', '.idea', 'build', 'dist'}
# 排除的文件
EXCLUDE_FILES = {'add_headers_auto.py'}

# 模板定义
HEADER_TEMPLATE = """{shebang}############################################################
# 📘 文件说明：
# {description}
#
# 📋 程序整体伪代码（中文）：
# {pseudocode}
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
# 数据流向：{data_flow}
#
# 🧩 文件结构：
# {structure}
#
# 🕒 创建时间：{date}
############################################################

"""


# ================= 智能分析逻辑 =================

def get_file_metadata(filename, content):
    """
    根据文件名和内容推断元数据
    """
    name_lower = filename.lower()
    tree = None
    try:
        tree = ast.parse(content)
    except:
        pass

    # 1. 推断功能描述 (Description) & 伪代码 (Pseudocode)
    desc = "本文件实现的功能：通用 Python 脚本模块，提供相关工具或逻辑支持。"
    pseudo = "1. 初始化模块\n# 2. 执行核心逻辑\n# 3. 返回处理结果"
    data_flow = "输入参数 → 逻辑处理 → 返回值/对象状态变更"

    if 'ui' in name_lower or 'gui' in name_lower or 'window' in name_lower:
        desc = "本文件实现的功能：用户界面（UI）构建与交互逻辑处理，负责窗口渲染及事件绑定。"
        pseudo = "1. 初始化 UI 库（如 CustomTkinter）\n# 2. 构建主窗口与布局容器\n# 3. 绑定按钮点击与事件回调\n# 4. 启动 GUI 主事件循环"
        data_flow = "用户操作（点击/输入） → 事件回调函数 → 核心逻辑调用 → 界面状态更新"

    elif 'config' in name_lower or 'setting' in name_lower:
        desc = "本文件实现的功能：全局配置管理，定义应用程序的常量、参数及样式标准。"
        pseudo = "1. 定义配置类或字典\n# 2. 设置颜色、字体、路径等静态常量\n# 3. 提供配置获取接口"
        data_flow = "硬编码常量 → 应用程序读取 → 全局样式/行为控制"

    elif 'core' in name_lower or 'manager' in name_lower or 'logic' in name_lower:
        desc = "本文件实现的功能：核心业务逻辑处理，包括数据计算、状态管理及资源调度。"
        pseudo = "1. 接收 UI 或外部指令\n# 2. 执行复杂业务算法（如计时、计算）\n# 3. 操作数据持久化层\n# 4. 返回执行结果或触发信号"
        data_flow = "UI 指令 → 业务逻辑层 → 数据处理/文件读写 → 状态反馈"

    elif 'main' in name_lower or 'run' in name_lower:
        desc = "本文件实现的功能：应用程序入口，负责初始化环境并启动主程序。"
        pseudo = "1. 导入 UI 与核心模块\n# 2. 实例化主应用程序类\n# 3. 捕获启动异常\n# 4. 进入程序主循环"
        data_flow = "系统启动 → 环境检查 → 加载主窗口 → 等待用户交互"

    elif 'utils' in name_lower or 'helper' in name_lower:
        desc = "本文件实现的功能：通用工具函数集合，提供跨模块复用的辅助功能（如路径处理、格式化）。"
        pseudo = "1. 定义静态工具函数\n# 2. 处理特定单一任务（如获取路径）\n# 3. 返回标准化结果"

    # 2. 提取文件结构 (Structure) - 分析 AST
    structure_lines = []
    if tree:
        # 提取 Import
        imports = [node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)]
        import_froms = [node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module]
        all_deps = list(set(imports + import_froms))
        if all_deps:
            structure_lines.append(f"- 依赖库：{', '.join(all_deps[:5])}" + ("..." if len(all_deps) > 5 else ""))

        # 提取 Class
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                structure_lines.append(f"- 类 (Class)：{node.name} - (封装核心对象)")
                # 提取类内主要方法
                methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef) and not n.name.startswith('_')]
                if methods:
                    method_str = ", ".join(methods[:3])
                    structure_lines.append(f"  └─ 核心方法：{method_str}" + ("..." if len(methods) > 3 else ""))

        # 提取 Top-level Function
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and isinstance(node.parent, ast.Module) if hasattr(node,
                                                                                                    'parent') else False:
                pass  # AST parent handling needs extra library, keeping simple loop for top level

        # 简单遍历 module body 找顶层函数
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                structure_lines.append(f"- 函数 (Function)：{node.name} - (独立功能模块)")

    if not structure_lines:
        structure_lines.append("- 暂无明确定义的类或顶层函数")

    return desc, pseudo, data_flow, "\n# ".join(structure_lines)


def process_file(filepath):
    filename = os.path.basename(filepath)

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    content_str = "".join(lines)

    # 检查是否已经添加过头注释
    if "📘 文件说明：" in content_str:
        print(f"⏩ 跳过 (已存在头注释): {filename}")
        return

    # 提取 Shebang 和 Encoding
    shebang_lines = ""
    code_start_idx = 0

    # 检查前两行是否有 #! 或 coding
    for i in range(min(2, len(lines))):
        line = lines[i]
        if line.startswith("#!") or "coding:" in line or "encoding=" in line:
            shebang_lines += line
            code_start_idx += 1
        else:
            break

    # 获取剩余代码内容用于分析
    remaining_code = "".join(lines[code_start_idx:])

    # 获取智能元数据
    desc, pseudo, data_flow, structure = get_file_metadata(filename, remaining_code)

    # 格式化模板
    new_header = HEADER_TEMPLATE.format(
        shebang=shebang_lines,
        description=desc,
        pseudocode=pseudo,
        data_flow=data_flow,
        structure=structure,
        date=datetime.datetime.now().strftime("%Y-%m-%d")
    )

    # 组合新内容
    new_content = new_header + remaining_code.lstrip()

    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✅ 处理完成: {filename}")


def main():
    root_dir = os.getcwd()
    print(f"📂 开始扫描项目: {root_dir}")
    print("-" * 50)

    count = 0
    for subdir, dirs, files in os.walk(root_dir):
        # 排除目录
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file in files:
            if file.endswith('.py') and file not in EXCLUDE_FILES:
                filepath = os.path.join(subdir, file)
                try:
                    process_file(filepath)
                    count += 1
                except Exception as e:
                    print(f"❌ 处理出错 {file}: {e}")

    print("-" * 50)
    print(f"🎉 全部完成！共处理 {count} 个文件。")


if __name__ == "__main__":
    main()