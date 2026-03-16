# langchain-nia

LangChain integration for [Nia AI](https://trynia.ai) — code search, research, and knowledge management.

## Installation

```bash
pip install langchain-nia
```

## Setup

Set your Nia API key:

```bash
export NIA_API_KEY="nk_..."
```

## Quick Start

### Using individual tools

```python
from langchain_nia import NiaSearch

tool = NiaSearch()
result = tool.invoke({"query": "how to use React hooks"})
```

### Using the toolkit

```python
from langchain_nia import NiaToolkit

toolkit = NiaToolkit()
tools = toolkit.get_tools()  # Returns all 20 Nia tools
```

You can control which tool groups are included:

```python
toolkit = NiaToolkit(
    include_search=True,
    include_sources=True,
    include_github=True,
    include_contexts=True,
    include_dependencies=True,
)
```

### With a LangChain agent

```python
from langchain_nia import NiaToolkit
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")
toolkit = NiaToolkit()
tools = toolkit.get_tools()

llm_with_tools = llm.bind_tools(tools)
```

## Available Tools

### Search (5 tools)
- **NiaSearch** — Semantic search across indexed repos, docs, and data sources
- **NiaWebSearch** — Web search with category and date filtering
- **NiaDeepResearch** — Multi-step comprehensive research
- **NiaUniversalSearch** — Search all sources simultaneously
- **NiaAdvisor** — Analyze code against indexed documentation

### Source Management (7 tools)
- **NiaIndex** — Index new sources (repos, docs, papers, datasets)
- **NiaSourceList** — List indexed sources
- **NiaSourceSubscribe** — Subscribe to pre-indexed public sources
- **NiaSourceSync** — Re-sync indexed sources
- **NiaRead** — Read files/pages from indexed sources
- **NiaGrep** — Regex search within indexed sources
- **NiaExplore** — Browse file tree of indexed sources

### GitHub (4 tools)
- **NiaGitHubSearch** — Search code in GitHub repos
- **NiaGitHubRead** — Read files from GitHub repos
- **NiaGitHubGlob** — Find files matching glob patterns
- **NiaGitHubTree** — Browse repo file tree

### Context/Memory (2 tools)
- **NiaContextSave** — Save context for cross-agent sharing
- **NiaContextSearch** — Semantic search over saved contexts

### Dependencies (2 tools)
- **NiaDependencySubscribe** — Auto-subscribe to docs for project dependencies
- **NiaDependencyAnalyze** — Analyze manifests to preview indexable dependencies
