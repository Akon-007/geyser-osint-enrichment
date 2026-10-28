# Security and operating boundaries

- Configure `OSINT_API_KEY` for server-to-server authentication; never commit it.
- Do not enable adapters without reviewing upstream site terms, rate limits, dependencies, and legal use.
- The first version does not fetch caller-provided URLs and does not perform email account-existence checks.
- No login bypass, CAPTCHA evasion, access-control circumvention, or image/embedding transfer is supported.
- Logs should contain job IDs, tool names, counts, and safe error categories only. The service has no persistence by default.
- Run the service in a restricted egress container if live upstream tools are enabled.

