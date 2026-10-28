import pytest
from pydantic import ValidationError
from app.models import EnrichRequest


def test_rejects_non_http_lead_source():
    with pytest.raises(ValidationError):
        EnrichRequest(job_id="j1", purpose="authorized research", leads=[{"identifier": "alice", "lead_type": "username", "lead_source_url": "file:///tmp/x"}])


def test_rejects_bad_job_id():
    with pytest.raises(ValidationError):
        EnrichRequest(job_id="bad id", purpose="authorized research", leads=[{"identifier": "alice", "lead_type": "username"}])

