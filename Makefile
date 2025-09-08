.PHONY: test test-smoke test-unit test-int test-reg

test:
	pytest -n auto --cov=app --cov-report=term-missing --cov-report=xml --cov-report=html

test-smoke:
	pytest -m "smoke" -n auto

test-unit:
	pytest tests/unit -n auto

test-int:
	pytest -m "integration" -n auto

test-reg:
	pytest -m "regression" -n auto
