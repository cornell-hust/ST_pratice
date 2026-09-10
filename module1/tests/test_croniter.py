import pytest
from datetime import datetime, timezone, timedelta
from croniter import croniter, croniter_range, CroniterBadCronError
import json
from pathlib import Path

# 从"账本"（testdata/cron_cases.json）读取全部用例数据：
# 每条用例自带 id、category，以及该用例需要的输入（expr/start）和预期（valid/expected/expect）。
CASES = json.loads((Path(__file__).parents[1] / "testdata" / "cron_cases.json").read_text())


def _dt(s):
    """把账本里的 ISO 时间字符串（如 "2024-01-01T00:00:00+00:00"）转成 datetime 对象"""
    return datetime.fromisoformat(s)


def _cases(category):
    """按设计方法（category）从账本中筛选用例"""
    return [c for c in CASES if c["category"] == category]


# 四组参数化数据全部来自账本，测试代码不再写死任何一条用例的输入或预期
EQUIVALENCE = _cases("equivalence")   # 12 条：合法/非法表达式等价类
BOUNDARY = _cases("boundary")         # 12 条：分钟/小时/日期/闰年/周日等边界值
SCENARIO = _cases("scenario")         # 5 条：连续迭代场景
MATCH = _cases("match")               # 6 条：匹配/范围/合法性专项检查（原独立测试函数并入）


@pytest.mark.parametrize("case", EQUIVALENCE, ids=[c["id"] for c in EQUIVALENCE])
def test_parser_equivalence(case):
    start = datetime(2024, 1, 1, tzinfo=timezone.utc)
    if case["valid"]:                                  # 账本说"应该合法"
        assert croniter(case["expr"], start).get_next(datetime)
    else:                                              # 账本说"应该非法"
        with pytest.raises(CroniterBadCronError):      # 必须抛出标准错误
            croniter(case["expr"], start)


@pytest.mark.parametrize("case", BOUNDARY, ids=[c["id"] for c in BOUNDARY])
def test_next_boundaries(case):
    if case.get("start") == "object":                  # 异常输入：非法起始类型
        with pytest.raises((TypeError, ValueError)):
            croniter(case["expr"], object()).get_next()
        return
    start = _dt(case["start"])                         # 起始时间来自账本
    if case.get("tz"):                                 # ZoneInfo 时区（夏令时边界）
        from zoneinfo import ZoneInfo
        start = start.replace(tzinfo=ZoneInfo(case["tz"]))
    if case.get("ret_type") == "float":                # 默认返回类型：秒级时间戳
        assert isinstance(croniter(case["expr"], start).get_next(), float)
        return
    expected = _dt(case["expected"])                   # 预期结果来自账本
    # 034/035 等月份/周日低界用例需按起点展开步进，才能在修复前基线版本上暴露对应历史缺陷
    expand = case.get("expand", False)
    assert croniter(case["expr"], start, expand_from_start_time=expand).get_next(datetime) == expected


@pytest.mark.parametrize("case", SCENARIO, ids=[c["id"] for c in SCENARIO])
def test_scenarios(case):
    start = _dt(case["start"])
    it = croniter(case["expr"], start)
    a, b = it.get_next(datetime), it.get_next(datetime)   # 连续取两次
    assert b - a == timedelta(minutes=10)                 # 断言：间隔必须正好是步长 10 分钟
    assert croniter(case["expr"], start).get_prev(datetime) < start  # 往回找必须早于起点


@pytest.mark.parametrize("case", MATCH, ids=[c["id"] for c in MATCH])
def test_match_and_ranges(case):
    """匹配/范围/合法性专项检查（原 5 个独立测试函数已并入账本参数化）"""
    if case["check"] == "match":                      # 时刻匹配
        assert croniter.match(case["expr"], _dt(case["start"])) == case["expected"]
    elif case["check"] == "match_range":              # 时段匹配
        assert croniter.match_range(case["expr"], _dt(case["start"]), _dt(case["end"])) == case["expected"]
    elif case["check"] == "range":                    # 窗口内触发点个数
        assert len(list(croniter_range(_dt(case["start"]), _dt(case["end"]), case["expr"]))) == case["count"]
    else:                                             # is_valid 合法性校验
        assert croniter.is_valid(case["expr"], second_at_beginning=case.get("second_at_beginning", False)) == case["expected"]
