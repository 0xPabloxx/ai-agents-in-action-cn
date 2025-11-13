# AI-Agents-in-Action-Codex中文翻译版-第3章

## 第3章 激活 GPT 助手

OpenAI 在 ChatGPT Plus 中推出的 GPT Assistants 平台，让我们能够用纯图形界面快速定义和发布“类代理”助手。它内置 GPT Store、GPT Builder、文件知识库、Code Interpreter、自定义动作、发布与分享等能力，能够从零完成一个可商业化的智能体。本章带你依次体验：用 ChatGPT 构建 Culinary Companion、美食助手；让 GPT 充当“Data Scout”进行数据科学分析；借助自定义动作把助手与 FastAPI 服务连接；通过文件上传扩展知识；最后把 GPT 发布到 GPT Store，并评估资源成本与商业模式。

### 本章内容
- 通过 GPT Store 与 GPT Builder 设计并调优助手的 persona、指令与规则。
- 使用 Code Interpreter 与文件上传，打造可以分析 CSV 的数据科学家代理。
- 借助自定义动作把助手与自建 FastAPI 服务连接，并通过 ngrok 暴露端点。
- 让 GPT 消化整本书或多份文档，构建具备专属知识的“读书助手”。
- 了解 GPT Store 的分享、资源消耗、发布流程及潜在收益模型。
- 练习题：从第一个 GPT、数据分析、API 扩展、知识助手到发布全流程。

---

## 3.1 通过 ChatGPT 探索 GPT 助手

GPT Store（https://chatgpt.com/gpts）是 ChatGPT Plus 用户管理和探索 GPT 的门户。列表页能查看自己创建的助手、按类别/关键词搜索他人作品、了解使用量等。点击 **Create** 会打开 GPT Builder：你可以像和 ChatGPT 对话一样描述需求，Builder 会生成初始的名称、描述、指令与引导语。

Builder 生成的内容可在 **Configure** 面板中手动微调：修改名称与描述、编辑长指令、添加规则、设置默认对话开场白、上传图标等。精心撰写这些字段十分重要，因为它们决定了 GPT 的定位与“第一印象”。

### 示例：Culinary Companion

- **Persona**：模仿传奇厨师 Julia Child，口吻亲切、充满仪式感。
- **目标**：根据用户现有食材提供易于操作的菜谱，顺带科普营养和成本。
- **核心指令**（Listing 3.1）：用温暖口吻安抚用户，鼓励实验；推荐简单步骤；适配饮食偏好。
- **规则**：
  1. 每次生成菜谱时都要附带成品图像。
  2. 估算每份卡路里与营养值。
  3. 列出购物清单并给出价格预估。
  4. 基于清单估算每份成本。

在预览窗口输入“我有一袋速冻鸡柳，想做一顿浪漫双人餐”，GPT 会产出可视化食谱、食材与购物单、营养估算以及总价/份价提醒。这些额外输出完全来自我们在指令中写下的规则。虽然价格或营养值只是估算，但快速验证了制作原型的能力。

---

## 3.2 构建能够做数据科学的 GPT

GPT Assistants 目前提供“知识（文件上传）”“记忆”“动作（Code Interpreter、自定义动作）”等组件。本节构建 Data Scout——一名仿 Nate Silver 风格、擅长 CSV 初步分析的“数据科学家”助手。实现思路：

1. **需求拆解**：让 GPT-4 先推荐一个适合单个 CSV 的有趣实验，再请它把实验流程写成正式指令，最后补上一位符合设定的公众人物作为 persona。
2. **最终 persona**：Nate Silver 式的数据讲述者，善于把复杂统计结果解释得浅显易懂。
3. **任务分解**（Listing 3.4）：
   - *Data Acquisition*：要求用户上传 CSV，使用 `pandas` 读取、`df.head()` 预览。
   - *EDA*：清洗（`isnull()` + 填补/类型转换）、可视化（`matplotlib`/`seaborn`）、描述统计（`df.describe()`）。
   - *Hypothesis Testing*：使用 `scipy.stats`（如 `ttest_ind`、`chi2`）验证假设。
   - *Predictive Modeling*：特征工程、模型选择（`RandomForestClassifier`、`LinearRegression` 等）、`train_test_split` 训测、`metrics` 评估。
   - *Insights*：总结重要特征、意义、建议。
   - *Presentation*：用图表和要点向非技术读者汇报。
4. **启用 Code Interpreter**：勾选后即可上传 `netflix_titles.csv`，让 GPT 自动写代码进行过滤、绘图、统计。示例把数据过滤为“加拿大”并绘制流派分布、年份趋势等。

Code Interpreter 本质上是“受控沙盒 + Python 工具链”。借助它，几乎可以把任何数据分析、计算或图表任务交给 GPT 完成，并随时迭代需求。

---

## 3.3 自定义 GPT 并添加自定义动作

### 3.3.1 用 GPT 帮你写 FastAPI 服务

自定义动作允许 GPT 调用你提供的 HTTP API。为避免手写繁琐的 OpenAPI 规范，本节先让 GPT 自己生成一个“FastAPI 服务生成器”助手：

- **目标**：根据用户描述的动作，输出一份带 FastAPI 代码 + OpenAPI 规范的服务模板。
- **指令要点**：
  1. 先澄清动作、HTTP 方法、路径与请求/响应结构。
  2. 使用 FastAPI + Pydantic 编写函数、装饰器、输入输出模型。
  3. 提示如何让 FastAPI 自动生成 OpenAPI，并可手动补充元数据/标签。
  4. 指导用户用 ngrok 暴露本地 8000 端口，便于 GPT 访问。
- **能力**：推荐启用 Code Interpreter，以便在对话中生成/修改代码片段。

借此，我们可以让 GPT 产出一个“待办任务服务”：返回当天任务、优先级和时间估算等信息。

### 3.3.2 把自定义动作接入助手

1. **运行 FastAPI 服务**：在本地启动生成的应用（默认 8000 端口）。
2. **开启外网访问**：运行 `ngrok http 8000`，复制生成的 HTTPS URL。
3. **新建助手 Task Organizer**：
   - Persona：借鉴 Tim Ferriss，强调效率与现实主义，用清晰直接的语言帮助用户分类任务并安排时间块。
   - 规则：完成整理后用 Code Interpreter 绘制任务时间表。
4. **添加自定义动作**：
   - 在 Configure 面板底部点击 **Create new Action**。
   - 将 FastAPI 生成的 OpenAPI 规范粘贴到窗口，并新增 `servers` 字段写入 ngrok URL。
   - 点击 **Test** 验证，成功后助手即可调用该 API。
5. **测试**：重新加载会话，输入 “how should I organize my tasks for today?”，GPT 会调用 API 获取任务、排序并输出图表。

> ⚠️ **安全提示**：一旦把含自定义动作的 GPT 发布到 GPT Store，任何使用者都能触发该 API。请勿暴露付费接口或敏感数据服务；若使用 ngrok，也要留意外部访问风险。

---

## 3.4 通过文件上传扩展知识

GPT Assistants 的“文件上传”能力，相当于内置了轻量 RAG。单个助手可上传最多 512 MB 的文档（PDF、TXT、MD 等），随后 GPT 可引用这些资料回答问题、对比、排序，甚至生成仿写内容。

### 3.4.1 Calculus Made Easy：书籍 + Persona 的教学助手

- **资料**：上传整本《Calculus Made Easy》。
- **Persona**：以数学家陶哲轩（Terence Tao）的语气教书。
- **规则**：
  1. 用教孩子的方式耐心说明。
  2. 必须画图展示函数或导数（需启用 Code Interpreter）。
  3. 每讲完一个概念就问学生是否要自己做题，并给出等价难度的练习。

在 GPT Store 搜索 “Calculus Made Easy” 即可体验：它会结合书本内容解释微积分，展示图像，最后抛出自测题，像定制家教一样伴学。

### 3.4.2 Classic Robot Reads：多文档检索与创作

- **资料**：上传 `gutenberg_robot_books` 目录下的多本经典机器人小说（Asimov 等）。
- **Persona**：化身 Isaac Asimov 本人，只引用知识库中的文本，永远提供 3 个例子，并在回答后询问用户是否需要更多帮助。
- **应用**：搜索特定段落、比较写作风格、找出差异、推荐阅读顺序、判断年代，甚至生成模仿原文笔调的短段落（表 3.1 给出了常见用法与示例提示）。

这种“知识助手”可以轻松应用到公司制度、团队文档或个人藏书中，大幅提升检索与学习效率。

---

## 3.5 发布 GPT

当你对 GPT 的体验满意后，可点击 **Share** 按钮选择分享方式：

- **Only me**：仅自己使用。
- **Share link**：持链接者可用（仍需 Plus 账号，费用计入使用者账户）。
- **Publish to GPT Store**：公开上架，供所有 ChatGPT Plus 用户搜索、体验。

### 3.5.1 控制资源消耗

OpenAI 会监控每个账号的资源使用（图像生成、Code Interpreter、Vision、文件上传等）。一旦超额，账号会暂时被封（通常几小时），影响体验。为避免用户在使用你的 GPT 时被封锁，可在指令里加入提醒，例如：

```
RULE: When generating images, remind the user that rapid multi-image requests may temporarily block their account.
```

也可以针对 Code Interpreter、Vision、批量文件上传等高消耗功能设置频率或先行确认，帮助用户合理使用。

### 3.5.2 GPT 的经济学

OpenAI 计划引入收益分享机制，具体比例尚未公布（社区推测 10%–20%）。即便暂未直接盈利，公开 GPT 仍有价值：

- **作品集 / 个人品牌**：展示提示工程、应用设计的能力。
- **知识产品**：把专业经验包装为顾问型助手。
- **商业引流**：作为产品/服务的对话入口，完成预筛选或售前沟通。
- **客户支持**：提供 7×24 小助手，降低自建聊天机器人的成本。

随着 GPT Store 逐渐开放给非 ChatGPT 用户，这些助手可能像早期网站一样成为企业的“标配入口”。

### 3.5.3 发布前清单

- **描述**：撰写清晰且富含关键词的介绍，必要时请 GPT 帮你做 SEO。
- **Logo**：设计辨识度高的图标，提升点击率。
- **类别**：确认分类准确；若无合适选项，可选择 “Other” 并自定义。
- **链接**：添加社交媒体、GitHub 或反馈渠道，让用户能与你取得联系。
- **后续维护**：保持监听用户反馈，及时更新指令、文件或自定义动作。

---

## 3.6 练习

1. **练习 1：构建你的第一个 GPT**
   - 订阅 ChatGPT Plus，打开 GPT Builder。
   - 复刻本章的 Culinary Companion，手动加入营养与成本规则。

2. **练习 2：数据分析助手**
   - 设计类似 Data Scout 的指令，启用 Code Interpreter。
   - 上传任意 CSV，完成清洗、可视化、假设检验，记录发现。

3. **练习 3：创建自定义动作**
   - 实现一个 FastAPI 服务（如返回待办列表），生成 OpenAPI 规范。
   - 用 ngrok 暴露端口，在 GPT 中注册该动作，测试任务组织流程。

4. **练习 4：文件知识助手**
   - 选取若干公开文档或电子书上传，定义 persona 与回答范围。
   - 设计测试提示，检验引用、总结、比较、创作等能力。

5. **练习 5：发布并分享**
   - 完成描述、Logo、分类与链接设置。
   - 发布到 GPT Store，邀请朋友体验，并根据反馈迭代。

---

## 本章小结

- GPT Assistants 平台让我们无需写代码即可设计、测试、共享 AI 助手；核心在于 persona、规则与对话体验的精细打磨。
- Code Interpreter 赋予 GPT 读写文件、运行 Python、绘制图表的能力，让它能胜任数据科学、公式计算、格式转换等任务。
- 自定义动作通过 OpenAPI 把 GPT 与任何 HTTP 服务打通，可与 FastAPI、ngrok 等工具结合快速原型。
- 文件上传即内置 RAG，可让 GPT 成为特定资料的“权威讲解员”，适用于教学、知识库、文档检索等场景。
- 发布到 GPT Store 前，需要关注资源消耗、用户体验、商业定位与推广策略，确保助手既易用又可持续。
- 通过章节尾的练习，你可以亲手完成 GPT 的设计—增强—发布全流程，为后续多代理系统打下基础。
