# 调研纪要 1：GitHub 开源工具与项目（2026-09-22）

调研方式：ZCode 子代理网络检索（只读），覆盖 promptfoo/deepeval/garak/Giskard、NL2Cron 先例、LLM 生成单测工具、扰动语料库。

## LLM 应用测试框架

| 框架 | 定位 | 对本作业的可用性 |
| --- | --- | --- |
| [promptfoo](https://github.com/promptfoo/promptfoo)（25.4k★，MIT） | YAML 配置评测 + 红队扫描 | 借鉴其断言分类学（is-json/python 断言/llm-rubric）设计自研评估器 |
| [deepeval](https://github.com/confident-ai/deepeval)（18.4k★，Apache-2.0） | pytest 原生 LLM 单测 | 思路参考；为 judge 指标引入 API 依赖，收益低 |
| [garak](https://github.com/NVIDIA/garak)（NVIDIA，9.3k★） | LLM 漏洞扫描器 | probe 分类表直接用作鲁棒性/安全性测试维度 checklist |
| Giskard / openai/evals | agent 场景 / 已停更 | 不适用 |

## 结论：自写 pytest 评估器 + 框架只做参考

cron 输出校验是确定性的（结构 + croniter 试解析 + 触发序列比对），不需要 LLM-as-judge。

## NL2Cron 先例

- [rodgetech/cron-ai](https://github.com/rodgetech/cron-ai)（187★，TS）：调已废弃模型，无许可证无测试——验证体系是空白点；
- [hulio-ai/cron-agent](https://github.com/hulio-ai/cron-agent)（2★，MIT，Python）：PydanticAI + 按 provider 分测试的骨架可借鉴；
- [kirbs-/text2cron](https://github.com/kirbs-/text2cron)：规则式对照基线；
- [bradymholt/cron-expression-descriptor](https://github.com/bradymholt/cron-expression-descriptor)：cron→自然语言反解，可做双向一致性校验（备选增强）。
- **已知失败模式**：星期编号歧义、`*/5` 步进语义、范围 off-by-one、时区忽略、Quartz 与 crontab 方言混淆、语法合法但语义错误（最难，需执行式 oracle）。无成熟 NL2Cron 评测集 ⇒ 自建用例集即贡献点。

## LLM 生成单测与扰动语料（方案 2 备选与安全用例素材）

- [se2p/pynguin](https://github.com/se2p/pynguin)（含 CodaMosa）可直接跑 croniter；TestPilot 的"生成→运行→报错回喂修复"循环可手工复刻；
- 文献共识：LLM 测试套件几乎必含错误/test smell，断言问题约占 64%（ACM 质量评估研究）；
- [microsoftarchive/promptbench](https://github.com/microsoftarchive/promptbench)：字符/词/句子/语义四级对抗扰动，含中文——鲁棒性用例素材；
- garak probes（promptinject/DAN/badchars 同形字/encoding）：安全用例维度来源；
- [JailbreakBench](https://github.com/JailbreakBench/jailbreakbench)（NeurIPS 2024）、[Open-Prompt-Injection](https://github.com/liu00222/Open-Prompt-Injection)（USENIX Sec 2024）：引用背景，对 cron 场景偏重。
