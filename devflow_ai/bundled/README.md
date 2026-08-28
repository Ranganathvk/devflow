# Bundled framework (install-time only)

`core/` and `adapters/` are embedded here when the **wheel** is built (`uv build` / `pip install`).

Source checkouts use the repo-root `core/` and `adapters/` instead — see `framework_root()` in `installer.py`.
