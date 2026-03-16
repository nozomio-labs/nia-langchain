"""Nia API wrapper for making authenticated HTTP requests."""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

import httpx
from pydantic import BaseModel, ConfigDict, Field, SecretStr, model_validator


class NiaAPIWrapper(BaseModel):
    """Wrapper around the Nia AI REST API.

    Handles authentication, sync/async HTTP calls, and response parsing.
    API key is resolved from the ``nia_api_key`` parameter or the
    ``NIA_API_KEY`` environment variable.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    nia_api_key: SecretStr = Field(default=None)  # type: ignore[assignment]
    base_url: str = "https://apigcp.trynia.ai/v2"
    timeout: float = 60.0

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if not values.get("nia_api_key"):
            api_key = os.environ.get("NIA_API_KEY", "")
            if not api_key:
                raise ValueError(
                    "Nia API key must be provided via 'nia_api_key' parameter "
                    "or 'NIA_API_KEY' environment variable."
                )
            values["nia_api_key"] = api_key
        if not values.get("base_url"):
            env_url = os.environ.get("NIA_API_URL")
            if env_url:
                values["base_url"] = env_url.rstrip("/")
        return values

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.nia_api_key.get_secret_value()}",
            "Content-Type": "application/json",
            "User-Agent": "langchain-nia/0.1.0",
        }

    def _request(
        self,
        method: str,
        path: str,
        *,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        url = f"{self.base_url}{path}"
        with httpx.Client(timeout=self.timeout) as client:
            response = client.request(
                method,
                url,
                headers=self._headers(),
                json=json,
                params=_strip_none(params),
            )
            response.raise_for_status()
            return response.json()

    async def _arequest(
        self,
        method: str,
        path: str,
        *,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        url = f"{self.base_url}{path}"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.request(
                method,
                url,
                headers=self._headers(),
                json=json,
                params=_strip_none(params),
            )
            response.raise_for_status()
            return response.json()

    # ── Search ───────────────────────────────────────────────────────────

    def search_query(
        self,
        messages: List[Dict[str, str]],
        *,
        repositories: Optional[List[str]] = None,
        data_sources: Optional[List[str]] = None,
        slack_workspaces: Optional[List[str]] = None,
        local_folders: Optional[List[str]] = None,
        fast_mode: bool = True,
        include_sources: bool = True,
        max_tokens: Optional[int] = None,
    ) -> Any:
        body: Dict[str, Any] = {
            "mode": "query",
            "messages": messages,
            "fast_mode": fast_mode,
            "include_sources": include_sources,
        }
        if repositories:
            body["repositories"] = repositories
        if data_sources:
            body["data_sources"] = data_sources
        if slack_workspaces:
            body["slack_workspaces"] = slack_workspaces
        if local_folders:
            body["local_folders"] = local_folders
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        return self._request("POST", "/search", json=body)

    async def asearch_query(
        self,
        messages: List[Dict[str, str]],
        *,
        repositories: Optional[List[str]] = None,
        data_sources: Optional[List[str]] = None,
        slack_workspaces: Optional[List[str]] = None,
        local_folders: Optional[List[str]] = None,
        fast_mode: bool = True,
        include_sources: bool = True,
        max_tokens: Optional[int] = None,
    ) -> Any:
        body: Dict[str, Any] = {
            "mode": "query",
            "messages": messages,
            "fast_mode": fast_mode,
            "include_sources": include_sources,
        }
        if repositories:
            body["repositories"] = repositories
        if data_sources:
            body["data_sources"] = data_sources
        if slack_workspaces:
            body["slack_workspaces"] = slack_workspaces
        if local_folders:
            body["local_folders"] = local_folders
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        return await self._arequest("POST", "/search", json=body)

    def search_web(
        self,
        query: str,
        *,
        num_results: int = 5,
        category: Optional[str] = None,
        days_back: Optional[int] = None,
    ) -> Any:
        body: Dict[str, Any] = {
            "mode": "web",
            "query": query,
            "num_results": num_results,
        }
        if category:
            body["category"] = category
        if days_back is not None:
            body["days_back"] = days_back
        return self._request("POST", "/search", json=body)

    async def asearch_web(
        self,
        query: str,
        *,
        num_results: int = 5,
        category: Optional[str] = None,
        days_back: Optional[int] = None,
    ) -> Any:
        body: Dict[str, Any] = {
            "mode": "web",
            "query": query,
            "num_results": num_results,
        }
        if category:
            body["category"] = category
        if days_back is not None:
            body["days_back"] = days_back
        return await self._arequest("POST", "/search", json=body)

    def search_deep(
        self,
        query: str,
        *,
        output_format: Optional[str] = None,
        verbose: bool = False,
    ) -> Any:
        body: Dict[str, Any] = {
            "mode": "deep",
            "query": query,
            "verbose": verbose,
        }
        if output_format:
            body["output_format"] = output_format
        return self._request("POST", "/search", json=body)

    async def asearch_deep(
        self,
        query: str,
        *,
        output_format: Optional[str] = None,
        verbose: bool = False,
    ) -> Any:
        body: Dict[str, Any] = {
            "mode": "deep",
            "query": query,
            "verbose": verbose,
        }
        if output_format:
            body["output_format"] = output_format
        return await self._arequest("POST", "/search", json=body)

    def search_universal(
        self,
        query: str,
        *,
        top_k: int = 20,
        include_repos: bool = True,
        include_docs: bool = True,
        compress_output: bool = False,
        max_tokens: Optional[int] = None,
    ) -> Any:
        body: Dict[str, Any] = {
            "mode": "universal",
            "query": query,
            "top_k": top_k,
            "include_repos": include_repos,
            "include_docs": include_docs,
            "compress_output": compress_output,
        }
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        return self._request("POST", "/search", json=body)

    async def asearch_universal(
        self,
        query: str,
        *,
        top_k: int = 20,
        include_repos: bool = True,
        include_docs: bool = True,
        compress_output: bool = False,
        max_tokens: Optional[int] = None,
    ) -> Any:
        body: Dict[str, Any] = {
            "mode": "universal",
            "query": query,
            "top_k": top_k,
            "include_repos": include_repos,
            "include_docs": include_docs,
            "compress_output": compress_output,
        }
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        return await self._arequest("POST", "/search", json=body)

    # ── Advisor ──────────────────────────────────────────────────────────

    def advisor(
        self,
        query: str,
        codebase: str,
        *,
        search_scope: Optional[List[str]] = None,
        output_format: Optional[str] = None,
    ) -> Any:
        body: Dict[str, Any] = {"query": query, "codebase": codebase}
        if search_scope:
            body["search_scope"] = search_scope
        if output_format:
            body["output_format"] = output_format
        return self._request("POST", "/advisor", json=body)

    async def aadvisor(
        self,
        query: str,
        codebase: str,
        *,
        search_scope: Optional[List[str]] = None,
        output_format: Optional[str] = None,
    ) -> Any:
        body: Dict[str, Any] = {"query": query, "codebase": codebase}
        if search_scope:
            body["search_scope"] = search_scope
        if output_format:
            body["output_format"] = output_format
        return await self._arequest("POST", "/advisor", json=body)

    # ── Sources ──────────────────────────────────────────────────────────

    def source_create(
        self,
        *,
        url: Optional[str] = None,
        type_: Optional[str] = None,
        display_name: Optional[str] = None,
        branch: Optional[str] = None,
        url_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
        check_llms_txt: Optional[bool] = None,
        repository: Optional[str] = None,
        **kwargs: Any,
    ) -> Any:
        body: Dict[str, Any] = {}
        if url:
            body["url"] = url
        if type_:
            body["type"] = type_
        if display_name:
            body["display_name"] = display_name
        if branch:
            body["branch"] = branch
        if url_patterns:
            body["url_patterns"] = url_patterns
        if exclude_patterns:
            body["exclude_patterns"] = exclude_patterns
        if check_llms_txt is not None:
            body["check_llms_txt"] = check_llms_txt
        if repository:
            body["repository"] = repository
        body.update(kwargs)
        return self._request("POST", "/sources", json=body)

    async def asource_create(
        self,
        *,
        url: Optional[str] = None,
        type_: Optional[str] = None,
        display_name: Optional[str] = None,
        branch: Optional[str] = None,
        url_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
        check_llms_txt: Optional[bool] = None,
        repository: Optional[str] = None,
        **kwargs: Any,
    ) -> Any:
        body: Dict[str, Any] = {}
        if url:
            body["url"] = url
        if type_:
            body["type"] = type_
        if display_name:
            body["display_name"] = display_name
        if branch:
            body["branch"] = branch
        if url_patterns:
            body["url_patterns"] = url_patterns
        if exclude_patterns:
            body["exclude_patterns"] = exclude_patterns
        if check_llms_txt is not None:
            body["check_llms_txt"] = check_llms_txt
        if repository:
            body["repository"] = repository
        body.update(kwargs)
        return await self._arequest("POST", "/sources", json=body)

    def sources_list(
        self,
        *,
        type_: Optional[str] = None,
        query: Optional[str] = None,
        status: Optional[str] = None,
        category_id: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> Any:
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if type_:
            params["type"] = type_
        if query:
            params["query"] = query
        if status:
            params["status"] = status
        if category_id:
            params["category_id"] = category_id
        return self._request("GET", "/sources", params=params)

    async def asources_list(
        self,
        *,
        type_: Optional[str] = None,
        query: Optional[str] = None,
        status: Optional[str] = None,
        category_id: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> Any:
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if type_:
            params["type"] = type_
        if query:
            params["query"] = query
        if status:
            params["status"] = status
        if category_id:
            params["category_id"] = category_id
        return await self._arequest("GET", "/sources", params=params)

    def source_subscribe(
        self,
        url: str,
        *,
        source_type: Optional[str] = None,
        ref: Optional[str] = None,
    ) -> Any:
        body: Dict[str, Any] = {"url": url}
        if source_type:
            body["source_type"] = source_type
        if ref:
            body["ref"] = ref
        return self._request("POST", "/sources/subscribe", json=body)

    async def asource_subscribe(
        self,
        url: str,
        *,
        source_type: Optional[str] = None,
        ref: Optional[str] = None,
    ) -> Any:
        body: Dict[str, Any] = {"url": url}
        if source_type:
            body["source_type"] = source_type
        if ref:
            body["ref"] = ref
        return await self._arequest("POST", "/sources/subscribe", json=body)

    def source_sync(self, source_id: str) -> Any:
        return self._request("POST", f"/sources/{source_id}/sync")

    async def asource_sync(self, source_id: str) -> Any:
        return await self._arequest("POST", f"/sources/{source_id}/sync")

    def source_content(
        self,
        source_id: str,
        *,
        path: Optional[str] = None,
        url: Optional[str] = None,
        branch: Optional[str] = None,
        page: Optional[int] = None,
        line_start: Optional[int] = None,
        line_end: Optional[int] = None,
        type_: Optional[str] = None,
    ) -> Any:
        params: Dict[str, Any] = {}
        if path:
            params["path"] = path
        if url:
            params["url"] = url
        if branch:
            params["branch"] = branch
        if page is not None:
            params["page"] = page
        if line_start is not None:
            params["line_start"] = line_start
        if line_end is not None:
            params["line_end"] = line_end
        if type_:
            params["type"] = type_
        return self._request("GET", f"/sources/{source_id}/content", params=params)

    async def asource_content(
        self,
        source_id: str,
        *,
        path: Optional[str] = None,
        url: Optional[str] = None,
        branch: Optional[str] = None,
        page: Optional[int] = None,
        line_start: Optional[int] = None,
        line_end: Optional[int] = None,
        type_: Optional[str] = None,
    ) -> Any:
        params: Dict[str, Any] = {}
        if path:
            params["path"] = path
        if url:
            params["url"] = url
        if branch:
            params["branch"] = branch
        if page is not None:
            params["page"] = page
        if line_start is not None:
            params["line_start"] = line_start
        if line_end is not None:
            params["line_end"] = line_end
        if type_:
            params["type"] = type_
        return await self._arequest(
            "GET", f"/sources/{source_id}/content", params=params
        )

    def source_grep(
        self,
        source_id: str,
        pattern: str,
        *,
        file_extensions: Optional[List[str]] = None,
        context_lines: Optional[int] = None,
        type_: Optional[str] = None,
    ) -> Any:
        body: Dict[str, Any] = {"pattern": pattern}
        if file_extensions:
            body["file_extensions"] = file_extensions
        if context_lines is not None:
            body["context_lines"] = context_lines
        params: Dict[str, Any] = {}
        if type_:
            params["type"] = type_
        return self._request(
            "POST", f"/sources/{source_id}/grep", json=body, params=params
        )

    async def asource_grep(
        self,
        source_id: str,
        pattern: str,
        *,
        file_extensions: Optional[List[str]] = None,
        context_lines: Optional[int] = None,
        type_: Optional[str] = None,
    ) -> Any:
        body: Dict[str, Any] = {"pattern": pattern}
        if file_extensions:
            body["file_extensions"] = file_extensions
        if context_lines is not None:
            body["context_lines"] = context_lines
        params: Dict[str, Any] = {}
        if type_:
            params["type"] = type_
        return await self._arequest(
            "POST", f"/sources/{source_id}/grep", json=body, params=params
        )

    def source_tree(
        self,
        source_id: str,
        *,
        branch: Optional[str] = None,
        max_depth: Optional[int] = None,
    ) -> Any:
        params: Dict[str, Any] = {}
        if branch:
            params["branch"] = branch
        if max_depth is not None:
            params["max_depth"] = max_depth
        return self._request("GET", f"/sources/{source_id}/tree", params=params)

    async def asource_tree(
        self,
        source_id: str,
        *,
        branch: Optional[str] = None,
        max_depth: Optional[int] = None,
    ) -> Any:
        params: Dict[str, Any] = {}
        if branch:
            params["branch"] = branch
        if max_depth is not None:
            params["max_depth"] = max_depth
        return await self._arequest("GET", f"/sources/{source_id}/tree", params=params)

    # ── GitHub ───────────────────────────────────────────────────────────

    def github_search(
        self,
        query: str,
        repository: str,
        *,
        language: Optional[str] = None,
    ) -> Any:
        body: Dict[str, Any] = {"query": query, "repository": repository}
        if language:
            body["language"] = language
        return self._request("POST", "/github/search", json=body)

    async def agithub_search(
        self,
        query: str,
        repository: str,
        *,
        language: Optional[str] = None,
    ) -> Any:
        body: Dict[str, Any] = {"query": query, "repository": repository}
        if language:
            body["language"] = language
        return await self._arequest("POST", "/github/search", json=body)

    def github_read(
        self,
        repository: str,
        path: str,
        *,
        ref: Optional[str] = None,
        start_line: Optional[int] = None,
        end_line: Optional[int] = None,
    ) -> Any:
        body: Dict[str, Any] = {"repository": repository, "path": path}
        if ref:
            body["ref"] = ref
        if start_line is not None:
            body["start_line"] = start_line
        if end_line is not None:
            body["end_line"] = end_line
        return self._request("POST", "/github/read", json=body)

    async def agithub_read(
        self,
        repository: str,
        path: str,
        *,
        ref: Optional[str] = None,
        start_line: Optional[int] = None,
        end_line: Optional[int] = None,
    ) -> Any:
        body: Dict[str, Any] = {"repository": repository, "path": path}
        if ref:
            body["ref"] = ref
        if start_line is not None:
            body["start_line"] = start_line
        if end_line is not None:
            body["end_line"] = end_line
        return await self._arequest("POST", "/github/read", json=body)

    def github_glob(
        self,
        repository: str,
        pattern: str,
        *,
        ref: Optional[str] = None,
    ) -> Any:
        body: Dict[str, Any] = {"repository": repository, "pattern": pattern}
        if ref:
            body["ref"] = ref
        return self._request("POST", "/github/glob", json=body)

    async def agithub_glob(
        self,
        repository: str,
        pattern: str,
        *,
        ref: Optional[str] = None,
    ) -> Any:
        body: Dict[str, Any] = {"repository": repository, "pattern": pattern}
        if ref:
            body["ref"] = ref
        return await self._arequest("POST", "/github/glob", json=body)

    def github_tree(
        self,
        owner: str,
        repo: str,
        *,
        ref: Optional[str] = None,
        path: Optional[str] = None,
    ) -> Any:
        params: Dict[str, Any] = {}
        if ref:
            params["ref"] = ref
        if path:
            params["path"] = path
        return self._request("GET", f"/github/tree/{owner}/{repo}", params=params)

    async def agithub_tree(
        self,
        owner: str,
        repo: str,
        *,
        ref: Optional[str] = None,
        path: Optional[str] = None,
    ) -> Any:
        params: Dict[str, Any] = {}
        if ref:
            params["ref"] = ref
        if path:
            params["path"] = path
        return await self._arequest(
            "GET", f"/github/tree/{owner}/{repo}", params=params
        )

    # ── Contexts ─────────────────────────────────────────────────────────

    def context_save(
        self,
        title: str,
        summary: str,
        content: str,
        *,
        agent_source: Optional[str] = None,
        tags: Optional[List[str]] = None,
        memory_type: Optional[str] = None,
    ) -> Any:
        body: Dict[str, Any] = {
            "title": title,
            "summary": summary,
            "content": content,
        }
        if agent_source:
            body["agent_source"] = agent_source
        if tags:
            body["tags"] = tags
        if memory_type:
            body["memory_type"] = memory_type
        return self._request("POST", "/contexts", json=body)

    async def acontext_save(
        self,
        title: str,
        summary: str,
        content: str,
        *,
        agent_source: Optional[str] = None,
        tags: Optional[List[str]] = None,
        memory_type: Optional[str] = None,
    ) -> Any:
        body: Dict[str, Any] = {
            "title": title,
            "summary": summary,
            "content": content,
        }
        if agent_source:
            body["agent_source"] = agent_source
        if tags:
            body["tags"] = tags
        if memory_type:
            body["memory_type"] = memory_type
        return await self._arequest("POST", "/contexts", json=body)

    def context_search(
        self,
        q: str,
        *,
        limit: int = 20,
        include_highlights: bool = False,
    ) -> Any:
        params: Dict[str, Any] = {
            "q": q,
            "limit": limit,
            "include_highlights": include_highlights,
        }
        return self._request("GET", "/contexts/semantic-search", params=params)

    async def acontext_search(
        self,
        q: str,
        *,
        limit: int = 20,
        include_highlights: bool = False,
    ) -> Any:
        params: Dict[str, Any] = {
            "q": q,
            "limit": limit,
            "include_highlights": include_highlights,
        }
        return await self._arequest("GET", "/contexts/semantic-search", params=params)

    # ── Dependencies ─────────────────────────────────────────────────────

    def dependency_subscribe(
        self,
        manifest_content: str,
        *,
        manifest_type: Optional[str] = None,
    ) -> Any:
        body: Dict[str, Any] = {"manifest_content": manifest_content}
        if manifest_type:
            body["manifest_type"] = manifest_type
        return self._request("POST", "/dependencies/subscribe", json=body)

    async def adependency_subscribe(
        self,
        manifest_content: str,
        *,
        manifest_type: Optional[str] = None,
    ) -> Any:
        body: Dict[str, Any] = {"manifest_content": manifest_content}
        if manifest_type:
            body["manifest_type"] = manifest_type
        return await self._arequest("POST", "/dependencies/subscribe", json=body)

    def dependency_analyze(
        self,
        manifest_content: str,
        *,
        manifest_type: Optional[str] = None,
    ) -> Any:
        body: Dict[str, Any] = {"manifest_content": manifest_content}
        if manifest_type:
            body["manifest_type"] = manifest_type
        return self._request("POST", "/dependencies/analyze", json=body)

    async def adependency_analyze(
        self,
        manifest_content: str,
        *,
        manifest_type: Optional[str] = None,
    ) -> Any:
        body: Dict[str, Any] = {"manifest_content": manifest_content}
        if manifest_type:
            body["manifest_type"] = manifest_type
        return await self._arequest("POST", "/dependencies/analyze", json=body)


def _strip_none(params: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if params is None:
        return None
    return {k: v for k, v in params.items() if v is not None}
