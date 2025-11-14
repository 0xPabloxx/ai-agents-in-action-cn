# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **bilingual Chinese-English translation project** of "AI Agents in Action: Building Effective AI Agents" by Michael Lanham. The project provides a comprehensive practical guide covering agent architectures, LLM integration, multi-agent systems, autonomous assistants, and agent platforms.

**Key Characteristics:**
- Pure documentation/translation project (no code to build, test, or run)
- All content is in Markdown format
- Uses HTML `<mark>` tags for Chinese text highlighting
- Follows strict bilingual format with English and Chinese side-by-side
- Original book has 322 pages across 11 chapters in 4 parts
- Publisher: Manning Publications

## File Structure

```
01-Chapter-01-Introduction-to-agents-and-their-world.md
02-Chapter-02-Harnessing-the-power-of-large-language-models.md
03-Chapter-03-Engaging-GPT-assistants.md
04-Chapter-04-Exploring-multi-agent-systems.md
05-Chapter-05-Empowering-agents-with-actions.md
06-Chapter-06-Building-autonomous-assistants.md
07-Chapter-07-Assembling-and-using-an-agent-platform.md
08-Chapter-08-Understanding-agent-memory-and-knowledge.md
09-Chapter-09-Mastering-agent-prompts-with-prompt-flow.md
10-Chapter-10-Agent-reasoning-and-evaluation.md (pending)
11-Chapter-11-Agent-planning-and-feedback.md (pending)

source/
  ├── AI Agents in Action.pdf
  ├── chapter1-11.txt (extracted text files)
  └── AI Agents in Action_chapters_smart/ (chapter extractions)

scripts/
  ├── pdf_to_text_by_chapter.py
  └── pdf_to_text_smart.py

rules/
  └── rules.md (translation guidelines)

README.md
CLAUDE.md
翻译计划.md
```

## Translation Format and Rules

### Mandatory Highlighting System

**All Chinese translations MUST use HTML `<mark>` tags:**
```markdown
English text here.

<mark>中文翻译在这里。</mark>
```

This creates yellow highlighting for Chinese content on GitHub, making it easy to distinguish between languages.

### Layout Format

**Bilingual paragraph-by-paragraph:**
```markdown
[English paragraph 1]

<mark>[中文翻译段落 1]</mark>

[English paragraph 2]

<mark>[中文翻译段落 2]</mark>
```

### Technical Term Conventions

Keep important terms in English with Chinese in parentheses on first use:
- Agent → 智能体 (Agent)
- Assistant → 助手 (Assistant)
- LLM → 大语言模型 (LLM)
- Prompt Engineering → 提示工程 (Prompt Engineering)
- Function Calling → 函数调用 (Function Calling)
- Semantic Kernel → 语义内核 (Semantic Kernel)
- Behavior Tree → 行为树 (Behavior Tree)
- RAG → 检索增强生成 (RAG)
- Multi-Agent System → 多智能体系统 (Multi-Agent System)

Reference the technical term dictionary in README.md for consistent translations.

### Spacing Rules

- Add space between Chinese and English: `AI 系统`
- Add space between Chinese and numbers: `9 个章节`
- Use Chinese punctuation in Chinese context
- Use English punctuation in English context

### Format Requirements

- Use horizontal rules (`---`) to separate major sections
- Preserve all original code examples with Chinese comments
- Maintain exact Markdown formatting from original
- Use proper Chinese quotation marks: 「」 or ""

## Translation Quality Standards

1. **Accuracy**: 100% faithful to original meaning
2. **Fluency**: Natural Chinese expression that follows local conventions
3. **Technical Precision**: Maintain technical document rigor
4. **Consistency**: Uniform terminology throughout
5. **Format Compliance**: 100% correct Markdown syntax

## Project Status

The project is being translated chapter by chapter:
- ✅ Completed: Chapters 1-9 (267/322 pages, 83%)
- ⏳ In Progress: None
- ❌ Pending: Chapters 10-11 (55 pages remaining)

Check README.md for detailed progress tracking.

## Common Tasks

### Adding a New Translation

1. Follow the file naming convention: `XX-Chapter-XX-English-title.md` (e.g., `10-Chapter-10-Agent-reasoning-and-evaluation.md`)
2. Apply `<mark>` tags to ALL Chinese text
3. Preserve original structure and code examples
4. Follow technical term dictionary for consistency
5. Update README.md progress table when complete

### Reviewing Translations

Check for:
- `<mark>` tags around all Chinese content
- Consistent technical term usage (check README.md dictionary)
- Proper spacing between Chinese/English and numbers
- Horizontal rules between major sections
- All code examples preserved and commented in Chinese
- Correct Markdown syntax rendering

### Continuing Translation Work

When asked to continue translation:
1. Check 翻译计划.md for current phase
2. Read corresponding chapter text from source/ folder
3. Create new translation file in translations/ folder
4. Follow bilingual format with `<mark>` tags
5. Update README.md progress tracking
6. Mark todo items as completed

## Important Notes

- **No build/test/run commands**: This is a pure documentation project
- **All files are Markdown**: No code compilation or execution needed
- **GitHub is the primary viewing platform**: Format optimized for GitHub rendering
- **Yellow highlighting is essential**: `<mark>` tags are mandatory for all Chinese text
- **License**: Translation released under CC BY-NC 4.0
- **Purpose**: Educational and community contribution only

## Book Structure

The book covers four parts:

**Part One: Foundations (62 pages)**
- Chapter 1: Introduction to agents and their world
- Chapter 2: Harnessing the power of large language models

**Part Two: Building Agents (60 pages)**
- Chapter 3: Engaging GPT assistants
- Chapter 4: Exploring multi-agent systems

**Part Three: Empowering Agents (62 pages)**
- Chapter 5: Empowering agents with actions
- Chapter 6: Building autonomous assistants

**Part Four: Platforms & Advanced Features (138 pages)**
- Chapter 7: Assembling and using an agent platform
- Chapter 8: Understanding agent memory and knowledge
- Chapter 9: Mastering agent prompts with prompt flow
- Chapter 10: Agent reasoning and evaluation
- Chapter 11: Agent planning and feedback

## Resources

- **Original Book**: [Manning - AI Agents in Action](https://www.manning.com/books/ai-agents-in-action)
- **GitHub Repository**: https://github.com/0xPabloxx/ai-agents-in-action-cn
- **Translation Rules**: rules/rules.md
- **Progress Tracking**: README.md
- **Translation Plan**: 翻译计划.md
