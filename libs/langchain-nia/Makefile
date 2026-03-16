.PHONY: all format lint test tests integration_test integration_tests help

all: help

.EXPORT_ALL_VARIABLES:
UV_FROZEN = true

TEST_FILE ?= tests/unit_tests/
integration_test integration_tests: TEST_FILE = tests/integration_tests/

test tests:
	uv run --group test pytest --disable-socket --allow-unix-socket $(TEST_FILE)

integration_test integration_tests:
	uv run --group test --group test_integration pytest $(TEST_FILE)

PYTHON_FILES = .
MYPY_CACHE = .mypy_cache
lint_package: PYTHON_FILES = langchain_nia
lint_tests: PYTHON_FILES = tests
lint_tests: MYPY_CACHE = .mypy_cache_test

lint lint_diff lint_package lint_tests:
	[ "$(PYTHON_FILES)" = "" ] || uv run --all-groups ruff check $(PYTHON_FILES)
	[ "$(PYTHON_FILES)" = "" ] || uv run --all-groups ruff format $(PYTHON_FILES) --diff
	[ "$(PYTHON_FILES)" = "" ] || mkdir -p $(MYPY_CACHE) && uv run --all-groups mypy $(PYTHON_FILES) --cache-dir $(MYPY_CACHE)

format format_diff:
	[ "$(PYTHON_FILES)" = "" ] || uv run --all-groups ruff format $(PYTHON_FILES)
	[ "$(PYTHON_FILES)" = "" ] || uv run --all-groups ruff check --fix $(PYTHON_FILES)

help:
	@echo "Available targets:"
	@echo "  test / tests              - Run unit tests"
	@echo "  integration_test(s)       - Run integration tests"
	@echo "  lint                      - Run linters"
	@echo "  format                    - Auto-format code"
