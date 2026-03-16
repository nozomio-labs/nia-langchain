"""Nia Universal Search tool for searching across all sources simultaneously."""

from __future__ import annotations

from typing import Any, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from langchain_nia._api_wrapper import NiaAPIWrapper


class NiaUniversalSearchInput(BaseModel):
    """Input for the NiaUniversalSearch tool."""

    query: str = Field(description="Natural language search query")
    top_k: int = Field(
        default=20,
        description="Maximum number of results to return",
    )
    include_repos: bool = Field(
        default=True,
        description="Whether to include indexed repository results",
    )
    include_docs: bool = Field(
        default=True,
        description="Whether to include documentation results",
    )
    compress_output: bool = Field(
        default=False,
        description="Whether to compress/summarize the output for brevity",
    )


class NiaUniversalSearch(BaseTool):
    """Search across all sources simultaneously using Nia.

    Queries indexed repositories, documentation, and the public Nia index
    in a single request. Returns ranked results from multiple sources with
    relevance scores.
    """

    name: str = "nia_universal_search"
    description: str = (
        "Search across all sources simultaneously - indexed repositories, "
        "documentation, and the public Nia index. Returns ranked results "
        "from multiple sources with relevance scores."
    )
    args_schema: Type[BaseModel] = NiaUniversalSearchInput
    api_wrapper: NiaAPIWrapper = Field(default_factory=NiaAPIWrapper)

    def _run(
        self,
        query: str,
        top_k: int = 20,
        include_repos: bool = True,
        include_docs: bool = True,
        compress_output: bool = False,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return self.api_wrapper.search_universal(
                query=query,
                top_k=top_k,
                include_repos=include_repos,
                include_docs=include_docs,
                compress_output=compress_output,
            )
        except Exception as e:
            return repr(e)

    async def _arun(
        self,
        query: str,
        top_k: int = 20,
        include_repos: bool = True,
        include_docs: bool = True,
        compress_output: bool = False,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return await self.api_wrapper.asearch_universal(
                query=query,
                top_k=top_k,
                include_repos=include_repos,
                include_docs=include_docs,
                compress_output=compress_output,
            )
        except Exception as e:
            return repr(e)
