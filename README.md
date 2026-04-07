<div align="center">

<img src="https://p-mira-img-sign-sgnontt.byteintl.net/tos-mya-i-xobrcjvdq7/a4e1062c41d341c48e793da47dfd090e.jpg~tplv-xobrcjvdq7-image-jpeg.jpeg?lk3s=3523e930&x-orig-authkey=miraorigin&x-orig-expires=1776171600&x-orig-sign=5Sch%2F%2BRC5QiJxmPvydMPAGYpTPc%3D" width="100%" alt="LLM Wiki KB Banner" style="max-width: 1280px; aspect-ratio: 16/9; object-fit: cover;">


# 🧠 LLM Wiki KB

**让 LLM 像人类专家一样，把零散知识编译成一部不断生长的百科全书**

**Let LLMs compile scattered knowledge into an ever-growing encyclopedia — just like a human expert would**

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.7+](https://img.shields.io/badge/Python-3.7+-green.svg)](https://python.org)
[![Tests](https://img.shields.io/badge/Tests-35%2F35%20Passing-brightgreen.svg)](#-testing)

</div>

---

## 💡 灵感来源 · Inspiration

2026 年 4 月，Andrej Karpathy 发布了一篇 [LLM Wiki Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)，提出了一个极具洞察力的观点：

> **RAG 每次都在重新推导答案，而 Wiki 把知识编译一次、复用无数次。**

他描述了一种三层架构：**原始素材 → LLM 编译的 Wiki → Schema 约定**，让 LLM 不再只是"检索-回答"的管道，而是成为一个持续积累知识的编纂者。这个想法本身就像一颗种子——Karpathy 有意将它设计为一份"可以直接粘贴到你自己 LLM Agent 里"的抽象描述。

**但种子需要土壤、阳光和水。**

---

In April 2026, Andrej Karpathy published an [LLM Wiki Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) with a brilliantly simple insight:

> **RAG re-derives answers every time. A Wiki compiles knowledge once and reuses it forever.**

He described a three-layer architecture: **Raw Sources → LLM-compiled Wiki → Schema Conventions** — turning LLMs from "retrieve-and-answer" pipelines into persistent knowledge curators. The idea was intentionally abstract — "designed to be copy pasted to your own LLM Agent."

**But a seed needs soil, sunlight, and water.**

---

## 🎯 为什么要做这个项目 · Why This Project

Karpathy 的 Gist 是一份**设计文档**，不是一个**可运行的系统**。它描述了"应该做什么"，但没有回答：

- 📥 **怎样把一篇网页变成 Wiki 原始素材？** 图片怎么办？格式怎么处理？
- 🔍 **怎样在几百个 Wiki 页面中高效搜索？** 纯文本 grep 够用吗？
- 🏥 **怎样保证 Wiki 的健康度？** 死链接、孤儿页面、缺失的 frontmatter？
- 🔌 **怎样让不同的 LLM Agent 平台都能用？** Claude Code、OpenCode、Mira 各有各的约定。
- 📐 **怎样规范 Wiki 页面的结构？** 实体页、概念页、对比页的模板从哪来？

**LLM Wiki KB 把 Karpathy 的蓝图变成了一套即插即用的工具链。**

---

Karpathy's Gist is a **design document**, not a **runnable system**. It describes *what* to do, but leaves open:

- 📥 **How do you actually turn a webpage into raw material?** What about images? Formatting?
- 🔍 **How do you search efficiently across hundreds of wiki pages?** Is plain grep enough?
- 🏥 **How do you keep the wiki healthy?** Broken links, orphan pages, missing frontmatter?
- 🔌 **How do you support different LLM agent platforms?** Claude Code, OpenCode, and Mira each have their own conventions.
- 📐 **How do you standardize page structures?** Where do templates for entity pages, concept pages, and comparison pages come from?

**LLM Wiki KB turns Karpathy's blueprint into a plug-and-play toolkit.**

---

## 🚀 超越原版的优化 · What We Built Beyond the Original

<table>
<tr>
<th width="200">维度 · Dimension</th>
<th width="300">Karpathy 原版 · Original</th>
<th width="300">LLM Wiki KB 优化 · Enhancement</th>
</tr>
<tr>
<td><b>🛠 实现程度</b><br>Implementation</td>
<td>抽象描述文档，无可执行代码<br><i>Abstract description, no executable code</i></td>
<td><b>5 个 Python CLI 工具</b>：init / ingest / query / search / lint，共 1200+ 行生产级代码<br><i><b>5 Python CLI tools</b>, 1200+ lines of production code</i></td>
</tr>
<tr>
<td><b>📥 素材获取</b><br>Ingestion</td>
<td>提及"ingest"概念<br><i>Mentions "ingest" concept</i></td>
<td><b>完整的 Web 抓取管线</b>：URL→Markdown 转换、图片本地化下载、批量目录导入、元数据提取<br><i><b>Full web scraping pipeline</b>: URL→Markdown, image localization, batch import, metadata extraction</i></td>
</tr>
<tr>
<td><b>🔍 搜索能力</b><br>Search</td>
<td>提及使用搜索<br><i>Mentions using search</i></td>
<td><b>3 级搜索回退</b>：qmd（混合 BM25 + 向量检索）→ index.md 解析 → grep 兜底，任何环境都能工作<br><i><b>3-tier search fallback</b>: qmd (hybrid BM25 + vector) → index.md → grep</i></td>
</tr>
<tr>
<td><b>📐 页面规范</b><br>Page Schema</td>
<td>提及 page types 概念<br><i>Mentions page types concept</i></td>
<td><b>5 种页面模板</b>（Source Summary / Entity / Concept / Comparison / Synthesis），每种含完整 YAML frontmatter schema<br><i><b>5 page templates</b> with full YAML frontmatter schemas</i></td>
</tr>
<tr>
<td><b>🏥 质量保障</b><br>Quality Assurance</td>
<td>提及 lint 概念<br><i>Mentions lint concept</i></td>
<td><b>6 项自动化健康检查</b>：死链接、孤儿页、缺失 frontmatter、不完整 frontmatter、缺失 index、index 不一致<br><i><b>6 automated health checks</b>: broken links, orphan pages, missing/incomplete frontmatter, index consistency</i></td>
</tr>
<tr>
<td><b>📊 输出格式</b><br>Output Formats</td>
<td>Markdown 输出<br><i>Markdown output</i></td>
<td><b>4 种输出格式</b>：Markdown / Marp 幻灯片 / Matplotlib 图表 / Obsidian Canvas<br><i><b>4 output formats</b>: Markdown / Marp slides / Charts / Canvas</i></td>
</tr>
<tr>
<td><b>🔌 平台适配</b><br>Platform Support</td>
<td>单一 Agent 使用<br><i>Single agent usage</i></td>
<td><b>3 套平台适配器</b>：Claude Code（CLAUDE.md）/ OpenCode（AGENTS.md）/ Mira（飞书导出）<br><i><b>3 platform adapters</b>: Claude Code / OpenCode / Mira</i></td>
</tr>
<tr>
<td><b>🧪 测试覆盖</b><br>Testing</td>
<td>无<br><i>None</i></td>
<td><b>35 项端到端测试</b>，覆盖 7 个模块，全部通过<br><i><b>35 end-to-end tests</b> across 7 modules, all passing</i></td>
</tr>
<tr>
<td><b>👁 可视化前端</b><br>Frontend</td>
<td>未指定<br><i>Not specified</i></td>
<td><b>Obsidian 深度集成</b>：热重载、Dataview 查询、Web Clipper、Marp 预览<br><i><b>Deep Obsidian integration</b>: hot-reload, Dataview queries, Web Clipper, Marp preview</i></td>
</tr>
</table>

---

## 🏗 架构 · Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Your LLM Agent                     │
│           (Claude Code / OpenCode / Mira)            │
├─────────────┬─────────────┬─────────────┬───────────┤
│   Ingest    │    Query    │    Lint     │  Search   │
│  wiki_      │  wiki_      │  wiki_      │  wiki_    │
│  ingest.py  │  query.py   │  lint.py    │  search.py│
├─────────────┴─────────────┴─────────────┴───────────┤
│                  SKILL.md (Core Schema)              │
├─────────────────────────────────────────────────────┤
│                    Obsidian Vault                     │
│  ┌──────┐  ┌──────────┐  ┌──────────────────────┐  │
│  │ raw/ │→ │  wiki/    │→ │ output/ (md/marp/…)  │  │
│  │      │  │ index.md  │  │                      │  │
│  │      │  │ log.md    │  │                      │  │
│  └──────┘  └──────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

**三层数据流 · Three-Layer Data Flow:**

1. **Raw（原始素材）** — URL 或本地文件经 `wiki_ingest.py` 转为 Markdown，存入 `raw/`
2. **Wiki（知识编译）** — LLM 阅读原始素材，按模板编写 Wiki 页面，存入 `wiki/`，更新 `index.md` 和 `log.md`
3. **Output（输出制品）** — `wiki_query.py` 生成 Markdown、幻灯片、图表或 Canvas

---

## 📖 分平台使用指南 · Step-by-Step Usage by Platform

> 以下指南假设你已经 `git clone` 了本仓库。下文用 `<skill-path>` 指代 clone 下来的 `llm-wiki-kb/` 目录。
>
> The guides below assume you've cloned this repo. `<skill-path>` refers to the cloned `llm-wiki-kb/` directory.

---

### 🟣 Claude Code

Claude Code 是目前与本 Skill 最自然的搭配——它原生读取 `CLAUDE.md`，能直接读写本地文件系统，且可运行 Python 脚本。

Claude Code is the most natural pairing — it natively reads `CLAUDE.md`, has direct filesystem access, and runs Python scripts.

#### Step 1: Clone 并设置环境变量 · Clone & Set Env

```bash
git clone https://github.com/chengjialu8888/LLM-Wiki-KB.git
cd LLM-Wiki-KB

# 设置你的 Obsidian vault 路径（也可以新建一个）
export WIKI_VAULT=~/obsidian-vaults/my-research
```

#### Step 2: 初始化 Wiki · Initialize

```bash
python scripts/wiki_init.py $WIKI_VAULT --domain "你的研究领域"
```

这会在 `$WIKI_VAULT` 下创建完整的目录结构和 `SCHEMA.md`。

#### Step 3: 部署 Schema 到 Claude Code · Deploy Schema

```bash
# 将 schema 复制为 CLAUDE.md（Claude Code 自动读取此文件作为项目上下文）
cp $WIKI_VAULT/SCHEMA.md $WIKI_VAULT/CLAUDE.md
```

#### Step 4:（可选）配置 qmd 搜索引擎 · Optional: Configure qmd Search

如果你安装了 [qmd](https://github.com/tobi/qmd)，可以配置为 MCP 工具获得更强的混合搜索能力：

```bash
# 安装 qmd
go install github.com/tobi/qmd@latest

# 在项目根目录创建 .mcp.json
cat > $WIKI_VAULT/.mcp.json << 'EOF'
{
  "mcpServers": {
    "qmd": {
      "command": "qmd",
      "args": ["serve", "--dir", "wiki/"]
    }
  }
}
EOF
```

没有 qmd 也完全没问题——系统会自动回退到 index.md 解析 + grep 搜索。

#### Step 5: 在 Claude Code 中使用 · Start Using

打开 Claude Code，进入 vault 目录，然后直接用自然语言指挥：

```bash
cd $WIKI_VAULT
claude  # 启动 Claude Code
```

**导入素材：**
```
> 把这篇文章加入我的知识库：https://lilianweng.github.io/posts/2023-06-23-agent/
```

**查询知识：**
```
> 我的知识库里关于 LLM Agent 架构有哪些研究？帮我做一个综合分析
```

**生成幻灯片：**
```
> 把 scaling laws 的相关内容整理成一份 Marp 幻灯片
```

**健康检查：**
```
> 检查一下 wiki 有没有死链接或孤儿页面
```

Claude Code 会自动阅读 `CLAUDE.md`，理解整个 wiki 的约定，执行相应的 Python 脚本，并维护 `index.md`、`log.md` 和 `[[wikilinks]]`。

---

### 🟢 OpenCode / Codex / 其他 OpenAI 系 Agent

OpenCode 和 Codex 使用 `AGENTS.md` 作为项目指令文件，工作流与 Claude Code 类似。

OpenCode and Codex use `AGENTS.md` as the project instruction file. The workflow is similar to Claude Code.

#### Step 1: Clone 并设置环境 · Clone & Setup

```bash
git clone https://github.com/chengjialu8888/LLM-Wiki-KB.git
cd LLM-Wiki-KB
export WIKI_VAULT=~/obsidian-vaults/my-research
```

#### Step 2: 初始化并部署 Schema · Initialize & Deploy

```bash
python scripts/wiki_init.py $WIKI_VAULT --domain "你的研究领域"

# 复制为 AGENTS.md（OpenCode/Codex 自动读取）
cp $WIKI_VAULT/SCHEMA.md $WIKI_VAULT/AGENTS.md
```

#### Step 3: 注册工具 · Register Tools

在你的 Agent 配置中注册 wiki 工具（具体格式取决于你的平台）：

```yaml
# 示例：工具注册配置
tools:
  - name: wiki_init
    command: python <skill-path>/scripts/wiki_init.py --vault $WIKI_VAULT
  - name: wiki_ingest
    command: python <skill-path>/scripts/wiki_ingest.py --vault $WIKI_VAULT
  - name: wiki_query
    command: python <skill-path>/scripts/wiki_query.py --vault $WIKI_VAULT
  - name: wiki_search
    command: python <skill-path>/scripts/wiki_search.py --vault $WIKI_VAULT
  - name: wiki_lint
    command: python <skill-path>/scripts/wiki_lint.py --vault $WIKI_VAULT
```

#### Step 4: 开始使用 · Start Using

```
> Ingest this paper into my KB: https://arxiv.org/abs/2305.10601
> What connections exist between RLHF and constitutional AI in my wiki?
> Run lint and fix any issues
```

Agent 会读取 `AGENTS.md`，按照 wiki 约定执行操作。

---

### 🔵 Mira（字节跳动 AI 助手）

Mira 运行在沙盒环境中，操作方式与本地 Agent 略有不同，但核心流程一致。额外的优势是可以直接导出到飞书文档。

Mira runs in a sandboxed environment. The core workflow is the same, with the bonus of Feishu doc export.

#### Step 1: 让 Mira 初始化知识库 · Ask Mira to Initialize

直接对 Mira 说：

```
帮我初始化一个知识库，主题是"AI Agent 研究"
```

Mira 会在沙盒的 `workspace/` 中运行 `wiki_init.py`。

> **持久化提示**：如果你希望知识库跨对话保留，让 Mira 把 vault 建在 `userdata/` 目录下：
> ```
> 帮我在 userdata 目录下初始化一个持久的知识库
> ```

#### Step 2: 导入素材 · Ingest Sources

```
把这篇文章加入我的知识库：https://lilianweng.github.io/posts/2023-06-23-agent/
```

Mira 会用内置的 `web_builtin_fetch` 工具抓取网页，通过 `wiki_ingest.py` 转为 Markdown，然后自动编译为 Wiki 页面。

你也可以批量导入：
```
把这三篇文章都加入知识库：
1. https://example.com/paper-1
2. https://example.com/paper-2
3. https://example.com/paper-3
```

#### Step 3: 查询和分析 · Query & Analyze

```
根据我的知识库，对比一下 RAG 和 Fine-tuning 的优劣势
```

```
用我知识库里的内容，生成一份关于 Transformer 架构演进的 Marp 幻灯片
```

#### Step 4: 导出到飞书 · Export to Feishu

Mira 独有的能力——把 wiki 内容导出为飞书文档，方便分享给团队：

```
把我知识库中关于 scaling laws 的综合分析导出到飞书文档
```

#### Step 5: 健康检查 · Health Check

```
检查一下我的知识库有没有问题，如果有就修复
```

#### Mira 特别注意事项 · Mira-Specific Notes

| 事项 | 说明 |
|------|------|
| **Obsidian 查看** | 沙盒内无法直接用 Obsidian 打开。可下载 vault 文件到本地，或导出飞书文档查看 |
| **搜索** | qmd 在沙盒中不可用，系统自动用 grep 回退搜索，对中小型 wiki 完全够用 |
| **持久化** | `workspace/` 仅当次会话有效；使用 `userdata/` 目录可跨对话保留 |
| **网络访问** | 通过 Mira 内置的 `web_builtin_fetch` 抓取网页，不受沙盒网络限制 |

---

### 🟡 其他 AI 助手 · Other AI Assistants

如果你使用的是 Cursor、Windsurf、Aider 或其他带有文件系统访问能力的 AI 助手，通用步骤如下：

If you use Cursor, Windsurf, Aider, or any AI assistant with filesystem access:

#### 通用 3 步上手 · Universal 3-Step Setup

**① 初始化 vault：**
```bash
git clone https://github.com/chengjialu8888/LLM-Wiki-KB.git
python LLM-Wiki-KB/scripts/wiki_init.py ~/my-wiki --domain "My Research"
```

**② 让 AI 读取 SKILL.md：**

把 `SKILL.md` 的内容粘贴到你的 AI 助手的系统 prompt、项目说明、或指令文件中。这是 LLM 理解整个 wiki 运作方式的核心文件。

Paste the content of `SKILL.md` into your AI assistant's system prompt, project instructions, or instruction file. This is the core file that tells the LLM how the wiki works.

**③ 开始对话：**
```
I've set up a wiki KB at ~/my-wiki. Please read the SKILL.md and help me ingest this article: <URL>
```

你的 AI 助手只要能运行 Python 和读写文件，就能驱动整个 wiki 工作流。`SKILL.md` 里包含了所有它需要知道的约定。

Any AI assistant that can run Python and read/write files can drive the entire wiki workflow. `SKILL.md` contains everything it needs to know.

---

## ⚡ 快速命令速查 · Quick Command Reference

| 操作 · Operation | 命令 · Command |
|---|---|
| 初始化 | `python scripts/wiki_init.py <vault> [--domain "领域"]` |
| 导入 URL | `python scripts/wiki_ingest.py --vault <vault> --url <URL>` |
| 导入本地文件 | `python scripts/wiki_ingest.py --vault <vault> --file <path>` |
| 批量导入目录 | `python scripts/wiki_ingest.py --vault <vault> --dir <dir>` |
| 搜索 | `python scripts/wiki_search.py --vault <vault> --query "关键词"` |
| 查询（Markdown） | `python scripts/wiki_query.py --vault <vault> --query "问题"` |
| 查询（幻灯片） | `python scripts/wiki_query.py --vault <vault> --query "主题" --format marp` |
| 健康检查 | `python scripts/wiki_lint.py --vault <vault>` |
| 健康检查 + 修复 | `python scripts/wiki_lint.py --vault <vault> --fix` |

---

## 🔍 搜索引擎 · Search Engine

LLM Wiki KB 集成了 [qmd](https://github.com/tobi/qmd) 作为主力搜索引擎，支持 **BM25 + 向量混合检索**。同时提供优雅的降级方案：

| 层级 · Tier | 引擎 · Engine | 场景 · When |
|:---:|---|---|
| 🥇 | **qmd** (hybrid BM25 + vector) | qmd 已安装时优先使用 |
| 🥈 | **index.md 解析** | qmd 不可用，解析 wiki 目录 |
| 🥉 | **grep 全文搜索** | 最终兜底，任何环境都能工作 |

---

## 🔌 平台适配器 · Platform Adapters

| Platform | Schema File | Key Integration |
|----------|-------------|-----------------|
| **Claude Code** | `CLAUDE.md` | MCP server for qmd, native file access |
| **OpenCode / Codex** | `AGENTS.md` | Tool registration YAML |
| **Mira** | `SKILL.md` + sandbox | Feishu export, `web_builtin_fetch` |
| **Cursor / Others** | `SKILL.md` (paste to system prompt) | Python + filesystem |

每个适配器目录（`adapters/`）包含平台专属的配置说明和示例。

---

## 📂 项目结构 · Project Structure

```
llm-wiki-kb/
├── SKILL.md                    # 🧠 核心技能定义 (LLM reads this)
├── scripts/
│   ├── wiki_init.py            # 初始化 vault
│   ├── wiki_ingest.py          # 素材导入（URL / 本地文件）
│   ├── wiki_query.py           # 查询与多格式输出
│   ├── wiki_search.py          # 搜索（qmd / index / grep）
│   └── wiki_lint.py            # 健康检查（6 项自动化检测）
├── references/
│   ├── page-templates.md       # 5 种页面模板
│   ├── schema-template.md      # SCHEMA.md 生成模板
│   ├── qmd-integration.md      # qmd 搜索引擎集成指南
│   ├── obsidian-setup.md       # Obsidian 配置推荐
│   └── karpathy-llm-wiki.md   # Karpathy 原始设计原则
├── adapters/
│   ├── claude-code/            # Claude Code 适配器 (CLAUDE.md)
│   ├── opencode/               # OpenCode / Codex 适配器 (AGENTS.md)
│   └── mira/                   # Mira 适配器 (Feishu export)
├── LICENSE                     # MIT
└── README.md                   # 📖 你正在读的这个文件
```

---

## 🧪 Testing

```
✅ 35/35 tests passing

Module                    Tests    Status
─────────────────────────────────────────
wiki_init.py              5        ✅ All pass
wiki_ingest.py (file)     5        ✅ All pass
wiki_ingest.py (URL)      5        ✅ All pass
wiki_query.py             5        ✅ All pass
wiki_search.py            5        ✅ All pass
wiki_lint.py              5        ✅ All pass
Integration               5        ✅ All pass
```

---

## 🙏 致谢 · Acknowledgments

- **[Andrej Karpathy](https://x.com/karpathy)** — LLM Wiki 理念的提出者。本项目站在巨人的肩膀上。
- **[qmd](https://github.com/tobi/qmd)** by Tobias Lütke — 优雅的本地 Markdown 混合搜索引擎。
- **[Obsidian](https://obsidian.md)** — 让 Wiki 可视化变得如此自然。

---

<div align="center">

**从一条推文到一个工具链 · From a tweet to a toolkit**

*"The best way to understand an idea is to build it."*

[⭐ Star this repo](https://github.com/chengjialu8888/LLM-Wiki-KB) if you find it useful!

</div>
