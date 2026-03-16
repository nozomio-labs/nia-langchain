"""Tool for subscribing to dependency documentation via the Nia API."""

from __future__ import annotations

from typing import Any, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from langchain_nia._api_wrapper import NiaAPIWrapper


class NiaDependencySubscribeInput(BaseModel):
    """Input for the NiaDependencySubscribe tool."""

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


class NiaDependencySubscribe(BaseTool):
    """Auto-subscribe to docs for all dependencies in a manifest.

    Supports package.json, requirements.txt, pyproject.toml,
    Cargo.toml, and go.mod.
    """

    name: str = "nia_dependency_subscribe"
    description: str = (
        "Parse a package manifest and auto-subscribe to documentation for all "
        "dependencies. Supports package.json, requirements.txt, pyproject.toml, "
        "Cargo.toml, and go.mod."
    )
    args_schema: Type[BaseModel] = NiaDependencySubscribeInput
    api_wrapper: NiaAPIWrapper = Field(default_factory=NiaAPIWrapper)

    def _run(
        self,
        manifest_content: str,
        manifest_type: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return self.api_wrapper.dependency_subscribe(
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
            return await self.api_wrapper.adependency_subscribe(
                manifest_content=manifest_content, manifest_type=manifest_type
            )
        except Exception as e:
            return repr(e)
