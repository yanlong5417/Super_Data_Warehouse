#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日早报生成器
每天生成一条 Obsidian 笔记，包含天气 + 热点资讯 + 今日待办
输出到 400-日记/YYYY-MM-DD.md

用法:
  python daily_brief.py

定时任务 (Windows):
  schtasks /create /tn "Obsidian每日早报" /tr "python daily_brief.py" /sc daily /st 08:00
"""

import datetime
import json
import os
import re
import urllib.parse
import urllib.request

VAULT_PATH = r"E:\超级个体知识库"
DIARY_DIR = os.path.join(VAULT_PATH, "400-日记")

WEEKDAYS_CN = {
    0: "星期一", 1: "星期二", 2: "星期三", 3: "星期四",
    4: "星期五", 5: "星期六", 6: "星期日"
}


def get_weather(city=None):
    """从 wttr.in 获取天气"""
    if city is None:
        city = "上海"
    try:
        url = f"https://wttr.in/{urllib.parse.quote(city)}?format=j1"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        })
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read().decode('utf-8'))

        current = data['current_condition'][0]
        desc = current['weatherDesc'][0]['value']
        temp = current['temp_C']
        feels = current['FeelsLikeC']
        humidity = current['humidity']
        wind = current['windspeedKmph']

        return f"{desc}, {temp}C (体感 {feels}C), 湿度 {humidity}%, 风速 {wind}km/h"
    except Exception as e:
        return f"获取天气失败: {e}"


def get_hot_news():
    """从多个 RSS 源获取热点资讯"""
    headlines = []

    for source, url in [
        ("36氪", "https://36kr.com/feed"),
        ("阮一峰", "https://www.ruanyifeng.com/blog/atom.xml"),
    ]:
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0'
            })
            resp = urllib.request.urlopen(req, timeout=10)
            html = resp.read().decode('utf-8', errors='replace')
            # Extract article titles from RSS XML
            titles = re.findall(r'<title[^>]*><!\[CDATA\[(.*?)\]\]></title>', html)
            if not titles:
                titles = re.findall(r'<title[^>]*>(.*?)</title>', html)
            for t in titles[1:4]:  # skip feed title
                t = t.strip()
                if len(t) > 5:
                    headlines.append(f"- [{source}] {t}")
        except:
            pass

    return headlines[:6]


def generate_note():
    """生成日记笔记内容"""
    today = datetime.date.today()
    date_str = today.strftime("%Y-%m-%d")
    weekday = WEEKDAYS_CN[today.weekday()]

    weather = get_weather()
    news = get_hot_news()

    lines = []
    lines.append("---")
    lines.append(f"created: {date_str}")
    lines.append(f"type: daily")
    lines.append("---")
    lines.append("")
    lines.append(f"# {date_str} {weekday}")
    lines.append("")
    lines.append("## 天气")
    lines.append(weather)
    lines.append("")
    lines.append("## 今日待办")
    lines.append("- [ ] ")
    lines.append("")
    lines.append("## 热点资讯")
    if news:
        for h in news:
            lines.append(h)
    else:
        lines.append("- (暂无资讯)")
    lines.append("")
    lines.append("## 笔记 / 想法")
    lines.append("")
    lines.append("")
    lines.append("## 今日总结")
    lines.append("")

    return "\n".join(lines) + "\n", date_str


def main():
    os.makedirs(DIARY_DIR, exist_ok=True)
    note, date_str = generate_note()

    filepath = os.path.join(DIARY_DIR, f"{date_str}.md")

    if os.path.exists(filepath):
        print(f"早报已存在: {filepath}")
        return

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(note)

    print(f"早报已生成: {filepath}")


if __name__ == "__main__":
    main()
