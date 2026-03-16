"""Tool for regex/pattern searching within an indexed source in Nia."""

from __future__ import annotations

from typing import Any, List, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from langchain_nia._api_wrapper import NiaAPIWrapper


class NiaGrepInput(BaseModel):
    """Input for the NiaGrep tool."""

    source_id: str = Field(description="ID of the source to search within.")
    pattern: str = Field(description="Regex or text pattern to search for.")
    file_extensions: Optional[List[str]] = Field(
        default=None,
        description="File extensions to limit the search to (e.g., ['py', 'js']).",
    )
    context_lines: Optional[int] = Field(
        default=None,
        description="Number of context lines to include around each match.",
    )


class NiaGrep(BaseTool):
    """Regex/pattern search within an indexed source in Nia."""

    name: str = "nia_grep"
    description: str = (
        "Regex/pattern search within an indexed source. Search for code "
        "patterns, function names, or text across all files in a repository, "
        "documentation site, or other indexed source."
    )
    args_schema: Type[BaseModel] = NiaGrepInput
    api_wrapper: NiaAPIWrapper = Field(default_factory=NiaAPIWrapper)

    def _run(
        self,
        source_id: str,
        pattern: str,
        file_extensions: Optional[List[str]] = None,
        context_lines: Optional[int] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return self.api_wrapper.source_grep(
                source_id=source_id,
                pattern=pattern,
                file_extensions=file_extensions,
                context_lines=context_lines,
            )
        except Exception as e:
            return repr(e)

    async def _arun(
        self,
        source_id: str,
        pattern: str,
        file_extensions: Optional[List[str]] = None,
        context_lines: Optional[int] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return await self.api_wrapper.asource_grep(
                source_id=source_id,
                pattern=pattern,
                file_extensions=file_extensions,
                context_lines=context_lines,
            )
        except Exception as e:
            return repr(e)
