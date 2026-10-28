import asyncio
import json
import shlex
import time
import shutil
from pathlib import Path
from typing import Any
from .base import AdapterResult


class ProcessAdapter:
    def __init__(self, name, command: str, enabled: bool, timeout: float, retry_attempts: int = 2, cooldown_seconds: float = 30):
        self.name, self.command, self.enabled, self.timeout = name, command, enabled, timeout
        self.retry_attempts, self.cooldown_seconds, self._cooldown_until = retry_attempts, cooldown_seconds, 0.0

    def available(self) -> bool:
        if not self.enabled:
            return False
        try:
            executable = shlex.split(self.command, posix=False)[0]
            return bool(shutil.which(executable) or Path(executable).exists())
        except (IndexError, ValueError):
            return False

    async def execute(self, args: list[str]) -> AdapterResult:
        if time.monotonic() < self._cooldown_until:
            return AdapterResult([], "tool cooldown active")
        for attempt in range(max(1, self.retry_attempts)):
            try:
                argv = shlex.split(self.command, posix=False) + args
                proc = await asyncio.create_subprocess_exec(*argv, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                stdout, _stderr = await asyncio.wait_for(proc.communicate(), timeout=self.timeout)
                if proc.returncode != 0:
                    error = f"tool exited with code {proc.returncode}"
                else:
                    payload: Any = json.loads(stdout.decode("utf-8", errors="replace"))
                    if isinstance(payload, dict):
                        payload = payload.get("results", payload.get("profiles", payload.get("data", [])))
                    if not isinstance(payload, list):
                        return AdapterResult([], "unsupported tool output shape")
                    self._cooldown_until = 0.0
                    return AdapterResult([x for x in payload if isinstance(x, dict)])
            except asyncio.TimeoutError:
                proc.kill()
                await proc.communicate()
                error = "tool timeout"
            except json.JSONDecodeError:
                return AdapterResult([], "malformed tool output")
            except (OSError, ValueError) as exc:
                error = f"tool unavailable: {type(exc).__name__}"
            if attempt + 1 < max(1, self.retry_attempts):
                await asyncio.sleep(min(0.25 * (2 ** attempt), 1.0))
        self._cooldown_until = time.monotonic() + self.cooldown_seconds
        return AdapterResult([], error)

