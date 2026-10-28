# Architecture

```text
Geyser API -> POST /v1/enrich -> Pydantic validation -> bounded orchestrator
                                      |-> Blackbird subprocess (optional)
                                      |-> Social Analyzer subprocess (optional)
                                      |-> SpiderFoot adapter (opt-in)
                                      v
                              normalization -> deduplication -> JSON response
```

The service accepts only caller-supplied leads. It does not accept images, embeddings, private identifiers, or Geyser database handles. Each subprocess receives argument arrays, has a timeout, bounded retries, and a failure cooldown. Findings retain tool/source provenance and are explicitly heuristic. Audit logs record job IDs, invoked tools, counts, and safe error categories only.

