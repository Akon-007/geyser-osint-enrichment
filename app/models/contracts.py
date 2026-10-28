from datetime import datetime, timezone
from enum import Enum
from typing import Any
from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, field_validator


class LeadType(str, Enum):
    username = "username"
    profile_url = "profile_url"
    organization = "organization"


class ToolName(str, Enum):
    blackbird = "blackbird"
    social_analyzer = "social_analyzer"
    spiderfoot = "spiderfoot"


class Lead(BaseModel):
    model_config = ConfigDict(extra="forbid")
    identifier: str = Field(min_length=1, max_length=200)
    lead_type: LeadType
    lead_source_url: AnyHttpUrl | None = None

    @field_validator("identifier")
    @classmethod
    def clean_identifier(cls, value: str) -> str:
        value = value.strip()
        if not value or any(ord(c) < 32 for c in value):
            raise ValueError("identifier must be a printable, non-empty value")
        return value


class EnrichRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    job_id: str = Field(min_length=1, max_length=128, pattern=r"^[A-Za-z0-9._:-]+$")
    investigation_id: str | None = Field(default=None, max_length=128)
    leads: list[Lead] = Field(min_length=1, max_length=20)
    requested_tools: list[ToolName] | None = None
    purpose: str = Field(min_length=1, max_length=500)
    authorization_context: str | None = Field(default=None, max_length=500)


class Provenance(BaseModel):
    tool: ToolName
    source_url: AnyHttpUrl | None = None
    source_metadata: dict[str, Any] = Field(default_factory=dict)


class Finding(BaseModel):
    finding_id: str
    job_id: str
    tool: ToolName
    finding_type: str
    title: str | None = None
    url: AnyHttpUrl | None = None
    platform: str | None = None
    matched_identifier: str | None = None
    observed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    tool_signal: str | None = None
    confidence: float | None = Field(default=None, ge=0, le=100)
    evidence_summary: str = Field(max_length=500)
    provenance: list[Provenance] = Field(min_length=1)
    warnings: list[str] = Field(default_factory=list)


class ToolStatus(BaseModel):
    tool: ToolName
    enabled: bool
    available: bool
    status: str
    finding_count: int = 0
    error: str | None = None


class EnrichResponse(BaseModel):
    job_id: str
    findings: list[Finding]
    tool_status: list[ToolStatus]
    partial_results: bool
    warnings: list[str] = Field(default_factory=list)

