from app.models import Lead, LeadType, ToolName
from app.normalization import normalize


def test_normalizes_documented_style_profile():
    item = normalize({"name": "Example", "url": "https://example.com/alice", "rate": 90}, ToolName.social_analyzer, "job-1", Lead(identifier="alice", lead_type=LeadType.username))
    assert item and str(item.url) == "https://example.com/alice"
    assert "username_match_not_identity_proof" in item.warnings


def test_drops_unsafe_url():
    assert normalize({"url": "http://127.0.0.1/x"}, ToolName.blackbird, "job-1", Lead(identifier="alice", lead_type=LeadType.username)) is not None

