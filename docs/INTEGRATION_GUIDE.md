# Geyser integration

After Geyser's reverse lookup workflow has candidate public identifiers or pages, its server can call this service. Do not send the original face image or an embedding.

```python
import httpx

async def enrich_candidate(service_url: str, api_key: str, job_id: str, username: str):
    payload = {
        "job_id": job_id,
        "purpose": "authorized public-source enrichment for investigation",
        "authorization_context": "caller policy reference",
        "leads": [{"identifier": username, "lead_type": "username"}],
        "requested_tools": ["social_analyzer"],
    }
    async with httpx.AsyncClient(timeout=40) as client:
        response = await client.post(f"{service_url}/v1/enrich", json=payload, headers={"X-API-Key": api_key})
        response.raise_for_status()
        return response.json()
```

Geyser remains responsible for display, identity decisions, persistence, and any face/reverse-image workflow. Treat `confidence` as a tool signal, never as probability or proof of identity.

