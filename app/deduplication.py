from app.models import Finding


def merge(findings: list[Finding], limit: int) -> list[Finding]:
    out: dict[tuple[str, str], Finding] = {}
    for item in findings:
        key = (str(item.url), item.matched_identifier or "")
        if key not in out: out[key] = item
        else:
            current = out[key]
            current.provenance.extend(p for p in item.provenance if p not in current.provenance)
            current.warnings = sorted(set(current.warnings + item.warnings))
    return list(out.values())[:limit]

