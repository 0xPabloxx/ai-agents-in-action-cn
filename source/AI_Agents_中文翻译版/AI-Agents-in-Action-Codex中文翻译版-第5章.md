# AI-Agents-in-Action-Codex中文翻译版-第5章

## 第5章 让代理拥有行动力

上一章我们学会用多代理协作完成复杂任务，本章则深入“行动”这一核心能力：如何让 LLM 通过函数、插件、技能、工具去操作外部世界。我们先复盘 ChatGPT 插件与 OpenAI 函数调用，再介绍微软的 Semantic Kernel（SK），学习用语义函数 + 本地代码（Native Function）来封装服务，最终把任意 API 包装成 GPT 接口，让聊天/代理系统可语义化调用。

### 本章内容
- `5.1` 代理动作的含义：插件、工具、技能之间的映射关系。
- `5.2` 在 OpenAI API 中定义函数（tools）并执行，含多函数并发示例。
- `5.3` Semantic Kernel 入门：安装、创建语义函数、使用上下文变量。
- `5.4` 语义函数与本地函数的协同，如何注册/复用插件。
- `5.5` 用 SK 把 TMDB API 封装成 GPT 接口，驱动聊天代理。
- `5.6` “语义式思维”：返回结构化 JSON 让 LLM 进一步筛选。
- `5.7` 练习与总结。

---

## 5.1 代理动作与插件
- 插件相当于“代理的代理”：ChatGPT 安装“电影推荐插件”后，LLM 会自动识别用户意图、抽取参数、调用插件去抓取数据，再把结果回传给用户（图 5.1）。
- 插件内部可包含多个动作，真正执行任务的是“函数/技能/工具”。不同框架术语不一，本章统一称之为 **Action**。
- 动作既可以触发 API（抓取网页、查询数据库），也可以调用其他 LLM 做进一步处理。Chevron 图标标记了“代理动作发生的位置”。
- ChatGPT 插件 + OpenAI 函数调用 = 让 LLM 系统拥有“外部臂膀”。

---

## 5.2 在 OpenAI API 中执行函数
### 5.2.1 在 API 请求里定义函数
- Listing 5.1 展示 `chat.completions.create` 如何通过 `tools=[{"type":"function", ...}]` 定义函数；这就是 ChatGPT 插件和 Functions API 的底层协议。
- 参数定义遵循 JSON Schema，可描述类型、枚举以及必填字段。LLM 会解析用户输入，将其映射到满足 Schema 的参数上（图 5.3）。
- 示例 `first_function.py`：
  - 请求 1：“推荐一部穿越电影” → 返回 `Function(name='recommend', arguments='{"topic": "time travel movie"}')`
  - 请求 2：增加“good”评级 → 参数中自动带上 `rating`。
- 注意：**LLM 只返回函数名和参数，不会执行函数**。开发者需在拿到函数名后调用本地实现。

### 5.2.2 触发并执行函数
- `parallel_functions.py` 演示更完整流程（图 5.4）：
  1. 用户一次性请求“穿越电影/菜谱/礼物”三种推荐。
  2. LLM 返回 3 组 `tool_calls`（同一函数多次调用）。
  3. 代码遍历每个 `tool_call`，调用本地 `recommend()`，将结果写入 `messages`。
  4. 再次调用 LLM，让它把多个函数结果转成自然语言回答。
- 该示例使用更便宜的 GPT-3.5 Turbo，表明“函数委派”可以由较小模型承担。

---

## 5.3 Semantic Kernel（SK）入门
SK 是微软开源的 AI 应用框架，核心用途：管理语义函数（Prompt）和本地函数（代码），并通过统一的插件系统对外暴露。支持 Python/Java/C# 等多语言。

### 5.3.1 安装与首次运行
1. 卸载旧版本、克隆仓库并安装可编辑包（Listing 5.8）。
2. 在 `SK_connecting.py` 中：
   - 创建 `Kernel()`。
   - 选择 OpenAI 或 Azure OpenAI 服务并加载 `.env` 中的 API Key。
   - 调用 `kernel.invoke_prompt("recommend a movie about time travel")`（Listing 5.9）。
3. 输出即为运行语义函数（prompt template）的结果。

### 5.3.2 语义函数 + 上下文变量
- `SK_context_variables.py` 使用模板变量（`{{$format}}`, `{{$subject}}` 等）构建“推荐器”提示（Listing 5.10）。
- 通过 `PromptTemplateConfig` 声明输入变量及描述，`kernel.create_function_from_prompt()` 将其注册为函数。
- 调用 `kernel.invoke` 时用 `KernelArguments` 提供变量值即可，输出示例推荐了一部“中世纪、穿越、喜剧电影”。

---

## 5.4 语义函数与本地函数的协同
### 5.4.1 创建并注册语义插件
- VS Code SK 插件可生成语义技能：
  1. 新建 Skill → 选目录 → 命名函数 → 撰写描述（图 5.6）。
  2. `config.json` 描述函数类型（`completion`）、参数、采样策略（Listing 5.11）。
  3. `skprompt.txt` 写实际 Prompt（Listing 5.12）。
- 运行 `SK_first_skill.py`：
  - `kernel.import_plugin_from_prompt_directory("plugins", "Recommender")` 将技能注册进 Kernel。
  - 调用 `recommend = recommender["Recommend_Movies"]` + `kernel.invoke` 即可完成推荐（Listing 5.13）。

### 5.4.2 原生函数（Native Function）
- 原生函数用 Python/JS/C# 实现任意逻辑，通过 `@kernel_function` 装饰器描述（Listing 5.14）。
- `SK_native_functions.py`：
  - `MySeenMoviesDatabase.load_seen_movies()` 读取文本文件返回观影列表。
  - `kernel.import_plugin_from_object(..., "SeenMoviesPlugin")` 注册该函数（Listing 5.15）。
  - 语义函数 `Recommend_Movies` 使用加载的观影列表生成新推荐。

### 5.4.3 在语义函数中嵌入原生函数
- `SK_semantic_native_functions.py` 直接在 Prompt 里引用 `{{MySeenMoviesDatabase.LoadSeenMovies}}`（Listing 5.16）。
- 调用前需先把原生函数作为插件导入；语义函数可以只用 `create_function_from_prompt` 创建而不注册。
- 运行后 LLM 会基于原生函数返回的清单给出新片建议（Listing 5.17）。

---

## 5.5 把 Semantic Kernel 作为 GPT 接口
### 5.5.1 构建 TMDB 语义服务
- TMDB 提供影视 API，无语义层。我们在 `skills/Movies/tmdb.py` 中封装 `TMDbService`：
  - `get_movie_genre_id`：根据名称获取 genre id。
  - `get_top_movies_by_genre`：按类型拉取当前热映电影（Listing 5.18-5.19）。
- 每个方法都用 `@kernel_function` 标注，使其自动成为插件。

### 5.5.2 在 Shell/Chat 中调用
- `SK_service.py`：示范在命令行直接调用 TMDB 插件（图 5.8）。
- `SK_service_chat.py`：
  - 实现一个简易聊天循环；用户输入自然语句，程序用 `kernel.invoke` 调度 TMDB 插件（Listing 5.23-5.24）。
  - 例如“列出动作和喜剧的当前热映影片” → 会顺序调用 `get_top_movies_by_genre` + `get_movie_genre_id`，最后返回两个类别的列表。

---

## 5.6 用“语义思维”编写服务
- 如果插件只返回片名，LLM 无法进一步筛选。应尽量返回结构化 JSON，留给 LLM 自己过滤、排序、摘要。
- `tmdb_v2.py` 将 `get_top_movies_by_genre` 改为 `json.dumps(filtered_movies)`（Listing 5.25），`SK_service_chat.py` 中切换到新服务（Listing 5.26）。
- 于是用户可以追加条件“只要太空题材的动作片”，LLM 会在本地过滤 JSON，并把匹配结果转成自然语言（Listing 5.27）。
- 这体现了“服务返回越富信息量，LLM 越能展现推理与转写能力”。

---

## 5.7 练习
1. **温度转换插件**：实现摄氏/华氏互转，接入 OpenAI Chat API。
2. **天气查询插件**：调用公开天气 API，支持城市参数。
3. **创作型语义函数**：写诗/儿童故事，支持用户主题输入。
4. **语义 + 原生函数**：例如语义函数生成菜单、原生函数查营养信息。
5. **用 SK 包装新闻 API**：把新闻接口暴露为聊天插件，支持按主题查询。

---

## 本章小结
- 代理的行动力来自“可调用的外部函数/插件/工具”。OpenAI 的 Functions API 与 ChatGPT 插件遵循同一 Schema。
- Semantic Kernel 统一管理语义函数（Prompt 模板）与本地函数（代码实现），并用插件机制让它们被聊天/代理系统调用。
- 语义函数可复用 Prompt 模板；原生函数可访问文件、数据库、API；两者可以相互嵌套，实现“代码 + Prompt”混合流水线。
- SK 插件既能消费外部 API，也能对外暴露自身，让任意 Web Service 摇身变成 GPT 接口。
- 编写语义服务时要“多返回数据”：尽可能输出完整 JSON，利用 LLM 自己过滤/排序/生成，而非只能回传字符串列表。
- 通过这些手段，代理可以精准地“执行动作”、调用服务、组合函数，为下一章的“自治行为树”铺平道路。
