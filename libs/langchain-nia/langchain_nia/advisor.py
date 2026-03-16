"""Nia Advisor tool for code analysis against indexed documentation."""

from __future__ import annotations

from typing import Any, List, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from langchain_nia._api_wrapper import NiaAPIWrapper


class NiaAdvisorInput(BaseModel):
    """Input for the NiaAdvisor tool."""

    query: str = Field(description="Question or request about the provided code")
    codebase: str = Field(
        description="The code context to analyze",
    )
    search_scope: Optional[List[str]] = Field(
        default=None,
        description="Repository slugs or data source IDs to scope the advice search",
    )
    output_format: Optional[str] = Field(
        default=None,
        description=(
            "Desired output format. One of: explanation, checklist, diff, structured"
        ),
    )


class NiaAdvisor(BaseTool):
    """Analyze code against Nia-indexed documentation for tailored recommendations.

    Provide your code and a question, and get grounded advice based on
    official documentation, best practices, and indexed knowledge sources.
    """

    name: str = "nia_advisor"
    description: str = (
        "Analyze code against Nia-indexed documentation for tailored "
        "recommendations. Provide your code and a question, and get "
        "grounded advice based on official documentation."
    )
    args_schema: Type[BaseModel] = NiaAdvisorInput
    api_wrapper: NiaAPIWrapper = Field(default_factory=NiaAPIWrapper)

    def _run(
        self,
        query: str,
        codebase: str,
        search_scope: Optional[List[str]] = None,
        output_format: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return self.api_wrapper.advisor(
                query=query,
                codebase=codebase,
                search_scope=search_scope,
                output_format=output_format,
            )
        except Exception as e:
            return repr(e)

    async def _arun(
        self,
        query: str,
        codebase: str,
        search_scope: Optional[List[str]] = None,
        output_format: Optional[str] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return await self.api_wrapper.aadvisor(
                query=query,
                codebase=codebase,
                search_scope=search_scope,
                output_format=output_format,
            )
        except Exception as e:
            return repr(e)
