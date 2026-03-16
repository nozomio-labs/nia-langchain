"""Tool for reading files from GitHub repositories via the Nia API."""

from __future__ import annotations

from typing import Any, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from langchain_nia._api_wrapper import NiaAPIWrapper


class NiaGitHubReadInput(BaseModel):
    """Input for the NiaGitHubRead tool."""

    repository: str = Field(description="The GitHub repository in 'owner/repo' format.")
    path: str = Field(description="The file path within the repository to read.")
    ref: Optional[str] = Field(
        default=None, description="Optional branch, tag, or commit SHA to read from."
    )
    start_line: Optional[int] = Field(
        default=None, description="Optional starting line number for partial reads."
    )
    end_line: Optional[int] = Field(
        default=None, description="Optional ending line number for partial reads."
    )


class NiaGitHubRead(BaseTool):
    """Read a file from any GitHub repository.

    Works without indexing - read any file from any public repo directly.
    Supports reading specific line ranges.
    """

    name: str = "nia_github_read"
    description: str = (
        "Read a file from any GitHub repository. "
        "Works without indexing - read any file from any public repo directly. "
        "Supports reading specific line ranges."
    )
    args_schema: Type[BaseModel] = NiaGitHubReadInput
    api_wrapper: NiaAPIWrapper = Field(default_factory=NiaAPIWrapper)

    def _run(
        self,
        repository: str,
        path: str,
        ref: Optional[str] = None,
        start_line: Optional[int] = None,
        end_line: Optional[int] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return self.api_wrapper.github_read(
                repository=repository,
                path=path,
                ref=ref,
                start_line=start_line,
                end_line=end_line,
            )
        except Exception as e:
            return repr(e)

    async def _arun(
        self,
        repository: str,
        path: str,
        ref: Optional[str] = None,
        start_line: Optional[int] = None,
        end_line: Optional[int] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return await self.api_wrapper.agithub_read(
                repository=repository,
                path=path,
                ref=ref,
                start_line=start_line,
                end_line=end_line,
            )
        except Exception as e:
            return repr(e)
