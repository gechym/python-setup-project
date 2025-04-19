.PHONY: lint
lint:
	@echo "🚀 Linting with ruff"
	uvx ruff check --fix
	@echo "🚀 Formatting with ruff"
	uvx ruff format
	@echo "🚀 Linting with pylint"
	uvx pylint ./ --ignore=.venv
	@echo "🚀 Checking with mypy"
	uvx mypy ./
	@echo "🟢 All checks have passed"


	@echo "Clear cache"
	make clean


.PHONY: precommit
precommit:
	@echo "🚀 Running pre-commit hooks"
	uvx pre-commit run --all-files
	@echo "🟢 All pre-commit hooks have passed"
	@echo "🚀 check lint"
	make lint
	@echo "🟢 All checks have passed"

.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	find . | grep -E '(\.mypy_cache|\.ruff_cache|__pycache__|\.pyc|\.pyo$$)' | xargs rm -rf
