# AI-Agents-in-Action-Codex中文翻译版-第9章

## 第9章 使用 Prompt Flow 精通代理提示

本章聚焦 OpenAI “Test Changes Systematically” 策略，借助微软开源工具 **prompt flow** 实现“构建 → 评估 → 比较”提示迭代。我们将提示（prompt）视作代理 profile 的核心：它不仅包含 persona，还能扩展至工具、记忆、规划、反馈等组件。章内内容依次涵盖：迭代提示的重要性、profile 构成、prompt flow 的安装与运行、如何创建/部署/批量执行 prompt，以及用 **rubric + grounding** 自动评估不同提示版本。

---

## 9.1 为何需要系统化提示工程
1. **迭代提问示例**：直接问 “can you recommend something” → 需补充更多上下文；加入系统提示 `system: You are an expert on time travel movies.` 后，再提问即可得到更好回答。
2. **多轮对话 vs. 系统化流程**：手动在 ChatGPT 里反复提问虽然可行，但难以记录与评估。图 9.5 展示了结构化方法：编写提示 → 运行 → 评估 → 若输出符合预期则定版，否则继续修改。

## 9.2 代理 Profile 与 Persona
- Profile = 构成代理的全套提示：persona、规则、工具说明、记忆/知识指引、推理/规划/反馈要求等（图 9.6）。
- Persona 只是 Profile 的“语气 + 背景”部分；真正的 profile 还要对接 actions、memory 等组件。

## 9.3 Prompt Flow 实战入门
### 9.3.1 环境准备
- 需安装 VS Code、prompt flow 扩展、Python 虚拟环境，并 `pip install promptflow promptflow-tools`。
- 在 VS Code 的 prompt flow 面板创建 LLM 连接（图 9.7、图 9.8）。
- 打开 `chapter_09/promptflow/simpleflow/flow.dag.yaml`，使用 Visual Editor（图 9.9），设置 LLM block（图 9.10），点击 Run 即可看到基础推荐结果（图 9.11）。

### 9.3.2 基于 Jinja2 的 Profile 模板
- prompt flow 默认使用 **Jinja2** 生成 system/user prompt。修改 `recommended.jinja2` 即可改变 persona/提示文本（图 9.12）。

### 9.3.3 部署为本地应用
- 在 Flow Editor 中点 Build → Local App（图 9.13），即可生成网页（图 9.14），填写 `user_input` 后体验实时推荐。

## 9.4 Profiles 的变体与输入扩展
- 将 flow 改成 `recommender_with_variations`，新增输入 `subject/format/genre/custom`（图 9.15）。
- 输入可来自传统 UI（Option A）或代理对话（Option B）（图 9.16）。
- 在 Variants 中创建多个 Jinja2 模板；variant 0 把参数注入 user prompt；variant 1 注入 system prompt（图 9.17）。点击 “Run All” 可比较两个版本（图 9.18）。

## 9.5 Rubric 与 Grounding
- **Rubric** = 评价标准。构建步骤：明确目标 → 设定维度（subject/format/genre 等）→ 评分尺度（1~5）→ 描述每档标准（表 9.2）→ 应用、平均分、保持一致性 → 不断迭代。
- **Grounding** = 检查输出是否符合 Rubric/上下文要求。

## 9.6 用 LLM Prompt 做自动评分
- 在 `recommender_with_LLM_evaluation` flow 中添加 `evaluate_recommendation` block，模板内含 rubric 描述（图 9.19）。
- 运行后生成 JSON 文本，每条推荐都有 subject/format/genre 的 1-5 分（Listing 9.1）。

## 9.7 取得“完美提示”的方法
### 9.7.1 解析 LLM 评分输出
- 新增 `parsing_results` Python block（Listing 9.2），把字符串解析成字典列表，方便进一步处理（图 9.20）。

### 9.7.2 批量运行（Batch Processing）
1. 准备 JSONL 批量输入（示例见 Listing 9.3/9.4）。
2. 在 Flow Editor 中点击“Batch”（烧杯图标），选 JSONL 文件（图 9.21、9.22），prompt flow 会自动并发执行并记录日志。
3. 在 prompt flow 扩展的 Run History 中可查看每条运行，甚至查看 API 调用细节（图 9.23）。

### 9.7.3 评估与对比 Run
1. 使用 `evaluate_groundings` flow：`line_process.py` 计算每个推荐的平均分（Listing 9.3）；`aggregate.py` 聚合所有 run 的平均分并输出指标（Listing 9.4，图 9.24）。
2. 运行方法：在 flow 中选择 “Existing Run” 批量数据（图 9.25），执行后在 prompt flow 扩展里用 “Visualize Runs” 对比不同 Prompt 版本的指标（图 9.26）。示例显示：将参数注入 system prompt (variant 1) 获得更高评分。

## 9.7.4 练习建议
1. 为推荐场景创建新的 Prompt 变体，批量评估其效果。
2. 给 rubric 增添新指标并更新评估流程。
3. 设计全新用例 + Prompt + Rubric，比较不同场景下的表现。
4. 使用 LM Studio 托管本地 LLM，与 prompt flow 一起测试开源模型。
5. 应用“Write Clear Instructions”策略构建更多 prompt，并用 prompt flow 评估。

## 本章结论
- 代理 profile = 多个提示组件的集合，可扩展至工具/记忆/规划/反馈等维度。
- Prompt flow 提供“图形化编辑 + 模板管理 + 本地运行 + 批量评估 + 结果可视化”等全流程能力，非常适合系统化提示工程。
- LLM Prompt 可用作“评分器”，配合 rubric 在无人工介入下完成 grounding，易于量化不同 prompt 的表现。
- Batch Run + Evaluate Flow + Run Visualization 构成完整的“测试-比较-选择最佳 prompt”的闭环。

借助这些方法，你可以用 prompt flow 构建出高质量、可验证、易部署的代理 profile，为后续章节中的推理、规划与评估奠定基础。
