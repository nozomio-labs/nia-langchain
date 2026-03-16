"""Tool for listing indexed sources in Nia."""

from __future__ import annotations

from typing import Any, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from langchain_nia._api_wrapper import NiaAPIWrapper


class NiaSourceListInput(BaseModel):
    """Input for the NiaSourceList tool."""

    type_: Optional[str] = Field(
        default=None,
        description=(
            "Filter by source type. One of: repository, documentation, "
            "research_paper, huggingface_dataset, local_folder."
        ),
    )
    query: Optional[str] = Field(
        default=None,
        description="Search sources by name.",
    )
    status: Optional[str] = Field(
        default=None,
        description="Filter by indexing status.",
    )
    limit: int = Field(
        default=20,
        description="Maximum number of sources to return.",
    )


class NiaSourceList(BaseTool):
    """List all indexed sources in Nia."""

    name: str = "nia_source_list"
    description: str = (
        "List all indexed sources in Nia. Filter by type (repository, "
        "documentation, research_paper, huggingface_dataset, local_folder), "
        "search by name, or filter by indexing status."
    )
    args_schema: Type[BaseModel] = NiaSourceListInput
    api_wrapper: NiaAPIWrapper = Field(default_factory=NiaAPIWrapper)

    def _run(
        self,
        type_: Optional[str] = None,
        query: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 20,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return self.api_wrapper.sources_list(
                type_=type_,
                query=query,
                status=status,
                limit=limit,
            )
        except Exception as e:
            return repr(e)

    async def _arun(
        self,
        type_: Optional[str] = None,
        query: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 20,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return await self.api_wrapper.asources_list(
                type_=type_,
                query=query,
                status=status,
                limit=limit,
            )
        except Exception as e:
            return repr(e)
