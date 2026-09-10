# tests/ — 自动化测试

本目录保存 pytest 自动化测试。被测代码由 `conftest.py` 在测试启动时把 `module1/subject/` 加入 `sys.path`，测试文件直接 `import croniter`。

## 文件

| 文件 | 作用 |
|---|---|
| `conftest.py` | 路径注入；不定义公共 fixture（用例数据由 testdata 账本提供） |
| `test_croniter.py` | 参数化用例 + 5 条专项自动化检查 |

## 用例段与测试函数映射

| 用例编号 | 测试函数 | 方法 |
|---|---|---|
| CRON-UT-001—012 | `test_parser_equivalence` | 等价类、异常 |
| CRON-UT-013—024 | `test_next_boundaries` | 边界值 |
| CRON-UT-025—032 | `test_scenarios` | 场景法、状态转换 |
| CRON-UT-033—036 | `test_regressions` | 回归（带 `@pytest.mark.regression`） |

标记（`smoke`、`boundary`、`regression`、`scenario`）定义于 `module1/pytest.ini`。

## 运行

在 `module1` 目录下执行：

```bash
.venv/Scripts/python.exe -m pytest -q                         # 全量
.venv/Scripts/python.exe -m pytest -q -m regression           # 仅历史缺陷回归
.venv/Scripts/python.exe -m coverage run --branch -m pytest -q
.venv/Scripts/python.exe -m coverage report -m
```

当前基线结果：41 passed；branch coverage 55%（详见 `module1/README.md` 与 `requirements_traceability.md`）。

## 新增用例的步骤

1. 在 `testdata/cron_cases.json` 添加记录（编号按 `CRON-UT-XXX` 连续，不重号）；
2. 确认该记录 `category` 对应的参数化函数，或新增测试函数；
3. 在 `requirements_traceability.md` 登记函数名与编号范围；
4. 运行全量测试，同步更新覆盖率数字与附录一清单。

测试不得依赖网络、数据库或外部服务。
