"""LangChain integration for Nia AI.

Code search, research, and knowledge management.
"""

from importlib import metadata

from langchain_nia._api_wrapper import NiaAPIWrapper
from langchain_nia.advisor import NiaAdvisor
from langchain_nia.context_save import NiaContextSave
from langchain_nia.context_search import NiaContextSearch
from langchain_nia.deep_research import NiaDeepResearch
from langchain_nia.dependency_analyze import NiaDependencyAnalyze
from langchain_nia.dependency_subscribe import NiaDependencySubscribe
from langchain_nia.github_glob import NiaGitHubGlob
from langchain_nia.github_read import NiaGitHubRead
from langchain_nia.github_search import NiaGitHubSearch
from langchain_nia.github_tree import NiaGitHubTree
from langchain_nia.search import NiaSearch
from langchain_nia.source_explore import NiaExplore
from langchain_nia.source_grep import NiaGrep
from langchain_nia.source_index import NiaIndex
from langchain_nia.source_list import NiaSourceList
from langchain_nia.source_read import NiaRead
from langchain_nia.source_subscribe import NiaSourceSubscribe
from langchain_nia.source_sync import NiaSourceSync
from langchain_nia.toolkit import NiaToolkit
from langchain_nia.universal_search import NiaUniversalSearch
from langchain_nia.web_search import NiaWebSearch

try:
    __version__: str = metadata.version(__package__)
except metadata.PackageNotFoundError:
    __version__ = ""
del metadata

__all__ = [
    "__version__",
    "NiaAPIWrapper",
    "NiaAdvisor",
    "NiaContextSave",
    "NiaContextSearch",
    "NiaDeepResearch",
    "NiaDependencyAnalyze",
    "NiaDependencySubscribe",
    "NiaExplore",
    "NiaGitHubGlob",
    "NiaGitHubRead",
    "NiaGitHubSearch",
    "NiaGitHubTree",
    "NiaGrep",
    "NiaIndex",
    "NiaRead",
    "NiaSearch",
    "NiaSourceList",
    "NiaSourceSubscribe",
    "NiaSourceSync",
    "NiaToolkit",
    "NiaUniversalSearch",
    "NiaWebSearch",
]
