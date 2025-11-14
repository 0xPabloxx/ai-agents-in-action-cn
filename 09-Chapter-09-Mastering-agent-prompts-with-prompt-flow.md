# Chapter 9: Mastering agent prompts with prompt flow | <mark>第9章：使用 Prompt Flow 掌握智能体提示</mark>

## This chapter covers | <mark>本章内容</mark>

- Understanding systematic prompt engineering and setting up your first prompt flow | <mark>理解系统化提示工程并设置你的第一个 Prompt Flow</mark>
- Crafting an effective profile/persona prompt | <mark>制作有效的配置文件/人设提示</mark>
- Evaluating profiles: Rubrics and grounding | <mark>评估配置文件：评分标准和基础验证</mark>
- Grounding evaluation of a large language model profile | <mark>大语言模型配置文件的基础评估</mark>
- Comparing prompts: Getting the perfect profile | <mark>比较提示：获得完美的配置文件</mark>

---

In this chapter, we delve into the Test Changes Systematically prompt engineering strategy. If you recall, we covered the grand strategies of the OpenAI prompt engineering framework in chapter 2. These strategies are instrumental in helping us build better prompts and, consequently, better agent profiles and personas. Understanding this role is key to our prompt engineering journey.

<mark>在本章中，我们深入研究"系统地测试更改"提示工程策略。如果你还记得，我们在第 2 章中介绍了 OpenAI 提示工程框架的宏观策略。这些策略有助于我们构建更好的提示，从而构建更好的智能体配置文件和人设。理解这一角色是我们提示工程之旅的关键。</mark>

Test Changes Systematically is such a core facet of prompt engineering that Microsoft developed a tool around this strategy called prompt flow, described later in this chapter. Before getting to prompt flow, we need to understand why we need systemic prompt engineering.

<mark>系统地测试更改是提示工程的核心方面，以至于 Microsoft 围绕这一策略开发了一个名为 Prompt Flow 的工具，本章稍后将进行描述。在使用 Prompt Flow 之前，我们需要理解为什么需要系统化的提示工程。</mark>

---

## 9.1 Why we need systematic prompt engineering

<mark>## 9.1 为什么我们需要系统化的提示工程</mark>

Prompt engineering, by its nature, is an iterative process. When building a prompt, you'll often iterate and evaluate. To see this concept in action, consider the simple application of prompt engineering to a ChatGPT question.

<mark>提示工程本质上是一个迭代过程。构建提示时，你通常会迭代和评估。要看到这个概念的实际应用，请考虑将提示工程简单应用于 ChatGPT 问题。</mark>

You can follow along by opening your browser to ChatGPT (https://chat.openai.com/), entering the following (text) prompt into ChatGPT, and clicking the Send Message button (an example of this conversation is shown in figure 9.1, on the left side):

<mark>你可以通过在浏览器中打开 ChatGPT (https://chat.openai.com/)，在 ChatGPT 中输入以下（文本）提示，然后单击"发送消息"按钮来跟随操作（此对话的示例显示在图 9.1 的左侧）：</mark>

```
can you recommend something
```

<mark>```
你能推荐点什么吗
```</mark>

We can see that the response from ChatGPT is asking for more information. Go ahead and open a new conversation with ChatGPT, and enter the following prompt, as shown in figure 9.1, on the right side:

<mark>我们可以看到 ChatGPT 的响应要求更多信息。继续打开一个新的 ChatGPT 对话，并输入以下提示，如图 9.1 右侧所示：</mark>

```
Can you please recommend a time travel movie set in the medieval period.
```

<mark>```
你能推荐一部设定在中世纪的时间旅行电影吗。
```</mark>

The results in figure 9.1 show a clear difference between leaving out details and being more specific in your request. We just applied the tactic of politely Writing Clear Instructions, and ChatGPT provided us with a good recommendation. But also notice how ChatGPT itself guides the user into better prompting. The refreshed screen shown in figure 9.2 shows the OpenAI prompt engineering strategies.

<mark>图 9.1 中的结果显示了遗漏细节和在请求中更具体之间的明显差异。我们刚刚应用了礼貌地"编写清晰指令"的策略，ChatGPT 为我们提供了一个好的推荐。但也请注意 ChatGPT 本身如何引导用户进行更好的提示。图 9.2 中显示的刷新屏幕显示了 OpenAI 提示工程策略。</mark>

**Figure 9.1 The differences in applying prompt engineering and iterating** | <mark>**图 9.1 应用提示工程和迭代的差异**</mark>

<mark>*图片描述：两个并排的ChatGPT对话截图*</mark>

- No prompt engineering | <mark>无提示工程</mark>
  - ChatGPT guides the user to supply additional details. | <mark>ChatGPT 引导用户提供更多细节。</mark>

- Applying prompt engineering | <mark>应用提示工程</mark>
  - Details are included in the prompt/request. | <mark>提示/请求中包含详细信息。</mark>

We just applied simple iteration to improve our prompt. We can extend this example by using a system prompt/message. Figure 9.3 demonstrates the use and role of the system prompt in iterative communication. In chapter 2, we used the system message/prompt in various examples.

<mark>我们刚刚应用了简单的迭代来改进我们的提示。我们可以通过使用系统提示/消息来扩展此示例。图 9.3 演示了系统提示在迭代通信中的使用和作用。在第 2 章中，我们在各种示例中使用了系统消息/提示。</mark>

**Figure 9.2 OpenAI prompt engineering strategies, broken down by agent component** | <mark>**图 9.2 OpenAI 提示工程策略，按智能体组件细分**</mark>

<mark>*图片描述：提示工程策略列表*</mark>

**Prompt Engineering Strategies** | <mark>**提示工程策略**</mark>

1. **Write Clear Instructions** — Be specific in what you ask. Tactics include detailing queries, adopting personas, using delimiters, specifying steps, providing examples, and specifying output length. → Basics | <mark>**编写清晰指令** — 明确你的要求。策略包括详细说明查询、采用人设、使用分隔符、指定步骤、提供示例和指定输出长度。→ 基础</mark>

2. **Provide Reference Text** — Helps reduce fabrications. Tactics involve instructing the model to use or cite reference texts. → Memory | <mark>**提供参考文本** — 帮助减少虚构内容。策略包括指导模型使用或引用参考文本。→ 记忆</mark>

3. **Use External Tools** — Enhances model capabilities. Tactics include embeddings-based search, code execution, and access to specific functions. → Memory | <mark>**使用外部工具** — 增强模型能力。策略包括基于嵌入的搜索、代码执行和访问特定函数。→ 记忆</mark>

4. **Split Complex Tasks into Simpler Subtasks** — Reduces error rates. Tactics include intent classification, summarizing dialogues, and piecewise summarization of documents. → Planning | <mark>**将复杂任务拆分为更简单的子任务** — 降低错误率。策略包括意图分类、总结对话和逐段总结文档。→ 规划</mark>

5. **Give Models Time to "Think"** — Allows more reliable reasoning. Tactics involve working out solutions before conclusions, using inner monologue, and reviewing previous answers. → Planning | <mark>**给模型时间"思考"** — 允许更可靠的推理。策略包括在得出结论之前制定解决方案、使用内心独白和回顾先前的答案。→ 规划</mark>

6. **Test Changes Systematically** — Ensures improvements are genuine. Tactics involve evaluating model outputs with reference to standard answers. → Evaluation | <mark>**系统地测试更改** — 确保改进是真实的。策略包括参考标准答案评估模型输出。→ 评估</mark>

**Figure 9.3 The messages to and from an LLM conversation and the iteration of messages** | <mark>**图 9.3 LLM 对话的消息往来和消息迭代**</mark>

<mark>*图片描述：消息流程图*</mark>

- The system prompt defines the role and rules and continues across the conversation. | <mark>系统提示定义角色和规则，并在整个对话中持续。</mark>
- The user prompt defines the details of the ask. | <mark>用户提示定义询问的详细信息。</mark>
- A user prompt may refine the ask or start a new ask. | <mark>用户提示可以细化询问或开始新的询问。</mark>
- The Assistant marks the response from the LLM. | <mark>助手标记来自 LLM 的响应。</mark>

You can also try this in ChatGPT. This time, enter the following prompt and include the word system in lowercase, followed by a new line (enter a new line in the message window without sending the message by pressing Shift-Enter):

<mark>你也可以在 ChatGPT 中尝试这个。这次，输入以下提示并包含小写的单词 system，后跟一个新行（在消息窗口中输入新行而不发送消息，按 Shift-Enter）：</mark>

```
system
You are an expert on time travel movies.
```

<mark>```
system
你是时间旅行电影方面的专家。
```</mark>

ChatGPT will respond with some pleasant comments, as shown in figure 9.4. Because of this, it's happy to accept its new role and asks for any follow-up questions. Now enter the following generic prompt as we did previously:

<mark>ChatGPT 将以一些愉快的评论回应，如图 9.4 所示。因此，它很乐意接受其新角色并询问任何后续问题。现在输入以下通用提示，就像我们之前做的那样：</mark>

```
can you recommend something
```

<mark>```
你能推荐点什么吗
```</mark>

**Figure 9.4 The effect of adding a system prompt to our previous conversation** | <mark>**图 9.4 向我们之前的对话添加系统提示的效果**</mark>

<mark>*图片描述：ChatGPT对话截图*</mark>

- This sets the system prompt, the role the LLM will take for the remainder of the conversation. | <mark>这设置了系统提示，LLM 将在剩余对话中扮演的角色。</mark>
- The LLM responds happily with the new role. | <mark>LLM 愉快地以新角色回应。</mark>
- Make the generic ask again. | <mark>再次进行通用询问。</mark>
- The LLM now provides a list of recommendations. | <mark>LLM 现在提供了一个推荐列表。</mark>

We've just seen the iteration of refining a prompt, the prompt engineering, to extract a better response. This was accomplished over three different conversations using the ChatGPT UI. While not the most efficient way, it works.

<mark>我们刚刚看到了完善提示、提示工程以提取更好响应的迭代。这是通过使用 ChatGPT UI 进行三个不同的对话来完成的。虽然不是最有效的方式，但它有效。</mark>

However, we haven't defined the iterative flow for evaluating the prompt and determining when a prompt is effective. Figure 9.5 shows a systemic method of prompt engineering using a system of iteration and evaluation.

<mark>然而，我们还没有定义评估提示和确定提示何时有效的迭代流程。图 9.5 显示了使用迭代和评估系统的系统化提示工程方法。</mark>

**Figure 9.5 The systemic method of prompt engineering** | <mark>**图 9.5 系统化提示工程方法**</mark>

<mark>*图片描述：提示工程流程图*</mark>

**Systemic Prompt Engineering (Strategy - Test Changes Systematically)** | <mark>**系统化提示工程（策略 - 系统地测试更改）**</mark>

- Build prompt or profile | <mark>构建提示或配置文件</mark>
  - Use prompt engineering to write the prompt. | <mark>使用提示工程编写提示。</mark>

- Write/update the prompt | <mark>编写/更新提示</mark>

- Evaluate prompt is working | <mark>评估提示是否有效</mark>
  - Prompt or profile is grounded. | <mark>提示或配置文件已基础验证。</mark>
  - Evaluate the prompt based on rubrics. | <mark>基于评分标准评估提示。</mark>

- Batch evaluation of prompt | <mark>批量评估提示</mark>
  - Evaluate variations of the prompt/profile. | <mark>评估提示/配置文件的变体。</mark>

- Prompt is used | <mark>使用提示</mark>

The system of iterating and evaluating prompts covers the broad Test Changes Systematically strategy. Evaluating the performance and effectiveness of prompts is still new, but we'll use techniques from education, such as rubrics and grounding, which we'll explore in a later section of this chapter. However, as spelled out in the next section, we need to understand the difference between a persona and an agent profile before we do so.

<mark>迭代和评估提示的系统涵盖了广泛的"系统地测试更改"策略。评估提示的性能和有效性仍然是新的，但我们将使用教育中的技术，例如评分标准和基础验证，我们将在本章后面的部分中探讨这些内容。但是，如下一节所述，在这样做之前，我们需要理解人设和智能体配置文件之间的区别。</mark>

---

## 9.2 Understanding agent profiles and personas

<mark>## 9.2 理解智能体配置文件和人设</mark>

An agent profile is an encapsulation of component prompts or messages that describe an agent. It includes the agent's persona, special instructions, and other strategies that can guide the user or other agent consumers.

<mark>智能体配置文件是描述智能体的组件提示或消息的封装。它包括智能体的人设、特殊指令和其他可以指导用户或其他智能体消费者的策略。</mark>

Figure 9.6 shows the main elements of an agent profile. These elements map to prompt engineering strategies described in this book. Not all agents will use all the elements of a full agent profile.

<mark>图 9.6 显示了智能体配置文件的主要元素。这些元素映射到本书中描述的提示工程策略。并非所有智能体都会使用完整智能体配置文件的所有元素。</mark>

At a basic level, an agent profile is a set of prompts describing the agent. It may include other external elements related to actions/tools, knowledge, memory, reasoning, evaluation, planning, and feedback. The combination of these elements comprises an entire agent prompt profile.

<mark>在基本级别，智能体配置文件是一组描述智能体的提示。它可能包括与动作/工具、知识、记忆、推理、评估、规划和反馈相关的其他外部元素。这些元素的组合构成了完整的智能体提示配置文件。</mark>

Prompts are the heart of an agent's function. A prompt or set of prompts drives each of the agent components in the profile. For actions/tools, these prompts are well defined, but as we've seen, prompts for memory and knowledge can vary significantly by use case.

<mark>提示是智能体功能的核心。提示或一组提示驱动配置文件中的每个智能体组件。对于动作/工具，这些提示定义良好，但正如我们所见，记忆和知识的提示可能因用例而异。</mark>

**Figure 9.6 The component parts of an agent profile** | <mark>**图 9.6 智能体配置文件的组成部分**</mark>

<mark>*图片描述：智能体配置文件结构图*</mark>

**The Agent Profile (prompts)** | <mark>**智能体配置文件（提示）**</mark>

- **Persona** — Represents the background and role of the agent, and is often introduced in the first system message | <mark>**人设** — 代表智能体的背景和角色，通常在第一条系统消息中引入</mark>
  - Similar to prompt personas, the agent persona can give an agent specialized attributes, rules, and even personality. | <mark>与提示人设类似，智能体人设可以为智能体提供专门的属性、规则甚至个性。</mark>

- **Agent Tools** — Set of tools an agent can use to help accomplish a task | <mark>**智能体工具** — 智能体可用于帮助完成任务的工具集</mark>
  - Actions and tools are added to the prompt under the covers. | <mark>动作和工具在幕后添加到提示中。</mark>

- **Agent Evaluation and Reasoning** — Describes how the agent can reason and evaluate a task or tasks | <mark>**智能体评估和推理** — 描述智能体如何推理和评估任务</mark>
  - Adding reasoning to prompts | <mark>向提示添加推理</mark>

- **Agent Memory and Knowledge** — The backend store that helps the agent add context to a given task problem | <mark>**智能体记忆和知识** — 帮助智能体向给定任务问题添加上下文的后端存储</mark>
  - Knowledge and memory are prompts used to extract and identify memories. | <mark>知识和记忆是用于提取和识别记忆的提示。</mark>

- **Agent Planning and Feedback** — Describes how the agent can break down a task into execution steps, and then execute and receive feedback | <mark>**智能体规划和反馈** — 描述智能体如何将任务分解为执行步骤，然后执行并接收反馈</mark>
  - Planning and feedback | <mark>规划和反馈</mark>

The definition of an AI agent profile is more than just a system prompt. Prompt flow can allow us to construct the prompts and code comprising the agent profile but also include the ability to evaluate its effectiveness. In the next section, we'll open up prompt flow and start using it.

<mark>AI 智能体配置文件的定义不仅仅是系统提示。Prompt Flow 可以允许我们构建包含智能体配置文件的提示和代码，还包括评估其有效性的能力。在下一节中，我们将打开 Prompt Flow 并开始使用它。</mark>

---

## 9.3 Setting up your first prompt flow

<mark>## 9.3 设置你的第一个 Prompt Flow</mark>

Prompt flow is a tool developed by Microsoft within its Azure Machine Learning Studio platform. The tool was later released as an open source project on GitHub, where it has attracted more attention and use. While initially intended as an application platform, it has since shown its strength in developing and evaluating prompts/profiles.

<mark>Prompt Flow 是 Microsoft 在其 Azure 机器学习工作室平台内开发的工具。该工具后来作为开源项目在 GitHub 上发布，在那里它吸引了更多的关注和使用。虽然最初旨在作为应用程序平台，但它自那时以来已显示出在开发和评估提示/配置文件方面的优势。</mark>

Because prompt flow was initially developed to run on Azure as a service, it features a robust core architecture. The tool supports multi-threaded batch processing, which makes it ideal for evaluating prompts at scale. The following section will examine the basics of starting with prompt flow.

<mark>因为 Prompt Flow 最初是为在 Azure 上作为服务运行而开发的，所以它具有强大的核心架构。该工具支持多线程批处理，这使其非常适合大规模评估提示。以下部分将探讨开始使用 Prompt Flow 的基础知识。</mark>

---

### 9.3.1 Getting started

<mark>### 9.3.1 入门</mark>

There are a few prerequisites to undertake before working through the exercises in this book. The relevant prerequisites for this section and chapter are shown in the following list; make sure to complete them before attempting the exercises:

<mark>在完成本书中的练习之前，有一些先决条件需要完成。本节和本章的相关先决条件显示在以下列表中；在尝试练习之前确保完成它们：</mark>

- Visual Studio Code (VS Code) — Refer to appendix A for installation instructions, including additional extensions. | <mark>Visual Studio Code（VS Code）— 有关安装说明（包括其他扩展），请参考附录 A。</mark>

- Prompt flow, VS Code extension — Refer to appendix A for details on installing extensions. | <mark>Prompt Flow，VS Code 扩展 — 有关安装扩展的详细信息，请参考附录 A。</mark>

- Python virtual environment — Refer to appendix A for details on setting up a virtual environment. | <mark>Python 虚拟环境 — 有关设置虚拟环境的详细信息，请参考附录 A。</mark>

- Install prompt flow packages — Within your virtual environment, do a quick pip install, as shown here: | <mark>安装 Prompt Flow 包 — 在你的虚拟环境中，执行快速 pip 安装，如下所示：</mark>

```bash
pip install promptflow promptflow-tools
```

- LLM (GPT-4 or above) — You'll need access to GPT-4 or above through OpenAI or Azure OpenAI Studio. Refer to appendix B if you need assistance accessing these resources. | <mark>LLM（GPT-4 或更高版本）— 你需要通过 OpenAI 或 Azure OpenAI Studio 访问 GPT-4 或更高版本。如果需要帮助访问这些资源，请参考附录 B。</mark>

- Book's source code — Clone the book's source code to a local folder; refer to appendix A if you need help cloning the repository. | <mark>本书的源代码 — 将本书的源代码克隆到本地文件夹；如果需要帮助克隆存储库，请参考附录 A。</mark>

Open up VS Code to the book's source code folder, chapter 3. Ensure that you have a virtual environment connected and have installed the prompt flow packages and extension.

<mark>在 VS Code 中打开本书的源代码文件夹，第 3 章。确保你已连接虚拟环境并已安装 Prompt Flow 包和扩展。</mark>

First, you'll want to create a connection to your LLM resource within the prompt flow extension. Open the prompt flow extension within VS Code, and then click to open the connections. Then, click the plus sign beside the LLM resource to create a new connection, as shown in figure 9.7.

<mark>首先，你需要在 Prompt Flow 扩展中创建与 LLM 资源的连接。在 VS Code 中打开 Prompt Flow 扩展，然后单击以打开连接。然后，单击 LLM 资源旁边的加号以创建新连接，如图 9.7 所示。</mark>

This will open a YAML file where you'll need to populate the connection name and other information relevant to your connection. Follow the directions, and don't enter API keys into the document, as shown in figure 9.8.

<mark>这将打开一个 YAML 文件，你需要在其中填充连接名称和与连接相关的其他信息。按照说明操作，不要在文档中输入 API 密钥，如图 9.8 所示。</mark>

When the connection information is entered, click the Create Connection link at the bottom of the document. This will open a terminal prompt below the document, asking you to enter your key. Depending on your terminal configuration, you may be unable to paste (Ctrl-V, Cmd-V). Alternatively, you can paste the key by hovering the mouse cursor over the terminal and right-clicking on Windows.

<mark>输入连接信息后，单击文档底部的"创建连接"链接。这将在文档下方打开终端提示，要求你输入密钥。根据你的终端配置，你可能无法粘贴（Ctrl-V，Cmd-V）。或者，你可以通过将鼠标光标悬停在终端上并在 Windows 上右键单击来粘贴密钥。</mark>

---

### 9.3.2 Creating profiles with Jinja2 templates

<mark>### 9.3.2 使用 Jinja2 模板创建配置文件</mark>

The flow responds with time travel movie recommendations because of the prompt or profile it uses. By default, prompt flow uses Jinja2 templates to define the content of the prompt or what we'll call a profile. For the purposes of this book and our exploration of AI agents, we'll refer to these templates as the profile of a flow or agent.

<mark>该流程会响应时间旅行电影推荐，因为它使用的提示或配置文件。默认情况下，Prompt Flow 使用 Jinja2 模板来定义提示的内容或我们称之为配置文件的内容。出于本书和我们对 AI 智能体的探索的目的，我们将这些模板称为流程或智能体的配置文件。</mark>

While prompt flow doesn't explicitly refer to itself as an assistant or agent engine, it certainly meets the criteria of producing a proxy and general types of agents. As you'll see, prompt flow even supports deployments of flows into containers and as services.

<mark>虽然 Prompt Flow 没有明确地将自己称为助手或智能体引擎，但它肯定符合生成代理和通用类型智能体的标准。正如你将看到的，Prompt Flow 甚至支持将流程部署到容器和服务中。</mark>

Jinja is a templating engine, and Jinja2 is a particular version of that engine. Templates are an excellent way of defining the layout and parts of any form of text document. They have been extensively used to produce HTML, JSON, CSS, and other document forms. In addition, they support the ability to apply code directly into the template. While there is no standard way to construct prompts or agent profiles, our preference in this book is to use templating engines such as Jinja.

<mark>Jinja 是一个模板引擎，Jinja2 是该引擎的特定版本。模板是定义任何形式的文本文档的布局和部分的出色方式。它们已被广泛用于生成 HTML、JSON、CSS 和其他文档形式。此外，它们支持将代码直接应用到模板中的能力。虽然没有构建提示或智能体配置文件的标准方法，但我们在本书中的偏好是使用 Jinja 等模板引擎。</mark>

---

### 9.3.3 Deploying a prompt flow API

<mark>### 9.3.3 部署 Prompt Flow API</mark>

Because prompt flow was also designed to be deployed as a service, it supports a couple of ways to deploy as an app or API quickly. Prompt flow can be deployed as a local web application and API running from the terminal or as a Docker container.

<mark>因为 Prompt Flow 也被设计为作为服务部署，所以它支持几种快速部署为应用程序或 API 的方法。Prompt Flow 可以作为从终端运行的本地 Web 应用程序和 API 部署，或作为 Docker 容器部署。</mark>

---

## 9.4 Evaluating profiles: Rubrics and grounding

<mark>## 9.4 评估配置文件：评分标准和基础验证</mark>

A key element of any prompt or agent profile is how well it performs its given task. As we see in our recommendation example, prompting an agent profile to give a list of recommendations is relatively easy, but knowing whether those recommendations are helpful requires us to evaluate the response.

<mark>任何提示或智能体配置文件的关键要素是它执行其给定任务的程度。正如我们在推荐示例中看到的，提示智能体配置文件给出推荐列表相对容易，但了解这些推荐是否有用需要我们评估响应。</mark>

Fortunately, prompt flow has been designed to evaluate prompts/profiles at scale. The robust infrastructure allows for the evaluation of LLM interactions to be parallelized and managed as workers, allowing hundreds of profile evaluations and variations to happen quickly.

<mark>幸运的是，Prompt Flow 旨在大规模评估提示/配置文件。强大的基础设施允许将 LLM 交互的评估并行化并作为工作程序进行管理，允许数百个配置文件评估和变体快速发生。</mark>

---

## Summary

<mark>## 本章小结</mark>

- Systematic prompt engineering is an iterative process that requires evaluation and refinement to ensure prompts are effective and achieve desired outcomes. | <mark>系统化提示工程是一个迭代过程，需要评估和完善以确保提示有效并实现预期结果。</mark>

- Agent profiles encapsulate component prompts, personas, special instructions, and strategies that guide the agent's behavior and interaction with users or systems. | <mark>智能体配置文件封装了组件提示、人设、特殊指令和指导智能体与用户或系统交互行为的策略。</mark>

- Prompt flow is a Microsoft tool designed for developing, testing, and deploying agent prompts and profiles at scale with multi-threaded batch processing capabilities. | <mark>Prompt Flow 是 Microsoft 工具，旨在使用多线程批处理功能大规模开发、测试和部署智能体提示和配置文件。</mark>

- Jinja2 templates provide a flexible and standardized way to construct prompts and agent profiles, supporting code injection and dynamic content generation. | <mark>Jinja2 模板提供了一种灵活且标准化的方法来构建提示和智能体配置文件，支持代码注入和动态内容生成。</mark>

- Evaluation of prompts and profiles uses rubrics and grounding techniques from education to systematically assess performance and effectiveness. | <mark>提示和配置文件的评估使用教育中的评分标准和基础验证技术来系统地评估性能和有效性。</mark>

- Prompt flow supports deployment options including local web applications, APIs, and Docker containers, making it versatile for various use cases. | <mark>Prompt Flow 支持部署选项，包括本地 Web 应用程序、API 和 Docker 容器，使其在各种用例中具有多功能性。</mark>

- Test Changes Systematically is a core prompt engineering strategy that ensures improvements are genuine through systematic evaluation against reference standards. | <mark>系统地测试更改是一项核心提示工程策略，通过针对参考标准的系统评估来确保改进是真实的。</mark>

---

**参考资源 | References**

- Prompt Flow Documentation: https://microsoft.github.io/promptflow
- OpenAI Prompt Engineering Guide: https://platform.openai.com/docs/guides/prompt-engineering
- Jinja2 Documentation: https://jinja.palletsprojects.com
