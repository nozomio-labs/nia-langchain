"""Tool for semantic search over saved contexts via the Nia API."""

from __future__ import annotations

from typing import Any, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from langchain_nia._api_wrapper import NiaAPIWrapper


class NiaContextSearchInput(BaseModel):
    """Input for the NiaContextSearch tool."""

    q: str = Field(description="Natural language search query.")
    limit: int = Field(default=20, description="Maximum number of results to return.")
    include_highlights: bool = Field(
        default=False,
        description="Whether to include highlighted matching snippets in results.",
    )


class NiaContextSearch(BaseTool):
    """Semantic search over saved contexts.

    Find previously saved agent contexts, findings, and shared knowledge
    using natural language queries.
    """

    name: str = "nia_context_search"
    description: str = (
        "Semantic search over saved contexts. "
        "Find previously saved agent contexts, findings, and shared knowledge "
        "using natural language queries."
    )
    args_schema: Type[BaseModel] = NiaContextSearchInput
    api_wrapper: NiaAPIWrapper = Field(default_factory=NiaAPIWrapper)

    def _run(
        self,
        q: str,
        limit: int = 20,
        include_highlights: bool = False,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return self.api_wrapper.context_search(
                q=q, limit=limit, include_highlights=include_highlights
            )
        except Exception as e:
            return repr(e)

    async def _arun(
        self,
        q: str,
        limit: int = 20,
        include_highlights: bool = False,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return await self.api_wrapper.acontext_search(
                q=q, limit=limit, include_highlights=include_highlights
            )
        except Exception as e:
            return repr(e)
