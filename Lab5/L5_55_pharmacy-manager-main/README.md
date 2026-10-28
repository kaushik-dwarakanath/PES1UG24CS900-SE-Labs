# Lab 5: Static Code Analysis — Pharmacy Management System

Cleaned pharmacy inventory and billing demonstration, with documented findings,
original evidence, final analysis reports and behavioral regression tests.

From the Lab5 directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r L5_55_pharmacy-manager-main/requirements-dev.txt
python L5_55_pharmacy-manager-main/verify.py
```

The verification command regenerates all final reports and exits nonzero if any
analyzer, test or standalone demo fails. All tools use their default rules;
Pylint persistence is disabled only to avoid cache writes. The recorded run used
Python 3.14.8, Pylint 4.1.3, Bandit 1.9.4 and Flake8 7.4.1. The application
uses Python 3.10+ syntax; pinned development tools were verified on Python 3.14.

Run individual checks from this project directory with the environment active:

```bash
python -m pylint --persistent=n pharmacy_manager.py
python -m bandit -r pharmacy_manager.py
python -m flake8 pharmacy_manager.py
python -m unittest discover -v
python pharmacy_manager.py
```

The demo writes `pharmacy.json` to its working directory. Verification runs it in
a temporary directory. Login returns false unless PHARMACY_PASSWORD is configured;
the demo checks the configured value to illustrate the login function. It is not
an interactive authentication interface. Never commit real credentials.

- `issues.md`: prioritized findings, original line numbers, fixes and limitations.
- `reports/before/`: original source snapshot, original demo and analyzer outputs.
- `reports/after/`: final analyzer outputs, nine passing tests and demo output.
- `requirements-dev.txt`: exact tool environment used to generate evidence.
- `test_pharmacy_manager.py`: regression tests for security and inventory bugs.

The three implementation commits address Bandit security findings, Pylint quality
and behavior, then Flake8 formatting and final evidence. Reflection files are
omitted at the user's request; the handout discrepancy is recorded in issues.md.
