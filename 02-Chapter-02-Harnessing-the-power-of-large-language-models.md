# AI Agents in Action 第2章 Claude翻译版

================================================================================
第2章 驾驭大语言模型的力量
================================================================================
**原书名称:** AI Agents in Action.pdf
**页码范围:** 38 - 62
**翻译说明:** 本翻译由 Claude AI 协助完成，仅供个人学习使用
================================================================================

## 第2章 驾驭大语言模型的力量

"大语言模型"（LLM）这个术语现在已经成为一种 AI 形式的普遍描述。这些 LLM 是使用生成式预训练转换器（GPT）开发的。虽然其他架构也为 LLM 提供动力，但 GPT 形式目前是最成功的。

LLM 和 GPT 是生成式模型，这意味着它们被训练用于生成而不是预测或分类内容。为了进一步说明这一点，请考虑图 2.1，它显示了生成式模型和预测/分类模型之间的区别。生成式模型从输入创建某些内容，而预测和分类模型则对其进行分类。

### 本章内容概要
- 理解 LLM 的基础知识
- 连接和使用 OpenAI API
- 使用 LM Studio 探索和使用开源 LLM
- 使用提示工程技术提示 LLM
- 为你的特定需求选择最佳 LLM

我们可以通过其组成部分进一步定义 LLM，如图 2.2 所示。在此图中，**数据**代表用于训练模型的内容，**架构**是模型本身的属性，例如参数数量或模型大小。模型会进一步针对所需用例进行专门训练，包括聊天、补全或指令。最后，**微调**是添加到模型的功能，它改进输入数据和模型训练以更好地匹配特定用例或领域。

### LLM 的主要元素

**数据（Data）**
- 输入数据代表模型将训练的内容
- 这通常包括 TB 到 PB 级别的数据

**架构（Architecture）**
- 表示模型架构
- 架构定义诸如上下文、令牌限制、嵌入大小和参数数量（模型大小）等内容

**训练（Training）**
- 定义用于训练模型的训练形式
- 训练还将定义模型用例，例如聊天补全、补全、指令或问答

**微调（Fine-tuning）**
- 微调是使模型更特定于特定领域或数据集的过程

GPT 的转换器架构（这是 LLM 的特定架构）允许模型扩展到数十亿个参数的规模。这需要在大量文档上训练这些大型模型以建立基础。从那里，这些模型将使用各种方法针对模型的所需用例进行连续训练。

例如，ChatGPT 有效地在公共互联网上进行训练，然后使用多种训练策略进行微调。最终的微调训练使用一种称为**人类反馈强化学习**（RLHF）的高级形式完成。这产生了一个称为聊天补全的模型用例。

**聊天补全 LLM** 被设计为通过迭代和优化来改进——换句话说，聊天。这些模型也被基准测试为在任务完成、推理和规划方面表现最佳，这使它们成为构建智能体和助手的理想选择。补全模型仅被训练/设计用于根据输入文本提供生成的内容，因此它们不会从迭代中受益。

对于我们在本书中构建强大智能体的旅程，我们专注于称为聊天补全模型的 LLM 类别。当然，这并不排除你尝试其他模型形式用于你的智能体。但是，你可能必须显著修改提供的代码示例以支持其他模型形式。

我们将在本章后面查看本地运行开源 LLM 时揭示有关 LLM 和 GPT 的更多详细信息。在下一节中，我们将了解如何使用 OpenAI 日益增长的标准连接到 LLM。

## 2.1 掌握 OpenAI API

许多 AI 智能体和助手项目使用 OpenAI API SDK 连接到 LLM。虽然不是标准，但描述连接的基本概念现在遵循 OpenAI 模式。因此,我们必须理解使用 OpenAI SDK 进行 LLM 连接的核心概念。

本章将研究使用 OpenAI Python SDK/包连接到 LLM 模型。我们将讨论连接到 GPT-4 模型、模型响应、计数令牌以及如何定义一致的消息。从下面的小节开始，我们将研究如何使用 OpenAI。

### 2.1.1 连接到聊天补全模型

要完成本节和后续章节中的练习，你必须设置 Python 开发环境并获得对 LLM 的访问权限。附录 A 将指导你设置 OpenAI 帐户并访问 GPT-4 或其他模型。附录 B 演示了如何使用 Visual Studio Code（VS Code）设置 Python 开发环境，包括安装所需的扩展。如果你想跟随场景操作，请查看这些部分。

首先在 VS Code 中打开源代码 chapter_2 文件夹并创建一个新的 Python 虚拟环境。同样，如果需要帮助，请参阅附录 B。

然后，使用以下清单中的命令安装 OpenAI 和 Python dot environment 包。这将把所需的包安装到虚拟环境中。

```bash
pip install openai python-dotenv
```

接下来，在 VS Code 中打开 `connecting.py` 文件，并检查清单 2.2 中显示的代码。确保将模型名称设置为适当的名称——例如，gpt-4。在撰写本文时，gpt-4-1106-preview 用于代表 GPT-4 Turbo。

**代码清单 2.2: connecting.py**

```python
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # 加载存储在 .env 文件中的密钥
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:  # 检查是否设置了密钥
    raise ValueError("No API key found. Please check your .env file.")

client = OpenAI(api_key=api_key)  # 使用密钥创建客户端

def ask_chatgpt(user_message):
    response = client.chat.completions.create(  # 使用 create 函数生成响应
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content  # 仅返回响应的内容

user = "What is the capital of France?"
response = ask_chatgpt(user)  # 执行请求并返回响应
print(response)
```

这里发生了很多事情，所以让我们从开始和加载环境变量分解。在 chapter_2 文件夹中有另一个名为 `.env` 的文件，它保存环境变量。通过调用 `load_dotenv` 函数自动设置这些变量。

你必须在 `.env` 文件中设置你的 OpenAI API 密钥，如下一个清单所示。同样，请参阅附录 A 以了解如何获取密钥和查找模型名称。

**代码清单 2.3: .env**

```
OPENAI_API_KEY='your-openai-api-key'
```

设置密钥后，你可以通过按 F5 键或从 VS Code 菜单中选择 Run > Start Debugging 来调试文件。这将运行代码，你应该看到类似"The capital of France is Paris."的内容。

请记住，生成式模型的响应取决于概率。在这种情况下，模型可能会给我们一个正确且一致的答案。

你可以通过调整请求的温度来调整这些概率。如果你希望模型更一致，请将温度降至 0，但如果你希望模型产生更多变化，请提高温度。我们将在下一节中进一步探索温度设置。

### 2.1.2 理解请求和响应

深入了解聊天补全请求和响应功能可能会有所帮助。我们将首先关注请求，如下所示。请求封装了预期的模型、消息和温度。

**代码清单 2.4: 聊天补全请求**

```python
response = client.chat.completions.create(
    model="gpt-4-1106-preview",  # 用于响应请求的模型或部署
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},  # 系统角色消息
        {"role": "user", "content": user_message}  # 用户角色消息
    ],
    temperature=0.7,  # 请求的温度或可变性
)
```

在请求中，消息块描述了请求中使用的一组消息和角色。聊天补全模型的消息可以在三个角色中定义：

- **系统角色** - 描述请求的规则和准则的消息。它通常可以用于描述 LLM 在请求中的角色。
- **用户角色** - 代表并包含来自用户的消息。
- **助手角色** - 可用于捕获 LLM 先前响应的消息历史记录。它还可以在可能不存在的情况下注入消息历史记录。

单个请求中发送的消息可以封装整个对话，如下一个清单中的 JSON 所示。

**代码清单 2.5: 带历史记录的消息**

```json
[
    {
        "role": "system",
        "content": "You are a helpful assistant."
    },
    {
        "role": "user",
        "content": "What is the capital of France?"
    },
    {
        "role": "assistant",
        "content": "The capital of France is Paris."
    },
    {
        "role": "user",
        "content": "What is an interesting fact of Paris."
    }
]
```

你可以通过在 VS Code 中打开 `message_history.py` 并按 F5 进行调试来查看如何应用它。文件运行后，请务必检查输出。然后，尝试再运行几次样本以查看结果如何变化。

由于温度设置为 0.7，结果每次运行都会改变。继续将温度降低到 0.0，并再运行几次 `message_history.py` 样本。将温度保持在 0 将每次显示相同或相似的结果。

设置请求的温度通常取决于你的特定用例。有时，你可能希望限制响应的随机性。将温度降至 0 将给出一致的结果。同样，值为 1.0 将在响应中给出最大的可变性。

接下来，我们还想知道每个请求返回的信息。下一个清单显示了响应的输出格式。你可以通过在 VS Code 中运行 `message_history.py` 文件来查看此输出。

**代码清单 2.6: 聊天补全响应**

```json
{
    "id": "chatcmpl-8WWL23up3IRfK1nrDFQ3EHQfhx0U6",
    "choices": [  // 模型可能返回多个响应
        {
            "finish_reason": "stop",
            "index": 0,
            "message": {
                "content": "… omitted",
                "role": "assistant",  // 以助手角色返回的响应
                "function_call": null,
                "tool_calls": null
            },
            "logprobs": null
        }
    ],
    "created": 1702761496,
    "model": "gpt-4-1106-preview",  // 指示使用的模型
    "object": "chat.completion",
    "system_fingerprint": "fp_3905aa4f79",
    "usage": {
        "completion_tokens": 78,  // 计算输入（提示）和
        "prompt_tokens": 48,      // 输出（补全）令牌的使用数量
        "total_tokens": 126
    }
}
```

跟踪输入令牌（提示中使用的令牌）和输出令牌（通过补全返回的数量）的数量可能会有所帮助。有时，最小化和减少令牌数量可能至关重要。令牌更少通常意味着 LLM 交互会更便宜、响应更快，并产生更好、更一致的结果。

这涵盖了连接到 LLM 和返回响应的基础知识。在本书中，我们将回顾并扩展如何与 LLM 交互。在此之前，我们将在下一节中探索如何加载和使用开源 LLM。

## 2.2 使用 LM Studio 探索开源 LLM

像 OpenAI 的 GPT-4 这样的商业 LLM 是学习如何使用现代 AI 和构建智能体的绝佳起点。但是，商业智能体是一种外部资源，需要成本、降低数据隐私和安全性，并引入依赖性。其他外部影响可能会进一步使这些因素复杂化。

毫不奇怪，构建可比较的开源 LLM 的竞赛日益激烈。因此，现在有开源 LLM 可能足以应对许多任务和智能体系统。仅在一年内，工具方面就取得了如此多的进步，以至于本地托管 LLM 现在非常容易，我们将在下一节中看到。

### 2.2.1 安装和运行 LM Studio

LM Studio 是一个免费下载的软件，支持为 Windows、Mac 和 Linux 下载和本地托管 LLM 和其他模型。该软件易于使用，并提供了几个有用的功能可让你快速入门。以下是下载和设置 LM Studio 的快速步骤摘要：

1. 从 https://lmstudio.ai/ 下载 LM Studio。
2. 下载后，根据你的操作系统安装软件。请注意，某些版本的 LM Studio 可能处于测试阶段，需要安装其他工具或库。
3. 启动软件。

图 2.3 显示了正在运行的 LM Studio 窗口。从那里，你可以查看当前的热门模型列表、搜索其他模型，甚至下载。主页内容对于理解顶级模型的详细信息和规格非常有用。

LM Studio 的一个吸引人的功能是它能够分析你的硬件并将其与给定模型的要求对齐。该软件会让你知道你运行给定模型的效果如何。这在指导你尝试哪些模型方面可以节省大量时间。

**LM Studio 软件主页功能：**
- 搜索区域
- 浏览已下载的模型
- 聊天界面直接与本地 LLM 对话
- 将本地模型作为服务运行

输入一些文本以搜索模型，然后单击 Go。你将被带到搜索页面界面，如图 2.4 所示。从此页面，你可以看到所有模型变体和其他规格，例如上下文令牌大小。单击"兼容性猜测"按钮后，软件甚至会告诉你模型是否会在你的系统上运行。

单击以下载将在你的系统上运行的任何模型。你可能希望坚持使用为聊天补全设计的模型，但如果你的系统有限，请使用你拥有的内容。此外，如果你不确定使用哪个模型，请继续下载尝试它们。LM Studio 是探索和试验许多模型的好方法。

**LM Studio 搜索页面功能：**
- 搜索文本
- 在 Hugging Face 上查看模型卡
- 兼容性猜测器告诉你模型是否会运行
- 显示已下载的模型

下载模型后，你可以在聊天页面上加载和运行模型，或在服务器页面上作为服务器运行。图 2.5 显示在聊天页面上加载和运行模型。它还显示了启用和使用 GPU 的选项（如果你有的话）。

要加载和运行模型，请打开页面顶部中间的下拉菜单，然后选择一个已下载的模型。将出现一个进度条显示模型加载，当它准备就绪时，你可以开始在 UI 中输入。

如果检测到 GPU，该软件甚至允许你使用部分或全部 GPU 进行模型推理。GPU 通常会在某些方面加快模型响应时间。你可以通过查看页面底部的性能状态来了解添加 GPU 如何影响模型的性能，如图 2.5 所示。

**LM Studio 聊天页面功能：**
- 已加载的模型
- 对话历史
- 用户消息的文本区域
- 模型系统提示
- 启用 GPU 加速（检测到 GPU 时可用）
- 模型性能和使用情况

与模型聊天并使用或试验各种提示可以帮助你确定模型对你的给定用例的效果如何。更系统的方法是使用提示流工具来评估提示和 LLM。我们将在第 9 章中描述如何使用提示流。

LM Studio 还允许在服务器上运行模型，并使用 OpenAI 包进行访问。我们将在下一节中了解如何使用服务器功能和提供模型。

### 2.2.2 使用 LM Studio 在本地提供 LLM

使用 LM Studio 在本地作为服务器运行 LLM 很容易。只需打开服务器页面，加载模型，然后单击"启动服务器"按钮，如图 2.6 所示。从那里，你可以复制和粘贴任何示例以连接到你的模型。

你可以通过在 VS Code 中打开 `chapter_2/lmstudio_server.py` 来查看 Python 代码示例。代码也显示在清单 2.7 中。然后，在 VS Code 调试器中运行代码（按 F5）。

**代码清单 2.7: lmstudio_server.py**

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

completion = client.chat.completions.create(
    model="local-model",  # 当前未使用；可以是任何东西
    messages=[
        {"role": "system", "content": "Always answer in rhymes."},
        {"role": "user", "content": "Introduce yourself."}  # 随意更改消息
    ],
    temperature=0.7,
)

print(completion.choices[0].message)  # 默认代码输出整个消息
```

**LM Studio 服务器页面功能：**
- 已加载的模型
- 启用 GPU 加速（检测到 GPU 时可用）
- 连接到服务器的示例
- 启动/停止服务器
- 显示启动和连接信息的日志

如果你在连接到服务器时遇到问题或遇到任何其他问题，请确保服务器模型设置的配置与模型类型匹配。例如，在之前显示的图 2.6 中，加载的模型与服务器设置不同。更正后的设置显示在图 2.7 中。

现在，你可以使用本地托管的 LLM 或商业模型来构建、测试，甚至可能运行你的智能体。以下部分将研究如何使用提示工程更有效地构建提示。

## 2.3 使用提示工程提示 LLM

为 LLM 定义的提示是请求中使用的消息内容，用于获得更好的响应输出。**提示工程**是一个新兴领域，试图构建一种构建提示的方法论。不幸的是，提示构建不是一门完善的科学，并且有越来越多样化的方法被定义为提示工程。

幸运的是，OpenAI 等组织已经开始记录一套通用策略，如图 2.8 所示。这些策略涵盖了各种策略，其中一些需要额外的基础设施和考虑。因此，与更高级概念相关的提示工程策略将在指定的章节中介绍。

**OpenAI 提示工程策略（按本书章节位置）：**

1. **编写清晰的指令**（基础）
   - 具体说明你的要求
   - 策略包括详细查询、采用角色、使用分隔符、指定步骤、提供示例和指定输出长度

2. **提供参考文本**（记忆）
   - 帮助减少虚构
   - 策略涉及指示模型使用或引用参考文本

3. **使用外部工具**（记忆）
   - 增强模型能力
   - 策略包括基于嵌入的搜索、代码执行和访问特定功能

4. **将复杂任务拆分为更简单的子任务**（规划）
   - 降低错误率
   - 策略包括意图分类、总结对话和文档的分段总结

5. **给模型时间"思考"**（规划）
   - 允许更可靠的推理
   - 策略涉及在得出结论之前制定解决方案、使用内心独白和回顾以前的答案

6. **系统地测试变化**（评估）
   - 确保改进是真实的
   - 策略涉及参考标准答案评估模型输出

图 2.8 中的每个策略都展开为可以进一步细化特定提示工程方法的策略。本章将研究基本的"编写清晰指令"策略。图 2.9 更详细地显示了此策略的策略，以及每个策略的示例。我们将在以下部分中使用代码演示来查看运行这些示例。

### 编写清晰指令策略的策略

图 2.9 显示了"编写清晰指令"策略的策略：

**1. 详细查询**
- 无详细查询："Who's the prime minister?"
- 有详细查询："Who is the prime minister of Canada, and how frequently are elections held?"
- 提示：在查询中提供尽可能多的细节；通常，细节越多越好。

**2. 采用角色**
- 系统："You are a prompt expert and will suggest ways to improve a user request."
- 用户："What is the capital of Canada?"
- 提示：角色可以包括有关人口统计、知识和个性的详细信息。

**3. 使用分隔符**
- 用户："Summarize the text delimited by triple quotes with a limerick: '''text to be summarized'''"
- 提示：分隔符可以帮助将内容块与规格详细信息分开。

**4. 指定步骤**
- 系统："Use the following step-by-step instructions to respond to user inputs:
  - Step 1 - Summarize the text in triple quotes to one sentence with a prefix that says 'Summary: '.
  - Step 2 - Translate the summary from Step 1 into French, with a prefix that says 'Translation: '."
- 用户："'''text to summarize and translate'''"
- 提示：使用步骤可以帮助 LLM 更好地处理任务，但务必限制数量。

**5. 提供示例**
- 系统："Answer in a consistent style."
- 用户："Teach me about patience."
- 助手："The river that carves the deepest valley flows from a modest spring; the most intricate tapestry begins with a solitary thread."
- 用户："Teach me about the ocean."
- 提示：示例是少样本学习的一种形式，可以是指示所需响应格式和其他详细信息的绝佳方式。

**6. 指定输出长度**
- 用户："Summarize the text delimited by triple quotes in about 50 words. '''text to summarize here'''"
- 提示：限制输出长度可以具体到单词、项目符号或其他指标。

"编写清晰指令"策略是关于仔细和具体说明你要求的内容。要求 LLM 执行任务与要求一个人完成相同任务没有什么不同。通常，你可以在请求中指定与任务相关的信息和上下文越多，响应就越好。

此策略已分解为你可以应用于提示的特定策略。要了解如何使用这些策略，第 2 章源代码文件夹中有一个包含各种提示示例的代码演示（`prompt_engineering.py`）。

在 VS Code 中打开 `prompt_engineering.py` 文件，如清单 2.8 所示。此代码首先加载提示文件夹中的所有 JSON Lines 文件。然后，它将文件列表显示为选择，并允许用户选择提示选项。选择选项后，提示将提交给 LLM，并打印响应。

**代码清单 2.8: prompt_engineering.py (main())**

```python
def main():
    directory = "prompts"
    text_files = list_text_files_in_directory(directory)  # 收集给定文件夹的所有文件

    if not text_files:
        print("No text files found in the directory.")
        return

    def print_available():  # 打印文件列表作为选择
        print("Available prompt tactics:")
        for i, filename in enumerate(text_files, start=1):
            print(f"{i}. {filename}")

    while True:
        try:
            print_available()
            choice = int(input("Enter … 0 to exit): "))  # 输入用户的选择

            if choice == 0:
                break
            elif 1 <= choice <= len(text_files):
                selected_file = text_files[choice - 1]
                file_path = os.path.join(directory, selected_file)
                prompts = load_and_parse_json_file(file_path)  # 加载提示并解析为消息

                print(f"Running prompts for {selected_file}")
                for i, prompt in enumerate(prompts):
                    print(f"PROMPT {i+1} --------------------")
                    print(prompt)
                    print(f"REPLY ---------------------------")
                    print(prompt_llm(prompt))  # 将提示提交给 OpenAI LLM
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
```

清单中有一个注释掉的部分演示了如何连接到本地 LLM。这将允许你探索应用于本地运行的开源 LLM 的相同提示工程策略。默认情况下，此示例使用我们之前在 2.1.1 节中配置的 OpenAI 模型。如果你之前没有完成，请返回并在运行此示例之前完成它。

图 2.10 显示了运行提示工程策略测试器（在 VS Code 中的 `prompt_engineering.py` 文件）的输出。运行测试器时，你可以输入要测试的策略的值并观看其运行。

在以下部分中，我们将更详细地探索每个提示策略。我们还将研究各种示例。

### 2.3.1 创建详细查询

此策略的基本前提是提供尽可能多的细节，但也要小心不要提供不相关的细节。以下清单显示了用于探索此策略的 JSON Lines 文件示例。

**代码清单 2.9: detailed_queries.jsonl**

```json
[  // 第一个示例不使用详细查询
    {
        "role": "system",
        "content": "You are a helpful assistant."
    },
    {
        "role": "user",
        "content": "What is an agent?"  // 首先向 LLM 提出一个非常笼统的问题
    }
]
[
    {
        "role": "system",
        "content": "You are a helpful assistant."
    },
    {
        "role": "user",
        "content": """
What is a GPT Agent?
Please give me 3 examples of a GPT agent
"""  // 提出更具体的问题，并要求示例
    }
]
```

此示例演示了使用详细查询和不使用详细查询之间的区别。它还进一步要求示例。请记住，你可以在提示中提供的相关性和上下文越多，整体响应就越好。要求示例是强化问题和预期输出之间关系的另一种方式。

### 2.3.2 采用角色

采用角色赋予了为 LLM 定义总体上下文或一组规则的能力。然后 LLM 可以使用该上下文和/或规则来构建所有后续输出响应。这是一种引人注目的策略，我们将在本书中大量使用它。

清单 2.10 显示了使用两个角色回答相同问题的示例。这可以是探索从获取人口统计反馈到专门从事特定任务甚至橡皮鸭调试的广泛新颖应用的一种愉快技术。

**GPT 橡皮鸭调试**

橡皮鸭调试是一种问题解决技术，其中一个人向无生命的物体（如橡皮鸭）解释问题以理解或找到解决方案。这种方法在编程和调试中很流行，因为大声阐述问题通常有助于澄清问题，并可以导致新的见解或解决方案。

GPT 橡皮鸭调试使用相同的技术，但我们使用 LLM 而不是无生命的物体。通过为 LLM 提供特定于所需解决方案领域的角色，可以进一步扩展此策略。

**代码清单 2.10: adopting_personas.jsonl**

```json
[
    {
        "role": "system",
        "content": """
You are a 20 year old female who attends college
in computer science. Answer all your replies as
a junior programmer.
"""  // 第一个角色
    },
    {
        "role": "user",
        "content": "What is the best subject to study."
    }
]
[
    {
        "role": "system",
        "content": """
You are a 38 year old male registered nurse.
Answer all replies as a medical professional.
"""  // 第二个角色
    },
    {
        "role": "user",
        "content": "What is the best subject to study."
    }
]
```

智能体配置文件的核心元素是角色。我们将使用各种角色来协助智能体完成其任务。运行此策略时，请特别注意 LLM 输出响应的方式。

### 2.3.3 使用分隔符

分隔符是隔离和让 LLM 专注于消息的某些部分的有用方法。此策略通常与其他策略结合使用，但可以独立工作。以下清单演示了两个示例，但还有几种其他描述分隔符的方法，从 XML 标签到使用 markdown。

**代码清单 2.11: using_delimiters.jsonl**

```json
[
    {
        "role": "system",
        "content": """
Summarize the text delimited by triple quotes
with a haiku.
"""  // 分隔符由字符类型和重复定义
    },
    {
        "role": "user",
        "content": "A gold chain is cool '''but a silver chain is better'''"
    }
]
[
    {
        "role": "system",
        "content": """
You will be provided with a pair of statements
(delimited with XML tags) about the same topic.
First summarize the arguments of each statement.
Then indicate which of them makes a better statement
 and explain why.
"""  // 分隔符由 XML 标准定义
    },
    {
        "role": "user",
        "content": """
<statement>gold chains are cool</statement>
<statement>silver chains are better</statement>
"""
    }
]
```

运行此策略时，请注意 LLM 在输出响应时关注的文本部分。此策略对于描述层次结构或其他关系模式中的信息非常有益。

### 2.3.4 指定步骤

指定步骤是另一种强大的策略，可以有许多用途，包括在智能体中，如清单 2.12 所示。在为复杂的多步骤任务开发提示或智能体配置文件时，它尤其强大。你可以指定步骤将这些复杂提示分解为 LLM 可以遵循的分步过程。反过来，这些步骤可以在更长时间的对话和许多迭代中通过多次交互指导 LLM。

**代码清单 2.12: specifying_steps.jsonl**

```json
[
    {
        "role": "system",
        "content": """
Use the following step-by-step instructions to respond to user inputs.
Step 1 - The user will provide you with text in triple single quotes.
Summarize this text in one sentence with a prefix that says 'Summary: '.
Step 2 - Translate the summary from Step 1 into Spanish,
with a prefix that says 'Translation: '.
"""  // 注意使用分隔符的策略
    },
    {
        "role": "user",
        "content": "'''I am hungry and would like to order an appetizer.'''"
    }
]
[
    {
        "role": "system",
        "content": """
Use the following step-by-step instructions to respond to user inputs.
Step 1 - The user will provide you with text. Answer any questions in
the text in one sentence with a prefix that says 'Answer: '.
Step 2 - Translate the Answer from Step 1 into a dad joke,
 with a prefix that says 'Dad Joke: '."""  // 步骤可以是完全不同的操作
    },
    {
        "role": "user",
        "content": "What is the tallest structure in Paris?"
    }
]
```

### 2.3.5 提供示例

提供示例是指导 LLM 所需输出的绝佳方式。有许多方法可以向 LLM 演示示例。系统消息/提示可以是强调一般输出的有用方式。在以下清单中，示例被添加为给定提示"Teach me about Python."的最后一个 LLM 助手回复。

**代码清单 2.13: providing_examples.jsonl**

```json
[
    {
        "role": "system",
        "content": """
Answer all replies in a consistent style that follows the format,
length and style of your previous responses.
Example:
  user:
       Teach me about Python.
  assistant:  // 将示例输出注入为"以前的"助手回复
       Python is a programming language developed in 1989
 by Guido van Rossum.
  Future replies:
       The response was only a sentence so limit
 all future replies to a single sentence.
"""  // 添加限制输出策略以限制输出大小并匹配示例
    },
    {
        "role": "user",
        "content": "Teach me about Java."
    }
]
```

提供示例也可用于从派生输出的一系列复杂任务中请求特定输出格式。例如，要求 LLM 生成与示例输出匹配的代码是示例的绝佳用途。我们将在整本书中使用此策略，但还有其他指导输出的方法。

### 2.3.6 指定输出长度

指定输出长度的策略不仅有助于限制令牌，还有助于将输出引导到所需格式。清单 2.14 显示了使用两种不同技术进行此策略的示例。第一个将输出限制为少于 10 个单词。这可以具有使响应更简洁和更有针对性的额外好处，这对于某些用例可能是可取的。第二个示例演示了将输出限制为一组简洁的项目符号。此方法可以帮助缩小输出范围并保持答案简短。更简洁的答案通常意味着输出更集中，包含更少的填充内容。

**代码清单 2.14: specifying_output_length.jsonl**

```json
[
    {
        "role": "system",
        "content": """
Summarize all replies into 10 or fewer words.
"""  // 限制输出使答案更简洁
    },
    {
        "role": "user",
        "content": "Please tell me an exciting fact about Paris?"
    }
]
[
    {
        "role": "system",
        "content": """
Summarize all replies into 3 bullet points.
"""  // 将答案限制为一组简短的项目符号
    },
    {
        "role": "user",
        "content": "Please tell me an exciting fact about Paris?"
    }
]
```

保持答案简洁在开发多智能体系统时可以带来额外的好处。与其他智能体对话的任何智能体系统都可以从更简洁和更集中的回复中受益。它倾向于保持 LLM 更集中并减少嘈杂的通信。

务必运行此策略的所有提示策略示例。如前所述，我们将在以后的章节中介绍其他提示工程策略和策略。我们将通过研究如何为你的用例选择最佳 LLM 来完成本章。

## 2.4 为你的特定需求选择最佳 LLM

虽然成为 AI 智能体的成功制作者不需要对 LLM 有深入的了解，但能够评估规格会有所帮助。就像计算机用户一样，你不需要知道如何构建处理器来理解处理器型号之间的差异。这个类比对 LLM 也很适用，虽然标准可能不同，但它仍然取决于一些主要考虑因素。

从我们之前的讨论和对 LM Studio 的了解中，我们可以提取一些在考虑 LLM 时对我们很重要的基本标准。图 2.11 解释了在使用 LLM 时要考虑的重要标准。

### 选择 LLM 的重要标准

**1. 模型性能（Model Performance）**
- 确定模型在给定基准上的表现如何，例如回答 SAT 问题

**2. 模型参数（大小）（Model Parameters/Size）**
- 以十亿参数指定模型的大小
- 更大的模型通常在一般任务上表现更好

**3. 用例（模型类型）（Use Case/Model Type）**
- 确定模型的类型和预期用例
- 这可以是像 ChatGPT 这样的模型的聊天补全

**4. 训练输入（Training Input）**
- 指定用于训练模型的材料
- 这可以从互联网上的所有内容到特定领域的 Python 代码

**5. 训练方法（Training Method）**
- 指定模型的训练和/或微调方式
- 像 ChatGPT 这样的模型使用人类反馈强化学习进行训练

**6. 上下文令牌大小（Context Token Size）**
- 指定模型的上下文大小（以令牌为单位）
- 大型上下文对于冗长的智能体对话很重要

**7. 模型速度（模型部署）（Model Speed/Deployment）**
- 表示模型的速度
- 标记为 Turbo 的 OpenAI 模型通常更快
- 对于本地 LLM，速度将由基础设施确定

**8. 模型成本（项目预算）（Model Cost/Budget）**
- 可以代表服务的价格或在你的基础设施上托管和运行模型的成本

对于我们构建 AI 智能体的目的，我们需要从与任务相关的角度来看待这些标准中的每一个。模型上下文大小和速度可以被视为第六和第七标准，但它们通常被视为模型部署架构和基础设施的变化。考虑 LLM 的第八个标准是成本，但这取决于许多其他因素。以下是这些标准如何与构建 AI 智能体相关的摘要：

**模型性能** - 你通常会想了解 LLM 对给定任务集的性能。例如，如果你正在构建特定于编码的智能体，那么在代码上表现良好的 LLM 将至关重要。

**模型参数（大小）** - 模型的大小通常是推理性能和模型响应效果的良好指标。但是，模型的大小也将决定你的硬件要求。如果你计划使用自己的本地托管模型，模型大小也将主要决定你需要的计算机和 GPU。幸运的是，我们看到定期发布小型、非常有能力的开源模型。

**用例（模型类型）** - 模型的类型有几种变化。像 ChatGPT 这样的聊天补全模型对于迭代和推理问题非常有效，而补全、问答和指令等模型更与特定任务相关。聊天补全模型对于智能体应用程序至关重要，尤其是那些迭代的应用程序。

**训练输入** - 了解用于训练模型的内容通常会决定模型的领域。虽然通用模型可以在各种任务中有效，但更具体或微调的模型可能与领域更相关。对于特定领域的智能体，较小的、更微调的模型可能与较大的模型（如 GPT-4）表现一样好或更好，这可能是一个考虑因素。

**训练方法** - 这可能不太重要，但了解用于训练模型的方法可能会有所帮助。模型的训练方式会影响其泛化、推理和规划的能力。这对于规划智能体可能至关重要，但对于智能体来说可能不如对更特定于任务的助手重要。

**上下文令牌大小** - 模型的上下文大小更特定于模型架构和类型。它决定了模型可能保存的上下文或记忆的大小。小于 4,000 个令牌的较小上下文窗口通常对于简单任务来说绰绰有余。但是，在使用多个智能体时，大型上下文窗口可能至关重要——所有智能体都在讨论任务。模型通常会根据上下文窗口大小的变化进行部署。

**模型速度（模型部署）** - 模型的速度由其推理速度（或模型回复请求的速度）决定，而推理速度又由其运行的基础设施决定。如果你的智能体不直接与用户交互，可能不需要原始实时速度。另一方面，实时交互的 LLM 智能体需要尽可能快。对于商业模型，速度将由提供商确定和支持。对于那些想要运行自己的 LLM 的人来说，你的基础设施将决定速度。

**模型成本（项目预算）** - 成本通常由项目决定。无论是学习构建智能体还是实施企业软件，成本始终是一个考虑因素。运行你自己的 LLM 与使用商业 API 之间存在显著的权衡。

在选择要在其上构建生产智能体系统的模型时，有很多要考虑的。但是，对于研究和学习目的，选择和使用单个模型通常是最好的。如果你是 LLM 和智能体的新手，你可能会想选择像 GPT-4 Turbo 这样的商业选项。除非另有说明，否则本书中的工作将依赖于 GPT-4 Turbo。

随着时间的推移，模型无疑会被更好的模型取代。因此，你可能需要升级或更换模型。但是，要做到这一点，你必须了解 LLM 和智能体的性能指标。幸运的是，在第 9 章中，我们将探索使用提示流评估 LLM、提示和智能体配置文件。

## 2.5 练习

使用以下练习来帮助你参与本章的材料：

**练习 1 — 使用不同的 LLM**
- 目标：使用 `connecting.py` 代码示例使用来自 OpenAI 或其他提供商的不同 LLM
- 任务：
  - 修改 `connecting.py` 以连接到不同的 LLM
  - 从 OpenAI 或其他提供商选择一个 LLM
  - 更新代码中的 API 密钥和端点
  - 执行修改后的代码并验证响应

**练习 2 — 探索提示工程策略**
- 目标：探索各种提示工程策略，并为每个策略创建变化
- 任务：
  - 查看本章中介绍的提示工程策略
  - 为每个策略编写变化，尝试不同的措辞和结构
  - 使用 LLM 测试变化以观察不同的结果
  - 记录结果，并分析每个变化的有效性

**练习 3 — 使用 LM Studio 下载和运行 LLM**
- 目标：使用 LM Studio 下载 LLM，并将其连接到提示工程策略
- 任务：
  - 在你的机器上安装 LM Studio
  - 使用 LM Studio 下载 LLM
  - 使用 LM Studio 提供模型
  - 编写 Python 代码以连接到提供的模型
  - 将提示工程策略示例与提供的模型集成

**练习 4 — 比较商业和开源 LLM**
- 目标：使用提示工程示例比较商业 LLM（如 GPT-4 Turbo）与开源模型的性能
- 任务：
  - 使用 GPT-4 Turbo 实施提示工程示例
  - 使用开源 LLM 重复实施
  - 根据响应准确性、连贯性和速度等标准评估模型
  - 记录评估过程，并总结发现

**练习 5 — LLM 的托管替代方案**
- 目标：对比和比较托管 LLM 与使用商业模型的替代方案
- 任务：
  - 研究 LLM 的不同托管选项（例如，本地服务器、云服务）
  - 评估每个托管选项的好处和缺点
  - 在成本、性能和易用性方面将这些选项与使用商业模型进行比较
  - 撰写一份总结比较的报告，并根据特定用例推荐最佳方法

## 本章小结

- **LLM 使用一种称为生成式预训练转换器（GPT）的架构类型。**

- **生成式模型**（例如，LLM 和 GPT）与预测/分类模型的不同之处在于学习如何表示数据而不是简单地对其进行分类。

- **LLM 是数据、架构和针对特定用例训练的集合**，称为微调。

- **OpenAI API SDK 可用于连接到 LLM**（来自 GPT-4 等模型），也可用于使用开源 LLM。

- 你可以快速设置 Python 环境并安装 LLM 集成所需的包。

- LLM 可以处理各种请求并生成可用于增强与 LLM 集成相关的编程技能的独特响应。

- **开源 LLM 是商业模型的替代方案**，可以使用 LM Studio 等工具在本地托管。

- **提示工程**是一组技术，有助于制作更有效的提示以改进 LLM 响应。

- **LLM 可用于为智能体和助手提供动力**，从简单的聊天机器人到功能齐全的自主工作者。

- **为特定需求选择最合适的 LLM** 取决于性能、参数、用例、训练输入和其他标准。

- 在本地运行 LLM 需要各种技能，从设置 GPU 到理解各种配置选项。

---

**翻译完成日期:** 2025-11-13
**翻译工具:** Claude AI (Sonnet 4.5)
**用途说明:** 本翻译仅供个人学习使用，请勿用于商业用途
