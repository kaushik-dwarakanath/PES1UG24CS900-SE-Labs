#!/usr/bin/env bash
cd "$(dirname "$0")/.." || exit 1
cmp -s phone_repair_quote_parser.py evidence/original_phone_repair_quote_parser.py || {
    printf "Use baseline commit ffb09ca in a separate checkout for this script.\n"
    exit 1
}
source .venv/bin/activate
export COLUMNS=110
clear
printf 'LAB 7 | PES1UG24CS900 | SS1: Original application\n\n'
printf '$ python phone_repair_quote_parser.py\n'
printf '35-209900-176148-1\nscreen x1; battery x2\nSamsung Galaxy S23\n' | python phone_repair_quote_parser.py
printf '\n$ python phone_repair_quote_parser.py  # malformed parts input\n'
printf '35-209900-176148-1\nscreen\nSamsung\n' | python phone_repair_quote_parser.py
printf '\n[SS1 execution complete; original module, before fixes]\n'
read -r
