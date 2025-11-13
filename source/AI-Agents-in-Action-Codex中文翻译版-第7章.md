# AI-Agents-in-Action-Codex中文翻译版-第7章

## 第7章 搭建并使用代理平台

本章围绕开源教育平台 **Nexus** 展开，讲解如何组合人格（persona）、工具、记忆与规划，构建可调试、可扩展的聊天代理。我们先介绍 Nexus 的安装与开发模式，再用 Streamlit 打造 ChatGPT 式界面；随后编写新的 agent profile、接入自定义动作与工具，最后用练习与总结梳理要点。

---

## 7.1 Nexus 平台简介

Nexus 结合 Streamlit + OpenAI API，提供一个“所见即所得”的代理实验环境。界面允许用户自由选择：
- **Persona/Profile**：系统提示、语气、角色定位。
- **Actions/Tools**：语义函数或本地代码函数，驱动代理执行外部操作。
- **Memory/Knowledge/Planning**：未来章节逐步开放，用于扩展上下文、反馈与评估能力。

### 7.1.1 快速运行 Nexus
1. 准备 Python 3.10 虚拟环境。
2. 运行：
   ```bash
   pip install git+https://github.com/cxbxmxcx/Nexus.git
   export OPENAI_API_KEY="<你的 API Key>"   # Linux/Mac
   # Windows PowerShell 用：$env:OPENAI_API_KEY="<key>"
   # 或写入 .env：echo 'OPENAI_API_KEY="<key>"' > .env
   nexus run
   ```
3. 浏览器自动打开登录页（图 7.2）。首次使用选择 “Create New User”，之后可直接用 cookies 自动登录。
4. 进入主界面（类似图 7.1），新建聊天即可体验默认代理。

### 7.1.2 开发模式
- 为了调试/二次开发，建议直接克隆仓库：
  ```bash
  git clone https://github.com/cxbxmxcx/Nexus.git
  pip install -e Nexus
  export OPENAI_API_KEY="<你的 API Key>"
  nexus run
  ```
- 可在 VS Code 中创建 `.vscode/launch.json`，以 `streamlit` 模式（module）调试 `Nexus/nexus/streamlit_ui.py`。
- Nexus 结构（图 7.4）：Streamlit 界面 ↔ Chat System ↔ Agent Manager / Profile Manager / Action Manager / 数据库。agent、profile、action 均通过插件机制动态发现。

---

## 7.2 Streamlit：快速打造聊天界面

### 7.2.1 构建 ChatGPT clone
- 文件 `chatgpt_clone_response.py` 展示最小可用的聊天应用：
  - `st.session_state` 存储模型名与对话历史。
  - `st.chat_message` 循环渲染历史消息。
  - `st.chat_input` 捕获用户输入；当用户提交时，追加到 `session_state` 并调用 `client.chat.completions.create(...)`。
  - `st.spinner` 提示“LLM 正在思考”。
- 调试方法：在 VS Code 中配置 `launch.json`，使用 `"module": "streamlit", "args": ["run", "${file}"]`，按 F5 即可。界面如图 7.5。

### 7.2.2 加入流式输出
- `chatgpt_clone_streaming.py` 将 `stream=True`，并用 `st.write_stream(stream)` 边接收边展示（图 7.6），无需再显示 spinner。
- 这个例子证明：Streamlit 允许开发者纯用 Python 构建现代化的聊天 UI，后续 Nexus 亦沿用这一模式。

---

## 7.3 在 Nexus 中定义 Profiles / Personas
- Profile 通过 `nexus/nexus_base/nexus_profiles/*.yaml` 描述，包含：名称、头像符号、persona 文案、可用动作等（图 7.7）。
- 示例 `fiona.yaml`：
  ```yaml
  agentProfile:
    name: "Finona"
    avatar: "?"
    persona: "你是一个健谈、用食人魔语言回答一切问题的 AI。"
    actions:
      - search_wikipedia
    knowledge: null
    memory: null
    evaluators: null
    planners: null
    feedback: null
  ```
- 保存后重启 Nexus，即可在界面选择新 persona（图 7.8）。profile 实际上就是系统提示 + 动作声明，决定代理如何开场、如何回应。

---

## 7.4 Agent Engine 的结构
- 所有代理引擎继承自 `BaseAgent`（位于 `nexus_base/agent_manager.py`），实现：加载 persona、拼接消息、调用底层 LLM、处理工具调用等。
- 目前示例为 `OpenAIAgent`，核心流程（节选自 `oai_agent.py`）：
  1. 将用户输入写入 `self.messages`。
  2. 若启用了工具，则在 `chat.completions.create` 中附上 `tools` 列表与 `tool_choice="auto"`。
  3. 拿到 `response_message.tool_calls` 后，遍历每个函数调用，反射执行实际 Python 函数，再把结果写回消息堆栈。
  4. 再次请求 LLM 生成最终回答。
- 由于采用插件机制，未来可轻松添加“基于 SK 的 agent”“Anthropic agent”等实现，只需放入 `nexus_agents/` 目录即可被发现。

---

## 7.5 为代理添加动作与工具
- 所有动作放在 `nexus/nexus_base/nexus_actions/`，以普通 Python 函数形式存在。
- 通过 `@agent_action` 装饰器注册：
  ```python
  from nexus.nexus_base.action_manager import agent_action

  @agent_action
  def get_current_weather(location, unit="fahrenheit"):
      """获取指定地点的天气"""
      return f"当前 {location} 的气温是 0 {unit}."

  @agent_action
  def recommend(topic):
      """
      System:
        Provide a recommendation for {{topic}} …
      User:
        please …
      """
      pass  # 语义函数只需写提示模板
  ```
- 装饰器负责生成符合 OpenAI Functions 规范的 `tool` 描述（Listing 7.12），包括参数类型、枚举、描述等。
- Nexus 的 OpenAI agent 支持 **并行** 函数调用：LLM 可一次返回多个 `tool_call`，引擎逐个执行并合并结果（Listing 7.13、7.14）。
- Demo：在 Nexus 中选中 persona “Olly”（冷淡语气），启用 `recommend` + `get_current_weather` 两个动作，即可看到代理在一次回复中串联两个工具（图 7.9）。

---

## 7.6 练习
1. **Streamlit 入门**：写一个最简单的输入框 + 按钮页面，点击后把文本显示出来。
2. **创建自定义 persona**：在 Nexus 中新增一个主题鲜明的 profile（如“历史学家”），编写符合 persona 的回答，并在界面实际对话测试。
3. **开发自定义 action**：新增一个动作（如 `fetch_current_news`），分别做成本地函数和语义函数两个版本，集成后在 Nexus 内调用验证。
4. **接入第三方 API**：挑选任意公开接口（天气/新闻等），实现含错误处理的 action，并在 Nexus 中测试其稳健性。

---

## 本章小结
- **Nexus**：本书配套的开源代理实验平台，以 Streamlit 提供聊天 UI，可扩展 profile、action、agent 引擎等。
- **Streamlit**：让 Python 开发者快速构建交互式聊天页面，支持状态管理、流式输出、云部署等特性。
- **Profiles/Personas**：通过 YAML 描述代理身份、语气与可用动作，是塑造代理行为的基础。
- **Actions/Tools**：Nexus 同时支持语义函数与本地函数，借助 OpenAI Function 规范在 LLM 中被调用，可并行执行。
- **可扩展性**：凭借插件架构，任何人都能轻松新增 agent、profile、action；未来还将覆盖 API、Discord Bot 等部署形态。

下一章将继续深化代理能力，探讨如何为代理加入检索式记忆与知识库。
