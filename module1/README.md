# 模块一：测试基础实践

本目录保存基于 `croniter` 6.2.2 的测试基础实践材料。测试对象是 Python 定时表达式解析与迭代库；`subject/croniter/` 用于保存固定版本的被测源码及来源说明，`tests/` 保存自动化测试，`testdata/` 保存用例数据，`testcases/`、`defects/`、`reports/` 分别保存课程附录一、附录二和附录三的交付文件。

## 环境与运行

建议使用 Python 3.10 或更高版本，并在 `module1` 目录执行。被测源码运行时依赖 `python-dateutil`，已与测试工具一起列入 `requirements-dev.txt`：

```bash
python -m venv .venv
source .venv/bin/activate       # Windows PowerShell：.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m coverage run --branch -m pytest
python -m coverage report -m
```

测试不得依赖网络、数据库或外部服务。当前测试集已验证 43 条 pytest 用例通过；branch coverage 实测总覆盖率为 57%，低于原计划的 85% 目标。该数字仅反映当前测试集结果，后续扩充用例后需重新测量。

## 目录约定

```text
module1/
├── subject/croniter/       # croniter 6.2.2 基线源码和来源说明
├── tests/                  # pytest 测试代码
├── testdata/               # JSON 等测试数据
├── testcases/              # 附录一：测试用例清单
├── defects/                # 附录二：缺陷报告
├── reports/                # 附录三：模块一测试报告
├── requirements_traceability.md
├── requirements-dev.txt
└── README.md
```

## 用例、需求和缺陷编号

- 测试用例编号采用 `CRON-UT-001` 起始的连续编号；课程要求不少于 30 条，当前清单用例 43 条（满足要求；012 已删除、026—032 重复用例已去重、036 已删除；原 5 条专项检查并入 041—050，另新增 051—052），最终数量以清单和测试收集结果为准。
- 每条用例在 `testdata/cron_cases.json`（如存在）中记录输入、预期和设计方法，并在 Excel 的“备注”中标注等价类、边界值、场景法或异常测试。
- pytest 测试函数通过参数化数据中的 `case_id` 与用例关联；函数名应在 `requirements_traceability.md` 中登记。
- 历史缺陷编号采用 `CRON-D-001` 至 `CRON-D-003`。缺陷报告记录基线版本、复现步骤、日志、根因、修复提交和回归用例；没有证据的缺陷不得标记为已关闭。

## 基线、复现与修复

基线固定为上游 `croniter` 6.2.2；来源 URL、版本和校验信息以仓库中实际提交的来源说明或报告记录为准。历史缺陷复现应先在基线状态执行并保存输出，再在独立修复分支修改源码，最后用对应验证用例（CRON-UT-033—035，已归入等价类/边界值类）验证。

推荐的本地操作顺序：

```bash
git switch --detach <croniter-6.2.2-baseline>
python -m pytest -q
git switch -c fix/croniter-issue-<编号>
# 修改 subject/croniter/ 后重新执行全量验证
python -m pytest -q
```

`<croniter-6.2.2-baseline>` 和 `<编号>` 是占位符，必须替换为仓库中实际存在的引用和缺陷编号。每组逻辑修改单独提交到本地 Git；除非用户明确要求，不执行 `git push`。

## AI 使用披露

本项目允许使用 AI 工具辅助资料检索、测试设计、代码草拟和文档校对。提交报告时应说明使用的工具、辅助环节、人工复核方式，以及最终由小组成员运行和确认的命令。AI 生成内容不能替代上游 issue/CHANGELOG、测试日志或修复 diff 等可核验证据。

## 交付位置

- 测试用例清单：`module1/testcases/`
- 缺陷报告：`module1/defects/`
- 模块一测试报告：`module1/reports/`
- 需求—用例—实现—缺陷映射：`module1/requirements_traceability.md`

报告和附录应保留实际运行命令、日期及覆盖率输出；当前已验证结果为 43 passed、branch coverage 57%。
