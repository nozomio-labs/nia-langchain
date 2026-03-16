"""Tool for re-syncing an indexed source in Nia."""

from __future__ import annotations

from typing import Any, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from langchain_nia._api_wrapper import NiaAPIWrapper


class NiaSourceSyncInput(BaseModel):
    """Input for the NiaSourceSync tool."""

    source_id: str = Field(description="ID of the source to re-sync.")


class NiaSourceSync(BaseTool):
    """Refresh and re-sync an indexed source in Nia."""

    name: str = "nia_source_sync"
    description: str = (
        "Refresh and re-sync an indexed source to pull the latest changes. "
        "Use this to update a repository, documentation site, or other source "
        "that may have changed."
    )
    args_schema: Type[BaseModel] = NiaSourceSyncInput
    api_wrapper: NiaAPIWrapper = Field(default_factory=NiaAPIWrapper)

    def _run(
        self,
        source_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return self.api_wrapper.source_sync(source_id=source_id)
        except Exception as e:
            return repr(e)

    async def _arun(
        self,
        source_id: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return await self.api_wrapper.asource_sync(source_id=source_id)
        except Exception as e:
            return repr(e)
