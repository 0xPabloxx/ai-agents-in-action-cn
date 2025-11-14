# Chapter 7: Assembling and using an agent platform | <mark>第7章：组装和使用智能体平台</mark>

## This chapter covers | <mark>本章内容</mark>

- Introducing Nexus, an agent development platform | <mark>介绍 Nexus 智能体开发平台</mark>
- Building chat applications with Streamlit | <mark>使用 Streamlit 构建聊天应用</mark>
- Developing agent profiles and personas | <mark>开发智能体配置文件和人设</mark>
- Understanding the agent engine architecture | <mark>理解智能体引擎架构</mark>
- Implementing agent actions and tools | <mark>实现智能体动作和工具</mark>

---

## 7.1 Introducing Nexus, not just another agent platform

<mark>## 7.1 介绍 Nexus：不只是另一个智能体平台</mark>

In previous chapters, we've explored various agent frameworks and platforms. Each has strengths and weaknesses, and understanding how they work helps build better agents. In this chapter, we introduce Nexus, an open-source agent development platform specifically designed to accompany this book.

<mark>在之前的章节中，我们探索了各种智能体框架和平台。每个平台都有其优势和劣势，理解它们的工作原理有助于构建更好的智能体。在本章中，我们介绍 Nexus，这是一个专门为本书设计的开源智能体开发平台。</mark>

Nexus is built around the core agent components we've discussed throughout this book:

<mark>Nexus 围绕我们在本书中讨论的核心智能体组件构建：</mark>

- **Persona/profile** — Represents the agent's background and role, often introduced in the first system message. Personas/profiles can define everything from personality traits to specific domain expertise. We'll look in this chapter at how personas/profiles can be developed and consumed.

<mark>- **人设/配置文件（Persona/profile）** — 代表智能体的背景和角色，通常在第一条系统消息中引入。人设/配置文件可以定义从个性特征到特定领域专业知识的所有内容。在本章中，我们将探讨如何开发和使用人设/配置文件。</mark>

- **Actions/tools** — Represents the actions an agent can take using tools, whether they're semantic/prompt or native/code functions. In this chapter, we'll look at how to build both semantic and native functions within Nexus.

<mark>- **动作/工具（Actions/tools）** — 代表智能体可以使用工具执行的动作，无论是语义/提示函数还是原生/代码函数。在本章中，我们将探讨如何在 Nexus 中构建语义函数和原生函数。</mark>

- **Knowledge/memory** — Represents additional information an agent may have access to. At the same time, agent memory can represent various aspects, from short-term to semantic memory.

<mark>- **知识/记忆（Knowledge/memory）** — 代表智能体可能访问的附加信息。同时，智能体记忆可以代表各种方面，从短期记忆到语义记忆。</mark>

- **Planning/feedback** — Represents how the agent plans and receives feedback on the plans or the execution of plans. Nexus will allow the user to select options for the type of planning and feedback an agent uses.

<mark>- **规划/反馈（Planning/feedback）** — 代表智能体如何规划并接收关于计划或计划执行的反馈。Nexus 将允许用户选择智能体使用的规划和反馈类型的选项。</mark>

As we progress through this book, Nexus will be added to support new agent features. However, simultaneously, the intent will be to keep things relatively simple to teach many of these essential core concepts. In the next section, we'll look at how to quickly use Nexus before going under the hood to explore features in detail.

<mark>随着本书的深入，Nexus 将添加支持新的智能体功能。然而，同时，我们的目标是保持相对简单，以教授许多这些核心概念。在下一节中，我们将探讨如何快速使用 Nexus，然后深入探索其功能细节。</mark>

---

### 7.1.1 Running Nexus

<mark>### 7.1.1 运行 Nexus</mark>

Nexus is primarily intended to be a teaching platform for all levels of developers. As such, it will support various deployment and usage options. In the next exercise, we'll introduce how to get up and running with Nexus quickly.

<mark>Nexus 主要旨在成为面向所有级别开发者的教学平台。因此，它将支持各种部署和使用选项。在下一个练习中，我们将介绍如何快速启动和运行 Nexus。</mark>

Open a terminal to a new Python virtual environment (version 3.10). If you need assistance creating one, refer to appendix B. Then, execute the commands shown in listing 7.1 within this new environment. You can either set the environment variable at the command line or create a new .env file and add the setting.

<mark>打开一个新的 Python 虚拟环境（版本 3.10）的终端。如果需要帮助创建虚拟环境，请参考附录 B。然后，在这个新环境中执行列表 7.1 中显示的命令。你可以在命令行设置环境变量，或者创建一个新的 .env 文件并添加设置。</mark>

**Listing 7.1 Terminal command line** | <mark>**列表 7.1 终端命令行**</mark>

```bash
pip install git+https://github.com/cxbxmxcx/Nexus.git    # Installs the package directly from the repository and branch; be sure to include the branch.

# set your OpenAI API Key
export OPENAI_API_KEY="<your API key>"         # Creates the key as an environment variable
# or
$env:OPENAI_API_KEY="<your API key>"          # PowerShell
# or
echo 'OPENAI_API_KEY="<your API key>"' > .env # Creates a new .env file with the setting

nexus run     # Runs the application
```

<mark>```bash
pip install git+https://github.com/cxbxmxcx/Nexus.git    # 直接从仓库和分支安装包；确保包含分支。

# 设置你的 OpenAI API 密钥
export OPENAI_API_KEY="<your API key>"         # 将密钥创建为环境变量
# 或
$env:OPENAI_API_KEY="<your API key>"          # PowerShell
# 或
echo 'OPENAI_API_KEY="<your API key>"' > .env # 创建一个新的 .env 文件并添加设置

nexus run     # 运行应用程序
```</mark>

After entering the last command, a website will launch with a login page, as shown in figure 7.2. Go ahead and create a new user. A future version of Nexus will allow multiple users to engage in chat threads.

<mark>输入最后一条命令后，将启动一个带有登录页面的网站，如图 7.2 所示。继续创建一个新用户。Nexus 的未来版本将允许多个用户参与聊天线程。</mark>

After you log in, you'll see a page like figure 7.1. Create a new chat and start conversing with an agent. If you encounter a problem, be sure you have the API key set properly. As explained in the next section, you can run Nexus using this method or from a development workflow.

<mark>登录后，你将看到类似图 7.1 的页面。创建一个新的聊天并开始与智能体对话。如果遇到问题，请确保正确设置了 API 密钥。如下一节所述，你可以使用这种方法运行 Nexus，或者从开发工作流运行。</mark>

**Figure 7.2 Logging in or creating a new Nexus user** | <mark>**图 7.2 登录或创建新的 Nexus 用户**</mark>

<mark>*图片描述：登录或创建新用户界面，包含以下元素：*</mark>
- Select Create New User to start. | <mark>选择"创建新用户"开始。</mark>
- Username is used to track conversation history in the threads. | <mark>用户名用于跟踪线程中的对话历史。</mark>

---

### 7.1.2 Developing Nexus

<mark>### 7.1.2 开发 Nexus</mark>

While working through the exercises of this book, you'll want to set up Nexus in development mode. That means downloading the repository directly from GitHub and working with the code.

<mark>在完成本书练习的过程中，你需要以开发模式设置 Nexus。这意味着直接从 GitHub 下载仓库并使用代码。</mark>

Open a new terminal, and set your working directory to the chapter_7 source code folder. Then, set up a new Python virtual environment (version 3.10) and enter the commands shown in listing 7.2. Again, refer to appendix B if you need assistance with any previous setup.

<mark>打开一个新的终端，并将工作目录设置为 chapter_7 源代码文件夹。然后，设置一个新的 Python 虚拟环境（版本 3.10）并输入列表 7.2 中显示的命令。如果需要帮助进行任何先前的设置，请参考附录 B。</mark>

**Listing 7.2 Installing Nexus for development** | <mark>**列表 7.2 为开发安装 Nexus**</mark>

```bash
git clone https://github.com/cxbxmxcx/Nexus.git     # Downloads and installs the specific branch from the repository
pip install -e Nexus                                 # Installs the downloaded repository as an editable package

# set your OpenAI API Key (.env file is recommended)
export OPENAI_API_KEY="<your API key>"  # bash
# or
$env:OPENAI_API_KEY="<your API key>"    # powershell
# or
echo 'OPENAI_API_KEY="<your API key>"' > .env

nexus run                                            # Starts the application
```

<mark>```bash
git clone https://github.com/cxbxmxcx/Nexus.git     # 从仓库下载并安装特定分支
pip install -e Nexus                                 # 将下载的仓库安装为可编辑包

# 设置你的 OpenAI API 密钥（推荐使用 .env 文件）
export OPENAI_API_KEY="<your API key>"  # bash
# 或
$env:OPENAI_API_KEY="<your API key>"    # powershell
# 或
echo 'OPENAI_API_KEY="<your API key>"' > .env

nexus run                                            # 启动应用程序
```</mark>

Figure 7.3 shows the Login or Create New User screen. Create a new user, and the application will log you in. This application uses cookies to remember the user, so you won't have to log in the next time you start the application. If you have cookies disabled on your browser, you'll need to log in every time.

<mark>图 7.3 显示了"登录或创建新用户"屏幕。创建一个新用户，应用程序将让你登录。此应用程序使用 cookies 记住用户，因此下次启动应用程序时无需登录。如果在浏览器中禁用了 cookies，则每次都需要登录。</mark>

Go to the Nexus repository folder and look around. Figure 7.4 shows an architecture diagram of the application's main elements. At the top, the interface developed with Streamlit connects the rest of the system through the chat system. The chat system manages the database, agent manager, action manager, and profile managers.

<mark>转到 Nexus 仓库文件夹并查看。图 7.4 显示了应用程序主要元素的架构图。在顶部，使用 Streamlit 开发的界面通过聊天系统连接系统的其余部分。聊天系统管理数据库、智能体管理器、动作管理器和配置文件管理器。</mark>

This agent platform is written entirely in Python, and the web interface uses Streamlit. In the next section, we look at how to build an OpenAI LLM chat application.

<mark>这个智能体平台完全用 Python 编写，Web 界面使用 Streamlit。在下一节中，我们将探讨如何构建 OpenAI LLM 聊天应用程序。</mark>

**Figure 7.3 The Login or Create New User page** | <mark>**图 7.3 登录或创建新用户页面**</mark>

<mark>*图片描述：登录或创建新用户页面，包含以下元素：*</mark>
- The browser points to localhost:8501, which is the default for Streamlit apps. | <mark>浏览器指向 localhost:8501，这是 Streamlit 应用程序的默认端口。</mark>
- Streamlit apps can be deployed to the cloud using this option. | <mark>Streamlit 应用程序可以使用此选项部署到云端。</mark>
- Fill in the username, pick an avatar, and set a password or choose a browser-generated one. | <mark>填写用户名，选择头像，设置密码或选择浏览器生成的密码。</mark>

**Figure 7.4 A high-level architecture diagram of the main elements of the application** | <mark>**图 7.4 应用程序主要元素的高级架构图**</mark>

<mark>*图片描述：Nexus 应用架构图，包含以下组件：*</mark>

- Streamlit Interface | <mark>Streamlit 界面</mark>
  - The chat interface allows the user to select from various discovered agents, actions, and profiles, enabling the user to test different combinations. | <mark>聊天界面允许用户从各种发现的智能体、动作和配置文件中进行选择，使用户能够测试不同的组合。</mark>

- Chat system | <mark>聊天系统</mark>

- Nexus database | <mark>Nexus 数据库</mark>
  - The database stores chat threads, user participants, and conversation history. | <mark>数据库存储聊天线程、用户参与者和对话历史。</mark>

- Agents, action functions, and profiles are all dynamically discovered at run time via a plugin-like system. | <mark>智能体、动作函数和配置文件都通过类似插件的系统在运行时动态发现。</mark>

- Agent Manager | <mark>智能体管理器</mark>
  - Agent classes exposed as plugins | <mark>作为插件公开的智能体类</mark>

- Action Manager | <mark>动作管理器</mark>
  - Semantic and native functions exposed as actions | <mark>作为动作公开的语义函数和原生函数</mark>

- Profile Manager | <mark>配置文件管理器</mark>
  - A YAML file that comprises the agent profile and persona | <mark>包含智能体配置文件和人设的 YAML 文件</mark>

- GPT Nexus | <mark>GPT Nexus</mark>

---

## 7.2 Introducing Streamlit for chat application development

<mark>## 7.2 介绍 Streamlit 用于聊天应用开发</mark>

Streamlit is a quick and powerful web interface prototyping tool designed to be used for building machine learning dashboards and concepts. It allows applications to be written completely in Python and produces a modern React-powered web interface. You can even deploy the completed application quickly to the cloud or as a stand-alone application.

<mark>Streamlit 是一个快速而强大的 Web 界面原型工具，专为构建机器学习仪表板和概念而设计。它允许完全用 Python 编写应用程序，并生成一个由 React 驱动的现代 Web 界面。你甚至可以快速将完成的应用程序部署到云端或作为独立应用程序。</mark>

---

### 7.2.1 Building a Streamlit chat application

<mark>### 7.2.1 构建 Streamlit 聊天应用</mark>

Begin by opening Visual Studio Code (VS Code) to the chapter_07 source folder. If you've completed the previous exercise, you should already be ready. As always, if you need assistance setting up your environment and tools, refer to appendix B.

<mark>首先打开 Visual Studio Code（VS Code）并转到 chapter_07 源文件夹。如果你已完成前面的练习，应该已经准备好了。与往常一样，如果需要帮助设置环境和工具，请参考附录 B。</mark>

We'll start by opening the chatgpt_clone_response.py file in VS Code. The top section of the code is shown in listing 7.3. This code uses the Streamlit state to load the primary model and messages. Streamlit provides a mechanism to save the session state for any Python object. This state is only a session state and will expire when the user closes the browser.

<mark>我们将从在 VS Code 中打开 chatgpt_clone_response.py 文件开始。代码的顶部部分显示在列表 7.3 中。此代码使用 Streamlit 状态来加载主要模型和消息。Streamlit 提供了一种机制来保存任何 Python 对象的会话状态。此状态仅是会话状态，当用户关闭浏览器时将过期。</mark>

**Listing 7.3 chatgpt_clone_response.py (top section)** | <mark>**列表 7.3 chatgpt_clone_response.py（顶部部分）**</mark>

```python
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()     # Loads the environment variables from the .env file

st.title("ChatGPT-like clone")

client = OpenAI()     # Configures the OpenAI client

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-1106-preview"    # Checks the internal session state for the setting, and adds it if not there

if "messages" not in st.session_state:
    st.session_state["messages"] = []  # Checks for the presence of the message state; if none, adds an empty list

for message in st.session_state["messages"]:     # Loops through messages in the state and displays them
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
```

<mark>```python
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()     # 从 .env 文件加载环境变量

st.title("ChatGPT-like clone")

client = OpenAI()     # 配置 OpenAI 客户端

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-1106-preview"    # 检查内部会话状态中的设置，如果不存在则添加

if "messages" not in st.session_state:
    st.session_state["messages"] = []  # 检查消息状态是否存在；如果没有，添加一个空列表

for message in st.session_state["messages"]:     # 循环遍历状态中的消息并显示它们
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
```</mark>

The Streamlit app itself is stateless. This means the entire Python script will reexecute all interface components when the web page refreshes or a user selects an action. The Streamlit state allows for a temporary storage mechanism. Of course, a database needs to support more long-term storage.

<mark>Streamlit 应用本身是无状态的。这意味着当网页刷新或用户选择操作时，整个 Python 脚本将重新执行所有界面组件。Streamlit 状态允许临时存储机制。当然，数据库需要支持更长期的存储。</mark>

UI controls and components are added by using the st. prefix and then the element name. Streamlit supports several standard UI controls and supports images, video, sound, and, of course, chat.

<mark>通过使用 st. 前缀然后是元素名称来添加 UI 控件和组件。Streamlit 支持多个标准 UI 控件，并支持图像、视频、声音，当然还有聊天。</mark>

Scrolling down further will yield listing 7.4, which has a slightly more complex layout of the components. The main if statement controls the running of the remaining code. By using the Walrus operator (:=), the prompt is set to whatever the user enters. If the user doesn't enter any text, the code below the if statement doesn't execute.

<mark>继续向下滚动将得到列表 7.4，它具有稍微复杂的组件布局。主 if 语句控制剩余代码的运行。通过使用海象运算符（:=），提示被设置为用户输入的任何内容。如果用户没有输入任何文本，if 语句下面的代码不会执行。</mark>

**Listing 7.4 chatgpt_clone_response.py (bottom section)** | <mark>**列表 7.4 chatgpt_clone_response.py（底部部分）**</mark>

```python
if prompt := st.chat_input("What do you need?"):    # The chat input control is rendered, and content is set.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):    # Sets the chat message control to output as the user
        st.markdown(prompt)

    with st.spinner(text="The assistant is thinking..."):   # Shows a spinner to represent the long-running API call
        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],     # Calls the OpenAI API and sets the message history
            )
            response_content = response.choices[0].message.content
            response = st.markdown(response_content,
             unsafe_allow_html=True)     # Writes the message response as markdown to the interface
    st.session_state.messages.append(
{"role": "assistant", "content": response_content})     # Adds the assistant response to the message state
```

<mark>```python
if prompt := st.chat_input("What do you need?"):    # 渲染聊天输入控件，并设置内容。
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):    # 将聊天消息控件设置为用户输出
        st.markdown(prompt)

    with st.spinner(text="The assistant is thinking..."):   # 显示一个旋转器以表示长时间运行的 API 调用
        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],     # 调用 OpenAI API 并设置消息历史
            )
            response_content = response.choices[0].message.content
            response = st.markdown(response_content,
             unsafe_allow_html=True)     # 将消息响应作为 markdown 写入界面
    st.session_state.messages.append(
{"role": "assistant", "content": response_content})     # 将助手响应添加到消息状态
```</mark>

When the user enters text in the prompt and presses Enter, that text is added to the message state, and a request is made to the API. As the response is being processed, the st.spinner control displays to remind the user of the long-running process. Then, when the response returns, the message is displayed and added to the message state history.

<mark>当用户在提示中输入文本并按 Enter 键时，该文本被添加到消息状态，并向 API 发出请求。在处理响应时，st.spinner 控件显示以提醒用户长时间运行的过程。然后，当响应返回时，消息被显示并添加到消息状态历史中。</mark>

Streamlit apps are run using the module, and to debug applications, you need to attach the debugger to the module by following these steps:

<mark>Streamlit 应用使用模块运行，要调试应用程序，你需要按照以下步骤将调试器附加到模块：</mark>

1. Press Ctrl-Shift-D to open the VS Code debugger.
2. Click the link to create a new launch configuration, or click the gear icon to show the current one.
3. Edit or use the debugger configuration tools to edit the .vscode/launch.json file, like the one shown in the next listing. Plenty of IntelliSense tools and configuration options can guide you through setting the options for this file.

<mark>1. 按 Ctrl-Shift-D 打开 VS Code 调试器。
2. 单击链接创建新的启动配置，或单击齿轮图标显示当前配置。
3. 编辑或使用调试器配置工具编辑 .vscode/launch.json 文件，如下一个列表所示。大量的 IntelliSense 工具和配置选项可以指导你设置此文件的选项。</mark>

**Listing 7.5 .vscode/launch.json** | <mark>**列表 7.5 .vscode/launch.json**</mark>

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python Debugger: Module",    // Make sure that the debugger is set to Module.
      "type": "debugpy",
      "request": "launch",
      "module": "streamlit",    // Be sure the module is streamlit.
      "args": ["run", "${file}"]   // The ${file} is the current file, or you can hardcode this to a file path.
    }
  ]
}
```

<mark>```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python Debugger: Module",    // 确保调试器设置为 Module。
      "type": "debugpy",
      "request": "launch",
      "module": "streamlit",    // 确保模块是 streamlit。
      "args": ["run", "${file}"]   // ${file} 是当前文件，或者你可以将其硬编码为文件路径。
    }
  ]
}
```</mark>

After you have the launch.json file configuration set, save it, and open the chatgpt_clone_response.py file in VS Code. You can now run the application in debug mode by pressing F5. This will launch the application from the terminal, and in a few seconds, the app will display.

<mark>设置好 launch.json 文件配置后，保存它，并在 VS Code 中打开 chatgpt_clone_response.py 文件。你现在可以通过按 F5 在调试模式下运行应用程序。这将从终端启动应用程序，几秒钟后，应用程序将显示。</mark>

Figure 7.5 shows the app running and waiting to return a response. The interface is clean, modern, and already organized without any additional work. You can continue chatting to the LLM using the interface and then refresh the page to see what happens. What is most impressive about this demonstration is how easy it is to create a single-page application. In the next section, we'll continue looking at this application but with a few enhancements.

<mark>图 7.5 显示了正在运行并等待返回响应的应用程序。界面干净、现代，无需任何额外工作即已组织好。你可以继续使用界面与 LLM 聊天，然后刷新页面看看会发生什么。这个演示最令人印象深刻的是创建单页应用程序是多么容易。在下一节中，我们将继续查看此应用程序，但会进行一些增强。</mark>

**Figure 7.5 The simple interface and the waiting spinner** | <mark>**图 7.5 简单界面和等待旋转器**</mark>

<mark>*图片描述：简单的聊天界面，显示：*</mark>
- A spinner control displays while the response is being returned. | <mark>在返回响应时显示旋转器控件。</mark>

---

### 7.2.2 Creating a streaming chat application

<mark>### 7.2.2 创建流式聊天应用</mark>

Modern chat applications, such as ChatGPT and Gemini, mask the slowness of their models by using streaming. Streaming provides for the API call to immediately start seeing tokens as they are produced from the LLM. This streaming experience also better engages the user in how the content is generated.

<mark>现代聊天应用程序，如 ChatGPT 和 Gemini，通过使用流式传输来掩盖其模型的缓慢。流式传输使 API 调用能够立即开始看到从 LLM 生成的 token。这种流式体验也更好地让用户参与内容的生成方式。</mark>

Adding support for streaming to any application UI is generally not a trivial task, but fortunately, Streamlit has a control that can work seamlessly. In this next exercise, we'll look at how to update the app to support streaming.

<mark>为任何应用程序 UI 添加流式传输支持通常不是一项简单的任务，但幸运的是，Streamlit 有一个可以无缝工作的控件。在下一个练习中，我们将探讨如何更新应用程序以支持流式传输。</mark>

Open chapter_7/chatgpt_clone_streaming.py in VS Code. The relevant updates to the code are shown in listing 7.6. Using the st.write_stream control allows the UI to stream content. This also means the Python script is blocked waiting for this control to be completed.

<mark>在 VS Code 中打开 chapter_7/chatgpt_clone_streaming.py。代码的相关更新显示在列表 7.6 中。使用 st.write_stream 控件允许 UI 流式传输内容。这也意味着 Python 脚本被阻塞等待此控件完成。</mark>

**Listing 7.6 chatgpt_clone_streaming.py (relevant section)** | <mark>**列表 7.6 chatgpt_clone_streaming.py（相关部分）**</mark>

```python
with st.chat_message("assistant"):
    stream = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,    # Sets stream to True to initiate streaming on the API
    )
    response = st.write_stream(stream)    # Uses the stream control to write the stream to the interface
st.session_state.messages.append(
{"role": "assistant", "content": response})     # Adds the response to the message state history after the stream completes
```

<mark>```python
with st.chat_message("assistant"):
    stream = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,    # 将 stream 设置为 True 以在 API 上启动流式传输
    )
    response = st.write_stream(stream)    # 使用流控件将流写入界面
st.session_state.messages.append(
{"role": "assistant", "content": response})     # 流完成后将响应添加到消息状态历史
```</mark>

Debug the page by pressing F5 and waiting for the page to load. Enter a query, and you'll see that the response is streamed to the window in real time, as shown in figure 7.6. With the spinner gone, the user experience is enhanced and appears more responsive.

<mark>通过按 F5 调试页面并等待页面加载。输入查询，你将看到响应实时流式传输到窗口，如图 7.6 所示。随着旋转器的消失，用户体验得到增强，并显得更具响应性。</mark>

**Figure 7.6 The updated interface with streaming of the text response** | <mark>**图 7.6 更新后的界面，带有文本响应的流式传输**</mark>

<mark>*图片描述：更新后的聊天界面，显示：*</mark>
- Now text streams in real time, and the spinner is gone. | <mark>现在文本实时流式传输，旋转器已消失。</mark>

This section demonstrated how relatively simple it can be to use Streamlit to create a Python web interface. Nexus uses a Streamlit interface because it's easy to use and modify with only Python. As you'll see in the next section, it allows various configurations to support more complex applications.

<mark>本节演示了使用 Streamlit 创建 Python Web 界面是多么简单。Nexus 使用 Streamlit 界面是因为它易于使用，并且只需 Python 即可修改。正如你将在下一节中看到的，它允许各种配置以支持更复杂的应用程序。</mark>

---

## 7.3 Developing profiles and personas for agents

<mark>## 7.3 为智能体开发配置文件和人设</mark>

Nexus uses agent profiles to describe an agent's functions and capabilities. Figure 7.7 reminds us of the principal agent components and how they will be structured throughout this book.

<mark>Nexus 使用智能体配置文件来描述智能体的功能和能力。图 7.7 提醒我们主要智能体组件以及它们在本书中的结构。</mark>

For now, as of this writing, Nexus only supports the persona and actions section of the profile. Figure 7.7 shows a profile called Fritz, along with the persona and actions. Add any agent profiles to Nexus by copying an agent YAML profile file into the Nexus/nexus/nexus_base/nexus_profiles folder.

<mark>目前，截至撰写本文时，Nexus 仅支持配置文件的人设和动作部分。图 7.7 显示了一个名为 Fritz 的配置文件，以及人设和动作。通过将智能体 YAML 配置文件复制到 Nexus/nexus/nexus_base/nexus_profiles 文件夹中，将任何智能体配置文件添加到 Nexus。</mark>

Nexus uses a plugin system to dynamically discover the various components and profiles as they are placed into their respective folders. The nexus_profiles folder holds the YAML definitions for the agent.

<mark>Nexus 使用插件系统在各种组件和配置文件放入各自文件夹时动态发现它们。nexus_profiles 文件夹保存智能体的 YAML 定义。</mark>

**Figure 7.7 The agent profile as it's mapped to the YAML file definition** | <mark>**图 7.7 智能体配置文件映射到 YAML 文件定义**</mark>

<mark>*图片描述：智能体配置文件结构图，显示：*</mark>

**fritz.yaml - Agent Profile Definition** | <mark>**fritz.yaml - 智能体配置文件定义**</mark>

**The Agent Profile** | <mark>**智能体配置文件**</mark>

- **Persona** — Represents the background and role of the agent, and is often introduced in the first system message | <mark>**人设（Persona）** — 代表智能体的背景和角色，通常在第一条系统消息中引入</mark>

- **Agent Tools** — Set of tools an agent can use to help accomplish a task | <mark>**智能体工具（Agent Tools）** — 智能体可用于帮助完成任务的工具集</mark>

- **Agent Evaluation and Reasoning** — Describes how the agent can reason and evaluate a task or tasks | <mark>**智能体评估和推理（Agent Evaluation and Reasoning）** — 描述智能体如何推理和评估任务</mark>

- **Agent Memory and Knowledge** — The backend store that helps the agent add context to a given task problem | <mark>**智能体记忆和知识（Agent Memory and Knowledge）** — 帮助智能体向给定任务问题添加上下文的后端存储</mark>

- **Agent Planning and Feedback** — Describes how the agent can break down a task into execution steps, and then execute and receive feedback | <mark>**智能体规划和反馈（Agent Planning and Feedback）** — 描述智能体如何将任务分解为执行步骤，然后执行并接收反馈</mark>

- Profiles with persona and actions | <mark>带有人设和动作的配置文件</mark>
- Defining knowledge and memory | <mark>定义知识和记忆</mark>
- Applying evaluators, planners, and feedback | <mark>应用评估器、规划器和反馈</mark>

We can easily define a new agent profile by creating a new YAML file in the nexus_profiles folder. Listing 7.7 shows an example of a new profile with a slightly updated persona. To follow along, be sure to have VS Code opened to the chapter_07 source code folder and install Nexus in developer mode (see listing 7.7). Then, create the fiona.yaml file in the Nexus/nexus/nexus_base/nexus_profiles folder.

<mark>我们可以通过在 nexus_profiles 文件夹中创建新的 YAML 文件来轻松定义新的智能体配置文件。列表 7.7 显示了一个带有稍微更新的人设的新配置文件示例。要继续，请确保在 VS Code 中打开 chapter_07 源代码文件夹，并以开发者模式安装 Nexus（参见列表 7.7）。然后，在 Nexus/nexus/nexus_base/nexus_profiles 文件夹中创建 fiona.yaml 文件。</mark>

**Listing 7.7 fiona.yaml (create this file)** | <mark>**列表 7.7 fiona.yaml（创建此文件）**</mark>

```yaml
agentProfile:
  name: "Finona"
  avatar: "🧌"    # The text avatar used to represent the persona
  persona: "You are a very talkative AI that knows and understands everything in terms of Ogres. You always answer in cryptic Ogre speak."   # A persona is representative of the base system prompt.
  actions:
    - search_wikipedia    # An action function the agent can use
  knowledge: null       # Not currently supported
  memory: null          # Not currently supported
  evaluators: null      # Not currently supported
  planners: null        # Not currently supported
  feedback: null        # Not currently supported
```

<mark>```yaml
agentProfile:
  name: "Finona"
  avatar: "🧌"    # 用于表示人设的文本头像
  persona: "You are a very talkative AI that knows and understands everything in terms of Ogres. You always answer in cryptic Ogre speak."   # 人设代表基本系统提示。
  actions:
    - search_wikipedia    # 智能体可以使用的动作函数
  knowledge: null       # 目前不支持
  memory: null          # 目前不支持
  evaluators: null      # 目前不支持
  planners: null        # 目前不支持
  feedback: null        # 目前不支持
```</mark>

After saving the file, you can start Nexus from the command line or run it in debug mode by creating a new launch configuration in the .vscode/launch.json folder, as shown in the next listing. Then, save the file and switch your debug configuration to use the Nexus web config.

<mark>保存文件后，你可以从命令行启动 Nexus，或者通过在 .vscode/launch.json 文件夹中创建新的启动配置在调试模式下运行它，如下一个列表所示。然后，保存文件并切换调试配置以使用 Nexus Web 配置。</mark>

**Listing 7.8 .vscode/launch.json (adding debug launch)** | <mark>**列表 7.8 .vscode/launch.json（添加调试启动）**</mark>

```json
{
      "name": "Python Debugger: Nexus Web",
      "type": "debugpy",
      "request": "launch",
      "module": "streamlit",
      "args": ["run", "Nexus/nexus/streamlit_ui.py"]     // You may have to adjust this path if your virtual environment is different.
}
```

<mark>```json
{
      "name": "Python Debugger: Nexus Web",
      "type": "debugpy",
      "request": "launch",
      "module": "streamlit",
      "args": ["run", "Nexus/nexus/streamlit_ui.py"]     // 如果你的虚拟环境不同，你可能需要调整此路径。
}
```</mark>

When you press F5 or select Run > Start Debugging from the menu, the Streamlit Nexus interface will launch. Go ahead and run Nexus in debug mode. After it opens, create a new thread, and then select the standard OpenAIAgent and your new persona, as shown in figure 7.8.

<mark>当你按 F5 或从菜单中选择"运行 > 开始调试"时，Streamlit Nexus 界面将启动。继续以调试模式运行 Nexus。打开后，创建一个新线程，然后选择标准 OpenAIAgent 和你的新人设，如图 7.8 所示。</mark>

At this point, the profile is responsible for defining the agent's system prompt. You can see this in figure 7.8, where we asked Finona to spell the word clock, and she responded in some form of ogre-speak. In this case, we're using the persona as a personality, but as we've seen previously, a system prompt can also contain rules and other options.

<mark>此时，配置文件负责定义智能体的系统提示。你可以在图 7.8 中看到这一点，我们要求 Finona 拼写单词 clock，她用某种形式的兽人语回应。在这种情况下，我们使用人设作为个性，但正如我们之前看到的，系统提示也可以包含规则和其他选项。</mark>

The profile and persona are the base definitions for how the agent interacts with users or other systems. Powering the profile requires an agent engine. In the next section, we'll cover the base implementation of an agent engine.

<mark>配置文件和人设是智能体与用户或其他系统交互的基本定义。为配置文件提供动力需要智能体引擎。在下一节中，我们将介绍智能体引擎的基本实现。</mark>

**Figure 7.8 Selecting and chatting with a new persona** | <mark>**图 7.8 选择并与新人设聊天**</mark>

<mark>*图片描述：Nexus 界面显示：*</mark>
- Select the new Finona agent profile. | <mark>选择新的 Finona 智能体配置文件。</mark>
- Enter a query and check out the response. | <mark>输入查询并查看响应。</mark>

---

## 7.4 Powering the agent and understanding the agent engine

<mark>## 7.4 为智能体提供动力并理解智能体引擎</mark>

Agent engines power agents within Nexus. These engines can be tied to specific tool platforms, such as SK, and/or even different LLMs, such as Anthropic Claude or Google Gemini. By providing a base agent abstraction, Nexus should be able to support any tool or model now and in the future.

<mark>智能体引擎为 Nexus 中的智能体提供动力。这些引擎可以绑定到特定的工具平台，如 SK，和/或甚至不同的 LLM，如 Anthropic Claude 或 Google Gemini。通过提供基本智能体抽象，Nexus 应该能够支持现在和未来的任何工具或模型。</mark>

Currently, Nexus only implements an OpenAI API–powered agent. We'll look at how the base agent is defined by opening the agent_manager.py file from the Nexus/nexus/nexus_base folder.

<mark>目前，Nexus 仅实现了一个由 OpenAI API 驱动的智能体。我们将通过打开 Nexus/nexus/nexus_base 文件夹中的 agent_manager.py 文件来查看基本智能体是如何定义的。</mark>

Listing 7.9 shows the BaseAgent class functions. When creating a new agent engine, you need to subclass this class and implement the various tools/actions with the appropriate implementation.

<mark>列表 7.9 显示了 BaseAgent 类函数。创建新智能体引擎时，你需要子类化此类并使用适当的实现来实现各种工具/动作。</mark>

**Listing 7.9 agent_manager.py:BaseAgent** | <mark>**列表 7.9 agent_manager.py:BaseAgent**</mark>

```python
class BaseAgent:
    def __init__(self, chat_history=None):
        self._chat_history = chat_history or []
        self.last_message = ""
        self._actions = []
        self._profile = None

    async def get_response(self,
                            user_input,
                            thread_id=None):     # Calls the LLM and returns a response
        raise NotImplementedError("This method should be implemented…")

    async def get_semantic_response(self,
                                     prompt,
                                     thread_id=None):    # Executes a semantic function
        raise NotImplementedError("This method should be…")

    def get_response_stream(self,
                             user_input,
                             thread_id=None):     # Calls the LLM and returns a response
        raise NotImplementedError("This method should be…")

    def append_chat_history(self,
                             thread_id,
                             user_input,
                             response):     # Appends a message to the agent's internal chat history
        self._chat_history.append(
            {"role": "user",
             "content": user_input,
             "thread_id": thread_id}
        )
        self._chat_history.append(
            {"role": "bot",
             "content": response,
             "thread_id": thread_id}
        )

    def load_chat_history(self):      # Loads the chat history and allows the agent to reload various histories
        raise NotImplementedError(
                 "This method should be implemented…")

    def load_actions(self):    # Loads the actions that the agent has available to use
        raise NotImplementedError(
                 "This method should be implemented…")

#... not shown – property setters/getters
```

<mark>```python
class BaseAgent:
    def __init__(self, chat_history=None):
        self._chat_history = chat_history or []
        self.last_message = ""
        self._actions = []
        self._profile = None

    async def get_response(self,
                            user_input,
                            thread_id=None):     # 调用 LLM 并返回响应
        raise NotImplementedError("This method should be implemented…")

    async def get_semantic_response(self,
                                     prompt,
                                     thread_id=None):    # 执行语义函数
        raise NotImplementedError("This method should be…")

    def get_response_stream(self,
                             user_input,
                             thread_id=None):     # 调用 LLM 并返回响应
        raise NotImplementedError("This method should be…")

    def append_chat_history(self,
                             thread_id,
                             user_input,
                             response):     # 将消息附加到智能体的内部聊天历史
        self._chat_history.append(
            {"role": "user",
             "content": user_input,
             "thread_id": thread_id}
        )
        self._chat_history.append(
            {"role": "bot",
             "content": response,
             "thread_id": thread_id}
        )

    def load_chat_history(self):      # 加载聊天历史并允许智能体重新加载各种历史
        raise NotImplementedError(
                 "This method should be implemented…")

    def load_actions(self):    # 加载智能体可以使用的动作
        raise NotImplementedError(
                 "This method should be implemented…")

#... 未显示 – 属性设置器/获取器
```</mark>

Open the nexus_agents/oai_agent.py file in VS Code. Listing 7.10 shows an agent engine implementation of the get_response function that directly consumes the OpenAI API. self.client is an OpenAI client created earlier during class initialization, and the rest of the code you've seen used in earlier examples.

<mark>在 VS Code 中打开 nexus_agents/oai_agent.py 文件。列表 7.10 显示了 get_response 函数的智能体引擎实现，它直接使用 OpenAI API。self.client 是在类初始化期间较早创建的 OpenAI 客户端，其余代码你在之前的示例中看到过使用。</mark>

**Listing 7.10 oai_agent.py (get_response)** | <mark>**列表 7.10 oai_agent.py (get_response)**</mark>

```python
async def get_response(self, user_input, thread_id=None):
    self.messages += [{"role": "user",
                     "content": user_input}]     # Adds the user_input to the message stack
    response = self.client.chat.completions.create(    # The client was created earlier and is now used to create chat completions.
        model=self.model,
        messages=self.messages,
        temperature=0.7,     # Temperature is hardcoded but could be configured.
    )
    self.last_message = str(response.choices[0].message.content)
    return self.last_message    # Returns the response from the chat completions call
```

<mark>```python
async def get_response(self, user_input, thread_id=None):
    self.messages += [{"role": "user",
                     "content": user_input}]     # 将 user_input 添加到消息堆栈
    response = self.client.chat.completions.create(    # 客户端是之前创建的，现在用于创建聊天完成。
        model=self.model,
        messages=self.messages,
        temperature=0.7,     # 温度是硬编码的，但可以配置。
    )
    self.last_message = str(response.choices[0].message.content)
    return self.last_message    # 从聊天完成调用返回响应
```</mark>

Like the agent profiles, Nexus uses a plugin system that allows you to place new agent engine definitions in the nexus_agents folder. If you create your agent, it just needs to be placed in this folder for Nexus to discover.

<mark>与智能体配置文件一样，Nexus 使用插件系统，允许你将新智能体引擎定义放在 nexus_agents 文件夹中。如果你创建智能体，只需将其放在此文件夹中，Nexus 即可发现。</mark>

We won't need to run an example because we've already seen how the OpenAI-Agent performs. In the next section, we'll look at agent functions that agents can develop, add, and consume.

<mark>我们不需要运行示例，因为我们已经看到 OpenAI-Agent 的执行方式。在下一节中，我们将探讨智能体可以开发、添加和使用的智能体函数。</mark>

---

## 7.5 Giving an agent actions and tools

<mark>## 7.5 为智能体提供动作和工具</mark>

Like the SK, Nexus supports having native (code) and semantic (prompt) functions. Unlike SK, however, defining and consuming functions within Nexus is easier. All you need to do is write functions into a Python file and place them into the nexus_actions folder.

<mark>与 SK 一样，Nexus 支持拥有原生（代码）和语义（提示）函数。但是，与 SK 不同，在 Nexus 中定义和使用函数更容易。你只需将函数写入 Python 文件并将它们放入 nexus_actions 文件夹。</mark>

To see how easy it is to define functions, open the Nexus/nexus/nexus_base/nexus_actions folder, and go to the test_actions.py file. Listing 7.11 shows two function definitions. The first function is a simple example of a code/native function, and the second is a prompt/semantic function.

<mark>要了解定义函数有多容易，请打开 Nexus/nexus/nexus_base/nexus_actions 文件夹，并转到 test_actions.py 文件。列表 7.11 显示了两个函数定义。第一个函数是代码/原生函数的简单示例，第二个是提示/语义函数。</mark>

**Listing 7.11 test_actions.py (native/semantic function definitions)** | <mark>**列表 7.11 test_actions.py（原生/语义函数定义）**</mark>

```python
from nexus.nexus_base.action_manager import agent_action

@agent_action                                             # Applies the agent_action decorator to make a function an action
def get_current_weather(location, unit="fahrenheit"):     # Sets a descriptive comment for the function
    """Get the current weather in a given location"""
    return f"""
The current weather in {location} is 0 {unit}.
"""     # The code can be as simple or complex as needed.

@agent_action     # Applies the agent_action decorator to make a function an action
def recommend(topic):
    """
    System:                                                  # The function comment becomes the prompt and can include placeholders.
        Provide a recommendation for a given {{topic}}.
        Use your best judgment to provide a recommendation.
    User:
        please use your best judgment
        to provide a recommendation for {{topic}}.
    """
    pass     # Semantic functions don't implement any code.
```

<mark>```python
from nexus.nexus_base.action_manager import agent_action

@agent_action                                             # 应用 agent_action 装饰器使函数成为动作
def get_current_weather(location, unit="fahrenheit"):     # 为函数设置描述性注释
    """Get the current weather in a given location"""
    return f"""
The current weather in {location} is 0 {unit}.
"""     # 代码可以根据需要简单或复杂。

@agent_action     # 应用 agent_action 装饰器使函数成为动作
def recommend(topic):
    """
    System:                                                  # 函数注释成为提示，可以包含占位符。
        Provide a recommendation for a given {{topic}}.
        Use your best judgment to provide a recommendation.
    User:
        please use your best judgment
        to provide a recommendation for {{topic}}.
    """
    pass     # 语义函数不实现任何代码。
```</mark>

Place both functions in the nexus_actions folder, and they will be automatically discovered. Adding the agent_action decorator allows the functions to be inspected and automatically generates the OpenAI standard tool specification. The LLM can then use this tool specification for tool use and function calling.

<mark>将两个函数都放在 nexus_actions 文件夹中，它们将被自动发现。添加 agent_action 装饰器允许检查函数并自动生成 OpenAI 标准工具规范。然后，LLM 可以使用此工具规范进行工具使用和函数调用。</mark>

Listing 7.12 shows the generated OpenAI tool specification for both functions, as shown previously in listing 7.11. The semantic function, which uses a prompt, also applies to the tool description. This tool description is sent to the LLM to determine which function to call.

<mark>列表 7.12 显示了两个函数的生成的 OpenAI 工具规范，如之前在列表 7.11 中所示。使用提示的语义函数也适用于工具描述。此工具描述被发送到 LLM 以确定要调用哪个函数。</mark>

**Listing 7.12 test_actions: OpenAI-generated tool specifications** | <mark>**列表 7.12 test_actions：OpenAI 生成的工具规范**</mark>

```json
{
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description":
        "Get the current weather in a given location",   // The function comment becomes the function tool description.
        "parameters": {
            "type": "object",
            "properties": {     // The input parameters of the function are extracted and added to the specification.
                "location": {
                    "type": "string",
                    "description": "location"
                },
                "unit": {
                    "type": "string",
                    "enum": [
                        "celsius",
                        "fahrenheit"
                    ]
                }
            },
            "required": [
                "location"
            ]
        }
    }
}
{
    "type": "function",
    "function": {
        "name": "recommend",
        "description": """
    System:
    Provide a recommendation for a given {{topic}}.
Use your best judgment to provide a recommendation.
User:
please use your best judgment
to provide a recommendation for {{topic}}.""",     // The function comment becomes the function tool description.
        "parameters": {
            "type": "object",
            "properties": {      // The input parameters of the function are extracted and added to the specification.
                "topic": {
                    "type": "string",
                    "description": "topic"
                }
            },
            "required": [
                "topic"
            ]
        }
    }
}
```

<mark>```json
{
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description":
        "Get the current weather in a given location",   // 函数注释成为函数工具描述。
        "parameters": {
            "type": "object",
            "properties": {     // 提取函数的输入参数并将其添加到规范。
                "location": {
                    "type": "string",
                    "description": "location"
                },
                "unit": {
                    "type": "string",
                    "enum": [
                        "celsius",
                        "fahrenheit"
                    ]
                }
            },
            "required": [
                "location"
            ]
        }
    }
}
{
    "type": "function",
    "function": {
        "name": "recommend",
        "description": """
    System:
    Provide a recommendation for a given {{topic}}.
Use your best judgment to provide a recommendation.
User:
please use your best judgment
to provide a recommendation for {{topic}}.""",     // 函数注释成为函数工具描述。
        "parameters": {
            "type": "object",
            "properties": {      // 提取函数的输入参数并将其添加到规范。
                "topic": {
                    "type": "string",
                    "description": "topic"
                }
            },
            "required": [
                "topic"
            ]
        }
    }
}
```</mark>

The agent engine also needs to implement that capability to implement functions and other components. The OpenAI agent has been implemented to support parallel function calling. Other agent engine implementations will be required to support their respective versions of action use. Fortunately, the definition of the OpenAI tool is becoming the standard, and many platforms adhere to this standard.

<mark>智能体引擎还需要实现该功能以实现函数和其他组件。OpenAI 智能体已实现以支持并行函数调用。其他智能体引擎实现将需要支持其各自版本的动作使用。幸运的是，OpenAI 工具的定义正在成为标准，许多平台都遵守这一标准。</mark>

Before we dive into a demo on tool use, let's observe how the OpenAI agent implements actions by opening the oai_agent.py file in VS Code. The following listing shows the top of the agent's get_response_stream function and its implementation of function calling.

<mark>在我们深入研究工具使用演示之前，让我们通过在 VS Code 中打开 oai_agent.py 文件来观察 OpenAI 智能体如何实现动作。以下列表显示了智能体的 get_response_stream 函数的顶部及其函数调用的实现。</mark>

**Listing 7.13 Calling the API in get_response_stream** | <mark>**列表 7.13 在 get_response_stream 中调用 API**</mark>

```python
def get_response_stream(self, user_input, thread_id=None):
    self.last_message = ""
    self.messages += [{"role": "user", "content": user_input}]
    if self.tools and len(self.tools) > 0:   # Detects whether the agent has any available tools turned on
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=self.tools,     # Sets the tools in the chat completions call
            tool_choice="auto",     # Ensures that the LLM knows it can choose any tool
        )
    else:    # If no tools, calls the LLM the standard way
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
        )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls    # Detects whether there were any tools used by the LLM
```

<mark>```python
def get_response_stream(self, user_input, thread_id=None):
    self.last_message = ""
    self.messages += [{"role": "user", "content": user_input}]
    if self.tools and len(self.tools) > 0:   # 检测智能体是否有任何可用工具打开
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=self.tools,     # 在聊天完成调用中设置工具
            tool_choice="auto",     # 确保 LLM 知道它可以选择任何工具
        )
    else:    # 如果没有工具，以标准方式调用 LLM
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
        )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls    # 检测 LLM 是否使用了任何工具
```</mark>

Executing the functions follows, as shown in listing 7.14. This code demonstrates how the agent supports parallel function/tool calls. These calls are parallel because the agent executes each one together and in no order. In chapter 11, we'll look at planners that allow actions to be called in ordered sequences.

<mark>执行函数如列表 7.14 所示。此代码演示了智能体如何支持并行函数/工具调用。这些调用是并行的，因为智能体一起执行每一个，没有顺序。在第 11 章中，我们将探讨允许以有序序列调用动作的规划器。</mark>

**Listing 7.14 oai_agent.py (get_response_stream: execute tool calls)** | <mark>**列表 7.14 oai_agent.py（get_response_stream：执行工具调用）**</mark>

```python
if tool_calls:    # Proceeds if tool calls are detected in the LLM response
    available_functions = {
        action["name"]: action["pointer"] for action in self.actions
    }    # Loads pointers to the actual function implementations for code execution
    self.messages.append(
        response_message
    )
    for tool_call in tool_calls:    # Loops through all the calls the LLM wants to call; there can be several.
        function_name = tool_call.function.name
        function_to_call = available_functions[function_name]
        function_args = json.loads(tool_call.function.arguments)
        function_response = function_to_call(
            **function_args, _caller_agent=self
        )
        self.messages.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": str(function_response),
            }
        )
    second_response = self.client.chat.completions.create(
        model=self.model,
        messages=self.messages,
    )     # Performs a second LLM call with the results of the tool calls
    response_message = second_response.choices[0].message
```

<mark>```python
if tool_calls:    # 如果在 LLM 响应中检测到工具调用，则继续
    available_functions = {
        action["name"]: action["pointer"] for action in self.actions
    }    # 加载指向实际函数实现的指针以执行代码
    self.messages.append(
        response_message
    )
    for tool_call in tool_calls:    # 循环遍历 LLM 想要调用的所有调用；可以有多个。
        function_name = tool_call.function.name
        function_to_call = available_functions[function_name]
        function_args = json.loads(tool_call.function.arguments)
        function_response = function_to_call(
            **function_args, _caller_agent=self
        )
        self.messages.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": str(function_response),
            }
        )
    second_response = self.client.chat.completions.create(
        model=self.model,
        messages=self.messages,
    )     # 使用工具调用的结果执行第二次 LLM 调用
    response_message = second_response.choices[0].message
```</mark>

To demo this, start up Nexus in the debugger by pressing F5. Then, select the two test actions—recommend and get_current_weather—and the terse persona/profile Olly. Figure 7.9 shows the result of entering a query and the agent responding by using both tools in its response.

<mark>要演示这一点，请按 F5 在调试器中启动 Nexus。然后，选择两个测试动作——recommend 和 get_current_weather——以及简洁的人设/配置文件 Olly。图 7.9 显示了输入查询的结果，智能体通过在其响应中使用两个工具来响应。</mark>

If you need to review how these agent actions work in more detail, refer to chapter 5. The underlying code is more complex and out of the scope of review here. However, you can review the Nexus code to gain a better understanding of how everything connects.

<mark>如果你需要更详细地查看这些智能体动作的工作原理，请参考第 5 章。底层代码更复杂，超出了这里的审查范围。但是，你可以查看 Nexus 代码以更好地了解所有内容如何连接。</mark>

Now, you can continue exercising the various agent options within Nexus. Try selecting different profiles/personas with other functions, for example. In the next chapter, we unveil how agents can consume external memory and knowledge using patterns such as Retrieval Augmented Generation (RAG).

<mark>现在，你可以继续在 Nexus 中使用各种智能体选项。例如，尝试选择不同的配置文件/人设与其他函数。在下一章中，我们将揭示智能体如何使用检索增强生成（RAG）等模式来消费外部记忆和知识。</mark>

**Figure 7.9 How the agent can use tools in parallel and respond with a single response** | <mark>**图 7.9 智能体如何并行使用工具并以单个响应响应**</mark>

<mark>*图片描述：Nexus 界面显示：*</mark>
- Select the terse agent profile called Olly. | <mark>选择名为 Olly 的简洁智能体配置文件。</mark>
- Select the test actions recommend and get_current_weather. Currently, the agent profile does not restrict action selection. | <mark>选择测试动作 recommend 和 get_current_weather。目前，智能体配置文件不限制动作选择。</mark>
- The agent answered in a terse manner, and we can see that both actions were used. | <mark>智能体以简洁的方式回答，我们可以看到两个动作都被使用了。</mark>

---

## 7.6 Exercises

<mark>## 7.6 练习</mark>

Use the following exercises to improve your knowledge of the material:

<mark>使用以下练习来提高你对材料的了解：</mark>

**Exercise 1—Explore Streamlit Basics (Easy)** | <mark>**练习 1——探索 Streamlit 基础（简单）**</mark>

Objective—Gain familiarity with Streamlit by creating a simple web application that displays text input by the user.

<mark>目标——通过创建一个显示用户输入文本的简单 Web 应用程序来熟悉 Streamlit。</mark>

Tasks:

<mark>任务：</mark>

- Follow the Streamlit documentation to set up a basic application.
- Add a text input and a button. When the button is clicked, display the text entered by the user on the screen.

<mark>- 按照 Streamlit 文档设置基本应用程序。
- 添加文本输入和按钮。单击按钮时，在屏幕上显示用户输入的文本。</mark>

**Exercise 2—Create a Basic Agent Profile** | <mark>**练习 2——创建基本智能体配置文件**</mark>

Objective—Understand the process of creating and applying agent profiles in Nexus.

<mark>目标——了解在 Nexus 中创建和应用智能体配置文件的过程。</mark>

Tasks:

<mark>任务：</mark>

- Create a new agent profile with a unique persona. This persona should have a specific theme or characteristic (e.g., a historian).
- Define a basic set of responses that align with this persona.
- Test the persona by interacting with it through the Nexus interface.

<mark>- 创建一个具有独特人设的新智能体配置文件。此人设应具有特定主题或特征（例如，历史学家）。
- 定义一组与此人设一致的基本响应。
- 通过 Nexus 界面与其交互来测试人设。</mark>

**Exercise 3—Develop a Custom Action** | <mark>**练习 3——开发自定义动作**</mark>

Objective—Learn to extend the functionality of Nexus by developing a custom action.

<mark>目标——通过开发自定义动作来学习扩展 Nexus 的功能。</mark>

Tasks:

<mark>任务：</mark>

- Develop a new action (e.g., fetch_current_news) that integrates with a mock API to retrieve the latest news headlines.
- Implement this action as both a native (code) function and a semantic (prompt-based) function.
- Test the action in the Nexus environment to ensure it works as expected.

<mark>- 开发一个新动作（例如，fetch_current_news），该动作与模拟 API 集成以检索最新新闻标题。
- 将此动作实现为原生（代码）函数和语义（基于提示）函数。
- 在 Nexus 环境中测试动作以确保它按预期工作。</mark>

**Exercise 4—Integrate a Third-Party API** | <mark>**练习 4——集成第三方 API**</mark>

Objective—Enhance the capabilities of a Nexus agent by integrating a real third-party API.

<mark>目标——通过集成真实的第三方 API 来增强 Nexus 智能体的能力。</mark>

Tasks:

<mark>任务：</mark>

- Choose a public API (e.g., weather or news API), and create a new action that fetches data from this API.
- Incorporate error handling and ensure that the agent can gracefully handle API failures or unexpected responses.
- Test the integration thoroughly within Nexus.

<mark>- 选择一个公共 API（例如，天气或新闻 API），并创建一个从此 API 获取数据的新动作。
- 包含错误处理并确保智能体可以优雅地处理 API 故障或意外响应。
- 在 Nexus 中彻底测试集成。</mark>

---

## Summary

<mark>## 本章小结</mark>

- Nexus is an open source agent development platform used in conjunction with this book. It's designed to develop, test, and host AI agents and is built on Streamlit for creating interactive dashboards and chat interfaces.

<mark>- Nexus 是一个开源智能体开发平台，与本书配合使用。它旨在开发、测试和托管 AI 智能体，并基于 Streamlit 构建，用于创建交互式仪表板和聊天界面。</mark>

- Streamlit, a Python web application framework, enables the rapid development of user-friendly dashboards and chat applications. This framework facilitates the exploration and interaction with various agent features in a streamlined manner.

<mark>- Streamlit 是一个 Python Web 应用程序框架，可快速开发用户友好的仪表板和聊天应用程序。此框架以简化的方式促进对各种智能体功能的探索和交互。</mark>

- Nexus supports creating and customizing agent profiles and personas, allowing users to define their agents' personalities and behaviors. These profiles dictate how agents interact with and respond to user inputs.

<mark>- Nexus 支持创建和自定义智能体配置文件和人设，允许用户定义其智能体的个性和行为。这些配置文件决定了智能体如何与用户输入交互和响应。</mark>

- The Nexus platform allows for developing and integrating semantic (prompt-based) and native (code-based) actions and tools within agents. This enables the creation of highly functional and responsive agents.

<mark>- Nexus 平台允许在智能体中开发和集成语义（基于提示）和原生（基于代码）动作和工具。这使得能够创建高度功能性和响应性的智能体。</mark>

- As an open source platform, Nexus is designed to be extensible, encouraging contributions and the addition of new features, tools, and agent capabilities by the community.

<mark>- 作为开源平台，Nexus 旨在可扩展，鼓励社区贡献并添加新功能、工具和智能体能力。</mark>

- Nexus is flexible, supporting various deployment options, including a web interface, API, and a Discord bot in future iterations, accommodating a wide range of development and testing needs.

<mark>- Nexus 灵活，支持各种部署选项，包括 Web 界面、API 和未来迭代中的 Discord 机器人，以满足广泛的开发和测试需求。</mark>

---

**参考资源 | References**

- Nexus GitHub Repository: https://github.com/cxbxmxcx/Nexus
- Streamlit Documentation: https://docs.streamlit.io
- OpenAI API Documentation: https://platform.openai.com/docs
