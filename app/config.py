from dataclasses import dataclass
import os


def _bool(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    api_key: str = os.getenv("OSINT_API_KEY", "")
    max_leads: int = int(os.getenv("OSINT_MAX_LEADS", "20"))
    max_results: int = int(os.getenv("OSINT_MAX_RESULTS", "200"))
    timeout_seconds: float = float(os.getenv("OSINT_TOOL_TIMEOUT_SECONDS", "30"))
    max_concurrency: int = int(os.getenv("OSINT_MAX_CONCURRENCY", "3"))
    retry_attempts: int = int(os.getenv("OSINT_RETRY_ATTEMPTS", "2"))
    failure_cooldown_seconds: float = float(os.getenv("OSINT_FAILURE_COOLDOWN_SECONDS", "30"))
    enable_blackbird: bool = _bool("OSINT_ENABLE_BLACKBIRD")
    enable_social_analyzer: bool = _bool("OSINT_ENABLE_SOCIAL_ANALYZER")
    enable_spiderfoot: bool = _bool("OSINT_ENABLE_SPIDERFOOT")
    blackbird_command: str = os.getenv("OSINT_BLACKBIRD_COMMAND", "python vendor/blackbird/blackbird.py")
    social_analyzer_command: str = os.getenv("OSINT_SOCIAL_ANALYZER_COMMAND", "python vendor/social-analyzer/app.py")
    spiderfoot_command: str = os.getenv("OSINT_SPIDERFOOT_COMMAND", "python vendor/spiderfoot/sfcli.py")

