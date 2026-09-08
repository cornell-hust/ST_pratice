import pytest
from datetime import datetime, timezone, timedelta
from croniter import croniter, croniter_range, CroniterBadCronError
import json
from pathlib import Path
CASES=json.loads((Path(__file__).parents[1]/"testdata/cron_cases.json").read_text())

@pytest.mark.parametrize('case,expr,valid', [
 (CASES[0],'* * * * *',True),(CASES[1],'*/5 * * * *',True),(CASES[2],'0 0 * * *',True),(CASES[3],'1-5 * * * *',True),
 (CASES[4],'1,15,30 * * * *',True),(CASES[5],'0 9-17 * * 1-5',True),(CASES[6],'@daily',True),(CASES[7],'0 0 1 1 *',True),
 (CASES[8],'bad expr',False),(CASES[9],'* * * *',False),(CASES[10],'60 * * * *',False),(CASES[11],'*/0 * * * *',False)])
def test_parser_equivalence(case,expr,valid):
    start=datetime(2024,1,1,tzinfo=timezone.utc)
    if valid: assert croniter(expr,start).get_next(datetime)
    else:
        expected = CroniterBadCronError
        with pytest.raises(expected):
            croniter(expr, start)

@pytest.mark.parametrize('case,expr,start,expected', [
 (CASES[12],'* * * * *',datetime(2024,1,1,0,0,tzinfo=timezone.utc),datetime(2024,1,1,0,1,tzinfo=timezone.utc)),
 (CASES[13],'0 * * * *',datetime(2024,1,1,0,0,tzinfo=timezone.utc),datetime(2024,1,1,1,0,tzinfo=timezone.utc)),
 (CASES[14],'0 0 1 * *',datetime(2024,1,2,tzinfo=timezone.utc),datetime(2024,2,1,tzinfo=timezone.utc)),
 (CASES[15],'0 0 29 2 *',datetime(2023,1,1,tzinfo=timezone.utc),datetime(2024,2,29,tzinfo=timezone.utc)),
 (CASES[16],'59 23 31 12 *',datetime(2024,1,1,tzinfo=timezone.utc),datetime(2024,12,31,23,59,tzinfo=timezone.utc)),
 (CASES[17],'0 0 * * 0',datetime(2024,1,6,tzinfo=timezone.utc),datetime(2024,1,7,tzinfo=timezone.utc)),
 (CASES[18],'0 0 1 1 *',datetime(2024,1,2,tzinfo=timezone.utc),datetime(2025,1,1,tzinfo=timezone.utc)),
 (CASES[19],'*/15 * * * *',datetime(2024,1,1,0,1,tzinfo=timezone.utc),datetime(2024,1,1,0,15,tzinfo=timezone.utc)),
 (CASES[20],'0 0 1 * *',datetime(2024,1,1,tzinfo=timezone.utc),datetime(2024,2,1,tzinfo=timezone.utc)),
 (CASES[21],'0 0 * * 6',datetime(2024,1,1,tzinfo=timezone.utc),datetime(2024,1,6,tzinfo=timezone.utc)),
 (CASES[22],'0 12 * * *',datetime(2024,1,1,tzinfo=timezone.utc),datetime(2024,1,1,12,tzinfo=timezone.utc)),
 (CASES[23],'0 0 1 1 *',datetime(2023,12,31,tzinfo=timezone.utc),datetime(2024,1,1,tzinfo=timezone.utc)),])
def test_next_boundaries(case,expr,start,expected):
    assert croniter(expr,start).get_next(datetime)==expected

@pytest.mark.parametrize('case',CASES[24:32])
def test_scenarios(case,base_dt):
    it=croniter('*/10 * * * *',base_dt)
    a,b=it.get_next(datetime),it.get_next(datetime)
    assert b-a==timedelta(minutes=10)
    assert croniter('*/10 * * * *',base_dt).get_prev(datetime)<base_dt

@pytest.mark.parametrize('case,expr',[(CASES[32],'5-5/0 * * * *'),(CASES[33],'0 0 * * 0'),(CASES[34],'0 0 1 */2 *'),(CASES[35],'0 0 * * *')])
@pytest.mark.regression
def test_regressions(case,expr):
    if case['id']=='CRON-UT-033':
        with pytest.raises((CroniterBadCronError, ValueError)):
            croniter(expr,datetime(2024,1,1,tzinfo=timezone.utc))
    else:
        it=croniter(expr,datetime(2024,1,1,tzinfo=timezone.utc),expand_from_start_time=True)
        assert it.get_next(datetime)

def test_match_and_range():
    dt=datetime(2024,1,1,tzinfo=timezone.utc)
    assert croniter.match('0 0 * * *',dt)
    assert not croniter.match('0 0 * * *',dt+timedelta(minutes=1))
    vals=list(croniter_range(dt,dt+timedelta(minutes=3),'* * * * *'))
    assert len(vals)==4

def test_match_range_and_is_valid():
    dt=datetime(2024,1,1,tzinfo=timezone.utc)
    assert croniter.is_valid('0 0 * * *')
    assert not croniter.is_valid('not cron')
    assert croniter.match_range('0 0 * * *', dt, dt+timedelta(days=1))
    assert not croniter.match_range('0 1 * * *', dt, dt+timedelta(minutes=30))

def test_return_types_seconds_and_year():
    dt=datetime(2024,1,1,tzinfo=timezone.utc)
    assert isinstance(croniter('*/30 * * * * *',dt).get_next(), float)
    assert croniter.is_valid('0 0 0 1 1 *', second_at_beginning=True)

def test_timezone_dst_zoneinfo():
    from zoneinfo import ZoneInfo
    tz=ZoneInfo('America/New_York')
    start=datetime(2024,3,9,0,0,tzinfo=tz)
    nxt=croniter('0 2 * * *',start).get_next(datetime)
    assert nxt.tzinfo == tz
    assert nxt.day in (9, 10)

def test_exception_inputs():
    with pytest.raises((TypeError, ValueError)): croniter('* * * * *', object()).get_next()
    with pytest.raises(CroniterBadCronError): croniter('0 0 32 * *', datetime.now(timezone.utc))
