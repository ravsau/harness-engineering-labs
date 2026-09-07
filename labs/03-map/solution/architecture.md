# Architecture

`taskboard.py` is the small command surface. `features.json` records work in a
stable JSON shape. Harness lessons add files around the CLI: guides describe
work, sensors detect failure, verifiers gate claims, and handoffs persist state.
