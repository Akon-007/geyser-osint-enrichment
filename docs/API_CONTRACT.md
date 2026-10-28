# API contract

FastAPI publishes the machine-readable schema at `/openapi.json` and interactive documentation at `/docs`.

## Authentication

When `OSINT_API_KEY` is non-empty, `/v1/tools` and `/v1/enrich` require `X-API-Key`. `/health` is intentionally unauthenticated and does not expose configuration or secrets.

## Enrichment

`POST /v1/enrich` accepts `job_id`, optional `investigation_id`, one or more explicit `leads`, optional `requested_tools`, and a caller-supplied `purpose`. Leads are limited to `username`, `profile_url`, and `organization`. Responses contain normalized findings and a status record for every tool requested or configured.

`confidence` is a tool signal/heuristic on a 0–100 scale. It is not a probability and is never proof of identity. Errors are safe categories; subprocess stderr and credentials are never returned.

