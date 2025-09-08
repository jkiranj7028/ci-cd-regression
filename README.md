# CI/CD Pipeline with Fast & Reliable Regression Testing

This project is a real-world, ready-to-run example of a CI/CD pipeline designed for **speedy feedback** and **reliable regression testing**.
It includes a small Flask API, unit/integration/regression tests, a Jenkins pipeline, and a GitHub Actions workflow.

## Goals
- ⚡ Fast feedback via **parallel** test execution and **smoke vs regression** partitioning.
- ✅ Reliability via **regression tests** that lock-in previous bug fixes.
- 📦 Consistency via Docker, pinned dependencies, and reproducible commands.
- 📈 Quality gates using **coverage** and **JUnit** reports.

---

## Project Structure
```text
app/                     # Minimal Flask API & business logic
tests/
  unit/                  # Pure unit tests
  integration/           # API tests using Flask test client
  regression/            # Tests that reproduce past bugs
scripts/
  run_tests.sh           # Helper to run test groups locally
Jenkinsfile              # Jenkins pipeline with parallel stages
.github/workflows/ci.yml # GitHub Actions pipeline (matrix + caching)
Dockerfile               # Containerize the app
docker-compose.yml       # Local run
requirements.txt         # Python deps
pytest.ini               # Markers & defaults
Makefile                 # Developer-friendly commands
```

---

## How the Pipeline Ensures Speed **and** Reliability

1. **Test Partitioning**
   - `smoke`: fastest, critical-path checks (run on every push, PR).
   - `unit`: fast logic checks (run on every push, PR).
   - `integration`: API-level tests (parallelized).
   - `regression`: a curated suite that reproduces fixed bugs to prevent regressions.

2. **Parallel Execution**
   - Jenkins uses a `parallel` block to run `unit`, `integration`, and `regression` concurrently.
   - Pytest uses `xdist` to run tests across CPU cores (`-n auto`).

3. **Selective Runs (optional pattern)**
   - You can scope runs using markers, e.g. `pytest -m "smoke"` for PRs touching only docs/config,
     and run full `regression` on merges to `main` or nightly.

4. **Artifacts and Quality Gates**
   - JUnit XML results and coverage (`coverage.xml`, `htmlcov/`) are archived.
   - Fail the build if coverage < threshold (see `--cov-fail-under`).

---

## Run Locally

```bash
# 1) Create venv & install
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) Run smoke tests (super fast)
pytest -m "smoke" -n auto

# 3) Run everything with coverage
pytest -n auto --cov=app --cov-report=term-missing --cov-report=xml --cov-report=html
# open htmlcov/index.html in a browser to view coverage
```

### Docker
```bash
docker build -t ci-cd-regression:local .
docker run -p 8000:8000 ci-cd-regression:local
curl http://localhost:8000/health
```

---

## Jenkins (Declarative Pipeline)

- Add a multibranch pipeline or a pipeline project pointing to this repo.
- Ensure a node/agent with Docker and Python (or use Docker-in-Docker).
- The `Jenkinsfile` already:
  - Caches pip directory between builds (workspace-local).
  - Runs tests in **parallel** with JUnit + coverage artifacts.
  - Builds a Docker image (optional publish step is stubbed).

---

## GitHub Actions

- Workflow in `.github/workflows/ci.yml` uses:
  - Dependency caching
  - Matrix strategy to split tests by group (unit, integration, regression)
  - Coverage upload as an artifact

---

## API Endpoints

- `GET /health` → `{"status": "ok"}`
- `POST /sum` (body: `{"numbers": [1,2,3]}`) → `{"result": 6.0}`
- `GET /divide?a=10&b=2` → `{"result": 5.0}`

---

## Regression Philosophy

Each time a bug is fixed, add a test in `tests/regression/` that reproduces the scenario.
This suite guards against backsliding while keeping the baseline fast.

---

## Make Targets

```bash
make test           # all tests with coverage
make test-smoke     # only smoke tests
make test-unit      # unit tests
make test-int       # integration tests
make test-reg       # regression tests
```
