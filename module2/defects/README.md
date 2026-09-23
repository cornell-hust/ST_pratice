# defects/ — 缺陷清单与证据

> **入库说明**：生成脚本 `tools/dump_defect_evidence.py` 已入库，下方命令可直接运行；
> 产物 `NL2C-D-00*-repro.txt` 不入库（可由该脚本一键重新生成）。入库范围见
> [`module2/README.md`](../README.md) 的「入库范围」一节。

| 文件 | 作用 |
| --- | --- |
| `附录2：缺陷报告模板.doc` | **课程模板**（只读）：需在其上填写缺陷报告 |
| `缺陷报告填充.md` | **逐字段填充稿**：模板中每一个空位该写什么，含两轮测试口径、⚠️待补项与🚫无法填写项标注 |
| `缺陷清单素材.md` | 缺陷数据素材：按附录二模板的缺陷表字段整理，含根因与反思要点 |
| `NL2C-D-001-repro.txt` | 非确定性格式漂移：v1 复现 / v2 修复的逐步原始输出 |
| `NL2C-D-002-repro.txt` | 指令越权：同上 |
| `NL2C-D-003-repro.txt` | 输出形态不合规：同上 |

证据文件由 `tools/dump_defect_evidence.py` 从录制缓存生成，可随时重跑：

```bash
NL2CRON_MODEL=deepseek-flash python tools/dump_defect_evidence.py
```

## 约定（沿用模块一）

- **没有复现输出的缺陷不得标记为"已关闭"**；
- 缺陷认定依据 = 可重放的运行输出（回放缓存保证任何人可复现），不以推测代替证据；
- 缺陷编号 `NL2C-D-001` 起；回归用例为对应失败用例，修复验证 = `NL2CRON_PROMPT_VERSION=v2` 下全部通过且 v1 下可复现失败。
