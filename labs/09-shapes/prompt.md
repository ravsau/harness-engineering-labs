Implement `shapes.py` with deterministic `chain`, `fanout`, `advisor`, and
`loop` runs over `fixtures/tasks.json`. Give every work item one owner, keep the
advisor read-only, and enforce `--limit` in the loop. Print JSON events so a
fresh process can inspect the run.
