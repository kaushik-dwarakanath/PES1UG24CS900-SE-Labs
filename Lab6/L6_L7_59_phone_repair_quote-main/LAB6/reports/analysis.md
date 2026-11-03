# Lab 6: Coverage analysis

Student: PES1UG24CS900  
Application: L6_L7_59 — Phone Repair Quote

## Initial tests

The two supplied tests passed. Measurement was restricted to
`phone_repair_quote.py`, so test code does not inflate application coverage.

| Measurement | Covered | Total | Percentage |
| --- | ---: | ---: | ---: |
| Statements | 18 | 40 | 45% |
| Branch outcomes | 8 | 28 | 28.57% |

The initial branch-mode report displayed 38%, which combines statements and
branch outcomes: (18 + 8) / (40 + 28). It is not the branch-only percentage.
Untested statements were 6, 8, 11, 15, 17, 20, 26, 30–33 and 38–50.
There were eight partially covered decisions. Trade-in valuation was not called.
No screenshots of the initial results are included, as instructed by the handout.

## Code coverage

`CodeCoverageTest_PES1UG24CS900_phone_repair_quote.py` contains 14 test cases.
All pass, exercising all 40 statements (100% statement coverage).

The tests cover valid quotes, invalid parts and brand tiers, flagship pricing,
labour rates, warranty discounts, express fees, available and unavailable
technicians, stock delays, each depreciation bracket, cracked-screen deductions,
old phones and invalid prices. Expected prices and turnaround times are checked
explicitly rather than merely invoking the functions.

Evidence: `code_coverage.txt` and `code_coverage.png` in this directory.

## Interpreting the measurements

Statement coverage checks whether each executable statement was reached. Branch
coverage checks whether every decision took each outgoing path. Neither proves
that every combination or every possible execution path has been tested. Python
short-circuit expressions also need specific input combinations beyond what the
branch percentage alone establishes. Tests must assert correct results as well
as execute the relevant paths.
