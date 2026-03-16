"""Nia Deep Research tool for comprehensive multi-step AI research."""

from __future__ import annotations

from typing import Any, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from langchain_nia._api_wrapper import NiaAPIWrapper


class NiaDeepResearchInput(BaseModel):
    """Input for the NiaDeepResearch tool."""

    query: str = Field(description="Research question or topic to investigate")
    output_format: Optional[str] = Field(
        default=None,
        description="Desired output format for the research results",
    )
    verbose: bool = Field(
        default=False,
        description="Whether to include detailed intermediate steps in the output",
    )


class NiaDeepResearch(BaseTool):
    """Perform deep, multi-step AI research on complex topics.

    Returns comprehensive analysis with citations and source references.
    Best suited for questions requiring thorough investigation across
    multiple sources.
    """

    name: str = "nia_deep_research"
    description: str = (
        "Perform deep, multi-step AI research on complex topics. Returns "
        "comprehensive analysis with citations and source references. Best "
        "for questions requiring thorough investigation."
    )
    args_schema: Type[BaseModel] = NiaDeepResearchInput
    api_wrapper: NiaAPIWrapper = Field(default_factory=NiaAPIWrapper)

    def _run(
        self,
        query: str,
        output_format: Optional[str] = None,
        verbose: bool = False,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return self.api_wrapper.search_deep(
                query=query,
                output_format=output_format,
                verbose=verbose,
            )
        except Exception as e:
            return repr(e)

    async def _arun(
        self,
        query: str,
        output_format: Optional[str] = None,
        verbose: bool = False,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return await self.api_wrapper.asearch_deep(
                query=query,
                output_format=output_format,
                verbose=verbose,
            )
        except Exception as e:
            return repr(e)
