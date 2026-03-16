"""Nia toolkit providing all Nia tools for LangChain agents."""

from __future__ import annotations

from typing import List

from langchain_core.tools import BaseTool, BaseToolkit
from pydantic import Field

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
from langchain_nia.universal_search import NiaUniversalSearch
from langchain_nia.web_search import NiaWebSearch


class NiaToolkit(BaseToolkit):
    """Toolkit providing all Nia AI tools for LangChain agents.

    Use ``include_*`` flags to control which tool groups are returned.
    All tools share a single :class:`NiaAPIWrapper` instance.
    """

    api_wrapper: NiaAPIWrapper = Field(default_factory=NiaAPIWrapper)
    include_search: bool = True
    include_sources: bool = True
    include_github: bool = True
    include_contexts: bool = True
    include_dependencies: bool = True

    def get_tools(self) -> List[BaseTool]:
        tools: List[BaseTool] = []
        w = self.api_wrapper

        if self.include_search:
            tools.extend(
                [
                    NiaSearch(api_wrapper=w),
                    NiaWebSearch(api_wrapper=w),
                    NiaDeepResearch(api_wrapper=w),
                    NiaUniversalSearch(api_wrapper=w),
                    NiaAdvisor(api_wrapper=w),
                ]
            )

        if self.include_sources:
            tools.extend(
                [
                    NiaIndex(api_wrapper=w),
                    NiaSourceList(api_wrapper=w),
                    NiaSourceSubscribe(api_wrapper=w),
                    NiaSourceSync(api_wrapper=w),
                    NiaRead(api_wrapper=w),
                    NiaGrep(api_wrapper=w),
                    NiaExplore(api_wrapper=w),
                ]
            )

        if self.include_github:
            tools.extend(
                [
                    NiaGitHubSearch(api_wrapper=w),
                    NiaGitHubRead(api_wrapper=w),
                    NiaGitHubGlob(api_wrapper=w),
                    NiaGitHubTree(api_wrapper=w),
                ]
            )

        if self.include_contexts:
            tools.extend(
                [
                    NiaContextSave(api_wrapper=w),
                    NiaContextSearch(api_wrapper=w),
                ]
            )

        if self.include_dependencies:
            tools.extend(
                [
                    NiaDependencySubscribe(api_wrapper=w),
                    NiaDependencyAnalyze(api_wrapper=w),
                ]
            )

        return tools
