# 05 — Sensors

Sensors look for failure signals before a verifier turns them into a release
decision. Add a negative scripted control fixture that represents a completion
claim with no observed evidence. The sensor must reject it and accept a valid
event. Evidence is a list of objects with a string `command`, integer
`exit_code`, and integer `observed_at`. The sensor must reject missing or
malformed evidence and accept a valid event. Lab 10 exercises the real CLI.

The negative run is expected to fail with a useful signal:

```bash
python3 work/sensor.py work/fixtures/negative.json
# exit 1
```

Expected stdout:

```text
event 0: completed claim has missing evidence
```

After the valid fixture exits cleanly, the lesson check prints:

```text
PASS 05-sensors: negative completion claim is detected
```
