#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周报统计器
统计本周笔记产出：新增/修改文件数、字数、分布情况
输出到 400-日记/ 作为周复盘笔记

用法:
  python weekly_report.py
"""

import datetime
import os
import subprocess

VAULT_PATH = r"E:\超级个体知识库"
DIARY_DIR = os.path.join(VAULT_PATH, "400-日记")
SCRIPTS_DIR = os.path.join(VAULT_PATH, ".agents", "scripts")

WEEKDAYS_CN = {
    0: "星期一", 1: "星期二", 2: "星期三", 3: "星期四",
    4: "星期五", 5: "星期六", 6: "星期日"
}


def get_git_stats(days=7):
    """用 git log 统计本周变更"""
    try:
        since = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
        result = subprocess.run(
            ["git", "-C", VAULT_PATH, "log", f"--since={since}",
             "--name-only", "--pretty=format:%H %s", "--diff-filter=AM"],
            capture_output=True, text=True, timeout=10
        )
        output = result.stdout.strip()
        if not output:
            return {"commits": 0, "files": [], "commit_msgs": []}

        lines = output.split("\n")
        files = []
        commits = 0
        commit_msgs = []
        for line in lines:
            if line.startswith("commit"):
                continue
            if line.startswith("initial vault"):
                continue
            if not line.strip():
                continue
            if "vault backup:" in line or line.endswith(".py") or line.endswith(".json"):
                if "vault backup:" in line:
                    continue
                if "daily_brief" in line or "weekly_report" in line or "setup_schedule" in line:
                    continue
            files.append(line)

        return {"commits": commits, "files": files, "commit_msgs": commit_msgs}
    except Exception as e:
        return {"commits": 0, "files": [], "commit_msgs": [], "error": str(e)}


def scan_vault():
    """扫描仓库各目录的文件数"""
    skip_dirs = {".git", ".agents", ".obsidian", "attachments"}
    stats = {}
    total_files = 0
    total_size = 0

    for entry in os.listdir(VAULT_PATH):
        entry_path = os.path.join(VAULT_PATH, entry)
        if entry.startswith(".") or entry in skip_dirs or not os.path.isdir(entry_path):
            continue

        md_files = []
        for root, dirs, files in os.walk(entry_path):
            for f in files:
                if f.endswith((".md", ".txt")):
                    fp = os.path.join(root, f)
                    sz = os.path.getsize(fp)
                    md_files.append((f, sz))
                    total_files += 1
                    total_size += sz

        stats[entry] = {
            "count": len(md_files),
            "size_kb": round(sum(s for _, s in md_files) / 1024),
            "files": [f for f, _ in md_files]
        }

    return stats, total_files, total_size


def generate_weekly_report():
    today = datetime.date.today()
    week_start = today - datetime.timedelta(days=today.weekday())
    week_end = week_start + datetime.timedelta(days=6)

    stats, total_files, total_size = scan_vault()
    git_stats = get_git_stats(days=7)

    lines = []
    lines.append("---")
    lines.append(f"created: {today.isoformat()}")
    lines.append("type: weekly-report")
    lines.append("---")
    lines.append("")
    lines.append(f"# 周报 {week_start.isoformat()} ~ {week_end.isoformat()}")
    lines.append("")
    lines.append("## 本周产出")
    lines.append("")
    lines.append(f"| 目录 | 笔记数 | 总大小 |")
    lines.append(f"|------|--------|--------|")
    for name in sorted(stats.keys()):
        s = stats[name]
        lines.append(f"| {name} | {s['count']} | {s['size_kb']}KB |")
    lines.append(f"| **合计** | **{total_files}** | **{round(total_size/1024)}KB** |")
    lines.append("")
    lines.append("## 本周变更")
    lines.append("")
    if git_stats["files"]:
        for f in git_stats["files"][:20]:
            lines.append(f"- {f}")
        if len(git_stats["files"]) > 20:
            lines.append(f"- ...及其他 {len(git_stats['files']) - 20} 个文件")
    else:
        lines.append("(暂无可追踪变更)")
    lines.append("")
    lines.append("## 下周计划")
    lines.append("- [ ] ")
    lines.append("")
    lines.append("## 回顾 & 思考")
    lines.append("")

    return "\n".join(lines) + "\n"


def main():
    os.makedirs(DIARY_DIR, exist_ok=True)
    note = generate_weekly_report()

    today = datetime.date.today()
    week_start = today - datetime.timedelta(days=today.weekday())
    filename = f"{week_start.isoformat()}_weekly.md"
    filepath = os.path.join(DIARY_DIR, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(note)

    print(f"周报已生成: {filepath}")


if __name__ == "__main__":
    main()
