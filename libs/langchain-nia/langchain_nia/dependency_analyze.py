"""Tool for analyzing package manifests to identify dependencies via the Nia API."""

from __future__ import annotations

from typing import Any, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from langchain_nia._api_wrapper import NiaAPIWrapper


class NiaDependencyAnalyzeInput(BaseModel):
    """Input for the NiaDependencyAnalyze tool."""

    manifest_content: str = Field(
        description="The full content of the package manifest file."
    )
    manifest_type: Optional[str] = Field(
        default=None,
        description=(
            "Optional manifest file type, e.g. 'package.json', 'requirements.txt', "
            "'pyproject.toml', 'Cargo.toml', or 'go.mod'."
        ),
    )


class NiaDependencyAnalyze(BaseTool):
    """Analyze a package manifest to identify dependencies and their documentation URLs.

    Preview what dependencies would be indexed without subscribing.
    """

    name: str = "nia_dependency_analyze"
    description: str = (
        "Analyze a package manifest to identify dependencies and their documentation "
        "URLs without subscribing. Preview what dependencies would be indexed."
    )
    args_schema: Type[BaseModel] = NiaDependencyAnalyzeInput
    api_wrapper: NiaAPIWrapper = Field(default_factory=NiaAPIWrapper)

    def _run(
        self,
        manifest_content: str,
        manifest_type: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return self.api_wrapper.dependency_analyze(
                manifest_content=manifest_content, manifest_type=manifest_type
            )
        except Exception as e:
            return repr(e)

    async def _arun(
        self,
        manifest_content: str,
        manifest_type: Optional[str] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return await self.api_wrapper.adependency_analyze(
                manifest_content=manifest_content, manifest_type=manifest_type
            )
        except Exception as e:
            return repr(e)
