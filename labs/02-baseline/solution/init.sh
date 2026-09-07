#!/bin/sh
set -eu
test -f taskboard.py
test -f features.json
python3 -m json.tool features.json >/dev/null
feature_count=$(python3 -c 'import json; print(len(json.load(open("features.json"))))')
test "$feature_count" = 2
printf '%s\n' "baseline ready; $feature_count features loaded"
