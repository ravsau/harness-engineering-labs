#!/bin/sh
set -eu
test -f taskboard.py
test -f features.json
python3 -m json.tool features.json >/dev/null
printf '%s\n' 'baseline ready'
