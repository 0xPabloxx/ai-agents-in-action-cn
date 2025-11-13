# AI-Agents-in-Action-Codex中文翻译版-第4章

## 第4章 探索多代理系统

本章聚焦两大多代理平台：微软开源的 AutoGen 与近年来兴起的 CrewAI。前者强调“可对话”的代理协作，提供 AutoGen Studio 与 Python SDK 两种体验路径；后者面向企业场景，主打角色分工、顺序/层级流程与可观测性。章节中，你将动手安装 AutoGen Studio、为代理添加视觉技能、在代码层实践 UserProxy/ConversableAgent、让工程师与 Reviewer 协同、启用缓存与群聊；随后切换到 CrewAI，构建段子手小队、引入 AgentOps 观测、组建编码团队并比较顺序/层级流程；最后给出练习与要点总结。

---

## 4.1 AutoGen Studio：零代码体验多代理

### 4.1.1 安装与上手
1. 打开 `chapter_04` 目录，按附录 B 配好 Python 虚拟环境并安装 `requirements.txt`。
2. 在终端里设置 OpenAI Key 并启动 Studio（Listing 4.1）：
   ```bash
   export OPENAI_API_KEY="<你的 API Key>"
   autogenstudio ui --port 8081
   ```
   端口若冲突，可改成 8082 等。
3. 浏览器访问 `http://localhost:8081`。**Playground** 标签用于对话，**Build** 创建代理/技能，**Gallery** 回顾历史最佳输出。
4. 在输入框里给出复杂任务，例如 “Create a plot showing the popularity of the term GPT Agents in Google search.”，观察 UserProxy 如何分配子任务，Assistant 如何写代码，Proxy 再执行、评估并循环迭代（图 4.2、4.3、4.4）。
5. 若代码执行出错，可提示 Proxy 换方法；如需要更稳定的沙箱，官方推荐用 Docker 跑 Studio/AutoGen。

### 4.1.2 在 Studio 里添加技能
1. 切到 **Build → Skills**，点击 **New Skill**。
2. 把 `describe_image.py`（Listing 4.2）贴进去。该函数用 GPT-4 Turbo Vision 解析本地图像内容，可用于检查图片是否符合要求。
3. 在 **Build → Workflows** 中，选择默认的 `general` 工作流，编辑 `primary_assistant`，把 `describe_image` 技能加入。
4. 回到 Playground，输入（Listing 4.3）：
   > “Please create a cover for the book *GPT Agents in Action*, use the describe_image skill to ensure the title is spelled correctly.”
5. 助手会调用已有的 `generate_image` 技能生成封面，再用新建技能验证标题。图 4.6、4.7 展示了工作流配置与产出。

这种“写技能 → 加入工作流 → 通过语言触发”的模式，是 AutoGen Studio 最强的迭代路径之一。

---

## 4.2 AutoGen SDK：在代码层自定义代理

### 4.2.1 基础安装与 Hello World
1. 安装核心库：`pip install pyautogen`（Listing 4.4）。
2. 复制 `chapter_04/OAI_CONFIG_LIST.example` 为 `OAI_CONFIG_LIST`，填写模型/Key/Base URL 等配置（Listing 4.5）。可同时配置 OpenAI 与 Azure；凡是支持 OpenAI API 协议的服务（LM Studio、Groq 等）也可写入。
3. 查看 `autogen_start.py`（Listing 4.6）：
   - `ConversableAgent`：真正调用 LLM 的助手。
   - `UserProxyAgent`：代表人类，负责执行代码、提供反馈、判断何时 `TERMINATE`。
4. 运行脚本（F5），在终端输入简单的编程任务（Listing 4.7 如“一行写完 FizzBuzz”“写贪吃蛇”等）。Proxy 会自动执行生成的 Python 代码，并把源码写入 `working/` 目录以供复查。

### 4.2.2 引入 Reviewer 批改代码
- `autogen_coding_critic.py`（Listing 4.8）增加了第二个 `AssistantAgent`——Reviewer。
- 通过 `register_nested_chats`，当 Engineer 完成代码后自动触发 Reviewer 嵌套对话，调用 `review_code()` 读取最新代码并给出改进建议。
- 这种多角色结构让“写代码 + code review + 迭代”自动化完成。

### 4.2.3 理解缓存
- AutoGen 默认在工作目录创建 `.cache/`（SQLite）保存对话。
- 使用 `with Cache.disk(cache_seed=42)` 包裹 `initiate_chat`（Listing 4.9）可指定缓存文件，支持长任务暂停续跑、复现结果或分析历史对话。

---

## 4.3 群聊：让代理共享上下文

- 嵌套对话易造成“传话游戏”式失真。`autogen_coding_group.py`（Listing 4.10）展示 `GroupChat` + `GroupChatManager`：
  - `GroupChat` 持有多个代理与会话消息，像 Slack/Discord 频道。
  - Manager 负责指定谁在下一轮发言、避免重复。
  - 将 `human_input_mode` 设为 `NEVER`，实现完全自动协作。
- 运行后，工程师与 Reviewer 在群里同步讨论，Proxy 也能读全程记录。代价是 token 消耗更高，但协作质量显著提升。

---

## 4.4 CrewAI：面向企业的多代理框架

CrewAI 把多代理系统拆成“Agent + Task + Process + Memory/Tools”，默认不需要 UserProxy。它支持顺序（sequential）与层级（hierarchical）两种流程。

### 4.4.1 Jokester Crew：段子手小队
1. `crewai_introduction.py` 定义两个代理（Listing 4.11）：
   - **Senior Joke Researcher**：负责搜集题材笑点，可委派任务。
   - **Joke Writer**：根据研究成果写笑话。
2. 每个代理绑定 `Task`（Listing 4.12）：
   - `research_task`：输出 3 段报告 + 社会趋势分析。
   - `write_task`：写最终笑话，保存到 `the_best_joke.md`。
3. 用 `Crew(..., process=Process.sequential)` 组队（Listing 4.13），`crew.kickoff(inputs={"topic": "AI engineer jokes"})` 即可看到两位“段子手”在线合作，终端会输出多条机智回应。

### 4.4.2 加入 AgentOps 观测
1. 安装依赖：`pip install agentops` 或 `pip install crewai[agentops]`（Listing 4.14）。
2. 在 AgentOps 网站申请 API Key，写入 `.env`（Listing 4.15）。
3. 在脚本里 `import agentops` 并 `agentops.init()`（Listing 4.16）。
4. 运行 `crewai_agentops.py`，即可在仪表盘看到每次 GPT 调用的耗时、token、成本、日志、系统环境等（图 4.11）。

AgentOps 能同时接入 AutoGen/CrewAI 等多种框架，帮助追踪高成本或重复思考（Repeat Thoughts）等问题。

---

## 4.5 CrewAI 编码小队：顺序 vs 层级

### 4.5.1 顺序流程
1. `crewai_coding_crew.py` 定义三名代理（Listing 4.17）：
   - **Senior Engineer**：写代码。
   - **QA Engineer**：检查语法、逻辑、依赖。
   - **Chief QA Engineer**：最终审查，必要时可委派。
2. 任务（Listing 4.18）：
   - `code_task`：基于用户输入的游戏说明编写 Python 代码，并只输出最终代码。
   - `qa_task`：列出发现的问题。
   - `evaluate_task`：输出修正后的完整代码。
3. `Crew(..., process=Process.sequential)` 顺序执行（Listing 4.19）。运行脚本后输入想做的游戏（如贪吃蛇），观察三名角色如何串行协作。

### 4.5.2 层级流程
- `crewai_hierarchy.py` 把 `process` 换成 `Process.hierarchical`，并用 `manager_llm=ChatOpenAI(model="gpt-4", temperature=0)`（Listing 4.20）。
- 这时多了一个“Crew Manager”协调各 Agent，整体表现更像“项目经理 + 组员”结构。
- 搭配 AgentOps 的 Repeat Thoughts 图（图 4.13，可在原书看到完整页），能监控代理是否陷入重复尝试，必要时调整流程或提示。

层级调度适合复杂任务：Manager 负责拆解/调度，成员专注于执行；缺点是开销更高。

---

## 4.6 练习
1. **练习 1：AutoGen 基础通讯**——在 Studio 中搭建 UserProxy + 两个助手，让他们合写一段摘要。
2. **练习 2：扩展技能**——为 AutoGen 写一个可调用公开 API 的技能（例如天气/股价查询），让代理根据用户偏好返回实时信息。
3. **练习 3：CrewAI 角色分工**——设计“数据抓取→分析→报告”三段任务，观察信息如何在代理间传递。
4. **练习 4：AutoGen 群聊协作**——设定“出差行程规划”等复杂任务，启用 GroupChat 观察多代理讨论的过程与成果。
5. **练习 5：AgentOps 观测**——在 CrewAI 项目里集成 AgentOps，挑选一个耗时/高算力任务，分析性能、成本与潜在瓶颈。

---

## 本章小结
- **AutoGen**：微软推出的对话式多代理平台，提供 Studio GUI 与 Python SDK。UserProxy 负责执行/评估，Assistant 负责生成，可通过技能扩展图像/代码/数据等能力。
- **多种通讯模式**：AutoGen 支持代理链式/嵌套对话、群聊与层级代理；通过缓存和 Docker 隔离可提升稳定性。
- **CrewAI**：更偏企业级，强调角色/任务/流程配置，支持顺序或层级处理，易于把工具、记忆（RAG）、API 调用装配到各 Agent。
- **可观测性**：AgentOps 等平台可记录对话、成本、token、重复思考次数，是大规模部署代理时必备的“度量仪表”。
- **实践范式**：不论 AutoGen 还是 CrewAI，最佳体验都来自“明确定义 persona + 指令 + 工具 + 反馈”，并在必要时引入代码审查、群聊协作或层级调度。
- **成本意识**：多代理迭代能带来更高质量，也可能快速推高 token 花费。务必借助缓存/观测/流程优化控制成本。

下一章将把注意力转向“赋予代理行动能力”，继续完善你的 AI Agent 工程 toolbox。
