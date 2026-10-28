import hmac
import logging
from fastapi import Depends, FastAPI, Header, HTTPException
from app.adapters import BlackbirdAdapter, SocialAnalyzerAdapter, SpiderFootAdapter
from app.config import Settings
from app.models import EnrichRequest, EnrichResponse, ToolName
from app.orchestration import Orchestrator

logging.basicConfig(level=logging.INFO)
settings = Settings()
app = FastAPI(title="Geyser OSINT Enrichment", version="1.0.0")
adapters = {
    ToolName.blackbird: BlackbirdAdapter(ToolName.blackbird, settings.blackbird_command, settings.enable_blackbird, settings.timeout_seconds, settings.retry_attempts, settings.failure_cooldown_seconds),
    ToolName.social_analyzer: SocialAnalyzerAdapter(ToolName.social_analyzer, settings.social_analyzer_command, settings.enable_social_analyzer, settings.timeout_seconds, settings.retry_attempts, settings.failure_cooldown_seconds),
    ToolName.spiderfoot: SpiderFootAdapter(ToolName.spiderfoot, settings.spiderfoot_command, settings.enable_spiderfoot, settings.timeout_seconds, settings.retry_attempts, settings.failure_cooldown_seconds),
}
orchestrator = Orchestrator(adapters, settings.max_concurrency, settings.max_results)


def auth(x_api_key: str | None = Header(default=None)):
    if settings.api_key and not hmac.compare_digest(x_api_key or "", settings.api_key):
        raise HTTPException(401, detail={"code": "unauthorized", "message": "invalid API key"})


@app.get("/health")
async def health():
    return {"status": "ok", "service": "geyser-osint-enrichment", "version": app.version}


@app.get("/v1/tools", dependencies=[Depends(auth)])
async def tools():
    return {"tools": [{"tool": n.value, "enabled": a.enabled, "available": a.available(), "capability": a.capability()} for n, a in adapters.items()]}


@app.post("/v1/enrich", response_model=EnrichResponse, dependencies=[Depends(auth)])
async def enrich(request: EnrichRequest):
    if request.requested_tools and any(t not in adapters for t in request.requested_tools):
        raise HTTPException(400, detail={"code": "invalid_tool", "message": "requested tool is not allowlisted"})
    return await orchestrator.enrich(request)

