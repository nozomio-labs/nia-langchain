"""Standard LangChain unit tests for Nia tools."""

from typing import Type
from unittest.mock import patch

import pytest
from langchain_tests.unit_tests import ToolsUnitTests

from langchain_nia import (
    NiaAdvisor,
    NiaContextSave,
    NiaContextSearch,
    NiaDeepResearch,
    NiaDependencyAnalyze,
    NiaDependencySubscribe,
    NiaExplore,
    NiaGitHubGlob,
    NiaGitHubRead,
    NiaGitHubSearch,
    NiaGitHubTree,
    NiaGrep,
    NiaIndex,
    NiaRead,
    NiaSearch,
    NiaSourceList,
    NiaSourceSubscribe,
    NiaSourceSync,
    NiaUniversalSearch,
    NiaWebSearch,
)

_ENV_PATCH = patch.dict("os.environ", {"NIA_API_KEY": "nk_test_key_for_unit_tests"})


class TestNiaSearch(ToolsUnitTests):
    @pytest.fixture(autouse=True)
    def _set_env(self) -> None:
        with _ENV_PATCH:
            yield  # type: ignore[misc]

    @property
    def tool_constructor(self) -> Type[NiaSearch]:
        return NiaSearch

    @property
    def tool_constructor_params(self) -> dict:
        return {}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {"query": "how to use React hooks"}


class TestNiaWebSearch(ToolsUnitTests):
    @pytest.fixture(autouse=True)
    def _set_env(self) -> None:
        with _ENV_PATCH:
            yield  # type: ignore[misc]

    @property
    def tool_constructor(self) -> Type[NiaWebSearch]:
        return NiaWebSearch

    @property
    def tool_constructor_params(self) -> dict:
        return {}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {"query": "latest Python release"}


class TestNiaDeepResearch(ToolsUnitTests):
    @pytest.fixture(autouse=True)
    def _set_env(self) -> None:
        with _ENV_PATCH:
            yield  # type: ignore[misc]

    @property
    def tool_constructor(self) -> Type[NiaDeepResearch]:
        return NiaDeepResearch

    @property
    def tool_constructor_params(self) -> dict:
        return {}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {"query": "compare React vs Vue"}


class TestNiaUniversalSearch(ToolsUnitTests):
    @pytest.fixture(autouse=True)
    def _set_env(self) -> None:
        with _ENV_PATCH:
            yield  # type: ignore[misc]

    @property
    def tool_constructor(self) -> Type[NiaUniversalSearch]:
        return NiaUniversalSearch

    @property
    def tool_constructor_params(self) -> dict:
        return {}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {"query": "machine learning embeddings"}


class TestNiaAdvisor(ToolsUnitTests):
    @pytest.fixture(autouse=True)
    def _set_env(self) -> None:
        with _ENV_PATCH:
            yield  # type: ignore[misc]

    @property
    def tool_constructor(self) -> Type[NiaAdvisor]:
        return NiaAdvisor

    @property
    def tool_constructor_params(self) -> dict:
        return {}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {
            "query": "is this code correct?",
            "codebase": "def hello(): print('hi')",
        }


class TestNiaIndex(ToolsUnitTests):
    @pytest.fixture(autouse=True)
    def _set_env(self) -> None:
        with _ENV_PATCH:
            yield  # type: ignore[misc]

    @property
    def tool_constructor(self) -> Type[NiaIndex]:
        return NiaIndex

    @property
    def tool_constructor_params(self) -> dict:
        return {}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {"url": "https://github.com/langchain-ai/langchain"}


class TestNiaSourceList(ToolsUnitTests):
    @pytest.fixture(autouse=True)
    def _set_env(self) -> None:
        with _ENV_PATCH:
            yield  # type: ignore[misc]

    @property
    def tool_constructor(self) -> Type[NiaSourceList]:
        return NiaSourceList

    @property
    def tool_constructor_params(self) -> dict:
        return {}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {}


class TestNiaSourceSubscribe(ToolsUnitTests):
    @pytest.fixture(autouse=True)
    def _set_env(self) -> None:
        with _ENV_PATCH:
            yield  # type: ignore[misc]

    @property
    def tool_constructor(self) -> Type[NiaSourceSubscribe]:
        return NiaSourceSubscribe

    @property
    def tool_constructor_params(self) -> dict:
        return {}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {"url": "https://github.com/langchain-ai/langchain"}


class TestNiaSourceSync(ToolsUnitTests):
    @pytest.fixture(autouse=True)
    def _set_env(self) -> None:
        with _ENV_PATCH:
            yield  # type: ignore[misc]

    @property
    def tool_constructor(self) -> Type[NiaSourceSync]:
        return NiaSourceSync

    @property
    def tool_constructor_params(self) -> dict:
        return {}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {"source_id": "src_12345"}


class TestNiaRead(ToolsUnitTests):
    @pytest.fixture(autouse=True)
    def _set_env(self) -> None:
        with _ENV_PATCH:
            yield  # type: ignore[misc]

    @property
    def tool_constructor(self) -> Type[NiaRead]:
        return NiaRead

    @property
    def tool_constructor_params(self) -> dict:
        return {}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {"source_id": "src_12345", "path": "README.md"}


class TestNiaGrep(ToolsUnitTests):
    @pytest.fixture(autouse=True)
    def _set_env(self) -> None:
        with _ENV_PATCH:
            yield  # type: ignore[misc]

    @property
    def tool_constructor(self) -> Type[NiaGrep]:
        return NiaGrep

    @property
    def tool_constructor_params(self) -> dict:
        return {}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {"source_id": "src_12345", "pattern": "def main"}


class TestNiaExplore(ToolsUnitTests):
    @pytest.fixture(autouse=True)
    def _set_env(self) -> None:
        with _ENV_PATCH:
            yield  # type: ignore[misc]

    @property
    def tool_constructor(self) -> Type[NiaExplore]:
        return NiaExplore

    @property
    def tool_constructor_params(self) -> dict:
        return {}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {"source_id": "src_12345"}


class TestNiaGitHubSearch(ToolsUnitTests):
    @pytest.fixture(autouse=True)
    def _set_env(self) -> None:
        with _ENV_PATCH:
            yield  # type: ignore[misc]

    @property
    def tool_constructor(self) -> Type[NiaGitHubSearch]:
        return NiaGitHubSearch

    @property
    def tool_constructor_params(self) -> dict:
        return {}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {"query": "BaseTool", "repository": "langchain-ai/langchain"}


class TestNiaGitHubRead(ToolsUnitTests):
    @pytest.fixture(autouse=True)
    def _set_env(self) -> None:
        with _ENV_PATCH:
            yield  # type: ignore[misc]

    @property
    def tool_constructor(self) -> Type[NiaGitHubRead]:
        return NiaGitHubRead

    @property
    def tool_constructor_params(self) -> dict:
        return {}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {"repository": "langchain-ai/langchain", "path": "README.md"}


class TestNiaGitHubGlob(ToolsUnitTests):
    @pytest.fixture(autouse=True)
    def _set_env(self) -> None:
        with _ENV_PATCH:
            yield  # type: ignore[misc]

    @property
    def tool_constructor(self) -> Type[NiaGitHubGlob]:
        return NiaGitHubGlob

    @property
    def tool_constructor_params(self) -> dict:
        return {}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {"repository": "langchain-ai/langchain", "pattern": "*.py"}


class TestNiaGitHubTree(ToolsUnitTests):
    @pytest.fixture(autouse=True)
    def _set_env(self) -> None:
        with _ENV_PATCH:
            yield  # type: ignore[misc]

    @property
    def tool_constructor(self) -> Type[NiaGitHubTree]:
        return NiaGitHubTree

    @property
    def tool_constructor_params(self) -> dict:
        return {}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {"owner": "langchain-ai", "repo": "langchain"}


class TestNiaContextSave(ToolsUnitTests):
    @pytest.fixture(autouse=True)
    def _set_env(self) -> None:
        with _ENV_PATCH:
            yield  # type: ignore[misc]

    @property
    def tool_constructor(self) -> Type[NiaContextSave]:
        return NiaContextSave

    @property
    def tool_constructor_params(self) -> dict:
        return {}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {
            "title": "Test context",
            "summary": "A test",
            "content": "Test content",
        }


class TestNiaContextSearch(ToolsUnitTests):
    @pytest.fixture(autouse=True)
    def _set_env(self) -> None:
        with _ENV_PATCH:
            yield  # type: ignore[misc]

    @property
    def tool_constructor(self) -> Type[NiaContextSearch]:
        return NiaContextSearch

    @property
    def tool_constructor_params(self) -> dict:
        return {}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {"q": "React hooks tutorial"}


class TestNiaDependencySubscribe(ToolsUnitTests):
    @pytest.fixture(autouse=True)
    def _set_env(self) -> None:
        with _ENV_PATCH:
            yield  # type: ignore[misc]

    @property
    def tool_constructor(self) -> Type[NiaDependencySubscribe]:
        return NiaDependencySubscribe

    @property
    def tool_constructor_params(self) -> dict:
        return {}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {"manifest_content": '{"dependencies": {"react": "^18.0.0"}}'}


class TestNiaDependencyAnalyze(ToolsUnitTests):
    @pytest.fixture(autouse=True)
    def _set_env(self) -> None:
        with _ENV_PATCH:
            yield  # type: ignore[misc]

    @property
    def tool_constructor(self) -> Type[NiaDependencyAnalyze]:
        return NiaDependencyAnalyze

    @property
    def tool_constructor_params(self) -> dict:
        return {}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {"manifest_content": '{"dependencies": {"react": "^18.0.0"}}'}
