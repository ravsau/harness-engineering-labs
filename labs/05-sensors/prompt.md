Implement `sensor.py` as a read-only detector. It must report a missing-evidence
completion event from `fixtures/negative.json`, reject malformed evidence in
`fixtures/malformed.json`, accept `fixtures/valid.json`, and return a useful
nonzero exit code for the rejected cases. Evidence items require a non-empty
string `command`, an integer `exit_code` (where `bool` is not an integer), and
an integer `observed_at`. Add no network or model calls.
