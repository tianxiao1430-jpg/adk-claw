import re

with open("adk_claw/agent.py", "r") as f:
    content = f.read()

weather_code = """
def get_weather(location: str) -> str:
    \"\"\"获取指定城市的实时天气和未来三天预报
    
    Args:
        location: 城市拼音或英文名称，如 "Tokyo", "Beijing"
        
    Returns:
        天气预报的文本描述
    \"\"\"
    try:
        import urllib.request
        from urllib.parse import quote
        import json
        
        url = f"https://wttr.in/{quote(location)}?format=j1"
        req = urllib.request.Request(url, headers={'User-Agent': 'curl/7.68.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            result = [f"【{location} 天气预报】"]
            
            # 当前天气
            current = data['current_condition'][0]
            result.append(f"当前：{current['weatherDesc'][0]['value']}，气温 {current['temp_C']}°C，体感 {current['FeelsLikeC']}°C，湿度 {current['humidity']}%")
            
            # 未来几天
            for day in data['weather'][:3]:
                date = day['date']
                maxtemp = day['maxtempC']
                mintemp = day['mintempC']
                uv = day['uvIndex']
                result.append(f"{date}: 最高 {maxtemp}°C，最低 {mintemp}°C，UV指数 {uv}")
                
            return "\\n".join(result)
    except Exception as e:
        return f"获取 {location} 的天气失败: {str(e)}"

"""

# Replace the old get_weather
content = re.sub(r'def get_weather\(location: str\) -> str:.*?(?=\n# ============================================\n# 网络搜索工具)', weather_code, content, flags=re.DOTALL)

with open("adk_claw/agent.py", "w") as f:
    f.write(content)
