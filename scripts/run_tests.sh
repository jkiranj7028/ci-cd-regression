#!/usr/bin/env bash
set -euo pipefail

group="${1:-all}"

case "$group" in
  smoke) pytest -m "smoke" -n auto ;;
  unit) pytest tests/unit -n auto ;;
  integration) pytest -m "integration" -n auto ;;
  regression) pytest -m "regression" -n auto ;;
  all) pytest -n auto --cov=app --cov-report=xml --cov-report=html ;;
  *) echo "Usage: $0 [smoke|unit|integration|regression|all]"; exit 1 ;;
esac
