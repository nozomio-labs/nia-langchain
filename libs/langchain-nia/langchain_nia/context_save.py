"""Tool for saving conversation context for cross-agent sharing via the Nia API."""

from __future__ import annotations

from typing import Any, List, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from langchain_nia._api_wrapper import NiaAPIWrapper


class NiaContextSaveInput(BaseModel):
    """Input for the NiaContextSave tool."""

    title: str = Field(description="A short title for the saved context.")
    summary: str = Field(description="A brief summary of the context being saved.")
    content: str = Field(description="The full content to save.")
    agent_source: Optional[str] = Field(
        default=None,
        description="Optional identifier of the agent saving this context.",
    )
    tags: Optional[List[str]] = Field(
        default=None, description="Optional list of tags for categorization."
    )
    memory_type: Optional[str] = Field(
        default=None,
        description=(
            "Optional memory type: 'scratchpad', 'episodic', 'fact', or 'procedural'."
        ),
    )


class NiaContextSave(BaseTool):
    """Save conversation context for cross-agent sharing.

    Store findings, indexed resources, search results, or any information
    that should persist across agent sessions.
    """

    name: str = "nia_context_save"
    description: str = (
        "Save conversation context for cross-agent sharing. "
        "Store findings, indexed resources, search results, or any information "
        "that should persist across agent sessions."
    )
    args_schema: Type[BaseModel] = NiaContextSaveInput
    api_wrapper: NiaAPIWrapper = Field(default_factory=NiaAPIWrapper)

    def _run(
        self,
        title: str,
        summary: str,
        content: str,
        agent_source: Optional[str] = None,
        tags: Optional[List[str]] = None,
        memory_type: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return self.api_wrapper.context_save(
                title=title,
                summary=summary,
                content=content,
                agent_source=agent_source,
                tags=tags,
                memory_type=memory_type,
            )
        except Exception as e:
            return repr(e)

    async def _arun(
        self,
        title: str,
        summary: str,
        content: str,
        agent_source: Optional[str] = None,
        tags: Optional[List[str]] = None,
        memory_type: Optional[str] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return await self.api_wrapper.acontext_save(
                title=title,
                summary=summary,
                content=content,
                agent_source=agent_source,
                tags=tags,
                memory_type=memory_type,
            )
        except Exception as e:
            return repr(e)
