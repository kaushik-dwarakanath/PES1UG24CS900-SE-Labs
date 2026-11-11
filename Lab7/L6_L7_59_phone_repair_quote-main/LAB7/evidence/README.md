# Lab 7 execution evidence

Student: Kaushik Krishna Dwarakanath — PES1UG24CS900, Section 5-B.

SS1–SS4 are actual screenshots of Ptyxis terminal windows, captured directly
with `magick import -window TITLE FILE.png` using the X11 terminal backend.
They are not generated images or transcripts drawn onto an image.
The first two were captured before fixing the application.

| File | Result |
| --- | --- |
| SS1_original_application.png | Original CLI: valid run, then crash on `screen` |
| SS2_failing_fuzz_tests.png | All three Hypothesis tests fail; minimized `None` example |
| SS3_fixed_application.png | Valid run, same malformed input, and all three `None` calls complete |
| SS4_passing_tests.png | Full final suite: 23 passed |
| SS2_buggy_fuzz_full.txt | Detailed automatically generated/minimized failures |
| SS4_passing_tests.txt | Final terminal test output |
| final_fuzz_statistics.txt | 500 passing examples per fuzz test, plus 20 regressions |

The shell scripts under `tools/` feed the displayed runs through standard input.
SS1 uses `35-209900-176148-1`, `screen x1; battery x2`, and
`Samsung Galaxy S23` for the normal run, followed by the same IMEI, `screen`,
and `Samsung` for the malformed run. SS3 repeats both sequences after the fix.
Inputs piped into Python are not echoed by `input()`; the resulting prompts,
outputs, and traceback are visible in the screenshots.

`original_phone_repair_quote_parser.py` preserves the supplied module byte for
byte. Commit `ffb09ca` preserves the original parser and completed tests.
To repeat SS1/SS2, use that commit in a separate checkout; the current parser is
fixed. The SS2 command selects the three fuzz tests (`-k no_crash`), leaving
the 20 deterministic regression cases deselected. SS4 runs all 23 tests.

Fuzzing is finite sampling, not proof of correctness for all possible inputs.
Hypothesis statistics can include invalid draws discarded by its generators;
those do not indicate application failures.
