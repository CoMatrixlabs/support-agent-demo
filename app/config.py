"""Runtime settings for the customer-support agent.

Baseline posture is SAFE: sensitive tools require human approval, PII is masked on
read, generation temperature is low for tool-driving paths, and outbound export is
restricted to an allow-list. The vulnerable demo branch flips these.
"""
from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.2          # low for tool-driving / effectful paths
    max_tool_iterations: int = 6

    # --- data-boundary controls (safe defaults) ---
    require_tool_approval: bool = True        # human-in-the-loop for write / export tools
    mask_pii: bool = True                     # mask SSN / bank / card on read
    enforce_tenant_scope: bool = True         # every query is filtered by the caller's tenant
    allowed_export_domains: tuple[str, ...] = ()   # empty = no external export permitted

    log_level: str = "INFO"

    class Config:
        env_prefix = "SUPPORT_AGENT_"


settings = Settings()
