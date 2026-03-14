# skill-creator

> 🦞 第一个 kuma-claw skill - 用于创建和管理其他 skills

## 功能

### 1. init_skill()
初始化新 skill 的标准结构。

```python
init_skill(skill_name="my-skill")
```

**创建文件：**
- `skill.json` - 元数据配置
- `tools.py` - 工具实现
- `prompts.py` - 系统提示词
- `__init__.py` - 导出接口

### 2. validate_skill()
验证 skill 结构和配置。

```python
validate_skill(skill_name="my-skill")
```

**检查项：**
- 必需文件存在性
- skill.json 格式和字段
- tools.py 中的 TOOLS 列表
- prompts.py 中的 SYSTEM_PROMPT

### 3. package_skill()
打包 skill 为可分发文件。

```python
package_skill(skill_name="my-skill", output_dir="dist")
```

**生成：**
- `my-skill.skill` 文件（zip 格式）
- 包含所有 skill 文件
- 可分享给其他用户

## 使用示例

### 创建新 skill

```python
# 1. 初始化
init_skill(skill_name="github-analyzer")

# 2. 编辑文件
# - skill.json: 添加触发词 ["GitHub", "仓库分析"]
# - tools.py: 实现 analyze_repo() 函数
# - prompts.py: 编写系统提示词

# 3. 验证
validate_skill(skill_name="github-analyzer")

# 4. 打包
package_skill(skill_name="github-analyzer", output_dir="dist")
```

### 触发词示例

```python
# 用户消息匹配触发词
"创建一个新的skill叫weather"
"帮我开发一个分析股票的skill"
"初始化my-skill"
```

## 开发流程

1. **规划** - 确定功能、触发词、工具
2. **初始化** - 使用 init_skill() 创建结构
3. **实现** - 编写工具函数和提示词
4. **验证** - 检查配置和结构
5. **打包** - 生成 .skill 文件分发

## 最佳实践

### Skill 命名
- ✅ `github-analyzer`, `weather-api`
- ❌ `GitHub_Analyzer`, `Weather API`

### 触发词设计
- 包含中英文变体
- 覆盖常见表达方式
- 避免与其他 skill 冲突

### 工具实现
- 单一职责原则
- 清晰的参数说明
- 友好的错误处理

## 示例输出

### init_skill() 成功

```
✅ Skill 'github-analyzer' 初始化成功

📁 位置: kuma_claw/skills/github-analyzer

📝 已创建文件：
- skill.json    (元数据)
- tools.py      (工具定义)
- prompts.py    (提示词)
- __init__.py   (导出接口)

🎯 下一步：
1. 编辑 skill.json 添加触发词和工具定义
2. 实现 tools.py 中的工具函数
3. 完善 prompts.py 中的系统提示词
4. 使用 validate_skill() 验证结构
5. 使用 package_skill() 打包分发
```

### validate_skill() 失败

```
🔍 Skill 'my-skill' 验证结果:

❌ 错误:
  - 缺少必需文件: prompts.py
  - skill.json 缺少必需字段: triggers

⚠️  警告:
  - tools.py 中未找到 TOOLS 列表
```

## 文件结构

```
skill-creator/
├── skill.json      # Skill 元数据
├── tools.py        # 三个核心工具
├── prompts.py      # 系统提示词和使用指南
├── __init__.py     # 导出接口
└── README.md       # 本文件
```

## 作为第一个 Skill

这是 kuma-claw 的第一个官方 skill，展示了：

1. **标准结构** - 所有 skill 应遵循的目录和文件规范
2. **工具设计** - 如何使用 FunctionTool 定义工具
3. **提示词编写** - 如何编写清晰的 SYSTEM_PROMPT
4. **触发词设计** - 如何覆盖多种用户表达方式

## 下一步

使用本 skill 创建更多 skills：

```python
# 天气查询
init_skill(skill_name="weather")

# GitHub 分析
init_skill(skill_name="github-analyzer")

# 浏览器控制
init_skill(skill_name="browser-control")
```

---

**skill-creator v1.0.0** | kuma-claw 官方 skill
