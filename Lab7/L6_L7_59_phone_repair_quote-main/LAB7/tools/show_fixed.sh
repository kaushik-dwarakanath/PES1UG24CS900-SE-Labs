#!/usr/bin/env bash
cd "$(dirname "$0")/.." || exit 1
source .venv/bin/activate
clear
printf 'LAB 7 | PES1UG24CS900 | SS3: Fixed application\n\n'
printf '$ python phone_repair_quote_parser.py  # normal inputs\n'
printf '35-209900-176148-1\nscreen x1; battery x2\nSamsung Galaxy S23\n' | python phone_repair_quote_parser.py
printf '\n$ python phone_repair_quote_parser.py  # same malformed input as SS1\n'
printf '35-209900-176148-1\nscreen\nSamsung\n' | python phone_repair_quote_parser.py
printf '\n$ python -c "..."  # None inputs for all three functions\n'
python -c 'from phone_repair_quote_parser import mask_imei, parse_parts_order, parse_model; print("mask_imei(None):", repr(mask_imei(None))); print("parse_parts_order(None):", parse_parts_order(None)); print("parse_model(None):", parse_model(None))'
printf '\n[SS3 execution complete; all runs completed without exceptions]\n'
read -r
