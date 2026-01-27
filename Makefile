.PHONY: install dev test lint format clean run

install:
	poetry install

dev:
	poetry install --with dev

test:
	poetry run pytest tests/ -v

test-cov:
	poetry run pytest tests/ -v --cov=clawdbot --cov-report=html

lint:
	poetry run ruff check clawdbot/
	poetry run mypy clawdbot/

format:
	poetry run black clawdbot/ tests/
	poetry run ruff check --fix clawdbot/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf dist/ build/ *.egg-info
	rm -rf .pytest_cache/ .coverage htmlcov/

run:
	poetry run clawdbot gateway start

run-web:
	poetry run uvicorn clawdbot.web.app:app --reload --host 0.0.0.0 --port 8080

doctor:
	poetry run clawdbot doctor

onboard:
	poetry run clawdbot onboard
