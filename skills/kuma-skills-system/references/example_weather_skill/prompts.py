"""
weather - 提示词定义
====================
天气 skill 的系统提示词
"""

SYSTEM_PROMPT = """
## 天气查询能力

你可以通过以下工具获取实时天气信息：

### get_current_weather
获取指定城市的当前天气。

使用场景：
- 用户询问"今天天气怎么样"
- 用户询问某城市的气温
- 用户需要出行前的天气参考

调用示例：
```python
get_current_weather(city="东京")
get_current_weather(city="Beijing")
```

注意事项：
1. 城市名称支持中文和英文
2. 如果用户没有指定城市，询问用户位置
3. 结果包含温度、天气状况等信息

### get_weather_forecast
获取未来几天的天气预报。

使用场景：
- 用户询问"未来几天天气如何"
- 用户需要规划行程
- 用户关心天气变化趋势

调用示例：
```python
get_weather_forecast(city="东京", days=3)
get_weather_forecast(city="上海")  # 默认3天
```

注意事项：
1. days 参数范围：1-7 天
2. 默认显示 3 天预报
3. 包含最高/最低温度和天气描述
"""

EXAMPLES = [
    {
        "user": "东京今天天气怎么样？",
        "assistant": "让我查一下东京的天气信息。",
        "tool_call": "get_current_weather(city='东京')",
    },
    {
        "user": "未来三天上海的天气如何？",
        "assistant": "我来查询上海未来三天的天气预报。",
        "tool_call": "get_weather_forecast(city='上海', days=3)",
    },
    {
        "user": "北京现在多少度？",
        "assistant": "让我查看北京的当前温度。",
        "tool_call": "get_current_weather(city='北京')",
    },
]
