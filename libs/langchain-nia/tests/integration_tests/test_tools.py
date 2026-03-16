"""Standard LangChain integration tests for Nia tools.

These tests require a real NIA_API_KEY environment variable.
"""

from typing import Type

from langchain_tests.integration_tests import ToolsIntegrationTests

from langchain_nia import NiaSearch, NiaWebSearch


class TestNiaSearchIntegration(ToolsIntegrationTests):
    @property
    def tool_constructor(self) -> Type[NiaSearch]:
        return NiaSearch

    @property
    def tool_constructor_params(self) -> dict:
        return {}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {"query": "how to use React hooks"}


class TestNiaWebSearchIntegration(ToolsIntegrationTests):
    @property
    def tool_constructor(self) -> Type[NiaWebSearch]:
        return NiaWebSearch

    @property
    def tool_constructor_params(self) -> dict:
        return {}

    @property
    def tool_invoke_params_example(self) -> dict:
        return {"query": "Python 3.12 new features"}
