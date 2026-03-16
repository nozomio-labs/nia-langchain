"""Tool for subscribing to a pre-indexed source in Nia."""

from __future__ import annotations

from typing import Any, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from langchain_nia._api_wrapper import NiaAPIWrapper


class NiaSourceSubscribeInput(BaseModel):
    """Input for the NiaSourceSubscribe tool."""

    url: str = Field(description="URL of the source to subscribe to.")
    source_type: Optional[str] = Field(
        default=None,
        description="Type of the source, if known.",
    )
    ref: Optional[str] = Field(
        default=None,
        description="Git ref or version to subscribe to.",
    )


class NiaSourceSubscribe(BaseTool):
    """Subscribe to a pre-indexed public source in Nia."""

    name: str = "nia_source_subscribe"
    description: str = (
        "Subscribe to a pre-indexed public source in Nia for instant access. "
        "If the source is already indexed globally, you get immediate access "
        "without waiting for indexing."
    )
    args_schema: Type[BaseModel] = NiaSourceSubscribeInput
    api_wrapper: NiaAPIWrapper = Field(default_factory=NiaAPIWrapper)

    def _run(
        self,
        url: str,
        source_type: Optional[str] = None,
        ref: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return self.api_wrapper.source_subscribe(
                url=url,
                source_type=source_type,
                ref=ref,
            )
        except Exception as e:
            return repr(e)

    async def _arun(
        self,
        url: str,
        source_type: Optional[str] = None,
        ref: Optional[str] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return await self.api_wrapper.asource_subscribe(
                url=url,
                source_type=source_type,
                ref=ref,
            )
        except Exception as e:
            return repr(e)
