# 每日算法练习 — Cursor Automation 规则

本文件与 `daily_algo.py`（方案 A：SDK 脚本）共用同一套选题与记录逻辑。
Automation 运行时必须严格遵循本文，以保证与脚本结果一致、避免重复做题。

---

## Automations 配置（复制到 Cursor）

在 **Settings → Automations → New automation** 中填写：

| 字段 | 值 |
|------|-----|
| Name | Daily Algo (Automation) |
| Trigger | 每天 9:30（cron: `30 9 * * *`） |
| Runtime | **Local**（必须本地，才能读写 `history.json`） |
| Model | Auto |
| Repository | 本仓库 |

**Instructions（整段复制）：**

```
你是每日算法练习助手。请先完整阅读 .cursor/daily-algo-automation.md，严格按其中规则执行。

步骤概要：
1. 读取 problems.json；若 history.json 不存在则视为 {"runs": []}
2. 检查今天是否已完成 3 道题（history 中 date=今天 且 status=finished）
3. 若已满 3 道，汇报已完成题目列表后结束，不要做题
4. 否则按文档中的选题算法选出剩余题数，在同一对话中逐题完成
5. 每题：写 solutions/、写 logs/、追加 history.json（source 填 "automation"）
6. 全部完成后输出汇总

只修改 solutions/、logs/、history.json；不要改其他文件。
```

> 建议将 Windows 计划任务（方案 A）设在 9:00，Automation 设在 9:30，避免同时运行。

---

## 常量

| 名称 | 值 |
|------|-----|
| 每日目标题数 `DAILY_COUNT` | 3 |
| 题目列表 | `problems.json` |
| 历史记录 | `history.json` |
| 解答目录 | `solutions/` |
| 日志目录 | `logs/` |
| 记录来源标识 | `"automation"` |

---

## 1. 检查今日是否已完成

1. 取今天日期 `today`，格式 `YYYY-MM-DD`（本地时区）。
2. 从 `history.json` 的 `runs` 数组中，统计满足以下条件的记录数：
   - `date == today`
   - `status == "finished"`
3. 记这些记录的 `problem_id` 集合为 `done_today_ids`。
4. 若 `len(done_today_ids) >= DAILY_COUNT`（即 ≥ 3）：
   - **停止**，输出：`今天已完成 N 道题，无需继续。已完成: <id 列表>`
   - 不要选题，不要写文件。

---

## 2. 选题算法（与 daily_algo.py 一致）

设 `need = DAILY_COUNT - len(done_today_ids)`（本次还需完成的题数）。

### 2.1 排除今日已完成的题

`exclude_ids = done_today_ids`

### 2.2 历史完成集合

`done_ever` = 所有 `history.runs` 中 `status == "finished"` 的 `problem_id` 集合。

### 2.3 构建候选池

```
available = problems.json 中 id 不在 exclude_ids 的题目
never_done = available 中 id 不在 done_ever 的题目
done_before = available 中 id 在 done_ever 的题目
pool = never_done + done_before   # 未做过的题优先
```

若 `pool` 为空，停止并报告「没有可选题目」。

### 2.4 按日期轮转排序

```
start = today 的 ordinal 日期值 % len(pool)
ordered = pool[start:] + pool[:start]
```

### 2.5 选取题目

从 `ordered` 顺序取题，去重，直到选满 `need` 道或 `ordered` 耗尽。

---

## 3. 逐题完成（同一对话内连续做）

对每道选中的题，按顺序完成：

### 3.1 题目要求

使用 `problems.json` 中该题的 `title`、`difficulty`、`prompt`，并附加：

- 代码要有清晰注释
- 只修改/创建 `solutions/` 目录下的文件
- 完成后简要说明时间/空间复杂度
- 解答文件需包含 `if __name__ == "__main__"` 的简单测试（若题目 prompt 已要求则遵循 prompt）

### 3.2 写日志

路径：`logs/{today}_{problem_id}.log`

内容格式：

```
date: {today}
problem: {problem_id}
model: default
source: automation
status: finished

{解题说明、复杂度分析等正文}
```

若某题失败，`status` 改为 `error`，正文写错误原因。

### 3.3 更新 history.json

每完成一题，向 `runs` 数组 **追加** 一条记录（不要覆盖已有记录）：

```json
{
  "date": "YYYY-MM-DD",
  "problem_id": "题目 id",
  "title": "题目标题",
  "model": "default",
  "source": "automation",
  "status": "finished",
  "started_at": "ISO8601 本地时间",
  "finished_at": "ISO8601 本地时间",
  "log_file": "logs/YYYY-MM-DD_problem_id.log"
}
```

`history.json` 顶层结构：

```json
{
  "runs": [ ... ]
}
```

若文件不存在，创建 `{"runs": []}` 后再追加。

---

## 4. 结束汇总

全部题目处理完后，输出简短汇总：

- 今天日期
- 本次完成的题目列表（id + title + status）
- 日志目录 `logs/`
- 今日累计完成题数（含本次之前已完成的）

---

## 5. 禁止事项

- 不要修改 `problems.json`、`daily_algo.py`、`.env` 及其他非允许文件
- 不要删除 `history.json` 中的历史记录
- 不要在今日已满 3 道 finished 时强制加题（除非用户在本对话中明确要求 `--force` 等价行为）
- 不要使用 Cloud Agent 运行本 Automation（Cloud 无法读取本地 `history.json`）

---

## 两套方案并存说明

| 方案 | 触发方式 | source 字段 |
|------|----------|-------------|
| A — SDK 脚本 | `python daily_algo.py` 或 Windows 计划任务 | `sdk` |
| B — Automation | Cursor Automations 定时 | `automation` |

两边共用 `history.json`：任一方先跑满 3 道，另一方会自动跳过。
