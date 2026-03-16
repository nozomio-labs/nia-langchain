"""Nia Search tool for querying indexed repositories and documentation."""

from __future__ import annotations

from typing import Any, List, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from langchain_nia._api_wrapper import NiaAPIWrapper


class NiaSearchInput(BaseModel):
    """Input for the NiaSearch tool."""

    query: str = Field(description="Natural language search query")
    repositories: Optional[List[str]] = Field(
        default=None,
        description="Repository slugs (owner/repo) to search within",
    )
    data_sources: Optional[List[str]] = Field(
        default=None,
        description="Data source IDs or display names to search",
    )
    slack_workspaces: Optional[List[str]] = Field(
        default=None,
        description="Slack workspace IDs to include in search",
    )
    local_folders: Optional[List[str]] = Field(
        default=None,
        description="Local folder IDs to include in search",
    )


class NiaSearch(BaseTool):
    """Search across Nia-indexed repositories, documentation, and data sources.

    Performs AI-powered semantic search across all indexed sources including
    GitHub repositories, documentation sites, PDFs, datasets, Slack, and more.
    """

    name: str = "nia_search"
    description: str = (
        "Search across code repositories, documentation, datasets, and other "
        "sources indexed in Nia using natural language queries. Returns relevant "
        "code snippets, documentation sections, and source metadata."
    )
    args_schema: Type[BaseModel] = NiaSearchInput
    api_wrapper: NiaAPIWrapper = Field(default_factory=NiaAPIWrapper)

    def _run(
        self,
        query: str,
        repositories: Optional[List[str]] = None,
        data_sources: Optional[List[str]] = None,
        slack_workspaces: Optional[List[str]] = None,
        local_folders: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            messages = [{"role": "user", "content": query}]
            return self.api_wrapper.search_query(
                messages=messages,
                repositories=repositories,
                data_sources=data_sources,
                slack_workspaces=slack_workspaces,
                local_folders=local_folders,
            )
        except Exception as e:
            return repr(e)

    async def _arun(
        self,
        query: str,
        repositories: Optional[List[str]] = None,
        data_sources: Optional[List[str]] = None,
        slack_workspaces: Optional[List[str]] = None,
        local_folders: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            messages = [{"role": "user", "content": query}]
            return await self.api_wrapper.asearch_query(
                messages=messages,
                repositories=repositories,
                data_sources=data_sources,
                slack_workspaces=slack_workspaces,
                local_folders=local_folders,
            )
        except Exception as e:
            return repr(e)
