import asyncio
import logging
from app.deduplication import merge
from app.models import EnrichRequest, EnrichResponse, Finding, ToolName, ToolStatus
from app.normalization import normalize

log = logging.getLogger(__name__)


class Orchestrator:
    def __init__(self, adapters, max_concurrency: int, max_results: int):
        self.adapters, self.semaphore, self.max_results = adapters, asyncio.Semaphore(max_concurrency), max_results

    async def enrich(self, request: EnrichRequest) -> EnrichResponse:
        log.info("osint_job_start job_id=%s tools=%s lead_count=%d", request.job_id, ",".join(str(t) for t in (request.requested_tools or self.adapters.keys())), len(request.leads))
        allowed = set(request.requested_tools or self.adapters.keys())
        findings: list[Finding] = []
        statuses: list[ToolStatus] = []
        async def one(adapter, lead):
            async with self.semaphore:
                return await adapter.run(lead, request.job_id)
        tasks = []
        for name, adapter in self.adapters.items():
            if name in allowed and adapter.enabled:
                tasks.extend((name, lead, asyncio.create_task(one(adapter, lead))) for lead in request.leads)
        for name, adapter in self.adapters.items():
            if name not in allowed: statuses.append(ToolStatus(tool=name, enabled=adapter.enabled, available=adapter.enabled, status="not_requested"))
        grouped = {name: [] for name in allowed}
        for name, lead, task in tasks:
            result = await task
            grouped[name].append(result)
            for raw in result.findings:
                item = normalize(raw, name, request.job_id, lead)
                if item: findings.append(item)
        for name in allowed:
            adapter = self.adapters.get(name)
            if not adapter: continue
            results = grouped.get(name, [])
            error = next((r.error for r in results if r.error), None)
            statuses.append(ToolStatus(tool=name, enabled=adapter.enabled, available=adapter.enabled and error is None,
                                       status="ok" if not error and adapter.enabled else ("disabled" if not adapter.enabled else "error"),
                                       finding_count=sum(len(r.findings) for r in results), error=error))
        findings = merge(findings, self.max_results)
        partial = any(s.status in {"error", "disabled"} for s in statuses)
        log.info("osint_job_end job_id=%s result_count=%d partial=%s", request.job_id, len(findings), partial)
        return EnrichResponse(job_id=request.job_id, findings=findings, tool_status=statuses, partial_results=partial,
                              warnings=["partial_results"] if partial else [])

