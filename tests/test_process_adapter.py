import pytest
from app.adapters.process import ProcessAdapter


class FakeProcess:
    def __init__(self, output=b'[{"url":"https://example.org/a"}]', code=0):
        self.output, self.returncode, self.killed, self.code = output, code, False, code
    async def communicate(self):
        return self.output, b""
    def kill(self):
        self.killed = True


@pytest.mark.asyncio
async def test_malformed_output(monkeypatch):
    proc = FakeProcess(b"not-json")
    async def create(*args, **kwargs): return proc
    monkeypatch.setattr("asyncio.create_subprocess_exec", create)
    result = await ProcessAdapter("x", "python", True, 1, retry_attempts=1).execute([])
    assert result.error == "malformed tool output"


@pytest.mark.asyncio
async def test_nonzero_exit_retries_then_cools_down(monkeypatch):
    calls = 0
    async def create(*args, **kwargs):
        nonlocal calls
        calls += 1
        return FakeProcess(b"[]", 9)
    monkeypatch.setattr("asyncio.create_subprocess_exec", create)
    adapter = ProcessAdapter("x", "python", True, 1, retry_attempts=2, cooldown_seconds=60)
    result = await adapter.execute([])
    assert result.error == "tool exited with code 9"
    assert calls == 2
    assert (await adapter.execute([])).error == "tool cooldown active"

