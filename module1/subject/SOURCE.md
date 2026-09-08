# 被测对象来源

- 项目：croniter
- 官方仓库：https://github.com/pallets-eco/croniter
- 固定版本：`6.2.2`
- 获取地址：https://github.com/pallets-eco/croniter/archive/refs/tags/6.2.2.tar.gz
- 基线日期：2026-09-08（本地快照获取日）
- 快照内容：官方源码 `src/croniter/`，复制到本目录 `croniter/`；上游 MIT License 保留于 `module1/subject/LICENSE`。
- 版本核对：`pyproject.toml` 中的项目版本为 `6.2.2`；本快照不包含后续版本修改。

## 后续公开修复（用于模块一历史缺陷复现）

以下问题在 6.2.2 之后由上游公开记录并修复，模块一将在独立缺陷证据中引用其 CHANGELOG/issue，并在本地分支完成回归验证：

- `6.2.3`：修复零步长范围问题（issue #232）。
- `6.2.3`：修复 `expand_from_start_time` 月份边界问题（issue #235）。
- `6.2.4`：修复 `expand_from_start_time` 下 Sunday 边界问题（issue #239）。

证据入口：

- CHANGELOG：https://github.com/pallets-eco/croniter/blob/6.2.2/CHANGELOG.rst
- 发布历史：https://github.com/pallets-eco/croniter/releases
- Issues：https://github.com/pallets-eco/croniter/issues/232、https://github.com/pallets-eco/croniter/issues/235、https://github.com/pallets-eco/croniter/issues/239
