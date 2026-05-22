# Simple Dev Loop

This loop is documented as **[BROWNFIELD_DEV_LOOP.md](BROWNFIELD_DEV_LOOP.md)** — same commands as greenfield where possible (`/design`, `/tdd`, `/tasksplit`, `/implement-next`, `/review`, `/snapshot`).

```text
/understand [change]
/slice                    # optional
/design <FEATURE>
/tdd <FEATURE>
/tasksplit <FEATURE>
/implement-next → /review → /snapshot
```

`/plan-feature` is **deprecated** — use `/design`.
