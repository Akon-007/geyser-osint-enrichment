import hashlib
from urllib.parse import urlparse
from app.models import Finding, Lead, Provenance, ToolName


def _url(value):
    if not isinstance(value, str) or urlparse(value).scheme not in {"http", "https"}: return None
    return value


def normalize(raw: dict, tool: ToolName, job_id: str, lead: Lead) -> Finding | None:
    tool = ToolName(tool)
    url = _url(raw.get("url") or raw.get("link") or raw.get("profile_url"))
    if not url: return None
    title = str(raw.get("title") or raw.get("name") or "")[:200] or None
    platform = str(raw.get("site") or raw.get("platform") or raw.get("name") or "")[:100] or None
    signal = raw.get("rate") or raw.get("status") or raw.get("match")
    confidence = raw.get("rate") if isinstance(raw.get("rate"), (int, float)) else None
    source = lead.lead_source_url if lead.lead_source_url else None
    digest = hashlib.sha256(f"{job_id}|{tool.value}|{url}".encode()).hexdigest()[:24]
    return Finding(finding_id=digest, job_id=job_id, tool=tool, finding_type="social_profile_candidate", title=title,
                  url=url, platform=platform, matched_identifier=lead.identifier, tool_signal=str(signal) if signal is not None else None,
                  confidence=confidence, evidence_summary="Public URL returned by the configured upstream tool; username match is not identity proof.",
                  provenance=[Provenance(tool=tool, source_url=source, source_metadata={"upstream_fields": sorted(raw.keys())[:20]})],
                  warnings=["username_match_not_identity_proof"])

