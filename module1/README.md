# 模块一：测试基础实践

本目录保存基于 `croniter` 6.2.2 的测试基础实践材料。测试对象是 Python 定时表达式解析与迭代库。

## 目录约定

```text
module1/
├── subject/                       # 被测源码（含本地对 3 个历史缺陷的修复）
├── baseline/                      # 被测源码 6.2.2 原版快照，用于缺陷复现对照
├── tests/                         # pytest 测试代码
├── testdata/                      # 用例账本 cron_cases.json
├── testcases/                     # 附录一：测试用例清单
├── defects/                       # 附录二：缺陷报告与复现证据
├── reports/                       # 附录三：模块一测试报告
├── presentation/                  # 成果汇报 PPT、演示视频与录制材料
├── pytest.ini                     # pytest 配置与标记
├── requirements-dev.txt           # 测试依赖
├── requirements_traceability.md   # 需求 → 用例 → 实现 → 缺陷 追踪矩阵
└── README.md
```

各子目录另有 `README.md` 说明其职责。

## 环境与运行

建议使用 Python 3.10 或更高版本，并在 `module1` 目录下执行。被测源码的运行时依赖为 `python-dateutil`，已与测试工具一起列入 `requirements-dev.txt`：

```bash
python -m venv .venv
source .venv/bin/activate        # Windows：.venv/Scripts/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q              # 期望 40 passed
```

测试不得依赖网络、数据库或外部服务。

## 用例、需求和缺陷编号

- **测试用例**编号采用 `CRON-UT-001` 起始的连续编号，当前 **40 条**（课程要求不少于 30 条）。编号区间为 `CRON-UT-001—052`，其中 012、015、023、026—032、036、041 已于用例去重与精简中删除，故编号不连续但**不重号**。
- 每条用例的输入、预期与设计方法统一记录在 `testdata/cron_cases.json`（账本），并在附录一清单的"备注"列标注等价类、边界值、场景法或异常测试。
- pytest 测试函数通过 `pytest.mark.parametrize` 从账本加载用例，函数名与编号区间的对应关系登记在 `requirements_traceability.md`。
- **历史缺陷**编号采用 `CRON-D-001` 至 `CRON-D-003`。缺陷报告记录基线版本、复现步骤、日志、根因、修复提交和回归用例；**没有复现输出的缺陷不得标记为"已关闭"**。

## 基线与缺陷复现

- `subject/` —— **修复后**的被测源码，`tests/conftest.py` 在测试启动时把该目录注入 `sys.path`。
- `baseline/` —— 上游 croniter **6.2.2 原版**快照，来源与版本记录见 `baseline/SOURCE.md`。

复现历史缺陷、验证修复效果时，切换注入路径即可：

```bash
PYTHONPATH=baseline .venv/Scripts/python.exe presentation/演示-缺陷复现.py   # 三个缺陷原形毕露
PYTHONPATH=subject  .venv/Scripts/python.exe presentation/演示-缺陷复现.py   # 三个缺陷全部修复
```

> ⚠️ **注意**：`tests/conftest.py` 固定注入 `subject/`，因此 `PYTHONPATH=baseline python -m pytest -q` **不会**改变被测版本（pytest 仍会全部通过）。若要整套用例跑在基线上，需临时把 `tests/conftest.py` 第 7 行的 `'subject'` 改为 `'baseline'`——此时 40 条用例中有 **3 条失败**（CRON-UT-033／034／035），与三个缺陷一一对应；改回后应恢复 40 passed。

## 交付位置

| 附录 | 交付物 | 位置 |
| --- | --- | --- |
| 附录一 | 测试用例清单（40 条） | `module1/testcases/测试用例清单.xlsx` |
| 附录二 | 缺陷报告（CRON-D-001—003） | `module1/defects/缺陷报告.doc` |
| 附录三 | 测试报告（模块一） | `module1/reports/测试报告（模块一）.docx` |
| — | 成果汇报 PPT（12 页） | `module1/presentation/模块一成果汇报.pptx` |
| — | 演示视频 | `module1/presentation/` |

报告和附录应保留实际运行命令、日期及执行输出；当前已验证结果为 **40 passed**。
