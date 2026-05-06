"""
重要公告检测 — 基于 Web 搜索关键词识别 HIGH/MED 利空。

使用 gsk web_search（如果可用）或自定义搜索引擎适配。
"""
from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime, timedelta

# 关键词分级
KEYWORDS_HIGH = [
    "减持股份", "减持计划", "减持资产", "减股", "拟转让",
    "立案", "被调查", "证监会", "警示",
    "业绩预减", "业绩老", "诉讼",
]
KEYWORDS_MED = [
    "解禁", "限售股", "收购", "重组", "股东大会",
    "定增", "发行", "业绩预告", "终止", "处罚",
    "调查", "震荡", "出售", "终止",
]


def _is_within_days(date_str: str, days: int) -> bool:
    """判断 'X days ago' / 'X hours ago' / 'Apr 17, 2026' 是否在 days 内"""
    if not date_str:
        return False
    ds_low = str(date_str).lower().strip()
    if "ago" in ds_low:
        digits = "".join(c for c in date_str if c.isdigit())
        if not digits:
            return False
        try:
            n = int(digits)
        except ValueError:
            return False
        if "hour" in ds_low or "minute" in ds_low:
            return True
        if "day" in ds_low:
            return n <= days
        if "week" in ds_low:
            return n * 7 <= days
        if "month" in ds_low:
            return n * 30 <= days
        if "year" in ds_low:
            return False
        return n <= days
    # 尝试解析 ISO / 英文日期
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%b %d, %Y"):
        try:
            d = datetime.strptime(date_str[:11].strip(), fmt)
            return 0 <= (datetime.now() - d).days <= days
        except ValueError:
            continue
    return False


def _classify_title(title: str) -> tuple[str, str]:
    """识别公告等级 (HIGH/MED/LOW) 和触发关键词"""
    for kw in KEYWORDS_HIGH:
        if kw in title:
            return "HIGH", kw
    for kw in KEYWORDS_MED:
        if kw in title:
            return "MED", kw
    return "LOW", ""


def _gsk_search(query: str, timeout: int = 20) -> list[dict]:
    """通过 gsk CLI 搜索（OpenClaw/Hermes 环境提供）"""
    if not shutil.which("gsk"):
        return []
    try:
        r = subprocess.run(
            ["gsk", "search", query, "--output", "json"],
            capture_output=True, text=True, timeout=timeout,
        )
        if r.returncode != 0 or not r.stdout:
            return []
        res = json.loads(r.stdout)
        data = res.get("data", res) if isinstance(res, dict) else {}
        return data.get("organic_results") or res.get("organic_results") or []
    except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception):
        return []


def fetch_announcements(code: str, days: int = 14, max_results: int = 6) -> list[dict]:
    """拉取个股近 N 天重要公告。返回 list of dict {date, title, level, tag, url}"""
    out: list[dict] = []
    seen_titles = set()

    queries = [
        f"{code} 减持 计划",
        f"{code} 业绩 预告 OR 预减",
        f"{code} 解禁 限售股",
        f"{code} 处罚 OR 调查 OR 警示",
    ]

    for q in queries:
        for item in _gsk_search(q)[:8]:
            title = item.get("title", "")
            if not title or title in seen_titles:
                continue
            level, tag = _classify_title(title)
            if level == "LOW":
                continue
            date_str = str(item.get("date", "")).strip()
            if not _is_within_days(date_str, days):
                continue
            out.append({
                "date": date_str,
                "title": title,
                "level": level,
                "tag": tag,
                "url": item.get("link", ""),
            })
            seen_titles.add(title)

    # HIGH 排前
    out.sort(key=lambda x: 0 if x["level"] == "HIGH" else 1)
    return out[:max_results]
