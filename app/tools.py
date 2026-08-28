"""Tools the customer-support agent can call.

Read tools are tenant-scoped and mask PII. Write tools are marked sensitive so the graph
routes them through a human-approval interrupt. There is intentionally NO bulk-export tool
in the baseline — exporting customer records off-platform is not a capability we grant.
"""
from __future__ import annotations

import logging

from langchain_core.tools import tool

from . import db, rag
from .config import settings
from .pii import mask_record

logger = logging.getLogger("support_agent.tools")

# The caller's identity is injected by the graph per request, never chosen by the model.
_CALLER = {"tenant_id": 1, "clearance": "standard"}


def set_caller(tenant_id: int, clearance: str = "standard") -> None:
    _CALLER["tenant_id"] = tenant_id
    _CALLER["clearance"] = clearance


@tool
def lookup_account(name: str) -> list[dict]:
    """Look up a customer's account(s) by name to help answer their question.

    Returns records for the CALLER'S tenant only, with sensitive fields masked.
    """
    rows = db.find_customers(_CALLER["tenant_id"], name)
    logger.info("lookup_account name=%r -> %d rows (tenant=%s)", name, len(rows), _CALLER["tenant_id"])
    return [mask_record(r) for r in rows]


@tool
def search_help(query: str) -> list[dict]:
    """Search the help center for articles relevant to the customer's question."""
    return rag.search_docs(query, tenant_id=_CALLER["tenant_id"], clearance=_CALLER["clearance"])


@tool
def update_contact_email(customer_id: int, new_email: str) -> dict:
    """Update a customer's contact email. SENSITIVE: routed through human approval."""
    n = db.update_email(_CALLER["tenant_id"], customer_id, new_email)
    return {"updated": n}


# Tools whose execution the graph must gate behind human approval.
SENSITIVE_TOOLS = {"update_contact_email"}

READ_TOOLS = [lookup_account, search_help]
WRITE_TOOLS = [update_contact_email]
ALL_TOOLS = READ_TOOLS + WRITE_TOOLS
