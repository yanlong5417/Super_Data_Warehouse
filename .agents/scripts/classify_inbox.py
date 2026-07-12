#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
收件箱自动归类工具 v2
扫描 000-收件箱 中的 .md 文件，根据关键词匹配自动移入对应目录。
未匹配的文件留在收件箱。
"""

import os
import re
import shutil
import sys
from datetime import datetime

VAULT = r"E:\超级个体知识库"
INBOX = os.path.join(VAULT, "000-收件箱")
LOG_FILE = os.path.join(VAULT, "600-元知识", "归类日志.md")

# 归类规则：(目标目录, [关键词列表])
# 关键词匹配文件内容（不区分大小写）
RULES = [
    (r"100-领域\交易技术", [
        "MACD", "K线", "均线", "股票", "A股", "主力", "券商",
        "涨停", "跌停", "技术分析", "成交量", "RSI", "KDJ",
        "布林", "谐波", "Vegas", "大盘", "指数", "牛市", "熊市",
        "仓位", "止损", "止盈", "抄底", "逃顶", "死叉", "金叉",
        "缠论", "道氏", "波浪理论",
    ]),
    (r"100-领域\Web3", [
        "Web3", "比特币", "BTC", "以太坊", "ETH", "区块链",
        "NFT", "挖矿", "Depin", "元宇宙", "Token", "加密货币",
        "DEX", "DeFi", "Web 3.0", "SOL", "狗狗链", "BRC",
        "铭文", "空投", "跨链",
    ]),
    (r"100-领域\AI动漫制作", [
        "Stable Diffusion", "NovelAI", "ComfyUI", "AnimateDiff",
        "ControlNet", "LoRA", "AI绘画", "二次元", "动漫",
        "AI生成", "AIGC", "Runway", "Pika", "超分辨率",
        "AI视频", "文生图", "图生图", "大模型",
    ]),
    (r"300-资源\编程", [
        "Python", "JavaScript", "TypeScript", "GitHub", "开源",
        "程序员", "算法", "代码", "编程", "API", "前端",
        "后端", "数据库", "Docker", "机器学习", "深度学习",
        "React", "Vue", "Node", "Linux",
    ]),
    (r"200-项目", [
        "创业", "商业模式", "融资", "IP打造", "变现",
        "营销", "品牌", "产品", "商业",
    ]),
    (r"300-资源\课程", [
        "课程", "教程", "笔记", "学习笔记", "读书",
        "读后感", "书评",
    ]),
]


def classify_file(filepath: str) -> str:
    """返回目标目录的相对路径，None 表示无法归类"""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read().lower()

    filename = os.path.basename(filepath).lower()
    # 文件名 + 前 500 字符作为搜索范围
    search_text = filename + " " + content[:500]

    # 关键词匹配（统计命中数，取最高分）
    best_dest = None
    best_score = 0

    for dest, keywords in RULES:
        score = 0
        for kw in keywords:
            kw_lower = kw.lower()
            if kw_lower in filename:
                score += 3  # 文件名命中权重高
            cnt = search_text.count(kw_lower)
            score += cnt
        if score > best_score:
            best_score = score
            best_dest = dest

    if best_score >= 1:
        return best_dest
    return None


def log_move(ln: list, filename: str, src: str, dst: str):
    ln.append(f"| {filename} | {src} | {dst} |")


def main():
    os.makedirs(INBOX, exist_ok=True)

    files = [f for f in os.listdir(INBOX)
             if f.endswith(('.md', '.txt')) and not f.startswith('.')]
    if not files:
        print("收件箱为空，无需归类")
        return

    moved = []
    stayed = []
    log_entries = []

    for fname in files:
        fpath = os.path.join(INBOX, fname)
        if not os.path.isfile(fpath):
            continue

        dest_rel = classify_file(fpath)
        if dest_rel is None:
            stayed.append(fname)
            print(f"  待定: {fname}")
            continue

        dest_dir = os.path.join(VAULT, dest_rel)
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, fname)

        if os.path.exists(dest_path):
            base, ext = os.path.splitext(fname)
            dest_path = os.path.join(dest_dir, f"{base}_{datetime.now().strftime('%H%M%S')}{ext}")

        shutil.move(fpath, dest_path)
        moved.append(fname)
        log_entries.append((fname, "收件箱", dest_rel))
        print(f"  归类: {fname} -> {dest_rel}/")

    if log_entries:
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        log_line = f"\n### {date_str}\n| 文件 | 来源 | 去向 |\n|---|---|---|\n"
        for f, s, d in log_entries:
            log_line += f"| {f} | {s} | {d} |\n"
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_line)

    print(f"\n已归类: {len(moved)} 个文件")
    print(f"未匹配: {len(stayed)} 个文件 (留在收件箱)")
    if log_entries:
        print(f"日志: 600-元知识/归类日志.md")


if __name__ == "__main__":
    main()
