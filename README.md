<div align="center">

# 🧠 LLM Wiki KB

**让 LLM 像人类专家一样，把零散知识编译成一部不断生长的百科全书**

**Let LLMs compile scattered knowledge into an ever-growing encyclopedia — just like a human expert would**

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.7+](https://img.shields.io/badge/Python-3.7+-green.svg)](https://python.org)
[![Tests](https://img.shields.io/badge/Tests-35%2F35%20Passing-brightgreen.svg)](#testing)

</div>

---

## 💡 灵感来源 · Inspiration

2025 年 6 月，Andrej Karpathy 发布了一篇 [LLM Wiki Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)，提出了一个极具洞察力的观点：

> **RAG 每次都在重新推导答案，而 Wiki 把知识编译一次、复用无数次。**

他描述了一种三层架构：**原始素材 → LLM 编译的 Wiki → Schema 约定**，让 LLM 不再只是"检索-回答"的管道，而是成为一个持续积累知识的编纂者。这个想法本身就像一颗种子——Karpathy 有意将它设计为一份"可以直接粘贴到你自己 LLM Agent 里"的抽象描述。

**但种子需要土壤、阳光和水。**

---

In June 2025, Andrej Karpathy published an [LLM Wiki Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) with a brilliantly simple insight:

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

## ⚡ 快速开始 · Quick Start

### 1. 初始化 Wiki · Initialize

```bash
python scripts/wiki_init.py --vault ~/my-wiki
```

### 2. 导入素材 · Ingest Sources

```bash
# 导入 URL
python scripts/wiki_ingest.py --vault ~/my-wiki --url https://example.com/article

# 批量导入目录
python scripts/wiki_ingest.py --vault ~/my-wiki --dir ~/papers/
```

### 3. 让 LLM 编译 · Let LLM Compile

将 `SKILL.md` 提供给你的 LLM Agent，它会自动：
- 阅读 `raw/` 中的素材
- 按模板创建 Wiki 页面
- 更新 `index.md` 和 `log.md`
- 建立 `[[wikilinks]]` 交叉引用

### 4. 搜索与查询 · Search & Query

```bash
# 搜索（自动选择最佳引擎）
python scripts/wiki_search.py --vault ~/my-wiki --query "transformer attention"

# 带格式的查询
python scripts/wiki_query.py --vault ~/my-wiki --query "对比 RNN 和 Transformer" --format marp
```

### 5. 健康检查 · Health Check

```bash
python scripts/wiki_lint.py --vault ~/my-wiki
```

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
│   ├── claude-code/            # Claude Code 适配器
│   ├── opencode/               # OpenCode / Codex 适配器
│   └── mira/                   # Mira 适配器
├── LICENSE                     # MIT
└── README.md                   # 📖 你正在读的这个文件
```

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

| Platform | Schema File | Config |
|----------|-------------|--------|
| **Claude Code** | `CLAUDE.md` | MCP server for qmd |
| **OpenCode / Codex** | `AGENTS.md` | Tool registration YAML |
| **Mira** | `SKILL.md` + sandbox | Feishu export, web fetch |

每个适配器目录包含平台专属的配置说明和示例。

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
