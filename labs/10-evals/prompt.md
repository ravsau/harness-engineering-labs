Implement `scorecard.py` so it computes a deterministic score from the fixture,
not from a self-reported status. Run it against `good.json`, `bad.json`, and
`missing.json`; only the good fixture may pass. Add `--open` to the real
`taskboard.py list` command so it filters completed tasks. Run the subprocess
acceptance check and print bounded receipts. Do not make model improvement
claims.

Optional agent use: grant the agent access only to this lesson workspace and
ask it to edit the named files. If it cannot run tools, make the edits by hand;
the same local subprocess checks must pass.
