"""Small local harness: measures mocked orchestration duration and unique findings."""
import asyncio
import time
from app.adapters.base import AdapterResult
from app.models import EnrichRequest
from app.orchestration import Orchestrator


class BenchmarkAdapter:
    enabled = True
    def capability(self): return "benchmark"
    async def run(self, lead, job_id):
        return AdapterResult([{"url": f"https://example.org/{lead.identifier}", "name": "fixture"}])


async def main():
    request = EnrichRequest(job_id="benchmark", purpose="test", leads=[{"identifier": f"u{i}", "lead_type": "username"} for i in range(10)])
    started = time.perf_counter()
    result = await Orchestrator({"blackbird": BenchmarkAdapter()}, 3, 200).enrich(request)
    elapsed_ms = (time.perf_counter() - started) * 1000
    print({"elapsed_ms": round(elapsed_ms, 2), "unique_findings": len(result.findings)})


if __name__ == "__main__":
    asyncio.run(main())

