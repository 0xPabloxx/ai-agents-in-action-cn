# AI Agents in Action Codex中文翻译版 · 第2章

## 第2章 掌握大型语言模型的力量

“大型语言模型”（LLM）已经成为生成式 AI 的代名词。本章聚焦于这些由生成式预训练变换器（GPT）架构驱动的模型，说明它们如何被训练、为何适合作为代理的基础，并展示从 OpenAI API 到本地开源模型的完整使用链路。LLM 属于生成式模型：它们根据输入继续“生成”内容，而不是像预测或分类模型那样只给出标签。图 2.1 用直观示意对比了生成式与预测式模型。

### 本章要点
- 理解 LLM 的组成（数据、架构、训练、微调）及其在代理构建中的角色。
- 学会使用 OpenAI Python SDK 连接 GPT-4 等聊天补全模型，并掌握请求/响应细节。
- 通过 LM Studio 下载、运行并以服务形式托管开源 LLM，构建本地替代方案。
- 系统演练 Prompt Engineering——尤其是“写出清晰指令”策略下的六种战术。
- 根据性能、规模、上下文长度、训练方式等八类指标挑选最适合的模型。
- 通过实操练习巩固：API 集成、提示策略、LM Studio 部署、商用 vs 开源对比等。

LLM 由三大要素构成：训练语料（往往是 TB 到 PB 级别的数据）、模型架构（上下文窗口、token 限制、嵌入维度、参数量等）以及按用途定制的训练流程。最终的微调（fine-tuning）会让模型更契合特定领域或任务。Transformer 架构让 GPT 类模型能够扩展到数百亿参数并搭配 RLHF 等方法进行深度调优，因此尤其适合需要多轮推理、规划的聊天补全场景。本书的大多数代理示例都会使用聊天补全模型，但你也可以尝试其他模型类型，只是需要调整示例代码。

---

## 2.1 熟练掌握 OpenAI API

许多代理或助手项目都以 OpenAI API 为起点。虽然它不是行业标准，但其请求/响应模式已经成为事实规范。本节使用 OpenAI Python SDK 演示如何连接 GPT-4 系列模型，并解释消息结构、温度（temperature）和 token 计费等要点。

### 2.1.1 连接聊天补全模型

1. **准备开发环境**：按照附录 B 搭建 Python + VS Code 环境；附录 A 则介绍如何获取 OpenAI API Key。打开 `chapter_2` 目录并创建虚拟环境。
2. **安装依赖**：
   ```bash
   pip install openai python-dotenv
   ```
3. **配置密钥**：在 `.env` 中添加
   ```bash
   OPENAI_API_KEY='你的-openai-key'
   ```
4. **核心示例 `connecting.py`**（节选）：
   ```python
   load_dotenv()
   api_key = os.getenv("OPENAI_API_KEY")
   client = OpenAI(api_key=api_key)

   def ask_chatgpt(user_message):
       response = client.chat.completions.create(
           model="gpt-4-1106-preview",
           messages=[
               {"role": "system", "content": "You are a helpful assistant."},
               {"role": "user", "content": user_message}
           ],
           temperature=0.7,
       )
       return response.choices[0].message.content
   ```
   - `load_dotenv()` 读取 `.env` 中的密钥；若缺失，抛出异常。
   - `OpenAI(api_key=...)` 创建客户端；`chat.completions.create` 负责发起请求。
   - `messages` 数组记录聊天历史，`temperature` 控制输出多样性。

调试时按 `F5`（或 VS Code 菜单 Run > Start Debugging）。若请求“法国的首都是哪里？”，模型大概率回答“巴黎”。温度越低结果越稳定（0 几乎恒定），越高越有创意；根据业务场景选择即可。

### 2.1.2 理解请求与响应

**请求结构**（Listing 2.4）重点在 `model`、`messages`、`temperature`：
- `system` 角色：定义全局规则/身份，例如“你是一名乐于助人的助手”。
- `user` 角色：代表用户输入。
- `assistant` 角色：可以回放历史回复或人为注入上下文。

一个请求的 `messages` 可以保存整段对话：
```json
[
  {"role": "system", "content": "You are a helpful assistant."},
  {"role": "user", "content": "What is the capital of France?"},
  {"role": "assistant", "content": "The capital of France is Paris."},
  {"role": "user", "content": "What is an interesting fact of Paris."}
]
```
在 `message_history.py` 中多次运行可观察温度差异：`temperature=0.7` 输出多变，调为 `0.0` 则基本一致。

**响应结构**（Listing 2.6）包含：
- `choices`: 可能包含多条候选，每条都有 `message.role=assistant` 与 `content`。
- `model`: 实际使用的模型名称。
- `usage`: `prompt_tokens`（输入）、`completion_tokens`（输出）、`total_tokens` 总量。

监控 token 至关重要，较少的 token 意味着成本低、速度快、输出更集中。本书后续示例都会在此基础上扩展，接下来转向开源 LLM。

---

## 2.2 使用 LM Studio 体验开源 LLM

商用 LLM（如 GPT-4）部署简便、能力强，但需要外部 API、存在成本与数据合规顾虑。开源 LLM 正迅速追赶，配合 LM Studio 这类工具，个人电脑即可下载并运行多种模型。

### 2.2.1 安装与运行 LM Studio

1. 访问 <https://lmstudio.ai/> 下载对应平台版本（Windows/macOS/Linux）。部分版本尚在 beta，安装时可能提示附加依赖。
2. 安装并启动后，会看到如图 2.3 的主页：可浏览热门模型、搜索关键字、查看上下文长度等规格。
3. LM Studio 会自动检测硬件并给出“兼容性猜测”，帮你判断模型是否适配当前机器。
4. 选定模型后点击下载。若硬件有限，可优先尝试体量较小的聊天补全模型，但也鼓励多做实验。
5. 下载完成即可在 Chat 页面加载模型（图 2.5）。顶部下拉可切换模型，右侧可启用 GPU 加速。加载进度条完成后便能直接在界面中与模型对话。

### 2.2.2 将模型以服务形式运行

LM Studio 也能把本地模型暴露为兼容 OpenAI API 的服务：
1. 打开 Server 页，选择已下载的模型并确保 “Server Model Settings” 与之匹配（见图 2.7）。
2. 点击 **Start Server**，日志区会显示端口、推理状态等信息。
3. 示例代码 `chapter_2/lmstudio_server.py`：
   ```python
   from openai import OpenAI

   client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
   completion = client.chat.completions.create(
       model="local-model",
       messages=[
           {"role": "system", "content": "Always answer in rhymes."},
           {"role": "user", "content": "Introduce yourself."}
       ],
       temperature=0.7,
   )
   print(completion.choices[0].message)
   ```
   - 本地服务默认无需真实 API Key，`base_url` 指向 LM Studio。
   - 可随意修改系统/用户提示以验证本地推理效果。

配置不当时（例如服务设置与模型不符）会导致连接失败，记得核对后重启。至此，你既能调用商用 API，也能在本地运行模型，为后续的提示工程与代理开发提供多种选项。

---

## 2.3 用提示工程驱动 LLM

“提示”（prompt）是发送给 LLM 的文本指令，而“提示工程”（prompt engineering）旨在系统化地构造更高质量的指令。OpenAI 总结了若干策略（图 2.8），涵盖清晰指令、引用资料、调用外部工具、拆解复杂任务、给予思考时间、系统化回归测试等。本章专注于最基础也最通用的策略：**Write Clear Instructions（写出清晰指令）**，并实作六种常见战术（图 2.9）。

示例代码位于 `prompt_engineering.py`：
1. 扫描 `prompts/` 目录下的 JSON Lines 文件，把每种战术对应的提示列出供选择。
2. 读取所选文件，将提示转为 `messages` 并送入 LLM。
3. 打印请求与回复，便于观察差异。脚本还预留了连接本地 LLM 的代码，可与前述 LM Studio 服务配合使用。

### 2.3.1 编写细致的提问

`tactics/detailed_queries.jsonl` 展示“模糊 vs 详细”两种提问方式：
- 仅问 “What is an agent?” 得到泛泛定义。
- 详细说明 “What is a GPT Agent? Please give me 3 examples...” 则能获得更有针对性的解释与实例。

原则：尽量提供与任务高度相关的上下文，必要时直接要求示例或输出格式。

### 2.3.2 设定人物角色（Persona）

人物设定是代理档案的核心。`adopting_personas.jsonl` 演示同一问题在不同 persona 下的回答差异：
- 20 岁的女本科生（计算机专业，回答像初级程序员）。
- 38 岁男性注册护士（以医疗专业人士的口吻回答）。

通过 persona 可以获得特定语域、背景或价值观的视角。本书后续会大量用在代理系统提示中。

### 2.3.3 使用分隔符（Delimiter）

`using_delimiters.jsonl` 展示两种写法：
- 三个单引号 `'''` 包裹需要总结的文本。
- XML 标签 `<statement>...</statement>` 用于比较两个观点。

分隔符能让 LLM 清楚知道哪部分是处理对象、哪部分是指令，非常适合含有层次结构或多段文本的场景。

### 2.3.4 明确步骤

`specifying_steps.jsonl` 利用系统提示定义多步流程，例如：
1. 从三引号内文本生成一句“Summary: …”
2. 把 Summary 翻译成西班牙语并加“Translation: …”前缀。

步骤也可以完全不同，如先回答问题再把答案改写成“Dad Joke”。这种“拆分任务 + 明确顺序”非常适合复杂代理或需要多轮交互的提示。

### 2.3.5 提供示例

`providing_examples.jsonl` 中，系统提示要求“所有回复沿用前一次的格式、长度和风格”，并提供示例对话（用户：Teach me about Python. 助手：一句话简介）。之后再问 “Teach me about Java.”，模型就会按照示例限制输出。提供示例是经典的 few-shot 技巧，也可用于约束代码模板、数据结构等。

### 2.3.6 限制输出长度

`specifying_output_length.jsonl` 给出了两种方式：
- 要求“所有回复不超过 10 个词”。
- 要求“所有回复总结成 3 个要点”。

精简输出不仅省 token，也能在多代理对话中减少噪音，让系统保持聚焦。

建议逐一运行所有战术示例，并尝试改写提示观察效果。本书后续章节会继续扩展到“给予思考时间”“使用外部工具”等更进阶策略。

---

## 2.4 挑选最适合的 LLM

构建代理并不需要成为模型训练专家，但理解关键指标有助于做出选择。结合 LM Studio 的经验，我们可以从八个方面评估 LLM（图 2.11）：

1. **模型性能**：是否在目标任务上表现优秀（如代码生成、SAT 推理等）。
2. **参数规模**：参数越多通常越强，但也意味着本地部署对硬件要求更高。幸运的是，越来越多“小而强”的开源模型正在出现。
3. **模型类型/用例**：聊天补全更适合需要迭代、推理的代理；completion、QA、instruct 则偏任务型。构建代理时强烈建议选择聊天补全类模型。
4. **训练语料**：决定模型的领域知识。通用模型适合广泛任务，特定领域（例如医疗、金融）可考虑经过定向微调的模型。
5. **训练/微调方法**：例如是否使用 RLHF、指令微调等。它会影响模型的泛化、推理与规划能力。
6. **上下文 token 长度**：决定模型一次能“记住”多少内容。简单任务 4K token 足矣，多代理协作或长文档处理则需要 16K、32K 甚至更大窗口。
7. **推理速度 / 部署方式**：商用 API 的速度由服务商保证；自建模型则取决于 CPU/GPU 配置。若代理需要实时与用户对话，速度至关重要。
8. **成本 / 预算**：需要权衡 API 计费 vs 自建基础设施成本。教学或个人项目可以混合使用。

在实践中，通常会先锁定 1–2 个候选模型开展原型，再依据性能/成本做最终取舍。选择本地模型时，务必确认硬件（显存、内存、磁盘）是否满足需求。

---

## 2.5 练习

1. **练习 1：掌握 OpenAI API**  
   - 使用 OpenAI Python SDK 连接 GPT-4。  
   - 实现一个根据用户输入生成回复的脚本，并在终端展示结果。  
   - 记录请求/响应结构和 token 使用情况。

2. **练习 2：探索提示工程战术**  
   - 复现本章的六种战术，并为每种撰写不同表述。  
   - 把这些变体送入 LLM，比较输出差异。  
   - 记录最有效的写法及其原因。

3. **练习 3：用 LM Studio 下载并运行 LLM**  
   - 安装 LM Studio，下载一个聊天补全模型。  
   - 启动 LM Studio Server，并通过 Python 代码连接。  
   - 把提示工程示例切换到本地模型，观察表现差异。

4. **练习 4：对比商用与开源 LLM**  
   - 用 GPT-4 Turbo 运行提示工程示例。  
   - 使用同一套提示测试某个开源模型。  
   - 从准确性、一致性、响应速度等维度比较并记录结论。

5. **练习 5：分析多种托管方案**  
   - 调研自建服务器、云端推理、第三方 API 等托管方式。  
   - 比较各方案在成本、性能、维护复杂度上的差异。  
   - 写一份短报告，给出针对特定用例的推荐。

---

## 本章小结
- LLM 采用 GPT（生成式预训练 Transformer）架构，属于生成式模型，与传统预测/分类模型在训练目标上完全不同。
- 模型由数据、架构、训练/微调三要素构成，针对不同用例（聊天、补全、指令等）会有专门配置。
- OpenAI API SDK 为连接 GPT-4 及其它模型提供了统一接口，也可对接兼容协议的开源 LLM。
- Python 环境 + VS Code 足以完成 API 集成、调试和 token 监控，是构建代理的基础技能。
- 开源 LLM 在 LM Studio 等工具加持下可以轻松下载、运行并暴露为本地服务，便于离线或隐私场景。
- 提示工程是一套帮助 LLM 产出更佳答案的技巧，本章围绕“写出清晰指令”示范了六种常用战术。
- LLM 可以支撑从简单聊天机器人到完全自主代理的全谱系应用。
- 选择模型需综合性能、规模、用例、训练语料、上下文长度、速度与成本等多重因素。
- 自建或托管 LLM 需要掌握 GPU、推理服务、配置管理等多方面技能，并权衡与商用 API 的优劣。

