# presentation/ — 演示与汇报材料

| 文件/目录 | 作用 |
|---|---|
| `output/模块一成果汇报.pptx` | 模块一成果汇报演示稿（旧版，内容为 36 条用例口径，仅作历史存档） |
| `output/模块一成果汇报v2.pptx` | **现行汇报稿**（12 页，基于 `module1/华科ppt母版.pptx` 生成，含最新 41 条用例口径） |
| `演示视频脚本.md` | 演示视频录制脚本（数字待同步为 41 条用例口径） |
| `build/build.mjs` | 旧版演示稿构建脚本（依赖 macOS 上的 Codex 运行时，本机不可用，仅作参考） |

说明与约定：

- 最终产物放 `output/`，构建脚本与中间文件放 `build/`；
- **汇报稿 v2 的素材来源**：封面右上角徽标取自华中科技大学软件学院官网（https://sse.hust.edu.cn/ 招生横幅中的院徽，裁切为透明底圆盘）；母版其余版式（校徽、校名）保持 `module1/华科ppt母版.pptx` 原样，母版文件本身未做修改；
- `build/node_modules` 已被 git 跟踪，建议小组确认后取消跟踪：`git rm -r --cached module1/presentation/build/node_modules`（根目录 `.gitignore` 已加入忽略规则，但对已跟踪文件不生效），见 `docs/项目结构说明.md` 第 7 节 A5。
