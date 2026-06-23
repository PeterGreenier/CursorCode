#!/usr/bin/env python3
"""
每日算法练习 — 方案 A：通过 Cursor SDK 调用 Auto 模型自动解题。

用法:
  1. 复制 .env.example 为 .env，填入 CURSOR_API_KEY
  2. pip install -r requirements.txt
  3. python daily_algo.py              # 运行今日题目（默认每天 3 道）
  4. python daily_algo.py --count 5    # 今天跑 5 道
  5. python daily_algo.py --force      # 忽略今日已完成记录，强制再跑

环境变量:
  DAILY_COUNT=3      # 每天做题数量
  CURSOR_MODEL=default  # 模型，default = Auto 免费路由（不要用 composer-2.5 等付费模型）

Windows 定时任务: 运行 setup_task.ps1 注册每天自动执行。

方案 B（Cursor Automations）: 见 .cursor/daily-algo-automation.md
两套方案共用 problems.json / history.json，history 中 source 字段区分来源。
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import date, datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent
SOLUTIONS_DIR = WORKSPACE / "solutions"
LOGS_DIR = WORKSPACE / "logs"
HISTORY_FILE = WORKSPACE / "history.json"
PROBLEMS_FILE = WORKSPACE / "problems.json"
DEFAULT_DAILY_COUNT = 3
DEFAULT_MODEL = "default"  # Cursor 里的 Auto（免费路由，走 Auto+Composer 额度池）


def get_daily_count(cli_count: int | None) -> int:
    if cli_count is not None:
        return max(1, cli_count)
    env_val = os.environ.get("DAILY_COUNT", "").strip()
    if env_val.isdigit():
        return max(1, int(env_val))
    return DEFAULT_DAILY_COUNT


def get_model(cli_model: str | None) -> str:
    """解析模型 ID。default = Cursor 编辑器里的 Auto（免费路由）。"""
    raw = (cli_model or os.environ.get("CURSOR_MODEL", "") or DEFAULT_MODEL).strip()
    aliases = {
        "auto": "default",
        "Auto": "default",
        "free": "default",
    }
    return aliases.get(raw, raw)


def model_display_name(model_id: str) -> str:
    labels = {
        "default": "Auto（免费路由）",
        "composer-2.5": "Composer 2.5",
    }
    return labels.get(model_id, model_id)


def load_env() -> None:
    """从 .env 文件加载环境变量（若存在）。"""
    env_path = WORKSPACE / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def load_problems() -> list[dict]:
    with PROBLEMS_FILE.open(encoding="utf-8") as f:
        return json.load(f)


def load_history() -> dict:
    if not HISTORY_FILE.exists():
        return {"runs": []}
    with HISTORY_FILE.open(encoding="utf-8") as f:
        return json.load(f)


def save_history(history: dict) -> None:
    with HISTORY_FILE.open("w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def pick_today_problems(
    problems: list[dict], history: dict, count: int, force: bool
) -> list[dict]:
    today = date.today().isoformat()
    done_today_ids = {
        r["problem_id"]
        for r in history.get("runs", [])
        if r.get("date") == today and r.get("status") == "finished"
    }

    if not force:
        remaining = count - len(done_today_ids)
        if remaining <= 0:
            print(f"[跳过] 今天已完成 {len(done_today_ids)} 道题（目标 {count} 道）")
            print(f"  已完成: {', '.join(sorted(done_today_ids))}")
            print("如需再跑，加 --force 参数")
            return []
        need = remaining
        exclude_ids = done_today_ids
    else:
        need = count
        exclude_ids = set()

    done_ever = {
        r["problem_id"] for r in history.get("runs", []) if r.get("status") == "finished"
    }
    available = [p for p in problems if p["id"] not in exclude_ids]
    if not available:
        print("[跳过] 没有可选题目")
        return []

    never_done = [p for p in available if p["id"] not in done_ever]
    done_before = [p for p in available if p["id"] in done_ever]
    pool = never_done + done_before

    start = date.today().toordinal() % len(pool)
    ordered = pool[start:] + pool[:start]

    selected: list[dict] = []
    seen: set[str] = set()
    for problem in ordered:
        if problem["id"] in seen:
            continue
        selected.append(problem)
        seen.add(problem["id"])
        if len(selected) >= need:
            break

    return selected[:need]


def build_prompt(problem: dict) -> str:
    return f"""今天是算法练习日，请完成以下题目：

**{problem['title']}**（难度: {problem['difficulty']}）

{problem['prompt']}

额外要求：
- 代码要有清晰注释
- 只修改/创建 solutions/ 目录下的文件，不要动其他文件
- 完成后简要说明时间/空间复杂度
"""


async def run_all_problems(
    problems: list[dict], api_key: str, model_id: str
) -> list[tuple[dict, str, str | None]]:
    """逐题调用 AI，每道题使用独立的 Agent 会话。"""
    from cursor_sdk import CursorAgentError, LocalAgentOptions
    from cursor_sdk.asyncio import AsyncAgent, AsyncClient

    SOLUTIONS_DIR.mkdir(parents=True, exist_ok=True)
    results: list[tuple[dict, str, str | None]] = []

    try:
        async with await AsyncClient.launch_bridge(workspace=str(WORKSPACE)) as client:
            for index, problem in enumerate(problems, 1):
                print(f"\n[题目 {index}/{len(problems)}] {problem['title']} ({problem['id']})")
                print(f"[模型] {model_display_name(model_id)} ({model_id})")
                print("-" * 50)

                async with await AsyncAgent.create(
                    client=client,
                    api_key=api_key,
                    model=model_id,
                    local=LocalAgentOptions(cwd=str(WORKSPACE)),
                ) as agent:
                    run = await agent.send(build_prompt(problem))
                    result = await run.wait()
                    results.append((problem, result.status, result.result))
                    print(f"[完成] {problem['id']} — status={result.status}")
    except CursorAgentError as err:
        print(f"[错误] Agent 启动失败: {err.message} (retryable={err.is_retryable})")
        sys.exit(1)

    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="每日 Cursor 算法练习")
    parser.add_argument("--force", action="store_true", help="忽略今日已完成记录")
    parser.add_argument("--list", action="store_true", help="列出所有题目")
    parser.add_argument(
        "--count",
        type=int,
        default=None,
        help=f"今天做题数量（默认 {DEFAULT_DAILY_COUNT}，也可用 .env 的 DAILY_COUNT）",
    )
    parser.add_argument(
        "--model",
        default=None,
        help=f"模型 ID（默认 {DEFAULT_MODEL} = Auto 免费路由，也可用 .env 的 CURSOR_MODEL）",
    )
    args = parser.parse_args()

    load_env()

    problems = load_problems()
    if args.list:
        for i, p in enumerate(problems, 1):
            print(f"{i:2}. [{p['difficulty']:6}] {p['title']} ({p['id']})")
        return

    api_key = os.environ.get("CURSOR_API_KEY", "").strip()
    if not api_key:
        print("[错误] 请设置 CURSOR_API_KEY 环境变量，或在 .env 文件中配置")
        print("获取地址: https://cursor.com/dashboard/integrations")
        sys.exit(1)

    daily_count = get_daily_count(args.count)
    model_id = get_model(args.model)
    history = load_history()
    selected = pick_today_problems(problems, history, daily_count, args.force)
    if not selected:
        return

    today = date.today().isoformat()
    print(f"[开始] {today} — 今日目标 {daily_count} 道，本次运行 {len(selected)} 道")
    print(f"[模型] {model_display_name(model_id)} ({model_id})")

    results = asyncio.run(run_all_problems(selected, api_key, model_id))

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    has_error = False

    for problem, status, result_text in results:
        started_at = datetime.now().isoformat(timespec="seconds")
        log_file = LOGS_DIR / f"{today}_{problem['id']}.log"
        log_file.write_text(
            f"date: {today}\nproblem: {problem['id']}\nmodel: {model_id}\nsource: sdk\nstatus: {status}\n\n{result_text or ''}",
            encoding="utf-8",
        )

        run_record = {
            "date": today,
            "problem_id": problem["id"],
            "title": problem["title"],
            "model": model_id,
            "source": "sdk",
            "status": status,
            "started_at": started_at,
            "finished_at": datetime.now().isoformat(timespec="seconds"),
            "log_file": str(log_file.relative_to(WORKSPACE)),
        }
        history.setdefault("runs", []).append(run_record)

        if status == "error":
            has_error = True

    save_history(history)

    print("\n" + "=" * 50)
    print(f"[汇总] 完成 {len(results)} 道题")
    for problem, status, _ in results:
        print(f"  - {problem['title']} ({problem['id']}): {status}")
    print(f"[日志] {LOGS_DIR}")

    if has_error:
        sys.exit(2)


if __name__ == "__main__":
    main()
