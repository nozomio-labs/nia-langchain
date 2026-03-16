"""Tool for indexing a source in Nia."""

from __future__ import annotations

from typing import Any, List, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from langchain_nia._api_wrapper import NiaAPIWrapper


class NiaIndexInput(BaseModel):
    """Input for the NiaIndex tool."""

    url: str = Field(description="URL of the source to index.")
    type_: Optional[str] = Field(
        default=None,
        description=(
            "Type of the source. One of: repository, documentation, "
            "research_paper, huggingface_dataset, local_folder. "
            "Auto-detected from URL if not provided."
        ),
    )
    display_name: Optional[str] = Field(
        default=None,
        description="Optional display name for the source.",
    )
    branch: Optional[str] = Field(
        default=None,
        description="Branch to index (for repository sources).",
    )
    url_patterns: Optional[List[str]] = Field(
        default=None,
        description="URL patterns to include when indexing documentation sites.",
    )
    exclude_patterns: Optional[List[str]] = Field(
        default=None,
        description="URL patterns to exclude when indexing documentation sites.",
    )
    check_llms_txt: Optional[bool] = Field(
        default=None,
        description="Whether to check for llms.txt when indexing documentation.",
    )


class NiaIndex(BaseTool):
    """Index a source in Nia for searching."""

    name: str = "nia_index"
    description: str = (
        "Index a source in Nia for searching. Supports GitHub repositories, "
        "documentation sites, research papers (arXiv), HuggingFace datasets, "
        "PDFs, spreadsheets, and local folders. Auto-detects source type from URL."
    )
    args_schema: Type[BaseModel] = NiaIndexInput
    api_wrapper: NiaAPIWrapper = Field(default_factory=NiaAPIWrapper)

    def _run(
        self,
        url: str,
        type_: Optional[str] = None,
        display_name: Optional[str] = None,
        branch: Optional[str] = None,
        url_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
        check_llms_txt: Optional[bool] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return self.api_wrapper.source_create(
                url=url,
                type_=type_,
                display_name=display_name,
                branch=branch,
                url_patterns=url_patterns,
                exclude_patterns=exclude_patterns,
                check_llms_txt=check_llms_txt,
            )
        except Exception as e:
            return repr(e)

    async def _arun(
        self,
        url: str,
        type_: Optional[str] = None,
        display_name: Optional[str] = None,
        branch: Optional[str] = None,
        url_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
        check_llms_txt: Optional[bool] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Any:
        try:
            return await self.api_wrapper.asource_create(
                url=url,
                type_=type_,
                display_name=display_name,
                branch=branch,
                url_patterns=url_patterns,
                exclude_patterns=exclude_patterns,
                check_llms_txt=check_llms_txt,
            )
        except Exception as e:
            return repr(e)
