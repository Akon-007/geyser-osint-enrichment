from app.adapters.base import AdapterResult
from app.adapters.process import ProcessAdapter
from app.models import Lead, LeadType, ToolName


class SocialAnalyzerAdapter(ProcessAdapter):
    name = ToolName.social_analyzer
    def capability(self) -> str: return "username lookup through Social Analyzer JSON CLI output"
    async def run(self, lead: Lead, job_id: str) -> AdapterResult:
        if lead.lead_type != LeadType.username: return AdapterResult([])
        return await self.execute(["--username", lead.identifier, "--output", "json", "--silent", "--mode", "fast"])

