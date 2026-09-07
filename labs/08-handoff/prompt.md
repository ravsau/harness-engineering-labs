Implement `handoff.py` with append-only JSONL records and a read-only `show`
command. Record two handoffs, restart the process, and prove the first line was
not overwritten. `show` must reject stale evidence using the supplied fixed
clock. Validate every existing JSONL record before appending. A corrupt log
must remain byte-for-byte unchanged and both `show` and `record` must return
nonzero. Do not use a completion boolean as proof.
