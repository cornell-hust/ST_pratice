# presentation/ — 演示与汇报材料

| 文件 | 作用 |
| --- | --- |
| `模块一成果汇报.pptx` | **成果汇报 PPT**（12 页，基于学校 PPT 母版生成，含最新 40 条用例口径） |
| `模块一演示视频.mp4` | **演示视频成片**（2026-09-12 录制，41 MB） |
| `指令.md` | 录制时照着敲的**指令速查表**：全部命令按录制顺序编号，每条单独一个代码块，可一键复制 |
| `演示-缺陷复现.py` | 缺陷复现演示脚本：同一段代码分别以 `PYTHONPATH=baseline` / `subject` 跑两遍，对照缺陷 |

## 演示脚本的运行方式

在 `module1` 目录下执行（Git Bash）：

```bash
PYTHONPATH=baseline .venv/Scripts/python.exe presentation/演示-缺陷复现.py   # 6.2.2 原版：三个缺陷原形毕露
PYTHONPATH=subject  .venv/Scripts/python.exe presentation/演示-缺陷复现.py   # 修复后：三个缺陷全部消失
```

PowerShell 改用 `$env:PYTHONPATH="baseline"; .venv/Scripts/python.exe ...`。

脚本第一行会打印**实际加载的源码路径**，用于证明两遍运行加载的不是同一份源码。

## 说明与约定

- `演示-缺陷复现.py` 是**只读演示**，不修改任何被测源码；
- **汇报稿的素材来源**：封面右上角徽标取自华中科技大学软件学院官网（https://sse.hust.edu.cn/），其余版式沿用学校 PPT 母版；
- 旧版汇报稿（36 条用例口径）与 `output/` 目录、`build/` 构建脚本已于 2026-09-11 清理——构建脚本硬编码依赖创建者本机的 macOS 运行时，在其他机器无法运行；现行汇报稿由 Python（python-pptx）流程生成；
- 演示视频中第 3 段的 5 项核心功能（解析／迭代／范围／匹配／校验）为**现场手敲**，对应命令清单见 `指令.md`。
