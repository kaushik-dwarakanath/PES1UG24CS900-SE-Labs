# L6_L7_59 — Phone Repair Quote

Lab 7: Fuzzing for Input Validation Bugs

## About

A small Python module that reads phone repair quote details typed in by a user: IMEI numbers, parts orders and phone models. It assumes every input is well formed.

## Files

| File | Description |
|------|-------------|
| `phone_repair_quote_parser.py` | The buggy module you will fuzz and fix |
| `test_phone_repair_quote_parser.py` | Hypothesis test template to complete |

Keep all your Lab 7 work in this `LAB7` folder.

Follow the lab handout for the full instructions. Use the file names above wherever the handout refers to the code and test files.

## Screenshots

| Screenshot | What it must show |
|------------|-------------------|
| SS1 | `python phone_repair_quote_parser.py` run on the buggy module |
| SS2 | `pytest test_phone_repair_quote_parser.py` with your completed tests failing on the buggy module |
| SS3 | `python phone_repair_quote_parser.py` run on your fixed module |
| SS4 | `pytest test_phone_repair_quote_parser.py` with all tests passing on your fixed module |

## Deliverables

Commit these three files in this `LAB7` folder:

1. `phone_repair_quote_parser.py`: your fixed module. All three functions must handle any input without crashing.
2. `test_phone_repair_quote_parser.py`: your completed Hypothesis tests, one for each of the three functions.
3. `SRN_NAME_LAB7.pdf`: screenshots SS1 to SS4 and your answers to the three reflection questions in the handout.

Be ready to explain the bugs you found and how you fixed them. You may be called on to present.

## Completed work

Student: **Kaushik Krishna Dwarakanath**, **PES1UG24CS900**, Section **5-B**.

The consolidated submission is `PES1UG24CS900_Kaushik_Krishna_Dwarakanath_LAB7.pdf`.
It contains actual screenshots SS1–SS4, bug analysis, three learning reflections,
and the complete final application and test source code. The supplied handout
contains no numbered reflection questions; the report identifies its three
reflection prompts as supplementary.

Final validation: **23 tests pass** (three Hypothesis properties with 500
passing examples each, plus 20 deterministic regression cases). Before fixing
the parser, all three fuzz tests failed. Actual screenshots and text logs are in
[`evidence/`](evidence/README.md). The original parser is preserved there and in
baseline commit `ffb09ca`; the final tests are the same tests used for the baseline.

### Run locally

The recorded environment uses Python 3.15.0. The pinned dependencies require
Python 3.10 or newer; the parser itself uses Python 3.8-compatible syntax.

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python phone_repair_quote_parser.py
python -m pytest test_phone_repair_quote_parser.py
python -m pytest test_phone_repair_quote_parser.py --hypothesis-show-statistics
python tools/build_report.py
```

### Defined input behavior

- `mask_imei`: remove ASCII spaces and dashes, mask all but the last four
  ASCII digits; return `""` for empty, non-string, or non-digit input. Strings
  of at most four digits remain visible. This helper does not check IMEI length
  or checksum.
- `parse_parts_order`: accept `part xQTY` entries separated by semicolons.
  Require whitespace before lowercase `x` and a positive ASCII integer quantity
  of at most 4300 digits. Skip invalid entries, retain valid entries, and keep
  the last valid value for duplicate part names. Return `{}` for non-strings.
- `parse_model`: normalize whitespace and title-case the brand. A brand alone
  returns `(brand, "")`; empty or non-string values return `("", "")`.

The test functions use the requested `try`/`except` pattern to report crashes as
test failures. Assertions also check output types, masking and parsing behavior.
Finite fuzz testing does not prove correctness for every possible input.

### Submission

Push the local commits, then upload the consolidated PDF to the Google Form
linked in `lab7_info.png`. No remote push or form submission was performed.
