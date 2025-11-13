# AI Agents in Action 翻译规范 | Translation Rules

<mark>**版本**: 1.0 | **更新日期**: 2025-11-13</mark>

---

## 📋 目录 | Table of Contents

1. [翻译原则 | Translation Principles](#翻译原则--translation-principles)
2. [格式规范 | Format Standards](#格式规范--format-standards)
3. [术语对照表 | Terminology Dictionary](#术语对照表--terminology-dictionary)
4. [标点符号规范 | Punctuation Rules](#标点符号规范--punctuation-rules)
5. [代码示例规范 | Code Example Standards](#代码示例规范--code-example-standards)
6. [质量检查清单 | Quality Checklist](#质量检查清单--quality-checklist)

---

## 翻译原则 | Translation Principles

### 1. 准确性 (Accuracy)

<mark>**核心原则**: 100% 忠实于原文，不增删改内容</mark>

- ✅ **正确**: 完整翻译所有内容，保持原文含义
- ❌ **错误**: 省略段落、添加个人观点、改变原意

### 2. 流畅性 (Fluency)

<mark>**核心原则**: 符合中文表达习惯，自然流畅</mark>

- ✅ **正确**: "智能体可以自主执行任务"
- ❌ **错误**: "代理能够独立地执行任务们" (机翻痕迹)

### 3. 一致性 (Consistency)

<mark>**核心原则**: 全书术语统一，风格一致</mark>

- ✅ **正确**: Agent 全书统一译为 "智能体"
- ❌ **错误**: Agent 有时译为 "代理"，有时译为 "智能体"

### 4. 专业性 (Technical Precision)

<mark>**核心原则**: 保持技术文档的严谨性</mark>

- ✅ **正确**: 使用标准技术术语，准确传达技术概念
- ❌ **错误**: 使用口语化表达，技术概念模糊

---

## 格式规范 | Format Standards

### 1. 高亮标记 (Highlighting)

<mark>**所有中文内容必须使用 `<mark>` 标签进行黄色高亮**</mark>

**正确示例**:
```markdown
Agents are autonomous entities that can perceive their environment and take actions.

<mark>智能体是能够感知环境并采取行动的自主实体。</mark>
```

**错误示例**:
```markdown
Agents are autonomous entities that can perceive their environment and take actions.

智能体是能够感知环境并采取行动的自主实体。  <!-- 缺少 <mark> 标签 -->
```

### 2. 段落对照 (Paragraph Alignment)

<mark>**采用段落对段落的双语对照格式**</mark>

**格式**:
```markdown
[English paragraph 1]

<mark>[中文段落 1]</mark>

[English paragraph 2]

<mark>[中文段落 2]</mark>
```

### 3. 章节结构 (Chapter Structure)

<mark>**每章必须包含以下结构**:</mark>

```markdown
# Chapter X: [English Title] | <mark>第 X 章：[中文标题]</mark>

## 本章概览 | Chapter Overview

<mark>本章内容概述...</mark>

---

## [Section Title] | <mark>[章节标题]</mark>

[Content...]

---

## 本章小结 | Chapter Summary

<mark>本章总结...</mark>

---

## 参考资源 | References

- [Links and resources...]
```

### 4. 横线分隔 (Horizontal Rules)

<mark>**使用 `---` 分隔主要章节**</mark>

- 章节之间使用三短横线 (`---`)
- 段落之间不使用横线
- 二级标题之间使用横线

---

## 术语对照表 | Terminology Dictionary

### 核心概念 | Core Concepts

| 英文术语 | 中文翻译 | 首次出现处理 | 说明 |
|---------|---------|-------------|------|
| Agent | 智能体 | Agent(智能体) | 核心概念，全书统一 |
| Assistant | 助手 | Assistant(助手) | OpenAI 特定术语 |
| Autonomous | 自主的 | autonomous(自主的) | 形容词 |
| Multi-Agent System | 多智能体系统 | Multi-Agent System(多智能体系统) | 系统架构 |
| Environment | 环境 | environment(环境) | 智能体运行环境 |
| Action | 动作/行动 | action(动作) | 智能体执行的操作 |
| Perception | 感知 | perception(感知) | 智能体感知能力 |
| Goal | 目标 | goal(目标) | 智能体的目标 |

### LLM 相关 | LLM Related

| 英文术语 | 中文翻译 | 首次出现处理 | 说明 |
|---------|---------|-------------|------|
| Large Language Model | 大语言模型 | Large Language Model(大语言模型, LLM) | 核心技术 |
| LLM | 大语言模型 | LLM(大语言模型) | 缩写保留 |
| Prompt | 提示 | prompt(提示) | LLM 输入 |
| Prompt Engineering | 提示工程 | Prompt Engineering(提示工程) | 技术方法 |
| Token | Token/词元 | token(词元) | 保留或翻译均可 |
| Temperature | 温度 | temperature(温度参数) | 模型参数 |
| Hallucination | 幻觉 | hallucination(幻觉) | LLM 问题 |
| Fine-tuning | 微调 | fine-tuning(微调) | 训练方法 |

### OpenAI 生态 | OpenAI Ecosystem

| 英文术语 | 中文翻译 | 首次出现处理 | 说明 |
|---------|---------|-------------|------|
| GPT | GPT | GPT | 专有名词不译 |
| ChatGPT | ChatGPT | ChatGPT | 产品名不译 |
| GPT Store | GPT Store | GPT Store | 平台名不译 |
| GPT Builder | GPT Builder | GPT Builder | 工具名不译 |
| Custom Actions | 自定义动作 | Custom Actions(自定义动作) | 功能名称 |
| Code Interpreter | 代码解释器 | Code Interpreter(代码解释器) | 工具功能 |
| Function Calling | 函数调用 | Function Calling(函数调用) | API 功能 |
| Assistants API | Assistants API | Assistants API | API 名称不译 |

### 框架与工具 | Frameworks & Tools

| 英文术语 | 中文翻译 | 首次出现处理 | 说明 |
|---------|---------|-------------|------|
| AutoGen | AutoGen | AutoGen | 框架名不译 |
| CrewAI | CrewAI | CrewAI | 框架名不译 |
| Semantic Kernel | 语义内核 | Semantic Kernel(语义内核) | Microsoft 框架 |
| LangChain | LangChain | LangChain | 框架名不译 |
| LM Studio | LM Studio | LM Studio | 工具名不译 |
| Prompt Flow | Prompt Flow | Prompt Flow | 工具名不译 |

### 技术概念 | Technical Concepts

| 英文术语 | 中文翻译 | 首次出现处理 | 说明 |
|---------|---------|-------------|------|
| Behavior Tree | 行为树 | Behavior Tree(行为树) | 设计模式 |
| RAG | 检索增强生成 | RAG(Retrieval-Augmented Generation, 检索增强生成) | 技术方法 |
| Vector Database | 向量数据库 | Vector Database(向量数据库) | 数据存储 |
| Embedding | 嵌入/向量嵌入 | embedding(向量嵌入) | 技术概念 |
| Semantic Function | 语义函数 | Semantic Function(语义函数) | SK 概念 |
| Native Function | 原生函数 | Native Function(原生函数) | SK 概念 |
| Planner | 规划器 | Planner(规划器) | 智能体组件 |
| Memory | 记忆 | memory(记忆) | 智能体能力 |
| Knowledge Base | 知识库 | Knowledge Base(知识库) | 数据存储 |
| Back Chaining | 反向链接 | Back Chaining(反向链接) | 推理方法 |

### API 与集成 | APIs & Integration

| 英文术语 | 中文翻译 | 首次出现处理 | 说明 |
|---------|---------|-------------|------|
| API | API | API | 缩写不译 |
| REST API | REST API | REST API | 技术标准 |
| Endpoint | 端点 | endpoint(端点) | API 概念 |
| Webhook | Webhook | Webhook | 技术术语 |
| JSON | JSON | JSON | 数据格式 |
| TMDB | TMDB | TMDB(电影数据库) | The Movie Database |

---

## 标点符号规范 | Punctuation Rules

### 1. 中文标点 (Chinese Punctuation)

<mark>**在中文语境中使用中文标点符号**</mark>

| 标点 | 正确 | 错误 |
|------|------|------|
| 句号 | 。 | . |
| 逗号 | ，| , |
| 顿号 | 、| , |
| 分号 | ；| ; |
| 冒号 | ：| : |
| 问号 | ？| ? |
| 感叹号 | ！| ! |
| 引号 | 「」或 "" | "" |
| 书名号 | 《》| 无 |
| 省略号 | …… | ... |

### 2. 英文标点 (English Punctuation)

<mark>**在英文语境中使用英文标点符号**</mark>

- 代码中: 使用英文标点
- 英文原文: 保持英文标点
- 专有名词: 保持原标点

### 3. 空格规范 (Spacing Rules)

<mark>**严格遵循空格规范**</mark>

| 场景 | 规则 | 示例 |
|------|------|------|
| 中英混排 | 中文与英文之间加空格 | `使用 LLM 构建智能体` |
| 中文数字 | 中文与数字之间加空格 | `第 3 章`、`9 个章节` |
| 中文符号 | 中文标点后不加空格 | `你好，世界。` |
| 英文符号 | 英文标点后加空格 | `Hello, world.` |
| 代码引用 | 代码块前后加空格 | `使用 \`print()\` 函数` |

---

## 代码示例规范 | Code Example Standards

### 1. 代码块保留 (Code Preservation)

<mark>**所有代码示例必须完整保留，不做修改**</mark>

**正确示例**:
````markdown
```python
# Initialize the OpenAI client
client = OpenAI(api_key="your-api-key")
```

<mark>```python
# 初始化 OpenAI 客户端
client = OpenAI(api_key="your-api-key")
```</mark>
````

### 2. 注释翻译 (Comment Translation)

<mark>**代码注释翻译为中文，保持代码不变**</mark>

**原文**:
```python
# Create a simple agent
agent = Agent(name="Assistant")

# Define the agent's goal
goal = "Help users with their questions"
```

**翻译**:
```python
# 创建一个简单的智能体
agent = Agent(name="Assistant")

# 定义智能体的目标
goal = "Help users with their questions"
```

### 3. 输出示例 (Output Examples)

<mark>**输出示例可以翻译说明，但保留原始输出**</mark>

**格式**:
````markdown
Output | <mark>输出</mark>:
```
Response: Hello, how can I help you?
```

<mark>说明: 智能体返回了欢迎消息。</mark>
````

---

## 质量检查清单 | Quality Checklist

### 翻译前 (Before Translation)

- [ ] 阅读完整章节英文原文
- [ ] 理解所有技术概念和术语
- [ ] 查阅术语对照表确保一致性
- [ ] 准备好代码示例和图表说明

### 翻译中 (During Translation)

- [ ] 使用 `<mark>` 标签标记所有中文内容
- [ ] 段落对段落严格对照
- [ ] 术语首次出现时标注英文
- [ ] 代码示例完整保留
- [ ] 注释翻译为中文
- [ ] 遵循标点符号规范
- [ ] 遵循空格规范
- [ ] 使用横线分隔主要章节

### 翻译后 (After Translation)

- [ ] 通读全文检查流畅性
- [ ] 检查所有 `<mark>` 标签是否正确闭合
- [ ] 验证 Markdown 格式正确渲染
- [ ] 检查术语一致性
- [ ] 检查代码块格式
- [ ] 检查链接有效性
- [ ] 更新 README.md 进度
- [ ] 提交前再次校对

### 格式检查 (Format Check)

- [ ] 所有中文内容都有 `<mark>` 标签
- [ ] 章节标题格式正确
- [ ] 横线分隔符使用正确
- [ ] 代码块语法高亮正确
- [ ] 中英文间有空格
- [ ] 中文数字间有空格
- [ ] 标点符号使用正确

---

## 常见问题 | FAQ

### Q1: 专有名词是否需要翻译?

<mark>**A**: 保持原文，首次出现时括号注明中文含义。</mark>

**示例**: GPT Store(GPT 商店)、AutoGen 框架

### Q2: 如何处理图表?

<mark>**A**: PDF 无法直接提取图片，需要详细描述图表内容。</mark>

**格式**:
```markdown
**Figure X.X: [English Caption]** | <mark>**图 X.X: [中文标题]**</mark>

[Image description in English]

<mark>[图表详细描述中文]</mark>
```

### Q3: 如何处理链接?

<mark>**A**: 保留所有原始链接，标题可翻译。</mark>

**示例**:
```markdown
[OpenAI Documentation](https://platform.openai.com/docs) | <mark>[OpenAI 文档](https://platform.openai.com/docs)</mark>
```

### Q4: 遇到不确定的术语怎么办?

<mark>**A**: 优先查阅术语对照表，如无则保留英文并添加待确认标记。</mark>

**示例**: `某术语 (term) [待确认]`

---

## 版本历史 | Version History

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| 1.0 | 2025-11-13 | <mark>初始版本，建立翻译规范</mark> |

---

<div align="center">

**<mark>严格遵循翻译规范，确保翻译质量</mark>**

*Follow the translation rules strictly to ensure quality*

</div>
