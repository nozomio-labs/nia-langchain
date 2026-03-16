"""Nia Web Search tool for searching the web via Nia."""

from __future__ import annotations

from typing import Any, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from langchain_nia._api_wrapper import NiaAPIWrapper


class NiaWebSearchInput(BaseModel):
    """Input for the NiaWebSearch tool."""

    query: str = Field(description="Search query string")
    num_results: int = Field(
        default=5,
        description="Number of results to return",
    )
    category: Optional[str] = Field(
        default=None,
        description=(
            "Category filter for results. One of: "
            "github, company, research, news, tweet, pdf, blog"
        ),
    )
    days_back: Optional[int] = Field(
        default=None,
        description="Limit results to the last N days",
    )


class NiaWebSearch(BaseTool):
    """Search the web for information using Nia.

    Searches across GitHub repositories, documentation, research papers,
    news articles, tweets, PDFs, and blog posts.
    """

    name: str = "nia_web_search"
    description: str = (
        "Search the web for information including GitHub repositories, "
        "documentation, research papers, news, and more. Useful when you "
        "need current information from the internet."
    )
    args_schema: Type[BaseModel] = NiaWebSearchInput
    api_wrapper: NiaAPIWrapper = Field(default_factory=NiaAPIWrapper)

    def _run(
        self,
        query: str,
        num_results: int = 5,
        category: Optional[str] = None,
        days_back: Optional[int] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return self.api_wrapper.search_web(
                query=query,
                num_results=num_results,
                category=category,
                days_back=days_back,
            )
        except Exception as e:
            return repr(e)

    async def _arun(
        self,
        query: str,
        num_results: int = 5,
        category: Optional[str] = None,
        days_back: Optional[int] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return await self.api_wrapper.asearch_web(
                query=query,
                num_results=num_results,
                category=category,
                days_back=days_back,
            )
        except Exception as e:
            return repr(e)
