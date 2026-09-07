Implement `verify.py`. Accept a claim only when it has a successful command
observation newer than the fixed clock minus the freshness window. Require a
non-empty string `command`, an integer `exit_code` equal to zero, and an integer
`observed_at`; `bool` values do not count as integers. Reject stale, missing,
malformed, and explicitly failed evidence or checks. Print that the gate is
local and partial; do not claim total proof or model improvement.
