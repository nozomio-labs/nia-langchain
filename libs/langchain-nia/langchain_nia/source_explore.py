"""Tool for browsing the file tree of an indexed source in Nia."""

from __future__ import annotations

from typing import Any, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from langchain_nia._api_wrapper import NiaAPIWrapper


class NiaExploreInput(BaseModel):
    """Input for the NiaExplore tool."""

    source_id: str = Field(description="ID of the source to explore.")
    branch: Optional[str] = Field(
        default=None,
        description="Branch to explore (for repository sources).",
    )
    max_depth: Optional[int] = Field(
        default=None,
        description="Maximum depth of the file tree to return.",
    )


class NiaExplore(BaseTool):
    """Browse the file tree or directory structure of an indexed source."""

    name: str = "nia_explore"
    description: str = (
        "Browse the file tree or directory structure of an indexed source. "
        "View the hierarchy of files and folders in a repository, "
        "documentation site, local folder, or dataset."
    )
    args_schema: Type[BaseModel] = NiaExploreInput
    api_wrapper: NiaAPIWrapper = Field(default_factory=NiaAPIWrapper)

    def _run(
        self,
        source_id: str,
        branch: Optional[str] = None,
        max_depth: Optional[int] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return self.api_wrapper.source_tree(
                source_id=source_id,
                branch=branch,
                max_depth=max_depth,
            )
        except Exception as e:
            return repr(e)

    async def _arun(
        self,
        source_id: str,
        branch: Optional[str] = None,
        max_depth: Optional[int] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return await self.api_wrapper.asource_tree(
                source_id=source_id,
                branch=branch,
                max_depth=max_depth,
            )
        except Exception as e:
            return repr(e)
