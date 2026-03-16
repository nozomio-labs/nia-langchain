# 🦜️🔗 LangChain Nia

This repository contains 1 package with Nia AI integrations with LangChain:

- [langchain-nia](https://pypi.org/project/langchain-nia/)

## Quick Start

```bash
pip install langchain-nia
export NIA_API_KEY="nk_..."
```

```python
from langchain_nia import NiaToolkit

toolkit = NiaToolkit()
tools = toolkit.get_tools()  # 20 tools for search, source management, GitHub, contexts, and dependencies
```

See [libs/langchain-nia/README.md](libs/langchain-nia/README.md) for full documentation.
