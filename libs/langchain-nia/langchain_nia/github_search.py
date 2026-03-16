"""Tool for searching code in GitHub repositories via the Nia API."""

from __future__ import annotations

from typing import Any, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from langchain_nia._api_wrapper import NiaAPIWrapper


class NiaGitHubSearchInput(BaseModel):
    """Input for the NiaGitHubSearch tool."""

    query: str = Field(description="The search query string to find code.")
    repository: str = Field(description="The GitHub repository in 'owner/repo' format.")
    language: Optional[str] = Field(
        default=None, description="Optional programming language filter."
    )


class NiaGitHubSearch(BaseTool):
    """Search code in any GitHub repository using GitHub's Code Search API.

    Works without indexing - search any public repo directly.
    Rate limited to 10 requests per minute.
    """

    name: str = "nia_github_search"
    description: str = (
        "Search code in any GitHub repository using GitHub's Code Search API. "
        "Works without indexing - search any public repo directly. "
        "Rate limited to 10 requests per minute."
    )
    args_schema: Type[BaseModel] = NiaGitHubSearchInput
    api_wrapper: NiaAPIWrapper = Field(default_factory=NiaAPIWrapper)

    def _run(
        self,
        query: str,
        repository: str,
        language: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return self.api_wrapper.github_search(
                query=query, repository=repository, language=language
            )
        except Exception as e:
            return repr(e)

    async def _arun(
        self,
        query: str,
        repository: str,
        language: Optional[str] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return await self.api_wrapper.agithub_search(
                query=query, repository=repository, language=language
            )
        except Exception as e:
            return repr(e)
