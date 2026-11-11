#!/usr/bin/env bash
cd "$(dirname "$0")/.." || exit 1
cmp -s phone_repair_quote_parser.py evidence/original_phone_repair_quote_parser.py || {
    printf "Use baseline commit ffb09ca in a separate checkout for this script.\n"
    exit 1
}
source .venv/bin/activate
clear
printf 'LAB 7 | PES1UG24CS900 | SS2: Fuzz tests on original module\n\n'
printf '$ python -m pytest test_phone_repair_quote_parser.py -k no_crash --tb=line\n'
python -m pytest test_phone_repair_quote_parser.py -k no_crash --tb=line --color=no
printf '\nFull Hypothesis failures: evidence/SS2_buggy_fuzz_full.txt\n'
printf '\n$ python -c "from phone_repair_quote_parser import mask_imei; mask_imei(None)"\n'
python -c 'from phone_repair_quote_parser import mask_imei; mask_imei(None)'
printf '\n[SS2 execution complete; original module, before fixes]\n'
read -r
