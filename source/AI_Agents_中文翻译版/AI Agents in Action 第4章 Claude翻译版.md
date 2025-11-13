# AI Agents in Action 第4章 Claude翻译版

================================================================================
第4章 探索多智能体系统
================================================================================
**原书名称:** AI Agents in Action.pdf
**页码范围:** 92 - 121
**翻译说明:** 本翻译由 Claude AI 协助完成，仅供个人学习使用
================================================================================

## 第4章 探索多智能体系统

现在让我们踏上从 AutoGen 到 CrewAI 的旅程，这两个都是成熟的多智能体平台。我们将从 AutoGen 开始，这是一个 Microsoft 项目，支持多个智能体并提供一个工作室来协助你使用智能体。我们将探索 Microsoft 的一个名为 AutoGen 的项目，它不仅支持多个智能体，还提供一个工作室，让你更轻松地使用智能体。从那里开始，我们将更多地编码 AutoGen 智能体，通过对话和群聊协作来解决任务。

然后，我们将过渡到 CrewAI，一个自称的企业智能体系统，采用不同的方法。CrewAI 平衡基于角色和自主智能体，可以顺序或分层的灵活任务管理系统。我们将探索 CrewAI 如何解决多样化和复杂的问题。

### 本章内容概要
- 使用 AutoGen Studio 构建多智能体系统
- 构建简单的多智能体系统
- 创建可以通过群聊协作工作的智能体
- 使用 CrewAI 构建智能体团队和多智能体系统
- 使用 CrewAI 扩展智能体数量并探索处理模式

多智能体系统结合了单智能体系统使用的许多相同工具，但受益于向其他智能体提供外部反馈和评估的能力。这种内部支持和批评智能体解决方案的能力使多智能体系统更强大。我们将在下一节中从 AutoGen Studio 开始探索多智能体系统的介绍。

## 4.1 使用 AutoGen Studio 介绍多智能体系统

AutoGen Studio 是一个强大的工具，在幕后使用多个智能体来解决用户指导的任务和问题。这个工具已被用于开发本书中的一些更复杂的代码。出于这个原因和其他原因，它是实用多智能体系统的绝佳介绍。

图 4.1 显示了 AutoGen 采用的智能体连接/通信模式的示意图。AutoGen 是一个对话式多智能体平台，因为通信是使用自然语言完成的。自然语言对话似乎是智能体通信最自然的模式，但它不是唯一的方法，正如你稍后会看到的。

**图 4.1: AutoGen 智能体如何通过对话进行通信（来源：AutoGen）**
- AutoGen 使用可对话智能体，它们通过对话进行通信

AutoGen 支持各种对话模式，从群组和分层到更常见和简单的代理通信。在代理通信中，一个智能体充当代理并将通信定向到相关智能体以完成任务。代理类似于服务员接受订单并将其传递给厨房，厨房烹饪食物。然后，服务员提供烹饪好的食物。

AutoGen 中的基本模式使用 UserProxy 和一个或多个助手智能体。图 4.2 显示了用户代理从人类那里接受指示，然后指导启用编写代码以执行任务的助手智能体。每次助手完成一项任务时，代理智能体都会审查、评估并向助手提供反馈。这个迭代循环继续进行，直到代理对结果满意为止。

**图 4.2: 用户代理智能体和助手智能体通信（来源：AutoGen）**
- 人类与用户代理智能体通信，用户代理智能体与其他智能体通信
- 助手智能体承担完成直接任务
- 在代理和助手之间形成评估和反馈循环
- 配置为编写 Python 代码的 LLM

代理的好处是它可以替代所需的人工反馈和评估，在大多数情况下，它做得很好。虽然它不能消除对人工反馈和评估的需求，但它总体上产生更完整的结果。而且，虽然迭代循环很耗时，但这是你可以喝咖啡或处理其他任务的时间。

AutoGen Studio 是 AutoGen 团队开发的一个工具，为可对话智能体提供了有用的介绍。在下一个练习中，我们将安装 Studio 并运行一些实验来看看平台的表现如何。这些工具仍在快速开发周期中，因此如果你遇到任何问题，请查阅 AutoGen GitHub 存储库上的文档。

### 4.1.1 安装和使用 AutoGen Studio

在 Visual Studio Code (VS Code) 中打开 chapter_04 文件夹，创建一个本地 Python 虚拟环境，并安装 requirements.txt 文件。如果你需要帮助，请参阅附录 B 以安装本章所有练习的要求。

在 VS Code 中打开终端（Ctrl-`、Cmd-`）指向你的虚拟环境，并使用清单 4.1 中显示的命令运行 AutoGen Studio。你首先需要为你的 OpenAI 密钥定义一个环境变量。因为端口 8080 和 8081 很受欢迎，如果你有其他服务正在运行，请将端口更改为 8082 或你选择的端口。

**代码清单 4.1: 启动 AutoGen Studio**

```bash
# 在 Bash (Git Bash) 上设置环境变量
export OPENAI_API_KEY="<your API key>"

# 使用 PowerShell 设置环境变量
$env:VAR_NAME ="<your API key>"

autogenstudio ui --port 8081
```

**说明：**
- 为你的终端类型使用适当的命令
- 如果你预期或遇到机器上的冲突，请更改端口

导航你的浏览器到图 4.3 所示的 AutoGen Studio 界面（截至本文撰写时）。虽然可能存在差异，但有一点是肯定的：主要界面仍将是聊天。输入需要编码的复杂任务。这里使用的示例是"创建一个显示 GPT Agents 一词在 Google 搜索中受欢迎程度的图"。

**图 4.3: 在 AutoGen 界面中输入智能体要处理的任务**
- 输入智能体要处理的任务
- 你可以创建新会话或查看或继续以前的会话
- Playground 选项卡是你与智能体交互的地方。Build 选项卡用于创建新的智能体和技能，Gallery 选项卡用于查看以前的最佳输出
- 代理智能体和助手智能体现在将一起工作以完成任务

当智能体在示例中通过任务协作时，智能体助手生成代码片段以执行或完成各种子任务。然后，用户代理智能体尝试执行这些代码片段并评估输出。在许多情况下，证明代码运行并产生所需的输出足以让用户代理智能体批准任务完成。

如果你在助手智能体请求时遇到任何问题，请要求代理智能体尝试不同的方法或另一个问题。这突出了使用已过期且不再工作的包或库的智能体系统的更大问题。因此，通常最好让智能体执行动作而不是构建代码来执行动作作为工具。

**提示：** 建议使用 Docker 执行 AutoGen 和 AutoGen Studio，特别是在处理可能影响操作系统的代码时。Docker 可以隔离和虚拟化智能体的环境，从而隔离潜在有害的代码。使用 Docker 可以帮助缓解可能阻止智能体进程运行的任何辅助窗口或网站。

图 4.4 显示了智能体完成任务。代理智能体将收集任何生成的代码片段、图像或其他文档并将它们附加到消息中。

**图 4.4: 智能体完成任务后的输出**
- 生成的代码文件和其他输出将附加到最后一条消息
- 如果你完成了此智能体会话，请回复 TERMINATE。此停止词用于停止会话
- 在此示例中，在浏览器外部的新窗口中生成了 Matplotlib 图

你还可以通过打开 Agent Messages 展开器来查看智能体对话。在许多情况下，如果你要求智能体生成图或应用程序，辅助窗口将打开显示这些结果。

令人惊讶的是，智能体将很好地执行大多数任务并很好地完成它们。根据任务的复杂性，你可能需要与代理进一步迭代。有时，智能体可能只会完成任务到一定程度，因为它缺乏所需的技能。在下一节中，我们将了解如何向智能体添加技能。

### 4.1.2 在 AutoGen Studio 中添加技能

技能和工具，或者我们在本书中称之为动作，是智能体可以扩展自己的主要手段。动作赋予智能体执行代码、调用 API 甚至进一步评估和检查生成的输出的能力。AutoGen Studio 目前开始时只有一组基本工具来获取网络内容或生成图像。

**注意：** 许多智能体系统采用允许智能体编码以解决目标的做法。但是，我们发现代码很容易被破坏，需要维护，并且可能会快速变化。因此，正如我们将在后面的章节中讨论的那样，最好为智能体提供技能/动作/工具来解决问题。

在以下练习场景中，我们将添加一个技能/动作来使用 OpenAI 视觉模型检查图像。如果我们要求助手生成具有特定内容的图像，这将允许代理智能体提供反馈。

在 AutoGen Studio 运行时，转到 Build 选项卡并单击 Skills，如图 4.5 所示。然后，单击 New Skill 按钮以打开一个代码面板，你可以将代码复制粘贴到其中。从此选项卡，你还可以配置模型、智能体和智能体工作流。

**图 4.5: 在 Build 选项卡上创建新技能的步骤**
- 单击现有技能以查看它们的工作方式
- 单击以创建新技能
- 你还可以从这里配置其他模型、智能体和工作流

输入清单 4.2 中显示的代码，也在本书的源代码中提供为 describe_image.py。将此代码复制并粘贴到编辑器窗口中，然后单击底部的 Save 按钮。

**代码清单 4.2: describe_image.py**

```python
import base64
import requests
import os

def describe_image(image_path='animals.png') -> str:
    """
    Uses GPT-4 Vision to inspect and describe the contents of the image.
    :param input_path: str, the name of the PNG file to describe.
    """
    api_key = os.environ['OPEN_API_KEY']

    # Function to encode the image
    def encode_image(image_path):  # 加载并将图像编码为 Base64 字符串的函数
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-turbo",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What's in this image?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"  # 包含图像字符串以及 JSON 有效负载
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload)

    return response.json()["choices"][0]["message"]["content"]  # 解包响应并返回回复的内容
```

describe_image 函数使用 OpenAI GPT-4 视觉模型来描述图像中的内容。此技能可以与现有的 generate_image 技能配对作为质量评估。智能体可以确认生成的图像符合用户的要求。

添加技能后，必须将其添加到特定的智能体工作流和智能体中才能使用。图 4.6 演示了将新技能添加到通用或默认智能体工作流中的主要助手智能体。

**图 4.6: 使用新技能配置 primary_assistant 智能体**
- 选择 General Agent Workflow
- 选择在工作流面板底部编辑 primary_assistant
- 转到 Build 选项卡，然后转到 Workflows 选项卡
- 单击添加以添加新的 describe_image 技能
- 单击 OK 退出并返回到 Playground 选项卡

现在技能已添加到主要助手，我们可以任务智能体创建特定图像并使用新的 describe_image 技能验证它。由于图像生成器在处理正确的文本方面臭名昭著，我们将创建一个练习任务来做到这一点。

输入清单 4.3 中显示的文本以提示智能体为本书创建图书封面图像。我们将明确说明文本需要正确，并坚持智能体使用新的 describe_image 函数来验证图像。

**代码清单 4.3: 提示生成书籍封面**

```
Please create a cover for the book GPT Agents In Action, use the
describe_image skill to make sure the title of the book is spelled
correctly on the cover
```

输入提示后，等待一段时间，你可能会看到关于图像生成和验证过程的一些对话交换。最终，如果一切正常工作，智能体将返回图 4.7 所示的结果。

**图 4.7: 智能体在图像生成任务上工作的生成文件输出**
- 查看生成的输出文件
- 智能体生成额外的代码以根据需要使用技能
- 智能体甚至增强现有技能以更好地完成任务
- 经过几次迭代后，生成了带有正确文本的书籍封面

值得注意的是，智能体协调在几次迭代中完成了任务。除了图像之外，你还可以看到生成的各种辅助代码片段，以协助完成任务。AutoGen Studio 在集成智能体可以进一步适应以完成某些目标的技能方面令人印象深刻。下一节将展示这些强大的智能体如何在代码中实现。

## 4.2 探索 AutoGen

虽然 AutoGen Studio 是理解多智能体系统的绝佳工具，但我们必须深入研究代码。幸运的是，使用 AutoGen 编写多个智能体示例既简单又易于运行。我们将在下一节中介绍基本的 AutoGen 设置。

### 4.2.1 安装和使用 AutoGen

下一个练习将研究编码一个使用用户代理和可对话智能体的基本多智能体系统。不过，在此之前，我们想确保 AutoGen 已正确安装和配置。

在 VS Code 中打开终端，并按照附录 B 运行整个第 4 章的安装说明，或运行清单 4.4 中的 pip 命令。如果你已安装 requirements.txt 文件，你也将准备好运行 AutoGen。

**代码清单 4.4: 安装 AutoGen**

```bash
pip install pyautogen
```

接下来，将 chapter_04/OAI_CONFIG_LIST.example 复制到 OAI_CONFIG_LIST，从文件名中删除 .example。然后，在 VS Code 中打开新文件，并在清单 4.5 中的 OAI_CONFIG_LIST 文件中输入你的 OpenAI 或 Azure 配置。根据你的 API 服务要求填写你的 API 密钥、模型和其他详细信息。AutoGen 将与任何遵守 OpenAI 客户端的模型一起使用。这意味着你可以通过 LM Studio 使用本地 LLM 或 Groq、Hugging Face 等其他服务。

**代码清单 4.5: OAI_CONFIG_LIST**

```json
[
    {
        "model": "gpt-4",  // 选择模型；推荐 GPT-4
        "api_key": "<your OpenAI API key here>",  // 使用你通常会使用的服务密钥
        "tags": ["gpt-4", "tool"]
    },
    {
        "model": "<your Azure OpenAI deployment name>",  // 选择模型；推荐 GPT-4
        "api_key": "<your Azure OpenAI API key here>",  // 使用你通常会使用的服务密钥
        "base_url": "<your Azure OpenAI API base here>",  // 更改基本 URL 允许你指向其他服务，而不仅仅是 Azure OpenAI
        "api_type": "azure",
        "api_version": "2024-02-15-preview"
    }
]
```

现在，我们可以查看使用现成的 UserProxy 和 ConversableAgent 智能体进行基本多智能体聊天的代码。在 VS Code 中打开 autogen_start.py，如以下清单所示，并在运行文件之前查看各部分。

**代码清单 4.6: autogen_start.py**

```python
from autogen import ConversableAgent, UserProxyAgent, config_list_from_json

config_list = config_list_from_json(
    env_or_file="OAI_CONFIG_LIST")  # 从 JSON 文件 OAI_CONFIG_LIST 加载你的 LLM 配置

assistant = ConversableAgent(
    "agent",
    llm_config={"config_list": config_list})  # 此智能体直接与 LLM 对话

user_proxy = UserProxyAgent(  # 此智能体代理从用户到助手的对话
    "user",
    code_execution_config={
        "work_dir": "working",
        "use_docker": False,
    },
    human_input_mode="ALWAYS",
    is_termination_msg=lambda x: x.get("content", "")
    .rstrip()
    .endswith("TERMINATE"),  # 设置终止消息允许智能体迭代
)

user_proxy.initiate_chat(assistant, message="write a solution for fizz buzz in one line?")  # 通过 user_proxy 与助手发起聊天以完成任务
```

通过在 VS Code 中的调试器中运行文件（F5）来运行代码。清单 4.6 中的代码使用一个简单的任务来演示代码编写。清单 4.7 显示了一些可供选择的示例。这些编码任务也是作者评估 LLM 编码能力的一些常规基准。

**代码清单 4.7: 简单的编码任务示例**

```python
write a Python function to check if a number is prime
code a classic snake game using Pygame
code a classic asteroids game in Python using Pygame
```

**说明：** 要享受迭代这些任务，请在 Windows 上使用 Windows Subsystem for Linux (WSL)，或使用 Docker。

代码启动几秒钟后，助手将向代理回复解决方案。此时，代理将提示你提供反馈。按 Enter，基本上不提供反馈，这将提示代理运行代码以验证它是否按预期运行。

令人印象深刻的是，代理智能体甚至会提示安装所需的包，如 Pygame。然后它将运行代码，你将在终端中或作为新窗口或浏览器看到输出。如果代码生成了新窗口/浏览器，你可以玩游戏或使用界面。

请注意，生成的窗口/浏览器在 Windows 上不会关闭，并且需要退出整个程序。要避免此问题，请通过 Windows Subsystem for Linux (WSL) 或 Docker 运行代码。AutoGen 明确建议对代码执行智能体使用 Docker，如果你熟悉容器，这是一个不错的选择。

无论哪种方式，在代理生成并运行代码后，清单 4.6 中之前设置的 working_dir 文件夹现在应该有一个包含代码的 Python 文件。这将允许你随意运行代码、进行更改，甚至要求改进，正如我们将看到的。在下一节中，我们将了解如何提高编码智能体的能力。

### 4.2.2 使用智能体批评者增强代码输出

多智能体系统的一个强大好处是你可以在完成任务时自动分配的多个角色/角色。生成或帮助编写代码可以为任何开发人员提供极大的优势，但如果该代码也经过审查和测试呢？在下一个练习中，我们将向我们的智能体系统添加另一个智能体批评者，以帮助完成编码任务。打开 autogen_coding_critic.py，如以下清单所示。

**代码清单 4.8: autogen_coding_critic.py**

```python
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

user_proxy = UserProxyAgent(
    "user",
    code_execution_config={
        "work_dir": "working",
        "use_docker": False,
        "last_n_messages": 1,
    },
    human_input_mode="ALWAYS",
    is_termination_msg=lambda x:
        x.get("content", "").rstrip().endswith("TERMINATE"),
)

engineer = AssistantAgent(
    name="Engineer",
    llm_config={"config_list": config_list},
    system_message="""
    You are a profession Python engineer, known for your expertise in
software development.
    You use your skills to create software applications, tools, and
games that are both functional and efficient.
    Your preference is to write clean, well-structured code that is easy
to read and maintain.
    """,  # 这次，助手被赋予了系统/角色消息
)

critic = AssistantAgent(
    name="Reviewer",
    llm_config={"config_list": config_list},
    system_message="""
    You are a code reviewer, known for your thoroughness and commitment
to standards.
    Your task is to scrutinize code content for any harmful or
substandard elements.
    You ensure that the code is secure, efficient, and adheres to best
practices.
    You will identify any issues or areas for improvement in the code
and output them as a list.
    """,  # 创建了具有背景的第二个助手批评者智能体
)

def review_code(recipient, messages, sender, config):  # 自定义函数帮助提取代码供批评者审查
    return f"""
            Review and critque the following code.

            {recipient.chat_messages_for_summary(sender)[-1]['content']}
            """

user_proxy.register_nested_chats(  # 在批评者和工程师之间创建嵌套聊天
    [
        {
            "recipient": critic,
            "message": review_code,
            "summary_method": "last_msg",
            "max_turns": 1,
        }
    ],
    trigger=engineer,
)

task = """Write a snake game using Pygame."""

res = user_proxy.initiate_chat(
    recipient=engineer,
    message=task,
    max_turns=2,
    summary_method="last_msg"  # 代理智能体使用最大延迟和明确的摘要方法发起聊天
)
```

在 VS Code 中以调试模式运行 autogen_coding_critic.py 文件，并观察智能体之间的对话。这次，在代码返回后，批评者也将被触发以响应。然后，批评者将添加评论和改进代码的建议。

嵌套聊天对于支持和控制智能体交互效果很好，但我们将在以下部分看到更好的方法。不过，在此之前，我们将在下一节中查看 AutoGen 缓存的重要性。

### 4.2.3 理解 AutoGen 缓存

AutoGen 作为对话式多智能体平台可以在聊天迭代中消耗许多令牌。如果你要求 AutoGen 处理复杂或新颖的问题，你甚至可能会遇到 LLM 的令牌限制；因此，AutoGen 支持几种减少令牌使用的方法。

AutoGen 使用缓存来存储进度并减少令牌使用。默认情况下启用缓存，你可能已经遇到过它。如果你检查当前工作文件夹，你会注意到一个 .cache 文件夹，如图 4.8 所示。缓存允许你的智能体在被中断时继续对话。

**图 4.8: AutoGen 缓存和工作文件夹**
- 代码输出的文件夹在这里
- 输出代码文件以临时名称命名
- 缓存由文件夹表示，并包含消息历史记录的 SQLite 数据库

在代码中，你可以控制智能体运行的缓存文件夹，如清单 4.9 所示。通过使用 with 语句包装 initiate_chat 调用，你可以控制缓存的位置和种子。这将允许你通过设置上一个缓存的 cache_seed 来保存并返回到将来长期运行的 AutoGen 任务。

**代码清单 4.9: 设置缓存文件夹**

```python
with Cache.disk(cache_seed=42) as cache:  # 设置 seed_cache 表示单独的位置
    res = user_proxy.initiate_chat(
        recipient=engineer,
        message=task,
        max_turns=2,
        summary_method="last_msg",
        cache=cache,  # 将缓存设置为参数
    )
```

此缓存能力允许你从以前的缓存位置继续操作并捕获以前的运行。这也是演示和检查智能体对话如何生成结果的好方法。在下一节中，我们将了解 AutoGen 支持群聊的另一种对话模式。

## 4.3 使用智能体和 AutoGen 进行群聊

聊天委派和嵌套聊天或对话的一个问题是信息的传递。如果你玩过电话游戏，你就会亲身见证这一点，并体验到信息在迭代中变化的速度有多快。对于智能体来说，这当然也不例外，通过嵌套或顺序对话聊天可能会改变任务甚至所需的结果。

**电话游戏**

电话游戏是一个有趣但具有教育意义的游戏，演示了信息和连贯性的丧失。孩子们排成一排，第一个孩子收到一条只有他们能听到的消息。然后，孩子们依次口头将消息传递给下一个孩子，依此类推。最后，最后一个孩子向整个小组宣布消息，这通常与相同的消息相去甚远。

为了解决这个问题，AutoGen 提供了群聊，这是一种智能体参与共享对话的机制。这允许智能体查看所有过去的对话，并更好地协作处理长期运行和复杂的任务。

图 4.9 显示了嵌套和协作群聊之间的区别。我们在上一节中使用了嵌套聊天功能来构建嵌套智能体聊天。在本节中，我们使用群聊来提供更协作的体验。

**图 4.9: 可对话智能体的嵌套聊天和群聊之间的区别**

**可对话智能体嵌套聊天：**
- 用户代理
- 代理向批评者发起聊天
- 工程师
- 批评者
- 表示对批评者的嵌套聊天
- 批评者回复建议的更新和更改

**可对话智能体群聊：**
- 用户代理
- 聊天管理器
- 智能体现在通过群聊管理器协作
- 工程师
- 批评者
- 消息通过群聊管理器传递

打开 autogen_coding_group.py 和相关部分，如清单 4.10 所示。代码与之前的练习类似，但现在引入了 GroupChat 和 GroupChatManager。智能体和消息与群聊一起保存，类似于 Slack 或 Discord 等应用程序中的消息通道。聊天管理器协调消息响应以减少对话重叠。

**代码清单 4.10: autogen_coding_group.py（相关部分）**

```python
user_proxy = UserProxyAgent(
    "user",
    code_execution_config={
        "work_dir": "working",
        "use_docker": False,
        "last_n_messages": 3,
    },
    human_input_mode="NEVER",  # 人工输入现在设置为从不，所以没有人工反馈
)

llm_config = {"config_list": config_list}
engineer = AssistantAgent(…  # 代码省略，但请查阅文件中对角色的更改
critic = AssistantAgent(…

groupchat = GroupChat(agents=[user_proxy,
                              engineer,
                              critic],
                      messages=[],
                      max_round=20)  # 此对象保存到所有智能体的连接并存储消息

manager = GroupChatManager(groupchat=groupchat,
                           llm_config=llm_config)  # 管理器像主持人一样协调对话

task = """Write a snake game using Pygame."""

with Cache.disk(cache_seed=43) as cache:
    res = user_proxy.initiate_chat(
        recipient=manager,
        message=task,
        cache=cache,
    )
```

运行此练习，你将看到智能体如何协作。工程师现在将接受批评者的反馈并采取行动来解决批评者的建议。这也允许代理参与所有对话。

群组对话是加强智能体在任务上协作能力的绝佳方式。但是，它们也更加冗长且令牌昂贵。当然，随着 LLM 的成熟，其上下文令牌窗口的大小和令牌处理的价格也在成熟。随着令牌窗口的增加，对令牌消耗的担忧可能最终会消失。

AutoGen 是一个强大的多智能体平台，可以使用 Web 界面或代码体验。无论你的偏好如何，这个智能体协作工具都是构建代码或其他复杂任务的绝佳平台。当然，它不是唯一的平台，正如你将在下一节中看到的，我们将探索一个名为 CrewAI 的新手。

## 4.4 使用 CrewAI 构建智能体团队

CrewAI 在多智能体系统领域相对较新。AutoGen 最初是从研究开发然后扩展的，而 CrewAI 是考虑企业系统而构建的。因此，该平台更加健壮，这使得它在某些方面不太可扩展。

使用 CrewAI，你可以构建智能体团队专注于任务目标的特定领域。与 AutoGen 不同，CrewAI 不需要使用用户代理智能体，而是假设智能体只在它们之间工作。

图 4.10 显示了 CrewAI 平台的主要元素、它们如何连接在一起以及它们的主要功能。它显示了一个具有通用研究员和作家智能体的顺序处理智能体系统。智能体被分配任务，这些任务还可能包括工具或内存来协助它们。

**图 4.10: CrewAI 系统的组成**

**团队（Crew）:**
- 任务
- 智能体
- 工具
- 内存

**顺序处理:**
- 研究此{主题}
- 撰写此主题

**智能体:**
- 研究员
  - 目标：
  - 背景故事：
- 作家
  - 目标：
  - 背景故事：

**智能体有目标和背景故事作为他们的角色**

**工具:**
- 搜索
- 调用 API
- 访问数据

**内存:**
- 对话式
- 任务特定
- 语义

**支持各种形式的内存和检索增强生成（RAG）模式**

**处理可以是顺序的或分层的**

CrewAI 支持两种主要的处理形式：顺序和分层。图 4.10 通过迭代给定的智能体及其相关任务显示了顺序过程。在下一节中，我们深入研究一些代码来设置团队并使用它来完成目标并创建一个好笑话。

### 4.4.1 创建 CrewAI 智能体的笑话团队

CrewAI 需要比 AutoGen 更多的设置，但这也允许更多的控制和额外的指南，这提供了更具体的上下文来指导智能体完成给定的任务。这并非没有问题，但它确实提供了比 AutoGen 开箱即用的更多控制。

在 VS Code 中打开 crewai_introduction.py 并查看顶部部分，如清单 4.11 所示。配置智能体需要许多设置，包括角色、目标、冗长性、内存、背景故事、委派，甚至工具（未显示）。在此示例中，我们使用两个智能体：高级笑话研究员和笑话作家。

**代码清单 4.11: crewai_introduction.py（智能体部分）**

```python
from crewai import Agent, Crew, Process, Task
from dotenv import load_dotenv

load_dotenv()

joke_researcher = Agent(  # 创建智能体并为它们提供目标
    role="Senior Joke Researcher",
    goal="Research what makes things funny about the following {topic}",
    verbose=True,  # verbose 允许智能体向终端发出输出
    memory=True,  # 支持智能体使用内存
    backstory=(  # 背景故事是智能体的背景——它的角色
        "Driven by slapstick humor, you are a seasoned joke researcher"
        "who knows what makes people laugh. You have a knack for finding"
        "the funny in everyday situations and can turn a dull moment into"
        "a laugh riot."
    ),
    allow_delegation=True,  # 智能体可以被委派或允许委派；True 表示它们可以委派
)

joke_writer = Agent(  # 创建智能体并为它们提供目标
    role="Joke Writer",
    goal="Write a humourous and funny joke on the following {topic}",
    verbose=True,  # verbose 允许智能体向终端发出输出
    memory=True,  # 支持智能体使用内存
    backstory=(  # 背景故事是智能体的背景——它的角色
        "You are a joke writer with a flair for humor. You can turn a"
        "simple idea into a laugh riot. You have a way with words and"
        "can make people laugh with just a few lines."
    ),
    allow_delegation=False,  # 智能体可以被委派或允许委派；True 表示它们可以委派
)
```

向下移动代码，我们接下来看到任务，如清单 4.12 所示。任务表示智能体完成主要系统目标的过程。它们还将智能体链接到特定任务上工作，定义该任务的输出，并可能包括如何执行它。

**代码清单 4.12: crewai_introduction.py（任务部分）**

```python
research_task = Task(  # Task 描述定义了智能体将如何完成任务
    description=(
        "Identify what makes the following topic:{topic} so funny."
        "Be sure to include the key elements that make it humourous."
        "Also, provide an analysis of the current social trends,"
        "and how it impacts the perception of humor."
    ),
    expected_output="A comprehensive 3 paragraphs long report on the latest jokes.",  # 明确定义执行任务的预期输出
    agent=joke_researcher,  # 分配到任务的智能体
)

write_task = Task(  # Task 描述定义了智能体将如何完成任务
    description=(
        "Compose an insightful, humourous and socially aware joke on {topic}."
        "Be sure to include the key elements that make it funny and"
        "relevant to the current social trends."
    ),
    expected_output="A joke on {topic}.",  # 明确定义执行任务的预期输出
    agent=joke_writer,  # 分配到任务的智能体
    async_execution=False,  # 智能体是否应该异步执行
    output_file="the_best_joke.md",  # 智能体将生成的任何输出
)
```

现在，我们可以看到一切如何在文件底部作为 Crew 组合在一起，如清单 4.13 所示。同样，构建 Crew 时可以设置许多选项，包括智能体、任务、流程类型、内存、缓存、每分钟最大请求数（max_rpm）以及团队是否共享。

**代码清单 4.13: crewai_introduction.py（团队部分）**

```python
crew = Crew(
    agents=[joke_researcher, joke_writer],  # 组装到团队中的智能体
    tasks=[research_task, write_task],  # 智能体可以工作的任务
    process=Process.sequential,  # 定义智能体将如何交互
    memory=True,  # 系统是否应该使用内存；如果智能体/任务打开，则需要设置
    cache=True,  # 系统是否应该使用缓存，类似于 AutoGen
    max_rpm=100,  # 系统应限制自己的每分钟最大请求数
    share_crew=True,  # 团队是否应该共享信息，类似于群聊
)

result = crew.kickoff(inputs={"topic": "AI engineer jokes"})
print(result)
```

完成审查后，在 VS Code 中运行文件（F5），并观察终端中团队的对话和消息。正如你现在可能已经知道的，这个智能体系统的目标是制作与 AI 工程相关的笑话。以下是智能体系统在几次运行中生成的一些更有趣的笑话：

- 为什么计算机很冷？它把 Windows 打开了。
- 为什么 AI 工程师不和他们的算法玩捉迷藏？因为无论它们藏在哪里，算法总是在"过拟合"房间找到它们！
- AI 工程师最喜欢的歌是什么？"我只是打电话说我爱你……并为我的语音识别软件收集更多数据。"
- 为什么 AI 工程师破产了？因为他把所有钱都花在了 cookie 上，但他的浏览器一直在吃它们。

在运行笑话团队的更多迭代之前，你应该阅读下一节。本节展示了如何向多智能体系统添加可观察性。

### 4.4.2 使用 AgentOps 观察智能体工作

观察像多智能体系统这样的复杂组合对于理解可能发生的无数问题至关重要。通过应用程序跟踪的可观察性是任何复杂系统的关键元素，特别是那些从事企业使用的系统。

CrewAI 支持连接到一个名为 AgentOps 的专门智能体操作平台。这个可观察性平台是通用的，旨在支持任何特定于 LLM 使用的智能体平台的可观察性。目前，没有可用的定价或商业化详细信息。

连接到 AgentOps 就像安装包、获取 API 密钥并在团队设置中添加一行代码一样简单。下一个练习将介绍连接和运行 AgentOps 的步骤。

清单 4.14 显示了使用 pip 安装 agentops 包。你可以单独安装包，也可以作为 crewai 包的附加组件。请记住，AgentOps 也可以连接到其他智能体平台以进行可观察性。

**代码清单 4.14: 安装 AgentOps**

```bash
pip install agentops

# 或作为 CrewAI 的选项
pip install crewai[agentops]
```

在使用 AgentOps 之前，你需要注册一个 API 密钥。以下是在撰写本文时在注册密钥的一般步骤：

1. 在浏览器中访问 https://app.agentops.ai
2. 注册一个帐户
3. 创建一个项目，或使用默认项目
4. 转到设置 > 项目和 API 密钥
5. 复制和/或生成新的 API 密钥；这将把密钥复制到你的浏览器
6. 将密钥粘贴到项目中的 .env 文件

复制 API 密钥后，它应该类似于以下清单中显示的示例。

**代码清单 4.15: .env：添加 AgentOps 密钥**

```
AGENTOPS_API_KEY="your API key"
```

现在，我们需要向 CrewAI 脚本添加几行代码。清单 4.16 显示了添加到 crewai_agentops.py 文件的内容。创建自己的脚本时，你只需要在使用 CrewAI 时添加 agentops 包并初始化它。

**代码清单 4.16: crewai_agentops.py（AgentOps 添加）**

```python
import agentops  # 添加所需的包
from crewai import Agent, Crew, Process, Task
from dotenv import load_dotenv

load_dotenv()
agentops.init()  # 确保在加载环境变量后初始化包
```

在 VS Code 中运行 crewai_agentops.py 文件（F5），并像以前一样观察智能体工作。但是，你现在可以转到 AgentOps 仪表板并在各个级别查看智能体交互。

图 4.11 显示了运行笑话团队创建最佳笑话的仪表板。几个统计数据包括总持续时间、运行环境、提示和完成令牌、LLM 调用时间和估计成本。看到成本既可以清醒也可以表明智能体对话可以变得多么冗长。

**图 4.11: 运行笑话团队的 AgentOps 仪表板**
- 你甚至可以跟踪单个 LLM 调用、动作和工具使用
- 提示和回复也被捕获所有迭代
- 捕获了关于整个智能体对话序列的各种统计数据，包括成本
- 系统信息也被捕获

AgentOps 平台是任何智能体平台的绝佳补充。虽然它内置于 CrewAI 中，但可观察性可以添加到 AutoGen 或其他框架的帮助。AgentOps 的另一个吸引人的地方是它致力于观察智能体交互，而不是从机器学习操作平台转变。在未来，我们可能会看到更多智能体可观察性模式的产生。

一个不能被夸大的好处是可观察性平台可以提供的成本观察。你注意到图 4.11 中创建一个笑话的成本略高于 50 美分吗？智能体可以非常强大，但它们也可能变得非常昂贵，观察这些成本在实用性和商业化方面是至关重要的。

在本章的最后一节中，我们将回到 CrewAI 并重新审视构建可以编写游戏代码的智能体。这将提供 AutoGen 和 CrewAI 功能之间的绝佳比较。

## 4.5 使用 CrewAI 重新审视编码智能体

比较多智能体平台之间能力的一个好方法是在机器人中实现类似的任务。在下一组练习中，我们将使用 CrewAI 作为游戏编程团队。当然，这也可以适应其他编码任务。

在 VS Code 中打开 crewai_coding_crew.py，我们将首先查看清单 4.17 中的智能体部分。在这里，我们创建了一名高级工程师、一名 QA 工程师和一名首席 QA 工程师，具有角色、目标和背景故事。

**代码清单 4.17: crewai_coding_crew.py（智能体部分）**

```python
print("## Welcome to the Game Crew")
print("-------------------------------")
game = input("What is the game you would like to build? What will be the mechanics?\n")  # 允许用户输入游戏指令

senior_engineer_agent = Agent(
    role="Senior Software Engineer",
    goal="Create software as needed",
    backstory=dedent(
        """
        You are a Senior Software Engineer at a leading tech think tank.
        Your expertise in programming in python. and do your best to
        produce perfect code
        """
    ),
    allow_delegation=False,
    verbose=True,
)

qa_engineer_agent = Agent(
    role="Software Quality Control Engineer",
    goal="create prefect code, by analizing the code that is given for errors",
    backstory=dedent(
        """
        You are a software engineer that specializes in checking code
        for errors. You have an eye for detail and a knack for finding
        hidden bugs.
        You check for missing imports, variable declarations, mismatched
        brackets and syntax errors.
        You also check for security vulnerabilities, and logic errors
        """
    ),
    allow_delegation=False,
    verbose=True,
)

chief_qa_engineer_agent = Agent(
    role="Chief Software Quality Control Engineer",
    goal="Ensure that the code does the job that it is supposed to do",
    backstory=dedent(
        """
        You are a Chief Software Quality Control Engineer at a leading
        tech think tank. You are responsible for ensuring that the code
        that is written does the job that it is supposed to do.
        You are responsible for checking the code for errors and ensuring
        that it is of the highest quality.
        """
    ),
    allow_delegation=True,  # 只有首席 QA 工程师可以委派任务
    verbose=True,
)
```

在文件中向下滚动将显示智能体任务，如清单 4.18 所示。任务描述和预期输出应该易于理解。同样，每个智能体都有一个特定的任务，以在完成任务时提供更好的上下文。

**代码清单 4.18: crewai_coding_crew.py（任务部分）**

```python
code_task = Task(
    description=f"""
You will create a game using python, these are the instructions:
        Instructions
        ------------
        {game}  # 游戏指令使用 Python 格式化替换到提示中
        You will write the code for the game using python.""",
    expected_output="Your Final answer must be the full python code, only the python code and nothing else.",
    agent=senior_engineer_agent,
)

qa_task = Task(
    description=f"""You are helping create a game using python, these are the instructions:
        Instructions
        ------------
        {game}
        Using the code you got, check for errors. Check for logic errors,
        syntax errors, missing imports, variable declarations, mismatched brackets,
        and security vulnerabilities.""",
    expected_output="Output a list of issues you found in the code.",
    agent=qa_engineer_agent,
)

evaluate_task = Task(
    description=f"""You are helping create a game using python, these are the instructions:
        Instructions
        ------------
        {game}
        You will look over the code to insure that it is complete and
        does the job that it is supposed to do. """,
    expected_output="Your Final answer must be the corrected a full python code, only the python code and nothing else.",
    agent=chief_qa_engineer_agent,
)
```

最后，我们可以看到这如何通过转到文件底部组合在一起，如清单 4.19 所示。这个团队配置与我们之前看到的非常相似。添加了每个智能体和任务，以及 verbose 和 process 属性。对于此示例，我们将继续使用顺序方法。

**代码清单 4.19: crewai_coding_crew.py（团队部分）**

```python
crew = Crew(
    agents=[senior_engineer_agent,
            qa_engineer_agent,
            chief_qa_engineer_agent],
    tasks=[code_task, qa_task, evaluate_task],
    verbose=2,
    process=Process.sequential,  # 流程是顺序的
)

# 让你的团队工作！
result = crew.kickoff()  # kickoff 中没有提供额外的上下文
print("######################")
print(result)
```

当你运行 VS Code（F5）文件时，系统将提示你输入编写游戏的指令。输入一些指令，也许是贪吃蛇游戏或你选择的另一个游戏。然后，让智能体工作，并观察它们产生什么。

有了首席 QA 工程师的加入，结果通常看起来会比 AutoGen 产生的更好，至少是开箱即用的。如果你查看代码，你会看到它通常遵循良好的模式，在某些情况下，甚至可能包括测试和单元测试。

在完成本章之前，我们将对团队的处理模式进行最后一次更改。之前，我们使用了顺序处理，如图 4.10 所示。图 4.12 显示了 CrewAI 中的分层处理是什么样子的。

**图 4.12: 通过团队管理器协调的智能体分层处理**

**团队（Crew）:**
- 任务
- 智能体
- 工具
- 内存

**分层处理通过管理智能体协调**

**智能体:**
- 研究员
  - 目标：
  - 背景故事：
- 作家
  - 目标：
  - 背景故事：

**任务:**
- 研究此{主题}
- 撰写此主题

**团队管理器**

添加此管理器是一个相对简单的过程。清单 4.20 显示了使用分层方法使用编码团队的新文件的附加代码更改。除了从 LangChain 导入用于连接到 OpenAI 的类之外，另一个添加是将此类添加为团队管理器 manager_llm。

**代码清单 4.20: crewai_hierarchy.py（团队管理器部分）**

```python
from langchain_openai import ChatOpenAI  # 从 LangChain 导入 LLM 连接器

crew = Crew(
    agents=[senior_engineer_agent,
            qa_engineer_agent,
            chief_qa_engineer_agent],
    tasks=[code_task, qa_task, evaluate_task],
    verbose=2,
    process=Process.hierarchical,  # 选择分层处理时必须设置团队管理器
    manager_llm=ChatOpenAI(  # 将团队管理器设置为 LLM 连接器
        temperature=0, model="gpt-4"
    ),
)
```

在 VS Code 中运行此文件（F5）。提示时，输入你想创建的游戏。尝试使用你在 AutoGen 中尝试的相同游戏；贪吃蛇游戏也是一个很好的基准示例。观察智能体处理代码并反复审查问题。

运行文件后，你还可以跳转到 AgentOps 以查看此次运行的成本。机会是，它的成本将是没有智能体管理器时的两倍多。输出也可能不会显著更好。这是构建智能体系统而不了解事情会如何快速失控的陷阱。

当智能体不断迭代相同的动作时经常发生的这种螺旋的一个例子是频繁重复的任务。你可以在 AgentOps 中查看此问题，如图 4.13 所示，方法是查看 Repeat Thoughts 图。

**图 4.13: 智能体运行中发生的思想重复**
- 图表指示智能体交互中相同思想的重复

AgentOps 的 Repeat Thoughts 图是衡量你的智能体系统遇到的重复的绝佳方式。过度重复的思维模式通常意味着智能体不够果断，而是不断尝试生成不同的答案。如果你遇到此问题，你想要更改智能体的处理模式、任务和目标。你甚至可能想要改变系统的类型和智能体数量。

多智能体系统是根据工作和任务的工作模式分解工作的绝佳方式。通常，工作角色被分配给智能体角色/角色，它需要完成的任务可能是隐式的，如 AutoGen 中，或更明确的，如 CrewAI 中。

在本章中，我们介绍了许多你可以立即使用的有用工具和平台来改善你的工作、生活等。这完成了我们通过多智能体平台的旅程，但它并没有结束我们对多个智能体的探索和使用，正如我们将在后面的章节中发现的那样。

## 4.6 练习

使用以下练习来提高你对材料的了解：

**练习 1 — 使用 AutoGen 进行基本智能体通信**

目标 — 熟悉 AutoGen 中的基本智能体通信和设置。

任务：
- 按照本章中提供的说明在你的本地机器上设置 AutoGen Studio
- 创建一个具有用户代理和两个助手智能体的简单多智能体系统
- 实现一个基本任务，其中用户代理在助手智能体之间协调以生成简单的文本输出，例如总结一个简短的段落

**练习 2 — 在 AutoGen Studio 中实现高级智能体技能**

目标 — 通过添加高级技能来增强智能体能力。

任务：
- 开发并将新技能集成到 AutoGen 智能体中，使其能够从公共 API（例如，天气信息或股票价格）获取和显示实时数据
- 确保智能体可以询问用户偏好（例如，天气的城市、股票类型）并相应地显示获取的数据

**练习 3 — 使用 CrewAI 进行基于角色的任务管理**

目标 — 探索 CrewAI 中的基于角色的任务管理。

任务：
- 设计一个 CrewAI 设置，其中多个智能体被分配特定角色（例如，数据获取器、分析器、演示者）
- 配置一个任务序列，其中数据获取器收集数据，分析器处理数据，演示者生成报告
- 执行序列并观察智能体之间的信息流和任务委派

**练习 4 — 使用 AutoGen 在群聊中进行多智能体协作**

目标 — 理解并在 AutoGen 中实现群聊系统以促进智能体协作。

任务：
- 设置一个场景，其中多个智能体需要协作解决复杂问题（例如，规划商务旅行的行程）
- 使用群聊功能允许智能体共享信息、提出问题并向彼此提供更新
- 监控智能体的交互和在协作解决问题中的有效性

**练习 5 — 在 CrewAI 中使用 AgentOps 添加和测试可观察性**

目标 — 在 CrewAI 环境中使用 AgentOps 实现和评估智能体的可观察性。

任务：
- 将 AgentOps 集成到 CrewAI 多智能体系统中
- 为智能体设计一个涉及大量计算或数据处理的任务（例如，分析客户评论以确定情感趋势）
- 使用 AgentOps 监控智能体的性能、成本和输出准确性。识别智能体交互中的任何潜在低效或错误

## 本章小结

- AutoGen 由 Microsoft 开发，是一个对话式多智能体平台，使用各种智能体类型，如用户代理和助手智能体，通过自然语言交互促进任务执行。

- AutoGen Studio 充当开发环境，允许用户创建、测试和管理多智能体系统，增强 AutoGen 的可用性。

- AutoGen 支持多种通信模式，包括群聊以及分层和代理通信。代理通信涉及一个主要智能体（代理），它在用户和其他智能体之间进行接口以简化任务完成。

- CrewAI 提供了一种结构化的方法来构建多智能体系统，重点关注企业应用程序。它强调基于角色和自主智能体功能，允许灵活的、顺序的或分层的任务管理。

- 本章中的实际练习说明了如何设置和使用 AutoGen Studio，包括安装必要的组件和运行基本的多智能体系统。

- AutoGen 中的智能体可以配备特定技能来执行任务，如代码生成、图像分析和数据检索，从而扩大其应用范围。

- CrewAI 的区别在于它能够比 AutoGen 更严格地构建智能体交互，这在需要精确和受控智能体行为的设置中可能是有利的。

- CrewAI 支持集成内存和工具供智能体通过任务完成来消费。

- CrewAI 支持与 AgentOps 等可观察性工具集成，提供了对智能体性能、交互效率和成本管理的见解。

- AgentOps 是一个智能体可观察性平台，可以帮助你轻松监控广泛的智能体交互。

---

**翻译完成日期:** 2025-11-13
**翻译工具:** Claude AI (Sonnet 4.5)
**用途说明:** 本翻译仅供个人学习使用，请勿用于商业用途
