import re

with open("adk_claw/agent.py", "r") as f:
    content = f.read()

weather_code = """
def get_weather(location: str) -> str:
    \"\"\"获取指定城市的实时天气和未来三天预报
    
    Args:
        location: 城市名称，如 "Tokyo", "Beijing"
        
    Returns:
        天气预报的文本描述
    \"\"\"
    try:
        import urllib.request
        from urllib.parse import quote
        # 使用 wttr.in 获取简洁格式的天气
        url = f"https://wttr.in/{quote(location)}?format=3"
        req = urllib.request.Request(url, headers={'User-Agent': 'curl/7.68.0'})
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8').strip()
    except Exception as e:
        return f"获取 {location} 的天气失败: {str(e)}"

"""

if "def get_weather" not in content:
    content = content.replace("# ============================================\n# 网络搜索工具\n# ============================================", weather_code + "# ============================================\n# 网络搜索工具\n# ============================================")
    
    # Replace the duckduckgo import to ddgs
    content = content.replace("from duckduckgo_search import DDGS", "from ddgs import DDGS")
    
    # Add get_weather to tools list
    content = content.replace("FunctionTool(func=web_search),", "FunctionTool(func=web_search),\n    FunctionTool(func=get_weather),")
    
    # Update tools_prompt
    content = content.replace("- **get_current_time**: 获取当前时间", "- **get_current_time**: 获取当前时间\n- **get_weather**: 获取指定城市的天气预报\n  - 用法：get_weather(location)")

with open("adk_claw/agent.py", "w") as f:
    f.write(content)

# Update requirements.txt to replace duckduckgo-search with ddgs
with open("requirements.txt", "r") as f:
    reqs = f.read()
reqs = reqs.replace("duckduckgo-search>=6.0.0", "ddgs>=9.0.0")
with open("requirements.txt", "w") as f:
    f.write(reqs)

with open("pyproject.toml", "r") as f:
    toml = f.read()
toml = toml.replace('"duckduckgo-search>=6.0.0"', '"ddgs>=9.0.0"')
with open("pyproject.toml", "w") as f:
    f.write(toml)
    
