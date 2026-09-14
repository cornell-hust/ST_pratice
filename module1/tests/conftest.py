import sys
from pathlib import Path

# pytest 启动时先执行本文件：把被测源码目录 subject/ 加入模块搜索路径，
# 这样所有测试文件里的 `import croniter` 都能找到被测代码。
MODULE_ROOT = Path(__file__).parents[1]
SUBJECT_ROOT = MODULE_ROOT / 'subject'
sys.path.insert(0, str(SUBJECT_ROOT))

# 用例数据统一由测试文件从 testdata/cron_cases.json 读取（"数据单一来源"），
# 本文件不再重复加载；各用例的起始时间也由账本自带，无需公共 fixture。
