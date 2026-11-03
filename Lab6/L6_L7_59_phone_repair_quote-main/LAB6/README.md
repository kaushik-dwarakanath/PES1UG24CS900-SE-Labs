# L6_L7_59 — Phone Repair Quote

Lab 6: Code and Branch Coverage

## About

A small Python module that quotes phone repairs by part, brand tier, warranty and express service, estimates turnaround time and values phones offered for trade-in.

## Files

| File | Description |
|------|-------------|
| `phone_repair_quote.py` | The module under test |
| `test_phone_repair_quote.py` | Starter test file |

Keep all your Lab 6 work in this `LAB6` folder. Lab 7 will be added to this repo later.

Refer to the lab handout for instructions.

## Lab 6 submission — PES1UG24CS900

Create an environment and install the pinned dependencies:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Run these commands from this `LAB6` directory (with the environment active):

```sh
python -m coverage run --data-file=.coverage.code --source=phone_repair_quote -m pytest -q CodeCoverageTest_PES1UG24CS900_phone_repair_quote.py
python -m coverage report --data-file=.coverage.code -m --fail-under=100
```

The code coverage suite passes 14 tests with 100% statement coverage. Results
and the coverage analysis are in [reports](reports/analysis.md).

Run the branch suite independently:

```sh
python -m coverage run --data-file=.coverage.branch --branch --source=phone_repair_quote -m pytest -q BranchCoverageTest_PES1UG24CS900_phone_repair_quote.py
python -m coverage report --data-file=.coverage.branch -m --fail-under=100
```

The branch suite passes 115 tests with 100% statement and branch coverage
(40/40 statements, 28/28 branch outcomes, no partial branches).

Run all tests, including the two starter tests:

```sh
python -m coverage run --branch --source=phone_repair_quote -m pytest -q
python -m coverage report -m --fail-under=100
```

All 131 tests pass. `pytest.ini` includes both assignment filenames in test
discovery. The application code remains as supplied. Only application coverage
is measured; no lines or branches are excluded.

The submission PDF is
[Lab 6 report](reports/PES1UG24CS900_Lab6_Report.pdf). It includes the coverage
analysis, final terminal screenshots, and the complete separate test files.
