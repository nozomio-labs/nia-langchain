"""Glob-pattern file search in GitHub repositories via Nia."""

from __future__ import annotations

from typing import Any, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from langchain_nia._api_wrapper import NiaAPIWrapper


class NiaGitHubGlobInput(BaseModel):
    """Input for the NiaGitHubGlob tool."""

    repository: str = Field(description="GitHub repository in 'owner/repo' format.")
    pattern: str = Field(
        description=(
            "Glob pattern to match files, e.g. '*.py', 'src/**/*.ts', or 'docs/*.md'."
        )
    )
    ref: Optional[str] = Field(
        default=None, description="Optional branch, tag, or commit SHA to search in."
    )


class NiaGitHubGlob(BaseTool):
    """Find files matching a glob pattern in any GitHub repository.

    Works without indexing - use patterns like '*.py', 'src/**/*.ts',
    or 'docs/*.md' to find files.
    """

    name: str = "nia_github_glob"
    description: str = (
        "Find files matching a glob pattern in any GitHub repository. "
        "Works without indexing - use patterns like '*.py', 'src/**/*.ts', "
        "or 'docs/*.md' to find files."
    )
    args_schema: Type[BaseModel] = NiaGitHubGlobInput
    api_wrapper: NiaAPIWrapper = Field(default_factory=NiaAPIWrapper)

    def _run(
        self,
        repository: str,
        pattern: str,
        ref: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return self.api_wrapper.github_glob(
                repository=repository, pattern=pattern, ref=ref
            )
        except Exception as e:
            return repr(e)

    async def _arun(
        self,
        repository: str,
        pattern: str,
        ref: Optional[str] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return await self.api_wrapper.agithub_glob(
                repository=repository, pattern=pattern, ref=ref
            )
        except Exception as e:
            return repr(e)
