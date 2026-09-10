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
    start = _dt(case["start"])                         # 起始时间来自账本
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


def test_match_and_range():
    dt = datetime(2024, 1, 1, tzinfo=timezone.utc)
    assert croniter.match('0 0 * * *', dt)
    assert not croniter.match('0 0 * * *', dt + timedelta(minutes=1))
    vals = list(croniter_range(dt, dt + timedelta(minutes=3), '* * * * *'))
    assert len(vals) == 4


def test_match_range_and_is_valid():
    dt = datetime(2024, 1, 1, tzinfo=timezone.utc)
    assert croniter.is_valid('0 0 * * *')
    assert not croniter.is_valid('not cron')
    assert croniter.match_range('0 0 * * *', dt, dt + timedelta(days=1))
    assert not croniter.match_range('0 1 * * *', dt, dt + timedelta(minutes=30))


def test_return_types_seconds_and_year():
    dt = datetime(2024, 1, 1, tzinfo=timezone.utc)
    assert isinstance(croniter('*/30 * * * * *', dt).get_next(), float)
    assert croniter.is_valid('0 0 0 1 1 *', second_at_beginning=True)


def test_timezone_dst_zoneinfo():
    from zoneinfo import ZoneInfo
    tz = ZoneInfo('America/New_York')
    start = datetime(2024, 3, 9, 0, 0, tzinfo=tz)
    nxt = croniter('0 2 * * *', start).get_next(datetime)
    assert nxt.tzinfo == tz
    assert nxt.day in (9, 10)


def test_exception_inputs():
    with pytest.raises((TypeError, ValueError)):
        croniter('* * * * *', object()).get_next()
    with pytest.raises(CroniterBadCronError):
        croniter('0 0 32 * *', datetime.now(timezone.utc))
