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

## Branch coverage

`BranchCoverageTest_PES1UG24CS900_phone_repair_quote.py` independently passes
115 test cases. It covers 40/40 statements and 28/28 branch outcomes: **100%
statement coverage and 100% branch coverage**, with no partial branches or
excluded statements. The application was not modified.

| Area | Cases | Decisions and boundaries checked |
| --- | ---: | --- |
| Quotes | 32 | All four parts, both brand tiers, both warranty states, both express states |
| Quote validation | 7 | Unknown/empty/case-sensitive names, both invalid inputs and validation order |
| Turnaround | 24 | Every part, both stock states, zero/one/multiple free technicians |
| Trade-in age | 24 | Ages 0, 1, 11, 12, 13, 23, 24, 25, 47, 48, 49, 60; both screen conditions |
| Trade-in rounding | 18 | Prices 1, 101, 9999 across all depreciation brackets; both screen conditions |
| Trade-in validation | 10 | Zero/negative prices, negative age, both invalid, invalid price after 48 months; both screen conditions |

The warranty AND condition is checked with warranty false, warranty true for a
screen, and warranty true for each non-screen part. The stock-delay OR condition
is checked with screen, camera and neither. The validation OR condition is checked
with an invalid price, a valid price and negative age, and both valid. These cases
exercise short-circuit behavior that a percentage alone does not establish.

Evidence: `branch_coverage.txt` and `branch_coverage.png` in this directory.

The code suite already reaches every statement. The branch suite adds systematic
combinations, threshold neighbors, integer rounding and validation precedence,
and measures branches explicitly. Both suites run independently; neither imports
tests from the other. The final combined run includes the two starter tests:
14 + 115 + 2 = **131 passing tests**.
