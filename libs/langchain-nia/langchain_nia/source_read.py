"""Tool for reading content from an indexed source in Nia."""

from __future__ import annotations

from typing import Any, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from langchain_nia._api_wrapper import NiaAPIWrapper


class NiaReadInput(BaseModel):
    """Input for the NiaRead tool."""

    source_id: str = Field(description="ID of the source to read from.")
    path: Optional[str] = Field(
        default=None,
        description="File path within the source to read.",
    )
    url: Optional[str] = Field(
        default=None,
        description="URL of the specific page or resource to read.",
    )
    branch: Optional[str] = Field(
        default=None,
        description="Branch to read from (for repository sources).",
    )
    page: Optional[int] = Field(
        default=None,
        description="Page number to read (for paginated sources like PDFs).",
    )
    line_start: Optional[int] = Field(
        default=None,
        description="Starting line number for reading a range of lines.",
    )
    line_end: Optional[int] = Field(
        default=None,
        description="Ending line number for reading a range of lines.",
    )


class NiaRead(BaseTool):
    """Read content from any indexed source in Nia."""

    name: str = "nia_read"
    description: str = (
        "Read content from any indexed source in Nia. Supports reading files "
        "from repositories, pages from documentation, sections from PDFs, "
        "rows from datasets, and messages from Slack."
    )
    args_schema: Type[BaseModel] = NiaReadInput
    api_wrapper: NiaAPIWrapper = Field(default_factory=NiaAPIWrapper)

    def _run(
        self,
        source_id: str,
        path: Optional[str] = None,
        url: Optional[str] = None,
        branch: Optional[str] = None,
        page: Optional[int] = None,
        line_start: Optional[int] = None,
        line_end: Optional[int] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return self.api_wrapper.source_content(
                source_id=source_id,
                path=path,
                url=url,
                branch=branch,
                page=page,
                line_start=line_start,
                line_end=line_end,
            )
        except Exception as e:
            return repr(e)

    async def _arun(
        self,
        source_id: str,
        path: Optional[str] = None,
        url: Optional[str] = None,
        branch: Optional[str] = None,
        page: Optional[int] = None,
        line_start: Optional[int] = None,
        line_end: Optional[int] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return await self.api_wrapper.asource_content(
                source_id=source_id,
                path=path,
                url=url,
                branch=branch,
                page=page,
                line_start=line_start,
                line_end=line_end,
            )
        except Exception as e:
            return repr(e)
