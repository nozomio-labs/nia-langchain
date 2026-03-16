"""Compilation test — ensures integration test module imports without errors."""

import pytest


@pytest.mark.compile
def test_placeholder() -> None:
    """Placeholder so the integration_tests package is never empty."""
