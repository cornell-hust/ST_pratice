# presentation/ — 演示与汇报材料

| 文件/目录 | 作用 |
|---|---|
| `output/模块一成果汇报.pptx` | 模块一成果汇报最终演示稿 |
| `演示视频脚本.md` | 演示视频录制脚本 |
| `build/build.mjs` | 演示稿构建脚本（本地依赖 node_modules，在 `build/` 下执行 `npm install` 生成） |

说明与约定：

- 最终产物放 `output/`，构建脚本与中间文件放 `build/`；
- `build/node_modules` 已被 git 跟踪，建议小组确认后取消跟踪：`git rm -r --cached module1/presentation/build/node_modules`（根目录 `.gitignore` 已加入忽略规则，但对已跟踪文件不生效），见 `docs/项目结构说明.md` 第 7 节 A5。
