# Chapter 8: Understanding agent memory and knowledge | <mark>第8章：理解智能体记忆和知识</mark>

## This chapter covers | <mark>本章内容</mark>

- Retrieval in knowledge/memory in AI functions | <mark>AI 功能中的知识/记忆检索</mark>
- Building retrieval augmented generation workflows with LangChain | <mark>使用 LangChain 构建检索增强生成工作流</mark>
- Retrieval augmented generation for agentic knowledge systems in Nexus | <mark>Nexus 中智能体知识系统的检索增强生成</mark>
- Retrieval patterns for memory in agents | <mark>智能体中记忆的检索模式</mark>
- Improving augmented retrieval systems with memory and knowledge compression | <mark>通过记忆和知识压缩改进增强检索系统</mark>

---

Now that we've explored agent actions using external tools, such as plugins in the form of native or semantic functions, we can look at the role of memory and knowledge using retrieval in agents and chat interfaces. We'll describe memory and knowledge and how they relate to prompt engineering strategies, and then, to understand memory knowledge, we'll investigate document indexing, construct retrieval systems with LangChain, use memory with LangChain, and build semantic memory using Nexus.

<mark>现在我们已经探索了使用外部工具的智能体动作，例如以原生函数或语义函数形式的插件，我们可以探讨在智能体和聊天界面中使用检索的记忆和知识的作用。我们将描述记忆和知识以及它们与提示工程策略的关系，然后为了理解记忆知识，我们将研究文档索引，使用 LangChain 构建检索系统，使用 LangChain 的记忆功能，并使用 Nexus 构建语义记忆。</mark>

---

## 8.1 Understanding retrieval in AI applications

<mark>## 8.1 理解 AI 应用中的检索</mark>

Retrieval in agent and chat applications is a mechanism for obtaining knowledge to keep in storage that is typically external and long-lived. Unstructured knowledge includes conversation or task histories, facts, preferences, or other items necessary for contextualizing a prompt. Structured knowledge, typically stored in databases or files, is accessed through native functions or plugins.

<mark>智能体和聊天应用中的检索是一种获取知识的机制，这些知识存储在通常是外部和长期的存储中。非结构化知识包括对话或任务历史、事实、偏好或其他用于上下文化提示的必要项目。结构化知识通常存储在数据库或文件中，通过原生函数或插件访问。</mark>

Memory and knowledge, as shown in figure 8.1, are elements used to add further context and relevant information to a prompt. Prompts can be augmented with everything from information about a document to previous tasks or conversations and other reference information.

<mark>如图 8.1 所示，记忆和知识是用于向提示添加进一步上下文和相关信息的元素。提示可以通过从文档信息到先前任务或对话以及其他参考信息的所有内容进行增强。</mark>

The prompt engineering strategies shown in figure 8.1 can be applied to memory and knowledge. Knowledge isn't considered memory but rather an augmentation of the prompt from existing documents. Both knowledge and memory use retrieval as the basis for how unstructured information can be queried.

<mark>图 8.1 中显示的提示工程策略可以应用于记忆和知识。知识不被视为记忆，而是来自现有文档的提示增强。知识和记忆都使用检索作为如何查询非结构化信息的基础。</mark>

**Figure 8.1 Memory, retrieval, and augmentation of the prompt using the following prompt engineering strategies: Use External Tools and Provide Reference Text** | <mark>**图 8.1 使用以下提示工程策略的记忆、检索和提示增强：使用外部工具和提供参考文本**</mark>

<mark>*图片描述：显示提示工程策略的流程图*</mark>

**Prompt Engineering Strategies** | <mark>**提示工程策略**</mark>

- **Provide Reference Text** — Helps reduce hallucinations. Tactics involve instructing the model to use or cite reference texts. → Knowledge and Memory | <mark>**提供参考文本** — 帮助减少幻觉。策略包括指导模型使用或引用参考文本。→ 知识和记忆</mark>

- **Use External Tools** — Enhances model capabilities. Tactics include embeddings-based search, code execution, and access to specific functions. → Actions, Knowledge, Memory | <mark>**使用外部工具** — 增强模型能力。策略包括基于嵌入的搜索、代码执行和访问特定函数。→ 动作、知识、记忆</mark>

**Memory** | <mark>**记忆**</mark>

- Request → Made by a user or another system or agent | <mark>请求 → 由用户或其他系统或智能体发出</mark>
- Prompt (system: you are a ... Query) | <mark>提示（system: 你是一个... 查询）</mark>
- LLM → Response | <mark>LLM → 响应</mark>
- Retrieved memories → Database, Vector Store, Internal Memory | <mark>检索的记忆 → 数据库、向量存储、内部记忆</mark>
- Save to memory | <mark>保存到记忆</mark>
- Retrieved elements provide references and context | <mark>检索的元素提供参考和上下文</mark>
- May include the whole or parts of the conversation | <mark>可能包括整个或部分对话</mark>

**Knowledge** | <mark>**知识**</mark>

- Vector Store | <mark>向量存储</mark>
- Retrieved knowledge | <mark>检索的知识</mark>
- Retrieval is done using semantic similarity | <mark>使用语义相似性进行检索</mark>

The retrieval mechanism, called retrieval augmented generation (RAG), has become a standard for providing relevant context to a prompt. The exact mechanism that powers RAG also powers memory/knowledge, and it's essential to understand how it works. In the next section, we'll examine what RAG is.

<mark>检索机制称为检索增强生成（RAG），已成为向提示提供相关上下文的标准。为 RAG 提供动力的确切机制也为记忆/知识提供动力，理解它的工作原理至关重要。在下一节中，我们将探讨什么是 RAG。</mark>

---

## 8.2 The basics of retrieval augmented generation (RAG)

<mark>## 8.2 检索增强生成（RAG）的基础</mark>

RAG has become a popular mechanism for supporting document chat or question-and-answer chat. The system typically works by a user supplying a relevant document, such as a PDF, and then using RAG and a large language model (LLM) to query the document.

<mark>RAG 已成为支持文档聊天或问答聊天的流行机制。该系统通常通过用户提供相关文档（如 PDF）来工作，然后使用 RAG 和大语言模型（LLM）来查询文档。</mark>

Figure 8.2 shows how RAG can allow a document to be queried using an LLM. Before any document can be queried, it must first be loaded, transformed into context chunks, embedded into vectors, and stored in a vector database.

<mark>图 8.2 显示了 RAG 如何允许使用 LLM 查询文档。在查询任何文档之前，必须首先加载它，将其转换为上下文块，嵌入到向量中，并存储在向量数据库中。</mark>

A user can query previously indexed documents by submitting a query. That query is then embedded into a vector representation to search for similar chunks in the vector database. Content similar to the query is then used as context and populated into the prompt as augmentation. The prompt is pushed to an LLM, which can use the context information to help answer the query.

<mark>用户可以通过提交查询来查询先前索引的文档。然后将该查询嵌入到向量表示中，以在向量数据库中搜索相似的块。与查询相似的内容然后用作上下文，并作为增强填充到提示中。提示被推送到 LLM，LLM 可以使用上下文信息来帮助回答查询。</mark>

**Figure 8.2 The two phases of RAG: first, documents must be loaded, transformed, embedded, and stored, and, second, they can be queried using augmented generation** | <mark>**图 8.2 RAG 的两个阶段：首先，必须加载、转换、嵌入和存储文档，其次，可以使用增强生成查询它们**</mark>

<mark>*图片描述：RAG 工作流程图*</mark>

**Retrieval Augmented Generation (RAG)** | <mark>**检索增强生成（RAG）**</mark>

**Phase 1: Indexing** | <mark>**阶段 1：索引**</mark>

- Submit document to query | <mark>提交文档以查询</mark>
- Document is loaded, transformed, and split into chunks | <mark>文档被加载、转换并拆分为块</mark>
- Transform | <mark>转换</mark>
- Embedding — Chunks of text are converted to vectors | <mark>嵌入 — 文本块被转换为向量</mark>
- Vector DB — Vectors representing chunks of text are stored | <mark>向量数据库 — 存储表示文本块的向量</mark>
- Documents are first indexed to a vector database | <mark>文档首先被索引到向量数据库</mark>

**Phase 2: Query** | <mark>**阶段 2：查询**</mark>

- LLM Chat | <mark>LLM 聊天</mark>
- (1) Retrieve | <mark>(1) 检索</mark>
- (2) Augment | <mark>(2) 增强</mark>
- (3) Generate | <mark>(3) 生成</mark>
- Query → Embedding — Query is embedded to represent a vector | <mark>查询 → 嵌入 — 查询被嵌入以表示向量</mark>
- Vector DB — Retrieval works by using vector similarity search | <mark>向量数据库 — 检索通过使用向量相似性搜索工作</mark>
- Context — Retrieved context semantically matches the query | <mark>上下文 — 检索的上下文在语义上与查询匹配</mark>
- Prompt (system: you are a ... Query, Context) | <mark>提示（system: 你是一个... 查询，上下文）</mark>
- LLM — LLM generates a response based on the contextualized prompt | <mark>LLM — LLM 基于上下文化的提示生成响应</mark>
- Response | <mark>响应</mark>
- Indexed documents can be queried/questioned by the user | <mark>用户可以查询/询问索引的文档</mark>

Unstructured memory/knowledge concepts rely on some format of text-similarity search following the retrieval pattern shown in figure 8.2. Figure 8.3 shows how memory uses the same embedding and vector database components. Rather than preload documents, conversations or parts of a conversation are embedded and saved to a vector database.

<mark>非结构化记忆/知识概念依赖于遵循图 8.2 中显示的检索模式的某种形式的文本相似性搜索。图 8.3 显示了记忆如何使用相同的嵌入和向量数据库组件。与其预加载文档，不如将对话或对话的部分嵌入并保存到向量数据库。</mark>

The retrieval pattern and document indexing are nuanced and require careful consideration to be employed successfully. This requires understanding how data is stored and retrieved, which we'll start to unfold in the next section.

<mark>检索模式和文档索引是细致入微的，需要仔细考虑才能成功应用。这需要理解如何存储和检索数据，我们将在下一节开始展开。</mark>

**Figure 8.3 Memory retrieval for augmented generation uses the same embedding patterns to index items to a vector database** | <mark>**图 8.3 用于增强生成的记忆检索使用相同的嵌入模式将项目索引到向量数据库**</mark>

<mark>*图片描述：记忆检索增强生成流程图*</mark>

**Memory Retrieval Augmented Generation** | <mark>**记忆检索增强生成**</mark>

**Chat with memory** | <mark>**带记忆的聊天**</mark>

- LLM Chat | <mark>LLM 聊天</mark>
- (1) Retrieve | <mark>(1) 检索</mark>
- (2) Augment | <mark>(2) 增强</mark>
- (3) Generate | <mark>(3) 生成</mark>
- (4) Remember | <mark>(4) 记住</mark>
- Query → Embedding — Query is embedded to represent a vector | <mark>查询 → 嵌入 — 查询被嵌入以表示向量</mark>
- Vector DB — Retrieval works by using vector similarity search | <mark>向量数据库 — 检索通过使用向量相似性搜索工作</mark>
- Memory — Retrieved memory semantically matches the query | <mark>记忆 — 检索的记忆在语义上与查询匹配</mark>
- Prompt (system: you are a ... Query, Memory) | <mark>提示（system: 你是一个... 查询，记忆）</mark>
- LLM — LLM generates a response based on the contextualized prompt | <mark>LLM — LLM 基于上下文化的提示生成响应</mark>
- Response | <mark>响应</mark>
- Generated Response → Embedding — All or parts of the conversation are embedded and added to the vector database | <mark>生成的响应 → 嵌入 — 对话的全部或部分被嵌入并添加到向量数据库</mark>
- Vector DB | <mark>向量数据库</mark>

---

## 8.3 Delving into semantic search and document indexing

<mark>## 8.3 深入研究语义搜索和文档索引</mark>

Document indexing transforms a document's information to be more easily recovered. How the index will be queried or searched also plays a factor, whether searching for a particular set of words or wanting to match phrase for phrase.

<mark>文档索引将文档的信息转换为更容易恢复的形式。索引如何被查询或搜索也起着作用，无论是搜索特定的一组单词还是想要逐短语匹配。</mark>

A semantic search is a search for content that matches the searched phrase by words and meaning. The ability to search by meaning, semantically, is potent and worth investigating in some detail. In the next section, we look at how vector similarity search can lay the framework for semantic search.

<mark>语义搜索是按单词和含义匹配搜索短语的内容的搜索。按含义（语义）搜索的能力非常强大，值得详细研究。在下一节中，我们将探讨向量相似性搜索如何为语义搜索奠定框架。</mark>

---

### 8.3.1 Applying vector similarity search

<mark>### 8.3.1 应用向量相似性搜索</mark>

Let's look now at how a document can be transformed into a semantic vector, or a representation of text that can then be used to perform distance or similarity matching. There are numerous ways to convert text into a semantic vector, so we'll look at a simple one.

<mark>现在让我们看看如何将文档转换为语义向量，或文本的表示，然后可以用于执行距离或相似性匹配。有许多方法可以将文本转换为语义向量，因此我们将看一个简单的方法。</mark>

Open the chapter_08 folder in a new Visual Studio Code (VS Code) workspace. Create a new environment and pip install the requirements.txt file for all the chapter dependencies. If you need help setting up a new Python environment, consult appendix B.

<mark>在新的 Visual Studio Code（VS Code）工作区中打开 chapter_08 文件夹。创建一个新环境并 pip 安装 requirements.txt 文件以获取所有章节依赖项。如果需要帮助设置新的 Python 环境，请参考附录 B。</mark>

Now open the document_vector_similarity.py file in VS Code, and review the top section in listing 8.1. This example uses Term Frequency–Inverse Document Frequency (TF–IDF). This numerical statistic reflects how important a word is to a document in a collection or set of documents by increasing proportionally to the number of times a word appears in the document and offset by the frequency of the word in the document set. TF–IDF is a classic measure of understanding one document's importance within a set of documents.

<mark>现在在 VS Code 中打开 document_vector_similarity.py 文件，并查看列表 8.1 中的顶部部分。此示例使用词频-逆文档频率（TF-IDF）。这个数字统计反映了一个单词对文档集合或文档集中的文档有多重要，它与单词在文档中出现的次数成正比增加，并由文档集中单词的频率抵消。TF-IDF 是理解一个文档在一组文档中的重要性的经典度量。</mark>

**Listing 8.1 document_vector_similarity (transform to vector)** | <mark>**列表 8.1 document_vector_similarity（转换为向量）**</mark>

```python
import plotly.graph_objects as go
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

documents = [     # Samples of documents
    "The sky is blue and beautiful.",
    "Love this blue and beautiful sky!",
    "The quick brown fox jumps over the lazy dog.",
    "A king's breakfast has sausages, ham, bacon, eggs, toast, and beans",
    "I love green eggs, ham, sausages and bacon!",
    "The brown fox is quick and the blue dog is lazy!",
    "The sky is very blue and the sky is very beautiful today",
    "The dog is lazy but the brown fox is quick!"
]

vectorizer = TfidfVectorizer()    # Vectorization using TF–IDF
X = vectorizer.fit_transform(documents)     # Vectorize the documents.
```

<mark>```python
import plotly.graph_objects as go
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

documents = [     # 文档样本
    "The sky is blue and beautiful.",
    "Love this blue and beautiful sky!",
    "The quick brown fox jumps over the lazy dog.",
    "A king's breakfast has sausages, ham, bacon, eggs, toast, and beans",
    "I love green eggs, ham, sausages and bacon!",
    "The brown fox is quick and the blue dog is lazy!",
    "The sky is very blue and the sky is very beautiful today",
    "The dog is lazy but the brown fox is quick!"
]

vectorizer = TfidfVectorizer()    # 使用 TF-IDF 进行向量化
X = vectorizer.fit_transform(documents)     # 向量化文档。
```</mark>

Let's break down TF–IDF into its two components using the sample sentence, "The sky is blue and beautiful," and focusing on the word blue.

<mark>让我们使用示例句子"The sky is blue and beautiful"将 TF-IDF 分解为两个组成部分，并专注于单词 blue。</mark>

**TERM FREQUENCY (TF)** | <mark>**词频（TF）**</mark>

Term Frequency measures how frequently a term occurs in a document. Because we're considering only a single document (our sample sentence), the simplest form of the TF for blue can be calculated as the number of times blue appears in the document divided by the total number of words in the document. Let's calculate it:

<mark>词频衡量一个词在文档中出现的频率。因为我们只考虑一个文档（我们的示例句子），blue 的 TF 的最简单形式可以计算为 blue 在文档中出现的次数除以文档中的总单词数。让我们计算一下：</mark>

- Number of times blue appears in the document: 1 | <mark>blue 在文档中出现的次数：1</mark>
- Total number of words in the document: 6 | <mark>文档中的总单词数：6</mark>
- TF = 1 ÷ 6 = 0.16 | <mark>TF = 1 ÷ 6 = 0.16</mark>

**INVERSE DOCUMENT FREQUENCY (IDF)** | <mark>**逆文档频率（IDF）**</mark>

Inverse Document Frequency measures how important a term is within the entire corpus. It's calculated by dividing the total number of documents by the number of documents containing the term and then taking the logarithm of that quotient:

<mark>逆文档频率衡量一个词在整个语料库中有多重要。它通过将文档总数除以包含该词的文档数，然后取该商的对数来计算：</mark>

IDF = log(Total number of documents ÷ Number of documents containing the word)

<mark>IDF = log（文档总数 ÷ 包含该词的文档数）</mark>

In this example, the corpus is a small collection of eight documents, and blue appears in four of these documents.

<mark>在此示例中，语料库是八个文档的小集合，blue 出现在其中四个文档中。</mark>

IDF = log(8 ÷ 4)

**TF–IDF CALCULATION** | <mark>**TF-IDF 计算**</mark>

Finally, the TF–IDF score for blue in our sample sentence is calculated by multiplying the TF and the IDF scores:

<mark>最后，我们示例句子中 blue 的 TF-IDF 分数通过将 TF 和 IDF 分数相乘来计算：</mark>

TF–IDF = TF × IDF

Let's compute the actual values for TF–IDF for the word blue using the example provided; first, the term frequency (how often the word occurs in the document) is computed as follows:

<mark>让我们使用提供的示例计算单词 blue 的 TF-IDF 的实际值；首先，词频（单词在文档中出现的频率）计算如下：</mark>

TF = 1 ÷ 6

Assuming the base of the logarithm is 10 (commonly used), the inverse document frequency is computed as follows:

<mark>假设对数的底数是 10（常用），逆文档频率计算如下：</mark>

IDF = log₁₀(8 ÷ 4)

Now let's calculate the exact TF–IDF value for the word blue in the sentence, "The sky is blue and beautiful":

<mark>现在让我们计算句子"The sky is blue and beautiful"中单词 blue 的确切 TF-IDF 值：</mark>

- The Term Frequency (TF) is approximately 0.1670 | <mark>词频（TF）约为 0.1670</mark>
- The Inverse Document Frequency (IDF) is approximately 0.301 | <mark>逆文档频率（IDF）约为 0.301</mark>
- Thus, the TF–IDF (TF × IDF) score for blue is approximately 0.050 | <mark>因此，blue 的 TF-IDF（TF × IDF）分数约为 0.050</mark>

This TF–IDF score indicates the relative importance of the word blue in the given document (the sample sentence) within the context of the specified corpus (eight documents, with blue appearing in four of them). Higher TF–IDF scores imply greater importance.

<mark>这个 TF-IDF 分数表示单词 blue 在给定文档（示例句子）中在指定语料库（八个文档，blue 出现在其中四个）的上下文中的相对重要性。更高的 TF-IDF 分数意味着更大的重要性。</mark>

We use TF–IDF here because it's simple to apply and understand. Now that we have the elements represented as vectors, we can measure document similarity using cosine similarity. Cosine similarity is a measure used to calculate the cosine of the angle between two nonzero vectors in a multidimensional space, indicating how similar they are, irrespective of their size.

<mark>我们在这里使用 TF-IDF 是因为它易于应用和理解。现在我们已经将元素表示为向量，我们可以使用余弦相似度来衡量文档相似性。余弦相似度是用于计算多维空间中两个非零向量之间角度的余弦的度量，表示它们有多相似，与它们的大小无关。</mark>

Figure 8.4 shows how cosine distance compares the vector representations of two pieces or documents of text. Cosine similarity returns a value from –1 (not similar) to 1 (identical). Cosine distance is a normalized value ranging from 0 to 2, derived by taking 1 minus the cosine similarity. A cosine distance of 0 means identical items, and 2 indicates complete opposites.

<mark>图 8.4 显示了余弦距离如何比较两段或文档文本的向量表示。余弦相似度返回从 -1（不相似）到 1（相同）的值。余弦距离是一个归一化值，范围从 0 到 2，通过取 1 减去余弦相似度得出。余弦距离为 0 表示相同的项目，2 表示完全相反。</mark>

**Figure 8.4 How cosine similarity is measured** | <mark>**图 8.4 如何测量余弦相似度**</mark>

<mark>*图片描述：余弦相似度测量示意图*</mark>

**Cosine Similarity** | <mark>**余弦相似度**</mark>

- The angle or distance is a measure of how close the vectors are in space. It also represents their similarity to each other. | <mark>角度或距离是向量在空间中有多接近的度量。它也代表它们彼此的相似性。</mark>
- Cosine Distance θ | <mark>余弦距离 θ</mark>
- The sky is blue and beautiful. | <mark>天空是蓝色和美丽的。</mark>
- Love this blue and beautiful sky! | <mark>喜欢这片蓝色和美丽的天空！</mark>
- Vector representations of the text rendered in 2D and in reality vectors can be highly dimensional. | <mark>文本的向量表示在 2D 中渲染，实际上向量可以是高维的。</mark>

Listing 8.2 shows how the cosine similarities are computed using the cosine_similarity function from scikit-learn. Similarities are calculated for each document against all other documents in the set. The computed matrix of similarities for documents is stored in the cosine_similarities variable. Then, in the input loop, the user can select the document to view its similarities to the other documents.

<mark>列表 8.2 显示了如何使用 scikit-learn 的 cosine_similarity 函数计算余弦相似度。为集合中的每个文档与所有其他文档计算相似度。文档的计算相似度矩阵存储在 cosine_similarities 变量中。然后，在输入循环中，用户可以选择文档以查看其与其他文档的相似性。</mark>

**Listing 8.2 document_vector_similarity (cosine similarity)** | <mark>**列表 8.2 document_vector_similarity（余弦相似度）**</mark>

```python
cosine_similarities = cosine_similarity(X)     # Computes the document similarities for all vector pairs

while True:     # The main input loop
    selected_document_index = input(f"Enter a document number (0-{len(documents)-1}) or 'exit' to quit: ").strip()
    if selected_document_index.lower() == 'exit':
        break
    if not selected_document_index.isdigit() or not 0 <= int(selected_document_index) < len(documents):
        print("Invalid input. Please enter a valid document number.")
        continue
    selected_document_index = int(selected_document_index)   # Gets the selected document index to compare with
    selected_document_similarities = cosine_similarities[selected_document_index]    # Extracts the computed similarities against all documents
# code to plot document similarities omitted
```

<mark>```python
cosine_similarities = cosine_similarity(X)     # 计算所有向量对的文档相似度

while True:     # 主输入循环
    selected_document_index = input(f"Enter a document number (0-{len(documents)-1}) or 'exit' to quit: ").strip()
    if selected_document_index.lower() == 'exit':
        break
    if not selected_document_index.isdigit() or not 0 <= int(selected_document_index) < len(documents):
        print("Invalid input. Please enter a valid document number.")
        continue
    selected_document_index = int(selected_document_index)   # 获取要比较的选定文档索引
    selected_document_similarities = cosine_similarities[selected_document_index]    # 提取针对所有文档的计算相似度
# 绘制文档相似度的代码省略
```</mark>

Figure 8.5 shows the output of running the sample in VS Code (F5 for debugging mode). After you select a document, you'll see the similarities between the various documents in the set. A document will have a cosine similarity of 1 with itself. Note that you won't see a negative similarity because of the TF–IDF vectorization. We'll look later at other, more sophisticated means of measuring semantic similarity.

<mark>图 8.5 显示了在 VS Code 中运行示例的输出（F5 用于调试模式）。选择文档后，你将看到集合中各种文档之间的相似性。文档与其自身的余弦相似度为 1。请注意，由于 TF-IDF 向量化，你不会看到负相似度。我们稍后将探讨其他更复杂的测量语义相似性的方法。</mark>

**Figure 8.5 The cosine similarity between selected documents and the document set** | <mark>**图 8.5 选定文档与文档集之间的余弦相似度**</mark>

<mark>*图片描述：显示余弦相似度的条形图*</mark>

- The select document is compared against all other documents to show similarity measure between document vectors. | <mark>选定的文档与所有其他文档进行比较，以显示文档向量之间的相似性度量。</mark>
- Cosine Similarities of "The sky is blue and beautiful." with Others | <mark>"The sky is blue and beautiful."与其他文档的余弦相似度</mark>

The method of vectorization will dictate the measure of semantic similarity between documents. Before we move on to better methods of vectorizing documents, we'll examine storing vectors to perform vector similarity searches.

<mark>向量化方法将决定文档之间语义相似性的度量。在我们转向更好的文档向量化方法之前，我们将探讨存储向量以执行向量相似性搜索。</mark>

---

### 8.3.2 Vector databases and similarity search

<mark>### 8.3.2 向量数据库和相似性搜索</mark>

After vectorizing documents, they can be stored in a vector database for later similarity searches. To demonstrate how this works, we can efficiently replicate a simple vector database in Python code.

<mark>向量化文档后，它们可以存储在向量数据库中以供以后进行相似性搜索。为了演示这是如何工作的，我们可以在 Python 代码中有效地复制一个简单的向量数据库。</mark>

Open document_vector_database.py in VS Code, as shown in listing 8.3. This code demonstrates creating a vector database in memory and then allowing users to enter text to search the database and return results. The results returned show the document text and the similarity score.

<mark>在 VS Code 中打开 document_vector_database.py，如列表 8.3 所示。此代码演示了在内存中创建向量数据库，然后允许用户输入文本以搜索数据库并返回结果。返回的结果显示文档文本和相似度分数。</mark>

**Listing 8.3 document_vector_database.py** | <mark>**列表 8.3 document_vector_database.py**</mark>

```python
# code above omitted
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(documents)
vector_database = X.toarray()    # Stores the document vectors into an array

def cosine_similarity_search(query,
                             database,
                             vectorizer,
                             top_n=5):    # The function to perform similarity matching on query returns, matches, and similarity scores
    query_vec = vectorizer.transform([query]).toarray()
    similarities = cosine_similarity(query_vec, database)[0]
    top_indices = np.argsort(-similarities)[:top_n]  # Top n indices
    return [(idx, similarities[idx]) for idx in top_indices]

while True:     # The main input loop
    query = input("Enter a search query (or 'exit' to stop): ")
    if query.lower() == 'exit':
        break
    top_n = int(input("How many top matches do you want to see? "))
    search_results = cosine_similarity_search(query,
                                              vector_database,
                                              vectorizer,
                                              top_n)
    print("Top Matched Documents:")
    for idx, score in search_results:
        print(f"- {documents[idx]} (Score: {score:.4f})")  # Loops through results and outputs text and similarity score
    print("\n")

###Output
Enter a search query (or 'exit' to stop): blue
How many top matches do you want to see? 3
Top Matched Documents:
- The sky is blue and beautiful. (Score: 0.4080)
- Love this blue and beautiful sky! (Score: 0.3439)
- The brown fox is quick and the blue dog is lazy! (Score: 0.2560)
```

<mark>```python
# 上面的代码省略
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(documents)
vector_database = X.toarray()    # 将文档向量存储到数组中

def cosine_similarity_search(query,
                             database,
                             vectorizer,
                             top_n=5):    # 执行相似性匹配的函数返回查询、匹配和相似度分数
    query_vec = vectorizer.transform([query]).toarray()
    similarities = cosine_similarity(query_vec, database)[0]
    top_indices = np.argsort(-similarities)[:top_n]  # Top n 索引
    return [(idx, similarities[idx]) for idx in top_indices]

while True:     # 主输入循环
    query = input("Enter a search query (or 'exit' to stop): ")
    if query.lower() == 'exit':
        break
    top_n = int(input("How many top matches do you want to see? "))
    search_results = cosine_similarity_search(query,
                                              vector_database,
                                              vectorizer,
                                              top_n)
    print("Top Matched Documents:")
    for idx, score in search_results:
        print(f"- {documents[idx]} (Score: {score:.4f})")  # 循环遍历结果并输出文本和相似度分数
    print("\n")

###输出
Enter a search query (or 'exit' to stop): blue
How many top matches do you want to see? 3
Top Matched Documents:
- The sky is blue and beautiful. (Score: 0.4080)
- Love this blue and beautiful sky! (Score: 0.3439)
- The brown fox is quick and the blue dog is lazy! (Score: 0.2560)
```</mark>

Run this exercise to see the output (F5 in VS Code). Enter any text you like, and see the results of documents being returned. This search form works well for matching words and phrases with similar words and phrases. This form of search misses the word context and meaning from the document. In the next section, we'll look at a way of transforming documents into vectors that better preserves their semantic meaning.

<mark>运行此练习以查看输出（在 VS Code 中按 F5）。输入任何你喜欢的文本，并查看返回的文档结果。这种搜索形式适用于将单词和短语与相似的单词和短语进行匹配。这种搜索形式忽略了文档中的单词上下文和含义。在下一节中，我们将探讨一种将文档转换为向量的方法，该方法更好地保留其语义含义。</mark>

---

### 8.3.3 Demystifying document embeddings

<mark>### 8.3.3 揭秘文档嵌入</mark>

TF–IDF is a simple form that tries to capture semantic meaning in documents. However, it's unreliable because it only counts word frequency and doesn't understand the relationships between words. A better and more modern method uses document embedding, a form of document vectorizing that better preserves the semantic meaning of the document.

<mark>TF-IDF 是一种简单的形式，试图捕获文档中的语义含义。然而，它是不可靠的，因为它只计算单词频率，并不理解单词之间的关系。更好和更现代的方法使用文档嵌入，这是一种更好地保留文档语义含义的文档向量化形式。</mark>

Embedding networks are constructed by training neural networks on large datasets to map words, sentences, or documents to high-dimensional vectors, capturing semantic and syntactic relationships based on context and relationships in the data. You typically use a pretrained model trained on massive datasets to embed documents and perform embeddings. Models are available from many sources, including Hugging Face and, of course, OpenAI.

<mark>嵌入网络是通过在大型数据集上训练神经网络来构建的，将单词、句子或文档映射到高维向量，基于数据中的上下文和关系捕获语义和句法关系。你通常使用在大型数据集上训练的预训练模型来嵌入文档并执行嵌入。模型可从许多来源获得，包括 Hugging Face，当然还有 OpenAI。</mark>

In our next scenario, we'll use an OpenAI embedding model. These models are typically perfect for capturing the semantic context of embedded documents. Listing 8.4 shows the relevant code that uses OpenAI to embed the documents into vectors that are then reduced to three dimensions and rendered into a plot.

<mark>在我们的下一个场景中，我们将使用 OpenAI 嵌入模型。这些模型通常非常适合捕获嵌入文档的语义上下文。列表 8.4 显示了使用 OpenAI 将文档嵌入到向量中的相关代码，然后将这些向量减少到三个维度并渲染到图中。</mark>

**Listing 8.4 document_visualizing_embeddings.py (relevant sections)** | <mark>**列表 8.4 document_visualizing_embeddings.py（相关部分）**</mark>

```python
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("No API key found. Please check your .env file.")

client = OpenAI(api_key=api_key)

def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text],
              model=model).data[0].embedding                # Uses the OpenAI client to create the embedding

# Sample documents (omitted)

embeddings = [get_embedding(doc) for doc in documents]   # Generates embeddings for each document of size 1536 dimensions
print(embeddings_array.shape)

embeddings_array = np.array(embeddings)   # Converts embeddings to a NumPy array for PCA

pca = PCA(n_components=3)  # Applies PCA to reduce dimensions to 3 for plotting
reduced_embeddings = pca.fit_transform(embeddings_array)
```

<mark>```python
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("No API key found. Please check your .env file.")

client = OpenAI(api_key=api_key)

def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text],
              model=model).data[0].embedding                # 使用 OpenAI 客户端创建嵌入

# 示例文档（省略）

embeddings = [get_embedding(doc) for doc in documents]   # 为每个文档生成 1536 维的嵌入
print(embeddings_array.shape)

embeddings_array = np.array(embeddings)   # 将嵌入转换为 NumPy 数组以用于 PCA

pca = PCA(n_components=3)  # 应用 PCA 将维度减少到 3 以用于绘图
reduced_embeddings = pca.fit_transform(embeddings_array)
```</mark>

When a document is embedded using an OpenAI model, it transforms the text into a vector with dimensions of 1536. We can't visualize this number of dimensions, so we use a dimensionality reduction technique via principal component analysis (PCA) to convert the vector of size 1536 to 3 dimensions.

<mark>当使用 OpenAI 模型嵌入文档时，它将文本转换为具有 1536 个维度的向量。我们无法可视化这么多维度，因此我们使用通过主成分分析（PCA）的降维技术将大小为 1536 的向量转换为 3 个维度。</mark>

Figure 8.6 shows the output generated from running the file in VS Code. By reducing the embeddings to 3D, we can plot the output to show how semantically similar documents are now grouped.

<mark>图 8.6 显示了在 VS Code 中运行文件生成的输出。通过将嵌入减少到 3D，我们可以绘制输出以显示语义相似的文档现在如何分组。</mark>

**Figure 8.6 Embeddings in 3D, showing how similar semantic documents are grouped** | <mark>**图 8.6 3D 嵌入，显示相似语义文档如何分组**</mark>

<mark>*图片描述：3D 嵌入可视化图*</mark>

- Documents are projected to 3D based on their semantic meaning | <mark>文档基于其语义含义投影到 3D</mark>
- Similar documents are now similar in meaning and are shown grouped together | <mark>相似的文档现在在含义上相似，并显示为一组</mark>

The choice of which embedding model or service you use is up to you. The OpenAI embedding models are considered the best for general semantic similarity. This has made these models the standard for most memory and retrieval applications. With our understanding of how text can be vectorized with embeddings and stored in a vector database, we can move on to a more realistic example in the next section.

<mark>选择使用哪个嵌入模型或服务取决于你。OpenAI 嵌入模型被认为是通用语义相似性的最佳选择。这使得这些模型成为大多数记忆和检索应用的标准。通过我们对如何使用嵌入将文本向量化并存储在向量数据库中的理解，我们可以在下一节中转向更现实的示例。</mark>

---

### 8.3.4 Querying document embeddings from Chroma

<mark>### 8.3.4 从 Chroma 查询文档嵌入</mark>

We can combine all the pieces and look at a complete example using a local vector database called Chroma DB. Many vector database options exist, but Chroma DB is an excellent local vector store for development or small-scale projects. There are also plenty of more robust options that you can consider later.

<mark>我们可以组合所有部分，并使用名为 Chroma DB 的本地向量数据库查看完整示例。存在许多向量数据库选项，但 Chroma DB 是开发或小规模项目的出色本地向量存储。稍后你还可以考虑许多更强大的选项。</mark>

Listing 8.5 shows the new and relevant code sections from the document_query_chromadb.py file. Note that the results are scored by distance and not by similarity. Cosine distance is determined by this equation:

<mark>列表 8.5 显示了 document_query_chromadb.py 文件中的新相关代码部分。请注意，结果按距离而非相似度评分。余弦距离由此方程确定：</mark>

Cosine Distance(A,B) = 1 – Cosine Similarity(A,B)

This means that cosine distance will range from 0 for most similar to 2 for semantically opposite in meaning.

<mark>这意味着余弦距离的范围从最相似的 0 到语义上完全相反的 2。</mark>

**Listing 8.5 document_query_chromadb.py (relevant code sections)** | <mark>**列表 8.5 document_query_chromadb.py（相关代码部分）**</mark>

```python
embeddings = [get_embedding(doc) for doc in documents]    # Generates embeddings for each document and assigns an ID
ids = [f"id{i}" for i in range(len(documents))]

chroma_client = chromadb.Client()              # Creates a Chroma DB client and a collection
collection = chroma_client.create_collection(
                       name="documents")

collection.add(    # Adds document embeddings to the collection
    embeddings=embeddings,
    documents=documents,
    ids=ids
)

def query_chromadb(query, top_n=2):     # Queries the datastore and returns the top n relevant documents
    query_embedding = get_embedding(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_n
    )
    return [(id, score, text) for id, score, text in
            zip(results['ids'][0],
                results['distances'][0],
                results['documents'][0])]

while True:    # The input loop for user input and output of relevant documents/scores
    query = input("Enter a search query (or 'exit' to stop): ")
    if query.lower() == 'exit':
        break
    top_n = int(input("How many top matches do you want to see? "))
    search_results = query_chromadb(query, top_n)
    print("Top Matched Documents:")
    for id, score, text in search_results:
        print(f"""
ID:{id} TEXT: {text} SCORE: {round(score, 2)}
""")
    print("\n")

###Output
Enter a search query (or 'exit' to stop): dogs are lazy
How many top matches do you want to see? 3
Top Matched Documents:
ID:id7 TEXT: The dog is lazy but the brown fox is quick! SCORE: 0.24
ID:id5 TEXT: The brown fox is quick and the blue dog is lazy! SCORE: 0.28
ID:id2 TEXT: The quick brown fox jumps over the lazy dog. SCORE: 0.29
```

<mark>```python
embeddings = [get_embedding(doc) for doc in documents]    # 为每个文档生成嵌入并分配 ID
ids = [f"id{i}" for i in range(len(documents))]

chroma_client = chromadb.Client()              # 创建 Chroma DB 客户端和集合
collection = chroma_client.create_collection(
                       name="documents")

collection.add(    # 将文档嵌入添加到集合
    embeddings=embeddings,
    documents=documents,
    ids=ids
)

def query_chromadb(query, top_n=2):     # 查询数据存储并返回前 n 个相关文档
    query_embedding = get_embedding(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_n
    )
    return [(id, score, text) for id, score, text in
            zip(results['ids'][0],
                results['distances'][0],
                results['documents'][0])]

while True:    # 用户输入和相关文档/分数输出的输入循环
    query = input("Enter a search query (or 'exit' to stop): ")
    if query.lower() == 'exit':
        break
    top_n = int(input("How many top matches do you want to see? "))
    search_results = query_chromadb(query, top_n)
    print("Top Matched Documents:")
    for id, score, text in search_results:
        print(f"""
ID:{id} TEXT: {text} SCORE: {round(score, 2)}
""")
    print("\n")

###输出
Enter a search query (or 'exit' to stop): dogs are lazy
How many top matches do you want to see? 3
Top Matched Documents:
ID:id7 TEXT: The dog is lazy but the brown fox is quick! SCORE: 0.24
ID:id5 TEXT: The brown fox is quick and the blue dog is lazy! SCORE: 0.28
ID:id2 TEXT: The quick brown fox jumps over the lazy dog. SCORE: 0.29
```</mark>

As the earlier scenario demonstrated, you can now query the documents using semantic meaning rather than just key terms or phrases. These scenarios should now provide the background to see how the retrieval pattern works at a low level. In the next section, we'll see how the retrieval pattern can be employed using LangChain.

<mark>如前面的场景所示，你现在可以使用语义含义而不仅仅是关键词或短语来查询文档。这些场景现在应该提供了背景，以了解检索模式如何在低级别工作。在下一节中，我们将看到如何使用 LangChain 采用检索模式。</mark>

---

由于内容很长，我将继续在下一个消息中完成第8章的剩余部分翻译。