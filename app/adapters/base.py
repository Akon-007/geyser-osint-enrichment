from dataclasses import dataclass
from typing import Protocol
from app.models import Lead, ToolName


@dataclass
class AdapterResult:
    findings: list[dict]
    error: str | None = None


class Adapter(Protocol):
    name: ToolName
    enabled: bool
    async def run(self, lead: Lead, job_id: str) -> AdapterResult: ...
    def capability(self) -> str: ...

