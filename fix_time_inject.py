import re

with open("adk_claw/agent.py", "r") as f:
    content = f.read()

inject_time = """    # 组合基础提示词
    import datetime
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_prompt = f"\\n\\n## 系统信息\\n当前时间：{now_str}\\n"

    full_prompt = base_prompt + time_prompt + tools_prompt + internal_prompt"""

content = content.replace("    # 组合基础提示词\n    full_prompt = base_prompt + tools_prompt + internal_prompt", inject_time)

with open("adk_claw/agent.py", "w") as f:
    f.write(content)

