"""Tool for browsing the file tree of GitHub repositories via the Nia API."""

from __future__ import annotations

from typing import Any, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from langchain_nia._api_wrapper import NiaAPIWrapper


class NiaGitHubTreeInput(BaseModel):
    """Input for the NiaGitHubTree tool."""

    owner: str = Field(
        description="The GitHub repository owner (user or organization)."
    )
    repo: str = Field(description="The GitHub repository name.")
    ref: Optional[str] = Field(
        default=None,
        description="Optional branch, tag, or commit SHA. Defaults to HEAD.",
    )
    path: Optional[str] = Field(
        default=None, description="Optional subdirectory path to list."
    )


class NiaGitHubTree(BaseTool):
    """Get the file tree structure of any GitHub repository or subdirectory.

    Works without indexing - browse any public repo's structure directly.
    """

    name: str = "nia_github_tree"
    description: str = (
        "Get the file tree structure of any GitHub repository or subdirectory. "
        "Works without indexing - browse any public repo's structure directly."
    )
    args_schema: Type[BaseModel] = NiaGitHubTreeInput
    api_wrapper: NiaAPIWrapper = Field(default_factory=NiaAPIWrapper)

    def _run(
        self,
        owner: str,
        repo: str,
        ref: Optional[str] = None,
        path: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return self.api_wrapper.github_tree(
                owner=owner, repo=repo, ref=ref, path=path
            )
        except Exception as e:
            return repr(e)

    async def _arun(
        self,
        owner: str,
        repo: str,
        ref: Optional[str] = None,
        path: Optional[str] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return await self.api_wrapper.agithub_tree(
                owner=owner, repo=repo, ref=ref, path=path
            )
        except Exception as e:
            return repr(e)
