# Upstream review

Review performed against the pinned checkouts recorded in `THIRD_PARTY_NOTICES.md`.

| Project | Interface reviewed | License finding | Decision / risk |
|---|---|---|---|
| Blackbird | `blackbird.py --username ... --json`; `requirements.txt` | GPL-3.0-only in `docs/LICENSE`; README also references WhatsMyName data under CC BY-SA 4.0 | Keep as an external, optional process. Do not import or copy code. Commercial/closed-source redistribution needs legal review of GPL and transitive/data notices. |
| Social Analyzer | `app.py --username ... --output json --silent`; Python package and Node CLI manifests | GPL-3.0-only in `LICENSE` | Keep as an external, optional process. It performs live HTTP checks and has a large third-party dependency surface; no credentials or images are passed. |
| SpiderFoot | `sfcli.py` and HTTP API/export paths; `requirements.txt` | MIT in `LICENSE` | Optional adapter only. Its broad module set may call external APIs and needs per-deployment module/rate-limit policy. It is disabled by default and not bundled into the service runtime. |

This repository contains the requested upstream checkouts under `vendor/` for review and reproducibility, not as imported application code. Upstream dependencies are not installed by the service package. The adapters use documented command boundaries and parse JSON only. Exact dependency licenses must be reviewed before any production redistribution.

