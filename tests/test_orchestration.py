import pytest
from app.adapters.base import AdapterResult
from app.models import EnrichRequest
from app.orchestration import Orchestrator


class Fake:
    enabled = True
    def capability(self): return "fake"
    async def run(self, lead, job_id):
        return AdapterResult([{"url": "https://example.com/alice", "name": "Example"}])


@pytest.mark.asyncio
async def test_partial_failure_and_deduplication():
    req = EnrichRequest(job_id="j1", purpose="authorized research", leads=[{"identifier": "alice", "lead_type": "username"}], requested_tools=["blackbird"])
    result = await Orchestrator({"blackbird": Fake()}, 2, 20).enrich(req)
    assert len(result.findings) == 1
    assert result.findings[0].job_id == "j1"

