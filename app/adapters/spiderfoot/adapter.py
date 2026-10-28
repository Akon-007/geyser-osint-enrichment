from app.adapters.base import AdapterResult
from app.adapters.process import ProcessAdapter
from app.models import Lead, ToolName


class SpiderFootAdapter(ProcessAdapter):
    name = ToolName.spiderfoot
    def capability(self) -> str: return "opt-in SpiderFoot integration placeholder; requires a configured SpiderFoot service"
    async def run(self, lead: Lead, job_id: str) -> AdapterResult:
        return AdapterResult([], "SpiderFoot adapter requires explicit service configuration")

