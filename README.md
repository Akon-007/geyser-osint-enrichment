# Geyser OSINT enrichment service

Standalone, lead-driven enrichment for later server-to-server integration with Geyser. It does not replace Geyser reverse-image search, face detection, embeddings, database, or dashboard, and it does not accept face images.

## Setup

Use Python 3.11+, create a virtual environment, install `pip install -e ".[test]"`, copy `.env.example` to `.env`, and set a random `OSINT_API_KEY`. Optional upstream tools are intentionally disabled by default.

Run with `python -m app.main`. Check `GET /health`, then `GET /v1/tools`. The versioned endpoint is `POST /v1/enrich`; see `examples/request.json` and `docs/INTEGRATION_GUIDE.md`.
FastAPI also exposes the generated schema at `/openapi.json` and interactive docs at `/docs`.

## Test

Run `pytest`. Tests mock upstream behavior and do not require network access or upstream tools. No live scraping claim is made by this repository.

## Operational notes

Enable only explicitly requested tools. SpiderFoot remains opt-in. The response can be partial and every finding carries provenance plus a username-match warning. See `docs/UPSTREAM_REVIEW.md`, `docs/SECURITY.md`, and `THIRD_PARTY_NOTICES.md` before deployment. The current adapters are interface-ready; upstream execution/output compatibility should be tested in a controlled environment before enabling them in production.

Transient process failures are retried with bounded exponential backoff, then the adapter enters a cooldown. Missing optional executables are reported as unavailable and do not prevent service startup.

