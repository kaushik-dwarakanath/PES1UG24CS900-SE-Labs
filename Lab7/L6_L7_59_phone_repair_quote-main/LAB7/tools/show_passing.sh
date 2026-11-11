#!/usr/bin/env bash
cd "$(dirname "$0")/.." || exit 1
source .venv/bin/activate
clear
printf 'LAB 7 | PES1UG24CS900 | SS4: Final Hypothesis and regression results\n\n'
printf '$ python -m pytest test_phone_repair_quote_parser.py\n'
python -m pytest test_phone_repair_quote_parser.py --color=no | tee evidence/SS4_passing_tests.txt
printf '\n[SS4 execution complete]\n'
read -r
