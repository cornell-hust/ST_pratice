"""nl2cron —— 模块二被测的 AI 组件：自然语言 → 标准 5 字段 cron 表达式。

组件本身刻意保持薄：LLM 调用（OpenAI 兼容接口）+ 提示词 + 最小输出守卫。
它的问题正是模块二的测试对象。
"""

from .translator import TranslateResult, translate

__all__ = ["TranslateResult", "translate"]
