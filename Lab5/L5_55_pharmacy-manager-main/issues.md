# Issue register

Line numbers refer to the unchanged original in
`reports/before/pharmacy_manager.py.txt`. Bandit severity is reported as given
by the tool; other categories describe quality or behavioral impact.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| B605 shell injection | Security / High | 68 | Medicine text is concatenated into a shell command. | Print the label directly; shell metacharacters remain literal text. |
| B324 weak digest | Security / High | 51 | MD5 is unsuitable for security-sensitive identification. | SHA-256 over a JSON array also removes ambiguity between concatenated fields. |
| B307 arbitrary evaluation | Security / Medium | 48 | Doctor-note text can execute Python code through eval. | Parse an AST and allow only bounded numeric constants, +, -, *, / and unary minus; reject calls, names, powers and invalid arithmetic. |
| B301 unsafe deserialization | Security / Medium | 64 | Loading pickle can execute attacker-controlled code. | Use JSON; validate the complete schema and values before replacing live inventory. |
| B403 pickle import | Security / Low | 3 | Unsafe serialization dependency. | Remove pickle entirely. |
| B105 embedded credential | Security / Low | 11 | Password is stored in source control. | Read PHARMACY_PASSWORD from the environment; missing configuration fails closed; compare with secrets.compare_digest. |
| B110 silent exception handling; W0702 bare except | Security / Low; reliability | 23–28 | Failures disappear, hiding missing stock and programming mistakes. | Validate explicit failure conditions and raise ValueError; demo handles the expected missing-stock error. |
| B311 predictable randomness | Security / Low | 54 | Default random generator is unsuitable for sensitive references. | Use secrets.randbelow; document that six-digit references do not guarantee uniqueness. |
| W0102 mutable default | Bug | 13, 19 | Audit lists leak entries between unrelated calls. | Default to None; allocate a new list per call while supporting caller-provided lists. |
| W0611 unused imports | Maintainability | 2, 6 | sys and logging are unused. | Remove unused imports. |
| C0114/C0116 missing documentation | Maintainability | 1, 13–89 | Module and functions lack clear contracts. | Add module/function docstrings describing behavior and limitations. |
| C0103 naming | Maintainability | 10, 13–89 | Mixed-case function names and mutable global naming violate conventions. | Use snake_case functions and an explicit MEDICINES inventory mapping; update callers and tests. |
| R1705/R1703 redundant branches | Maintainability | 35–38, 79–82 | Boolean conditions are expanded into redundant branches. | Return comparisons directly; authentication also validates configuration. |
| R1732/W1514 unmanaged files and encoding | Reliability | 57–65 | Manual close can be skipped on failure; text encoding is unspecified after JSON migration. | Use context managers and explicit UTF-8. |
| E302/E305/E501 spacing and long lines | Style | 13–108, especially 87 and 98 | Missing top-level spacing and overlong statements hinder readability. | Add two blank lines between top-level definitions and wrap statements within 79 columns. |
| Invalid inventory inputs | Behavioral bug (manual review) | 14–18, 92–93 | Numeric names, negative quantities and invalid prices are accepted. | Validate names, integer quantities, finite nonnegative prices and ISO dates before mutation. |
| Unsafe dispensing | Behavioral bug (manual review) | 24–26 | Negative dispensing adds stock; overselling deletes inventory; expired stock can be dispensed. | Require positive integer quantities, sufficient stock and nonexpired medicine; failures leave stock unchanged. |
| Expiry-window boundary | Behavioral bug (manual review) | 74 | Already-expired medicines appear in expiring-soon results. | Use 0 <= days until expiry < window; test today, yesterday and upper boundary. |
| Import side effects | Design (manual review) | 108 | Importing executes the demo and writes a file. | Guard main with __name__ == '__main__'. |

## Verification

The original program ran successfully but printed negative stock and a numeric
medicine name. Its Pylint score was **4.83/10**. Bandit reported **8 issues**
(2 high, 2 medium, 4 low); Flake8 reported formatting and import violations.

Final unfiltered checks report **Pylint 10.00/10**, **zero Bandit issues** and
**zero Flake8 findings**. Nine regression tests pass, covering independent audit
lists, invalid inputs, dispensing atomicity, expiry boundaries, billing, rejected
executable expressions, JSON validation, configured login and literal labels.
The standalone demo also exits successfully. Reports are stored under
`reports/before/` and `reports/after/`. No rules are disabled or suppressed.

Static checks cannot establish domain correctness: the inventory and expiry bugs
required manual review and behavioral tests. This is a lab demonstration, with
in-memory single-process state, float billing, simple environment authentication
and a small reference namespace. Patient digests are deterministic identifiers,
not anonymization. Existing pickle files are intentionally not loaded; JSON is
the new storage format. Billing computes a quotation and does not dispense stock.

## Handout discrepancy

The PDF asks for reflection answers but supplies no reflection questions. The
starter README refers to four questions that are absent from the supplied PDF.
No reflection file has been created, as requested. No personal experience or
missing instructor questions have been fabricated. A final course grade depends
on the instructor's rubric and any separate submission requirements.
