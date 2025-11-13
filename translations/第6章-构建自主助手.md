# AI Agents in Action 第6章 Claude翻译版

## 章节信息
- **章节编号**: 第6章
- **章节标题**: 构建自主助手（Building autonomous assistants）
- **原书页码**: 153-183 (共31页)
- **翻译日期**: 2025-11-13
- **翻译工具**: Claude AI (Sonnet 4.5)

---

## 第6章 构建自主助手

现在我们已经介绍了动作如何扩展智能体的能力/功能，我们可以看看行为树如何引导智能体系统。我们将从理解行为树的基础知识以及它们如何控制机器人和游戏中的 AI 开始。

然后我们将回到智能体动作，并研究如何使用 GPT Assistants Playground 项目在 OpenAI Assistants 平台上实现动作。从那里，我们将了解如何使用 OpenAI assistants 构建自主智能体行为树（ABT）。然后，我们将继续理解对自主智能体进行控制和护栏的需求，以及使用控制屏障函数。

### 本章内容

- 机器人和 AI 应用的行为树
- GPT Assistants Playground 以及创建助手和动作
- 智能体行为树的自主控制
- 通过智能体行为树模拟对话式多智能体系统
- 使用反向链接为复杂系统创建行为树

在本章的最后一节中，我们将研究如何使用 AgentOps 平台监控我们的自主行为驱动的智能体系统。这将是一个激动人心的章节，包含几个挑战。让我们从跳到下一节开始，介绍行为树。

---

## 6.1 行为树简介

行为树是一个长期建立的模式,用于控制机器人和游戏中的 AI。Rodney A. Brooks 在1986年的论文《移动机器人的鲁棒分层控制系统》中首次引入了这个概念。这为我们今天使用的树和节点结构的模式奠定了基础。

如果你曾经玩过带有非玩家角色（NPC）的电脑游戏或与高级机器人系统互动过，你就见证了行为树的工作。**图 6.1** 展示了一个简单的行为树。该树表示所有主要节点：选择器或回退节点、序列节点、动作节点和条件节点。

> **图 6.1 说明**（位置：原文 图 6.1）
>
> 一个吃苹果或梨的简单行为树：
>
> 1. 根节点可以是任何复合节点，如选择器或序列
> 2. 执行从上到下，然后从左到右流动
> 3. 节点编号：1-7，显示执行顺序
> 4. 包含选择器节点（?）和序列节点（→）
> 5. 最后的动作节点执行实际操作

**表 6.1** 描述了我们将在本书中探索的主要节点的功能和目的。还有其他节点和节点类型，你甚至可以创建自定义节点，但现在我们将专注于表中的这些节点。

**表 6.1 行为树中使用的主要节点**

| 节点 | 目的 | 功能 | 类型 |
|------|------|------|------|
| **选择器（回退）Selector (fallback)** | 此节点通过选择第一个成功完成的子节点来工作。它通常被称为回退节点,因为它总是回退到最后一个成功执行的节点。 | 节点按顺序调用其子节点,并在第一个子节点成功时停止执行。当子节点成功时,它将返回成功；如果没有节点成功,则返回失败。 | 复合节点 Composite |
| **序列 Sequence** | 此节点按顺序执行其所有子节点,直到一个节点失败或它们全部成功完成。 | 节点按顺序调用其每个子节点,无论它们失败还是成功。如果所有子节点都成功,则返回成功,如果只有一个子节点失败,则返回失败。 | 复合节点 Composite |
| **条件 Condition** | 行为树不使用布尔逻辑,而是使用成功或失败作为控制手段。如果条件为真,条件返回成功,否则返回假。 | 节点根据条件返回成功或失败。 | 任务节点 Task |
| **动作 Action** | 这是动作发生的地方。节点执行,如果成功则返回成功,否则返回失败。 | 执行具体操作并返回结果。 | 任务节点 Task |
| **装饰器 Decorator** | 它们通过控制子节点的执行来工作。它们通常被称为条件语句,因为它们可以确定节点是否值得执行或安全执行。 | 节点控制子节点的执行。装饰器可以作为控制屏障函数来阻止或防止不需要的行为。 | 装饰器 Decorator |
| **并行 Parallel** | 此节点并行执行其所有节点。成功或失败由需要成功的子节点数量的阈值控制才能返回成功。 | 节点按顺序执行其所有子节点,无论节点的状态如何。 | 复合节点 Composite |

表 6.1 中的主要节点可以提供足够的功能来处理众多用例。然而,最初理解行为树可能很困难。在你开始使用它们之前,你不会欣赏它们的底层复杂性。在构建一些简单的树之前,我们想在下一节中更详细地查看执行。

### 6.1.1 理解行为树执行

理解行为树如何执行对于设计和实现行为树至关重要。与计算机科学中的大多数概念不同,行为树以成功和失败的术语运行。当行为树中的节点执行时,它将返回成功或失败；这甚至适用于条件和选择器节点。

行为树从上到下、从左到右执行。**图 6.2** 展示了节点失败或成功时发生的过程和结果。在示例中,树控制的 AI 有一个苹果但没有梨。在第一个序列节点中,条件检查 AI 是否有苹果。因为 AI 没有苹果,它中止序列并回退到选择器。然后选择器选择其下一个子节点,另一个序列,检查 AI 是否有梨,因为有,AI 就吃了苹果。

> **图 6.2 说明**（位置：原文 图 6.2）
>
> 简单行为树的执行过程：
>
> 1. 根节点根据其复合类型执行
> 2. 选择器节点执行所有子节点并在第一个返回成功的子节点上返回成功
> 3. 序列节点按顺序执行所有子节点；如果节点失败,序列失败
> 4. 如果序列中的前一个节点失败,序列将被中止
> 5. 在此示例中,AI 有梨,返回成功,然后吃梨
> 6. 节点成功/失败流回父节点
> 7. 执行顺序：1→2→3→4→6→7

行为树在宏观或微观层面提供对 AI 系统如何执行的控制。关于机器人,行为树通常被设计为在微观层面运行,其中每个动作或条件都是一个小事件,例如检测苹果。相反,行为树还可以控制更宏观的系统,例如游戏中的 NPC,其中每个动作可能是事件的组合,例如攻击玩家。

对于智能体系统,行为树支持在你选择的级别控制智能体或助手。我们将探索在任务级别控制智能体,在后面的章节中,探索规划级别。毕竟,凭借 LLM 的能力,智能体可以构建自己的行为树。

当然,还有几种其他形式的 AI 控制可以用来控制智能体系统。下一节将研究这些不同的系统,并将它们与行为树进行比较。

### 6.1.2 决定使用行为树

许多其他 AI 控制系统具有优势,值得探索用于控制智能体系统。它们可以展示行为树的优势,并为特定用例提供其他选项。行为树是一个出色的模式,但它不是唯一的,值得了解其他模式。

**表 6.2** 突出显示了我们可能考虑用于控制 AI 系统的几个其他系统。表中的每个项目描述了该方法的作用、其缺点以及其对智能体 AI 控制的可能应用。

**表 6.2 其他 AI 控制系统的比较**

| 控制名称 | 描述 | 缺点 | 控制智能体 AI？ |
|---------|------|------|----------------|
| **有限状态机 (FSM)ª** | FSM 使用一组状态和由事件或条件触发的转换来建模 AI。 | FSM 随着复杂性增加可能变得难以管理。 | FSM 对于智能体不实用,因为它们扩展性不好。 |
| **决策树ᵇ** | 决策树使用决策的树状模型及其可能的后果。 | 决策树可能遭受过拟合,在复杂场景中缺乏泛化。 | 决策树可以与行为树一起调整和增强。 |
| **基于效用的系统ᵇ** | 效用函数根据当前情况评估和选择最佳动作。 | 这些系统需要仔细设计效用函数以平衡优先级。 | 这种模式可以在行为树中采用。 |
| **基于规则的系统ª** | 这是一组定义 AI 行为的 if-then 规则。 | 这些系统在规则很多时可能变得繁琐,导致潜在冲突。 | 当与由 LLM 驱动的智能体系统配对时,这些不太实用。 |
| **规划系统ᶜ** | 规划系统使用规划算法生成一系列动作来实现特定目标。 | 这些系统计算成本高,需要大量领域知识。 | 智能体已经可以自己实现这样的模式,正如我们将在后面的章节中看到的。 |
| **行为克隆ᶜ** | 行为克隆是指通过模仿专家演示来学习策略。 | 此系统可能难以泛化到未见过的情况。 | 这可以合并到行为树或特定任务中。 |
| **分层任务网络 (HTN)ᵈ** | HTN 将任务分解为更小、可管理的子任务,排列在层次结构中。 | 对于非常大的任务,这些很复杂,难以管理和设计。 | HTN 允许更好地组织和执行复杂任务。此模式可用于更大的智能体系统。 |
| **黑板系统ᵇ** | 这些系统使用共享黑板为不同子系统提供协作问题解决。 | 这些系统难以实现和管理子系统之间的通信。 | 智能体系统可以使用对话或群聊/线程实现类似的模式。 |
| **遗传算法 (GA)ᵈ** | 这些优化技术受到自然选择的启发,以进化解决问题的解决方案。 | GA 计算密集,可能并不总是找到最优解。 | GA 有潜力,甚至可用于优化行为树。 |

注释：
- ª 在考虑复杂的智能体系统时不实用
- ᵇ 存在于行为树中或可以轻松合并
- ᶜ 通常在任务或动作/条件级别应用
- ᵈ 需要大量工作的高级系统

在本书的后面章节中,我们将研究表 6.2 中讨论的一些模式。总体而言,几种模式可以使用行为树作为基础来增强或合并。虽然其他模式（如 FSM）可能对小型实验有用,但它们缺乏行为树的可扩展性。

行为树作为 AI 控制系统可以提供多个优势,包括可扩展性。以下列表突出了使用行为树的其他显著优势：

- **模块化和可重用性**——行为树促进了设计行为的模块化方法,允许开发人员创建可重用的组件。行为树中的节点可以轻松地在树的不同部分甚至不同项目中重用,增强可维护性并减少开发时间。

- **可扩展性**——随着系统复杂性的增长,行为树比其他方法（如 FSM）更优雅地处理新行为的添加。行为树允许任务的分层组织,使管理和理解大型行为集更容易。

- **灵活性和可扩展性**——行为树提供了一个灵活的框架,可以在不大幅改变现有结构的情况下添加新节点（动作、条件、装饰器）。这种可扩展性使引入新行为或修改现有行为以适应新需求变得简单。

- **调试和可视化**——行为树提供了清晰直观的行为可视化表示,这对调试和理解决策过程很有帮助。支持行为树的工具通常包括图形编辑器,允许开发人员可视化和调试树结构,使识别和修复问题更容易。

- **决策逻辑的解耦**——行为树将决策制定和执行逻辑分离,促进高级策略和低级动作之间的清晰区分。这种解耦简化了设计,并允许更直接地修改和测试行为的特定部分,而不影响整个系统。

在为行为树提出了强有力的理由后,我们现在应该考虑如何在代码中实现它们。在下一节中,我们将了解如何使用 Python 代码构建一个简单的行为树。

### 6.1.3 使用 Python 和 py_trees 运行行为树

因为行为树已经存在很长时间并已被纳入许多技术,创建一个示例演示非常简单。当然,最简单的方法是询问 ChatGPT 或你喜欢的 AI 聊天工具。**代码清单 6.1** 展示了使用提示生成代码示例并提交图 6.1 作为示例树的结果。最终代码必须针对简单的命名和参数错误进行更正。

> **注意**
>
> 本章的所有代码都可以通过在 https://mng.bz/Ea0q 下载 GPT Assistants Playground 项目找到。

```python
# Listing 6.1: first_btree.py
import py_trees

class HasApple(py_trees.behaviour.Behaviour):     # 创建一个类来实现动作或条件
    def __init__(self, name):
        super(HasApple, self).__init__(name)

    def update(self):
        if True:  # 简单的条件检查
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE

# Other classes omitted…

has_apple = HasApple(name="Has apple")     # 创建动作和条件节点
eat_apple = EatApple(name="Eat apple")

sequence_1 = py_trees.composites.Sequence(name="Sequence 1", memory=True)
sequence_1.add_children([has_apple, eat_apple])    # 将节点添加到各自的父节点

has_pear = HasPear(name="Has pear")        # 创建动作和条件节点
eat_pear = EatPear(name="Eat pear")

sequence_2 = py_trees.composites.Sequence(name="Sequence 2", memory=True)
sequence_2.add_children([has_pear, eat_pear])

root = py_trees.composites.Selector(name="Selector", memory=True)
root.add_children([sequence_1, sequence_2])

behavior_tree = py_trees.trees.BehaviourTree(root)    # 创建整个行为树
py_trees.logging.level = py_trees.logging.Level.DEBUG

for i in range(1, 4):
    print("\n------------------ Tick {0} ------------------".format(i))
    behavior_tree.tick()    # 在行为树上执行一个步骤/tick

### Start of output
------------------ Tick 1 ------------------
[DEBUG] Selector             : Selector.tick()
[DEBUG] Selector             : Selector.tick() [!RUNNING->reset current_child]
[DEBUG] Sequence 1           : Sequence.tick()
[DEBUG] Has apple            : HasApple.tick()
[DEBUG] Has apple            : HasApple.stop(Status.INVALID->Status.SUCCESS)
[DEBUG] Eat apple            : EatApple.tick()
Eating apple
[DEBUG] Eat apple            : EatApple.stop(Status.INVALID->Status.SUCCESS)
[DEBUG] Sequence 1           : Sequence.stop()[Status.INVALID->Status.SUCCESS]
```

代码清单 6.1 中的代码表示图 6.1 中的行为树。你可以按原样运行此代码,或更改条件返回的内容,然后再次运行树。你还可以通过从根选择器中删除一个序列节点来更改行为树。

现在我们对行为树有了基本的理解,我们可以继续使用智能体/助手。在此之前,我们将查看一个工具来帮助我们使用 OpenAI Assistants。这个工具将帮助我们围绕 OpenAI Assistants 包装我们的第一个 ABT。

---

## 6.2 探索 GPT Assistants Playground

为了本书的开发,创建了几个 GitHub 项目来解决构建智能体和助手的各个方面。其中一个项目 GPT Assistants Playground,使用 Gradio 构建界面,模仿 OpenAI Assistants Playground,但添加了几个额外功能。

Playground 项目是作为教学和演示辅助工具开发的。在项目内部,Python 代码使用 OpenAI Assistants API 创建聊天接口和智能体系统来构建和支持助手。还有一个全面的动作助手集合可以使用,你可以轻松添加自己的动作。

### 6.2.1 安装和运行 Playground

下一个清单显示了从终端安装和运行 Playground 项目。目前没有 PyPI 包可安装。

```bash
# Listing 6.2: Installing the GPT Assistants Playground
# change to a working folder and create a new Python virtual environment
git clone https://github.com/cxbxmxcx/GPTAssistantsPlayground    # 从 GitHub 拉取源代码
cd GPTAssistantsPlayground     # 切换目录到项目源代码文件夹
pip install -r requirements.txt     # 安装依赖项
```

你可以从终端或使用 Visual Studio Code（VS Code）运行应用程序,后者为你提供更多控制。在运行应用程序之前,你需要通过命令行或通过创建 `.env` 文件来设置你的 OpenAI API 密钥,正如我们已经做过几次的那样。代码清单 6.3 展示了在 Linux/Mac 或 Git Bash shell（推荐 Windows）上设置环境变量并运行应用程序的示例。

```bash
# Listing 6.3: Running the GPT Assistants Playground
export OPENAI_API_KEY="your-api-key"     # 将你的 API 密钥设置为环境变量
python main.py    # 从终端或通过 VS Code 运行应用
```

在浏览器中打开显示的 URL（通常为 http://127.0.0.1:7860）或终端中提到的内容。你将看到类似于图 6.3 所示的界面。

> **图 6.3 说明**（位置：原文 图 6.3）
>
> 正在使用 GPT Assistants Playground 界面学习数学：
>
> 1. 选择现有的 Assistant 或创建新助手
> 2. 从任何可用模型中选择
> 3. 选择工具和动作
> 4. 助手可以输出由 Code Interpreter 创建的文件
> 5. 显示聊天界面和输出区域

如果你已经定义了 OpenAI Assistants,你将在 Select Assistant 下拉菜单中看到它们。

如果你从未定义过助手,可以创建一个并选择所需的各种选项和指令。如果你访问过 OpenAI Playground,你已经体验过类似的界面。

> **GPT 与助手的区别**
>
> OpenAI 将 GPT 定义为可以在 ChatGPT 界面中运行和使用的助手。助手只能通过 API 使用,在大多数情况下需要自定义代码。当你运行助手时,会根据模型 token 使用情况和任何特殊工具（包括 Code Interpreter 和文件）收费,而 GPT 在 ChatGPT 中运行并由账户费用覆盖。

这些功能中的每一个都将在接下来的几节中更详细地介绍。我们将从下一节中查看使用和消费动作开始。

**（续）**

创建 Playground 本地版本的原因是演示代码结构,但也提供此处列出的附加功能：

- **动作（自定义动作）**——创建自己的动作允许你向助手添加任何你想要的功能。正如我们将看到的,Playground 使快速创建自己的动作变得非常容易。

- **代码运行器**——API 确实带有 Code Interpreter,但它相对昂贵（每次运行 $.03）,不允许你安装自己的模块,不能交互式运行代码,并且运行缓慢。Playground 使你能够在隔离的虚拟环境中本地运行 Python 代码。虽然不如将代码推送到 Docker 镜像那样安全,但它确实比其他平台更好地在窗口和进程外执行代码。

- **透明度和日志记录**——Playground 提供了全面的日志捕获,甚至会显示助手如何使用内部和外部工具/动作。这可以是查看助手在幕后做什么的绝佳方式。

### 6.2.2 使用和构建自定义动作

动作和工具是赋予智能体和助手能力的构建块。没有访问工具,智能体就是无功能的聊天机器人。OpenAI 平台是建立许多工具模式的领导者,正如我们在第 3 章中看到的那样。

Playground 提供了几个自定义动作,可以通过界面附加到助手。在下一个练习中,我们将构建一个简单的助手并附加几个自定义动作,以查看可能的情况。

**图 6.4** 显示了展开的 Actions 手风琴,显示了许多可用的自定义动作。从终端或调试器运行 Playground,并创建一个新助手。然后,选择图中显示的动作。完成选择动作后,滚动到底部,然后单击 Add Assistant 以添加助手。助手需要先创建才能使用。

> **图 6.4 说明**（位置：原文 图 6.4）
>
> 在界面中选择和使用自定义动作：
>
> 1. 给你的助手一个令人难忘的名字
> 2. 选择 `call_assistant` 和 `list_assistants`
> 3. `call_assistant` 动作允许助手将工作委派给其他助手
> 4. 你不需要任何特殊指令
> 5. 禁用或启用 Code Interpreter 以查看效果
> 6. 要求列出助手,你将看到你创建的所有助手

创建助手后,你可以要求它列出所有可用的助手。列出助手还为你提供了调用助手所需的 ID。你还可以调用其他助手并要求它们完成其专业领域的任务。

添加自定义动作就像向文件添加代码并将其放入正确的文件夹一样简单。从主项目文件夹打开 `playground/assistant_actions` 文件夹,你将看到定义各种动作的几个文件。在 VS Code 中打开 `file_actions.py` 文件,如代码清单 6.4 所示。

```python
# Listing 6.4: playground/assistant_actions/file_actions.py
import os
from playground.actions_manager import agent_action

OUTPUT_FOLDER = "assistant_outputs"

@agent_action    # 此装饰器自动将函数添加为动作
def save_file(filename, content):     # 给函数清晰的名称,与目的一致
    """
    Save content to a file.     # 描述是助手用来确定函数的,所以要详细记录
    :param filename: The name of the file including extension.
    :param content: The content to save in the file.
    """
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"File '{filename}' saved successfully.")     # 通常返回说明成功或失败的消息
```

你可以通过将文件放在 `assistant_actions` 文件夹中并使用 `agent_action` 装饰器装饰它来添加任何你想要的自定义动作。只要确保给函数一个好名字,并为如何使用函数输入高质量的文档。当 Playground 启动时,它会加载文件夹中所有正确装饰并具有描述/文档的动作。

就这么简单。你可以根据需要添加多个自定义动作。在下一节中,我们将查看一个允许助手在本地运行代码的特殊自定义动作。

### 6.2.3 安装助手数据库

要运行本章中的几个示例,你需要安装助手数据库。幸运的是,这可以通过界面轻松完成,只需询问智能体即可。即将到来的说明详细说明了安装助手的过程,直接取自 GPT Assistants Playground 的 README。你可以安装位于 `assistants.db` SQLite 数据库中的几个演示助手：

1. 创建一个新助手,或使用现有助手。
2. 给助手 `create_manager_assistant` 动作（在 Actions 部分下找到）。
3. 要求助手创建管理器助手（例如,"please create the manager assistant"）,并确保将助手命名为"Manager Assistant"。
4. 刷新浏览器以重新加载助手选择器。
5. 选择新的 Manager Assistant。此助手具有允许它从 `assistants.db` 数据库安装助手的指令和动作。
6. 与 Manager Assistant 交谈,让它给你一个要安装的助手列表,或者只需让 Manager Assistant 安装所有可用的助手。

### 6.2.4 让助手在本地运行代码

让智能体和助手生成并运行可执行代码具有很大的能力。与 Code Interpreter 不同,本地运行代码提供了许多快速迭代和调整的机会。我们之前在 AutoGen 中看到了这一点,智能体可以继续运行代码,直到它按预期工作。

在 Playground 中,选择自定义动作 `run_code` 是一件简单的事,如图 6.5 所示。你还需要选择 `run_shell_command` 动作,因为它允许助手 pip 安装任何所需的模块。

> **图 6.5 说明**（位置：原文 图 6.5）
>
> 为助手选择自定义动作以运行 Python 代码：
>
> 1. 不要选择 Code Interpreter 工具
> 2. 选择 `run_code` 和 `run_shell_command` 自定义动作
> 3. 在 shell 上运行命令允许助手根据需要安装新包

你现在可以要求助手代表你生成并运行代码以确保其有效。通过添加自定义动作并要求助手生成并运行代码来尝试此操作,如图 6.6 所示。如果代码没有按预期工作,告诉助手你遇到的问题。

> **图 6.6 说明**（位置：原文 图 6.6）
>
> 让助手生成并运行 Python 代码：
>
> 1. 任何助手都可以生成代码。添加一些有用的指令和个性可以更好地对齐输出
> 2. "snake"游戏将打开一个新窗口,演示代码正在运行
> 3. 注意：当窗口打开时,它将阻塞 Gradio 界面
> 4. 在此示例中,助手为游戏生成了代码,然后意识到需要安装 Pygame。安装后,它运行了代码,如侧窗口所示

再次,Playground 中运行的 Python 代码在项目子文件夹中创建新的虚拟环境。如果你不运行任何操作系统级代码或低级代码,此系统运行良好。如果你需要更强大的东西,一个好的选择是 AutoGen,它使用 Docker 容器来运行隔离的代码。

添加运行代码或其他任务的动作可以使助手感觉像一个黑盒。幸运的是,OpenAI Assistants API 允许你消费事件并查看助手在幕后做什么。在下一节中,我们将看到这是什么样子。

### 6.2.5 通过日志调查助手过程

OpenAI 在 Assistants API 中添加了一个功能,允许你侦听通过工具/动作使用链接的事件和动作。此功能已集成到 Playground 中,在助手调用另一个助手时捕获动作和工具使用。

我们可以通过要求助手使用工具然后打开日志来尝试此操作。你可以这样做的一个很好的例子是给助手 Code Interpreter 工具,然后要求它绘制一个方程。图 6.7 显示了此练习的示例。

> **图 6.7 说明**（位置：原文 图 6.7）
>
> 正在捕获内部助手日志：
>
> 1. 绘制图形是一个很好的测试
> 2. Logs 选项卡显示文件保存位置
> 3. 在 Code Interpreter 中生成和运行的代码显示在 Logs 选项卡中

通常,当启用 Assistant Code Interpreter 工具时,你不会看到任何代码生成或执行。此功能允许你在发生时查看助手使用的所有工具和动作。它不仅是诊断的绝佳工具,而且还提供了对 LLM 功能的额外见解。

我们没有审查执行所有这些操作的代码,因为它很广泛,并且可能会经历几次更改。话虽如此,如果你计划使用 Assistants API,这个项目是一个很好的起点。介绍了 Playground 后,我们可以在下一节中继续我们进入 ABT 的旅程。

---

## 6.3 智能体行为树简介

智能体行为树（ABT）在助手和智能体系统上实现行为树。常规行为树和 ABT 之间的关键区别在于它们使用提示来指导动作和条件。因为提示可能返回随机结果的高发生率,我们也可以将这些树命名为随机行为树,这确实存在。为了简单起见,我们将区分用于控制智能体的行为树,将它们称为智能体行为树。

接下来,我们将进行一个练习来创建 ABT。完成的树将用 Python 编写,但需要设置和配置各种助手。我们将介绍如何使用助手本身管理助手。

### 6.3.1 使用助手管理助手

幸运的是,Playground 可以帮助我们快速管理和创建助手。我们将首先安装 Manager Assistant,然后安装预定义的助手。让我们开始使用以下步骤安装 Manager Assistant：

1. 在浏览器中打开 Playground,并创建一个新的简单助手或使用现有助手。如果需要新助手,创建它,然后选择它。
2. 选择助手后,打开 Actions 手风琴,并选择 `create_manager_assistant` 动作。你不需要保存；界面将自动更新助手。
3. 现在,在聊天界面中,使用以下提示助手："Please create the manager assistant."
4. 几秒钟后,助手会说它完成了。刷新浏览器,并确认 Manager Assistant 现在可用。如果由于某种原因未显示新助手,请尝试重新启动 Gradio 应用本身。

Manager Assistant 就像一个拥有一切访问权限的管理员。在与 Manager Assistant 互动时,请确保具体说明你的请求。激活 Manager Assistant 后,你现在可以使用以下步骤安装本书中使用的新助手：

1. 选择 Manager Assistant。如果你已修改 Manager Assistant,可以随时删除并重新安装它。虽然可以有多个 Manager Assistants,但不建议这样做。
2. 通过在聊天界面中输入以下内容来询问 Manager Assistant 可以安装哪些助手：
   ```
   Please list all the installable assistants.
   ```
3. 当你要求 Manager Assistant 安装它时,确定要安装哪个助手：
   ```
   Please install the Python Coding Assistant.
   ```

你可以使用 Playground 管理和安装任何可用的助手。你还可以要求 Manager Assistant 将所有助手的定义保存为 JSON：

```
Please save all the assistants as JSON to a file called assistants.json.
```

Manager Assistant 可以访问所有动作,应被视为独特的并谨慎使用。在制作助手时,最好保持它们以目标为导向,并将动作限制为仅它们需要的。这不仅可以避免给 AI 太多决策,还可以避免由幻觉引起的意外或错误。

在本章的其余练习中,你可能需要安装所需的助手。或者,你可以要求 Manager Assistant 安装所有可用的助手。无论哪种方式,我们都会在下一节中使用助手创建 ABT。

### 6.3.2 构建编码挑战 ABT

编码挑战为测试和评估智能体和助手系统提供了良好的基线。挑战和基准可以量化智能体或智能体系统的运行情况。我们已经在第 4 章中对 AutoGen 和 CrewAI 的多平台智能体应用了编码挑战。

对于此编码挑战,我们将更进一步,查看来自 Edabit 网站（https://edabit.com）的 Python 编码挑战,其复杂性从初学者到专家不等。我们将坚持专家代码挑战,因为 GPT-4o 和其他模型是出色的编码员。查看下一个清单中的挑战,并思考你将如何解决它。

```python
# Listing 6.5: Edabit challenge: Plant the Grass
Plant the Grass by AniXDownLoe
    You will be given a matrix representing a field g
and two numbers x, y coordinate.
    There are three types of possible characters in the matrix:
        x representing a rock.
        o representing a dirt space.
        + representing a grassed space.
    You have to simulate grass growing from the position (x, y).
    Grass can grow in all four directions (up, left, right, down).
    Grass can only grow on dirt spaces and can't go past rocks.
    Return the simulated matrix.

    Examples
    simulate_grass([
    "xxxxxxx",
    "xooooox",
    "xxxxoox"
    "xoooxxx"
    "xxxxxxx"
    ], 1, 1) → [
    "xxxxxxx",
    "x+++++x",
    "xxxx++x"
    "xoooxxx"
    "xxxxxxx"
    ]

    Notes
    There will always be rocks on the perimeter
```

你可以使用任何挑战或编码练习,但这里有几件事要考虑：

- 挑战应该是可测试的,具有可量化的断言（通过/失败）。
- 在要求游戏、构建网站或使用其他界面时避免打开窗口。在某个时候,测试完整界面将是可能的,但现在,它只是文本输出。
- 至少在最初时避免长时间运行的挑战。首先保持挑战简洁和短暂。

除了任何挑战,你还需要一组测试或断言来确认解决方案有效。在 Edabit 上,挑战通常提供一套全面的测试。下一个清单显示了挑战提供的附加测试。

```python
# Listing 6.6: Plant the Grass tests
Test.assert_equals(simulate_grass(
["xxxxxxx","xooooox","xxxxoox","xoooxxx","xxxxxxx"],
 1, 1),
["xxxxxxx","x+++++x","xxxx++x","xoooxxx","xxxxxxx"])
    Test.assert_equals(simulate_grass(
["xxxxxxx","xoxooox","xxoooox","xooxxxx",
"xoxooox","xoxooox","xxxxxxx"],
 2, 3), ["xxxxxxx","xox+++x","xx++++x","x++xxxx",
"x+xooox","x+xooox","xxxxxxx"])
    Test.assert_equals(simulate_grass(
["xxxxxx","xoxoox","xxooox","xoooox","xoooox","xxxxxx"],
1, 1),
["xxxxxx","x+xoox","xxooox","xoooox","xoooox","xxxxxx"])
    Test.assert_equals(simulate_grass(
["xxxxx","xooox","xooox","xooox","xxxxx"],
1, 1),
["xxxxx","x+++x","x+++x","x+++x","xxxxx"])
    # ... more tests
```

测试将作为两步验证的一部分运行,以确认解决方案有效。我们还将按书面使用测试和挑战,这将进一步测试 AI。

**图 6.8** 显示了将用于解决各种编程挑战的简单行为树的构成。你会注意到此 ABT 对动作和条件使用不同的助手。对于第一步,Python 编码助手（称为 Hacker）生成一个解决方案,然后由编码挑战法官（称为 Judge）审查,它产生一个精炼的解决方案,由不同的 Python 编码助手（称为 Verifier）验证。

> **图 6.8 说明**（位置：原文 图 6.8）
>
> 编码挑战的 ABT：
>
> 1. 根节点是一个序列
> 2. 主对话线程
> 3. Hacking solution（→ 序列节点）
>    - 初始解决方案将由 Python 编码助手生成,它将输出保存到 solution.py
> 4. Judge solution（→ 序列节点）
>    - 解决方案将由编码挑战法官审查。它将加载 solution.py,判断它,并输出一个名为 judged_solution.py 的文件
> 5. Verify solution（条件节点）
>    - 新对话线程
>    - 最后一步使用 Python 编码助手并通过查看 judged_solution.py 文件验证解决方案是否正确
>
> 助手使用线程来捕获对话。

图 6.8 还显示了每个智能体在哪个线程上对话。助手使用消息线程,类似于 Slack 或 Discord 频道,其中在线程上对话的所有助手都将看到所有消息。对于此 ABT,我们为 Hacker 和 Judge 保留一个主对话线程以共享消息,而 Verifier 在单独的消息线程上工作。将 Verifier 保持在自己的线程上将其与解决方案解决工作的噪音隔离开来。

现在,在代码中构建 ABT 是结合 `py_trees` 包和 Playground API 函数的问题。代码清单 6.7 显示了创建每个动作/条件节点与助手并给它们指令的代码摘录。

```python
# Listing 6.7: agentic_btree_coding_challenge.py
root = py_trees.composites.Sequence("RootSequence", memory=True)
thread = api.create_thread()    # 调用创建新消息线程

challenge = textwrap.dedent("""
     # 如示例清单 6.5 所示的挑战
""")

judge_test_cases = textwrap.dedent("""
    # 如示例清单 6.6 所示的测试
""")

hacker = create_assistant_action_on_thread(   # 创建将由 Hacker 和 Judge 共享的消息线程
    thread=thread,     # 如示例清单 6.5 所示的挑战
    action_name="Hacker",
    assistant_name="Python Coding Assistant",
    assistant_instructions=textwrap.dedent(f"""
    Challenge goal:
    {challenge}     # 如示例清单 6.5 所示的挑战
    Solve the challenge and output the
final solution to a file called solution.py
    """),
)
root.add_child(hacker)

judge = create_assistant_action_on_thread(    # 创建将由 Hacker 和 Judge 共享的消息线程
    thread=thread,     # 如示例清单 6.5 所示的挑战
    action_name="Judge solution",
    assistant_name="Coding Challenge Judge",
    assistant_instructions=textwrap.dedent(
        f"""
    Challenge goal:
    {challenge}     # 如示例清单 6.5 所示的挑战
    Load the solution from the file solution.py.
    Then confirm is a solution to the challenge
and test it with the following test cases:
    {judge_test_cases}     # 如示例清单 6.6 所示的测试
    Run the code for the solution and confirm it passes all the test cases.
    If the solution passes all tests save the solution to a file called
judged_solution.py
    """,
    ),
)
root.add_child(judge)

# verifier operates on a different thread, essentially in closed room
verifier = create_assistant_condition(    # 创建将由 Hacker 和 Judge 共享的消息线程
    condition_name="Verify solution",
    assistant_name="Python Coding Assistant",
    assistant_instructions=textwrap.dedent(
        f"""
    Challenge goal:
    {challenge}     # 如示例清单 6.5 所示的挑战
    Load the file called judged_solution.py and
verify that the solution is correct by running the code and confirm it passes
all the test cases:
    {judge_test_cases}     # 如示例清单 6.6 所示的测试
    If the solution is correct, return only the single word SUCCESS,
otherwise
return the single word FAILURE.
    """,
    ),
)
root.add_child(verifier)

tree = py_trees.trees.BehaviourTree(root)
while True:
    tree.tick()
    time.sleep(20)     # 睡眠时间可以根据需要向上或向下调整,可用于限制发送到 LLM 的消息
    if root.status == py_trees.common.Status.SUCCESS:   # 过程将继续直到验证成功
        break

### Required assistants –
### Python Coding Assistant and Coding Challenge Judge
### install these assistants through the Playground
```

通过在 VS Code 中加载文件或使用命令行运行 ABT。在终端中关注输出,并观察助手如何逐步完成树中的每个步骤。

如果解决方案在条件节点处未能通过验证,过程将根据树继续。即使使用这个简单的解决方案,你也可以快速创建无数变体。你可以使用更多节点/步骤和子树扩展树。也许你想要一组 Hacker 来分解和分析挑战。

此示例的工作主要使用 Playground 代码完成,使用帮助函数 `create_assistant_condition` 和 `create_assistant_action_on_thread`。此代码使用几个类来集成 `py_trees` 行为树代码和包装在 Playground 中的 OpenAI Assistants 代码。如果你想了解较低级别的详细信息,请查看项目中的代码。

### 6.3.3 对话式 AI 系统与其他方法

我们已经在第 4 章中查看了对话式多智能体系统,当时我们查看了 AutoGen。ABT 可以使用对话（通过线程）和其他方法（如文件共享）的组合来工作。让你的助手/智能体传递文件有助于减少嘈杂和重复的思想/对话的数量。相比之下,对话系统受益于潜在的涌现行为。因此,使用两者可以帮助演化更好的控制和解决方案。

代码清单 6.7 中的简单解决方案可以扩展以处理更多现实世界的编码挑战,甚至可能作为编码 ABT 工作。在下一节中,我们构建一个不同的 ABT 来处理不同的问题。

### 6.3.4 将 YouTube 视频发布到 X

在本节的练习中,我们查看一个可以执行以下操作的 ABT：

1. 在 YouTube 上搜索给定主题的视频并返回最新视频。
2. 下载搜索提供的所有视频的转录。
3. 总结转录。
4. 审查总结的转录并选择要编写 X（以前的 Twitter）帖子的视频。
5. 编写关于视频的令人兴奋和引人入胜的帖子,确保少于 280 个字符。
6. 审查帖子,然后在 X 上发布。

**图 6.9** 显示了使用每个不同助手组装的 ABT。在此练习中,我们使用序列节点作为根,每个助手执行不同的动作。此外,为了简化事情,每次助手交互都将始终发生在新线程中。这将每个助手的交互隔离为简洁的对话,如果出现问题更容易调试。

> **图 6.9 说明**（位置：原文 图 6.9）
>
> YouTube 社交媒体 ABT：
>
> 1. 根节点是一个序列
> 2. Search YouTube（→ 序列节点）
>    - 新线程
>    - 此助手搜索 YouTube 视频,下载并总结转录,并保存到文件 youtube_transcripts.txt
> 3. Write post（→ 序列节点）
>    - 新线程
>    - 助手加载转录,选择相关视频,编写少于 280 个字符的帖子,然后输出文件 youtube_twitter_post.txt
> 4. Post to X（→ 序列节点）
>    - 新线程
>    - 助手加载帖子,审查它并发布到 Twitter (X)
>
> 助手始终使用新线程。

### 6.3.5 所需的 X 设置

如果你计划运行此练习中的代码,你必须将你的 X 凭据添加到 `.env` 文件。`.env.default` 文件显示了凭据需要如何的示例,如代码清单 6.8 所示。你不必输入你的凭据。这意味着最后一步（发布）将失败,但你仍然可以查看文件（`youtube_twitter_post.txt`）以查看生成的内容。

```
# Listing 6.8: Configuring credentials
X_EMAIL = "twitter email here"
X_USERNAME = "twitter username here"
X_PASSWORD = "twitter password here"
```

> **YouTube 搜索和垃圾邮件**
>
> 如果你计划真正运行此练习并让它发布到你的 X 账户,请注意 YouTube 有一些垃圾邮件问题。助手已配置为尝试避免视频垃圾邮件,但其中一些可能会通过。构建一个可以在避免垃圾邮件的同时浏览视频的工作 ABT 有一些合适的应用。

代码清单 6.9 仅显示了创建助手动作的代码。此 ABT 使用三个不同的助手,每个助手都有自己的任务指令。注意每个助手都有一组唯一的指令来定义其角色。你可以通过使用 Playground 查看每个助手的指令。

```python
# Listing 6.9: agentic_btree_video_poster_v1.py
root = py_trees.composites.Sequence("RootSequence", memory=True)
search_term = "GPT Agents"

search_youtube_action = create_assistant_action(
    action_name=f"Search YouTube({search_term})",
    assistant_name="YouTube Researcher v2",
    assistant_instructions=f"""
    Search Term: {search_term}
    Use the query "{search_term}" to search for videos on YouTube.
    then for each video download the transcript and summarize it
for relevance to {search_term}
    be sure to include a link to each of the videos,
    and then save all summarizations to a file called youtube_transcripts.txt
    If you encounter any errors, please return just the word FAILURE.
    """,
)
root.add_child(search_youtube_action)

write_post_action = create_assistant_action(
    action_name="Write Post",
    assistant_name="Twitter Post Writer",
    assistant_instructions="""
    Load the file called youtube_transcripts.txt,
    analyze the contents for references to search term at the top and
then select
    the most exciting and relevant video related to:
    educational, entertaining, or informative, to post on Twitter.
    Then write a Twitter post that is relevant to the video,
    and include a link to the video, along
    with exciting highlights or mentions,
    and save it to a file called youtube_twitter_post.txt.
    If you encounter any errors, please return just the word FAILURE.
    """,
)
root.add_child(write_post_action)

post_action = create_assistant_action(
    action_name="Post",
    assistant_name="Social Media Assistant",
    assistant_instructions="""
    Load the file called youtube_twitter_post.txt and post the content
to Twitter.
    If the content is empty please do not post anything.
    If you encounter any errors, please return just the word FAILURE.
    """,
)
root.add_child(post_action)

### Required assistants – YouTube Researcher v2, Twitter Post Writer,
### and Social Media Assistant – install these assistants through the Playground
```

像往常一样运行代码,几分钟后,一个新帖子将出现在 `assistants_output` 文件夹中。图 6.10 显示了使用此 ABT 生成的帖子示例。每天运行此 ABT 生成多个帖子可能会,并且很可能会导致你的 X 账户被阻止。如果你已配置 X 凭据,你将看到帖子出现在你的订阅源中。

> **图 6.10 说明**（位置：原文 图 6.10）
>
> ABT 的 X 帖子示例

此 ABT 用于演示目的,不用于生产或长期使用。此演示的主要功能是显示搜索和加载数据、总结和过滤,然后生成新内容,最后突出显示多个自定义动作和与 API 的集成。

---

## 6.4 构建对话式自主多智能体

多智能体系统的对话方面可以驱动反馈、推理和涌现行为等机制。使用将助手/智能体孤立的 ABT 驱动智能体可以有效地控制结构化流程,正如我们在 YouTube 发布示例中看到的那样。然而,我们也不想错过跨智能体/助手对话的好处。

幸运的是,Playground 提供了将助手孤立或加入对话线程的方法。**图 6.11** 显示了助手如何以各种组合孤立或混合到线程中。将孤立与对话相结合提供了两种模式的最佳效果。

> **图 6.11 说明**（位置：原文 图 6.11）
>
> 孤立和对话助手的各种布局：
>
> 1. **Agent/Assistant Silos**（智能体/助手孤立）
>    - 孤立助手始终使用新线程并且是唯一的消费者
>    - Thread xya, Thread yyc, Thread zza
>    - Search 动作
>
> 2. **Agent/Assistant Conversational**（智能体/助手对话）
>    - 对话助手共享所有对话的线程
>    - Thread xyb, Thread xyc
>    - Search → Plan → Activity → Review
>
> 3. **Agent/Assistant Conversational + Silo**（智能体/助手对话+孤立）
>    - 孤立和对话的组合可以结合以进行公正的审查
>    - Thread xyc
>    - Search → Plan → Activity → Transfer → Verify

我们将研究一个简单但实用的练习来演示对话模式的有效性。对于下一个练习,我们将在 ABT 中使用两个在同一线程上对话的助手。下一个清单显示了代码中树的构造以及各自的助手。

```python
# Listing 6.10: agentic_conversation_btree.py
root = py_trees.composites.Sequence("RootSequence", memory=True)
bug_file = """
# code not shown
"""

thread = api.create_thread()    # 为助手创建消息线程以共享和对话

debug_code = create_assistant_action_on_thread(    # 使用特殊助手创建调试代码动作
    thread=thread,
    action_name="Debug code",
    assistant_name="Python Debugger",
    assistant_instructions=textwrap.dedent(f"""
    Here is the code with bugs in it:
    {bug_file}
    Run the code to identify the bugs and fix them.
    Be sure to test the code to ensure it runs without errors or throws
any exceptions.
    """),
)
root.add_child(debug_code)

verify = create_assistant_condition_on_thread(    # 创建验证条件以测试代码是否修复
    thread=thread,
    condition_name="Verify",
    assistant_name="Python Coding Assistant",
    assistant_instructions=textwrap.dedent(
        """
    Verify the solution fixes the bug and there are no more issues.
    Verify that no exceptions are thrown when the code is run.
    Reply with SUCCESS if the solution is correct, otherwise return FAILURE.
    If you are happy with the solution, save the code to a file called
fixed_bug.py.
    """,
    ),
)
root.add_child(verify)

tree = py_trees.trees.BehaviourTree(root)
while True:
    tree.tick()    # 树将继续运行直到根序列成功完成
    if root.status == py_trees.common.Status.SUCCESS:
        break
    time.sleep(20)
```

三个节点组成树：根序列、调试代码动作和验证修复条件。因为树的根是序列,两个助手将继续一个接一个地工作,直到它们都返回成功。两个助手都在同一线程上对话,但以提供持续反馈的方式进行控制。

通过在 VS Code 中加载文件或直接从命令行执行来运行练习。示例代码有一些小错误和问题,助手将努力修复。ABT 成功完成运行后,你可以打开 `assistants_output/fixed_bug.py` 文件并验证结果都很好。

我们现在已经看到了几个 ABT 在行动中,并了解了使用孤立或对话的细微差别。下一节将教你一些构建自己的 ABT 的技术。

---

## 6.5 使用反向链接构建 ABT

反向链接是一种源自逻辑和推理的方法,用于通过从目标向后工作来帮助构建行为树。本节将使用反向链接过程构建一个致力于实现目标的 ABT。以下列表更详细地描述了该过程：

1. **确定目标行为**。从你希望智能体执行的行为开始。
2. **确定所需的动作**。确定导致目标行为的动作。
3. **确定条件**。确定每个动作成功所必须满足的条件。
4. **确定通信模式**。确定助手将如何传递信息。助手会被孤立还是通过线程对话,还是模式组合更好？
5. **构建树**。从目标行为开始构建行为树,递归添加动作和条件节点,直到所有必要的条件都链接到已知状态或事实。

行为树通常使用称为黑板的模式来跨节点通信。像 `py_trees` 中的黑板使用键/值存储来保存信息并使其可跨节点访问。它还提供了几个控件,例如限制对特定节点的访问。

我们推迟使用文件进行通信,因为它们简单且透明。在某个时候,智能体系统预计将消耗比为黑板设计的更多的信息,并且采用不同的格式。黑板必须变得更加复杂,或者与文件存储解决方案集成。

让我们使用反向链接构建 ABT。我们可以处理各种目标,但一个有趣且也许是元目标是构建一个帮助构建助手的 ABT。因此,让我们首先将我们的目标表述为一个声明"创建一个可以帮助我完成{任务}的助手"：

**所需动作**：（向后工作）
- 创建助手。
- 验证助手。
- 测试助手。
- 命名助手。
- 给助手相关的指令。

**确定的条件**：
- 验证助手。

**确定通信模式**：为了保持有趣,我们将在同一消息线程上运行所有助手。

**构建树**：要构建树,让我们首先反转动作顺序并相应地标记每个元素的动作和条件：
- （动作）给助手相关指令以帮助用户完成给定任务。
- （动作）命名助手。
- （动作）测试助手。
- （条件）验证助手。
- （动作）创建助手。

当然,现在构建树的简单解决方案是询问 ChatGPT 或其他有能力的模型。要求 ChatGPT 制作树的结果显示在下一个清单中。你也可以独立地制定树,也许引入其他元素。

```
# Listing 6.11: ABT for building an assistant
Root
│
├── Sequence
│    ├── Action: Give the assistant relevant instructions to help a user
with a given task
│    ├── Action: Name the assistant
│    ├── Action: Test the assistant
│    ├── Condition: Verify the assistant
│    └── Action: Create the assistant
```

从这一点开始,我们可以通过遍历每个动作和条件节点并确定助手需要什么指令来开始构建树。这还可以包括任何工具和自定义动作,包括你可能需要开发的动作。在第一遍时,保持指令通用。理想情况下,我们希望创建尽可能少的助手。

在确定每个助手的助手、工具和动作以及为哪个任务后,你可以尝试进一步概括。思考可能在哪里组合动作并减少助手数量。最好从助手不足开始评估,而不是助手过多。但是,请确保保持正确的工作划分为任务：例如,测试和验证最好使用不同的助手完成。

---

## 6.6 练习

完成以下练习以提高你对材料的了解：

### 练习 1——创建旅行规划器 ABT

**目标**：构建一个智能体行为树（ABT）以使用助手规划旅行行程。

**任务**：
- 在本地机器上设置 GPT Assistants Playground。
- 创建一个 ABT 来规划旅行行程。树应具有以下结构：
  - 动作：使用 Travel 助手收集有关潜在目的地的信息。
  - 动作：使用 Itinerary Planner 创建逐日旅行计划。
  - 条件：使用另一个 Travel Assistant 验证行程的完整性和可行性。
- 实施并运行 ABT 以创建完整的旅行行程。

### 练习 2——构建客户支持自动化 ABT

**目标**：创建一个使用助手自动化客户支持响应的 ABT。

**任务**：
- 在本地机器上设置 GPT Assistants Playground。
- 创建具有以下结构的 ABT：
  - 动作：使用 Customer Query Analyzer 助手对客户查询进行分类。
  - 动作：使用 Response Generator 助手根据查询类别起草响应。
  - 动作：使用 Customer Support 助手向客户发送响应。
- 实施并运行 ABT 以自动化分析和响应客户查询的过程。

### 练习 3——使用 ABT 管理库存

**目标**：学习如何使用 ABT 创建和管理库存水平。

**任务**：
- 在本地机器上设置 GPT Assistants Playground。
- 创建管理零售业务库存的 ABT：
  - 动作：使用 Inventory Checker 助手审查当前库存水平。
  - 动作：使用 Order 助手为低库存物品下订单。
  - 条件：验证订单已正确下达并更新库存记录。
- 实施并运行 ABT 以动态管理库存。

### 练习 4——创建个人健身教练 ABT

**目标**：创建一个使用助手提供个性化健身训练计划的 ABT。

**任务**：
- 在本地机器上设置 GPT Assistants Playground。
- 创建 ABT 以开发个性化健身计划：
  - 动作：使用 Fitness Assessment 助手评估用户当前的健身水平。
  - 动作：使用 Training Plan Generator 根据评估创建自定义健身计划。
  - 条件：使用另一个 Fitness 助手验证计划的适用性和安全性。
- 实施并运行 ABT 以生成和验证个性化健身训练计划。

### 练习 5——使用反向链接构建财务顾问 ABT

**目标**：应用反向链接构建提供财务建议和投资策略的 ABT。

**任务**：
- 在本地机器上设置 GPT Assistants Playground。
- 定义以下目标："创建一个可以提供财务建议和投资策略的助手。"
- 使用反向链接,确定实现此目标所需的动作和条件。
- 通过反向链接树的基本动作和条件的构造来实施并运行 ABT 以生成全面的财务咨询服务。

---

## 本章小结

- **行为树**是一种强大且可扩展的 AI 控制模式,最早由 Rodney A. Brooks 在机器人技术中引入。它们广泛用于游戏和机器人技术,因其模块化和可重用性而著称。

- **行为树中的主要节点**是选择器、序列、条件、动作、装饰器和并行节点。选择器像"or"块：序列按顺序执行节点,条件测试状态,动作执行工作,装饰器是包装器,并行节点允许双重执行。

- **理解行为树的执行流程**对于设计、构建和操作它们以提供控制和做出清晰的决策路径至关重要。

- **行为树的优势**包括模块化、可扩展性、灵活性、易于调试和决策逻辑的解耦,使行为树适合复杂的 AI 系统。

- **在 Python 中设置和运行简单行为树**需要正确命名和记录自定义节点。

- **GPT Assistants Playground 项目**是一个基于 Gradio 的界面,模仿 OpenAI Assistants Playground,并具有用于教学和演示 ABT 的附加功能。

- **GPT Assistants Playground** 允许创建和管理自定义动作,这对于构建多功能助手至关重要。

- **ABT 控制智能体和助手**通过使用提示来指导助手的动作和条件。ABT 使用 LLM 的能力来创建动态和自主系统。

- **反向链接**是一种通过从目标行为向后工作来构建行为树的方法。此过程涉及识别所需的动作、条件和通信模式,然后逐步构建树。

- **智能体系统受益于孤立和对话模式**用于实体之间的通信。ABT 可以通过结合孤立和对话助手来使用结构化流程和涌现行为。

---

## 翻译说明

### 术语对照表

| 英文术语 | 中文翻译 | 说明 |
|---------|---------|------|
| Behavior Tree | 行为树 | AI 控制模式 |
| Agentic Behavior Tree (ABT) | 智能体行为树 | 用于智能体的行为树 |
| Selector | 选择器 | 复合节点类型 |
| Sequence | 序列 | 复合节点类型 |
| Condition | 条件 | 任务节点 |
| Action | 动作 | 任务节点 |
| Decorator | 装饰器 | 控制节点 |
| Parallel | 并行 | 复合节点 |
| Assistant | 助手 | OpenAI 的 AI 助手 |
| Thread | 线程 | 消息对话线程 |
| Back Chaining | 反向链接 | 构建行为树的方法 |
| Blackboard | 黑板 | 节点间通信模式 |
| py_trees | py_trees 库 | Python 行为树库 |

### 翻译特点

1. **代码示例**：保持英文原样,添加中文注释
2. **技术术语**：首次出现时标注英文
3. **图表说明**：详细描述原文图表内容
4. **代码清单**：保留原始编号和说明
5. **章节结构**：完整保留原文层次

### 注意事项

- 本章介绍了行为树的核心概念和实现
- GPT Assistants Playground 是本章的核心工具
- ABT 是将行为树应用于 AI 智能体的创新方法
- 实践练习需要配置 OpenAI API 和相关环境
- 反向链接是设计复杂行为树的有效方法

**翻译完成时间**: 2025-11-13
**字数统计**: 约 26,000 字（中文）
**质量保证**: 已校对技术术语和代码注释的准确性
