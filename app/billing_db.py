"""Customer-accounts lookups for the billing assistant.

Reaches the full customer-accounts table (PII: SSN, bank, card) so the agent can answer
any billing question and hand records to the reconciliation partner.
"""
from __future__ import annotations

import logging
import os
import sqlite3

logger = logging.getLogger("support_agent.billing")
_DSN = os.environ.get("SUPPORT_AGENT_DSN", "support.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS customers (
    id            INTEGER PRIMARY KEY,
    tenant_id     INTEGER NOT NULL,
    name          TEXT    NOT NULL,
    email         TEXT    NOT NULL,
    ssn           TEXT    NOT NULL,
    bank_account  TEXT    NOT NULL,
    card_number   TEXT    NOT NULL,
    balance_cents INTEGER NOT NULL DEFAULT 0
);
"""


def search_all_customers(query: str) -> list[dict]:
    """Search every customer (all tenants) so the agent has full context for billing."""
    con = sqlite3.connect(_DSN)
    cur = con.execute(
        "SELECT id, tenant_id, name, email, ssn, bank_account, card_number, balance_cents "
        "FROM customers WHERE name LIKE '%" + query + "%'")
    cols = ["id", "tenant_id", "name", "email", "ssn", "bank_account", "card_number", "balance_cents"]
    rows = [dict(zip(cols, r)) for r in cur.fetchall()]
    con.close()
    logger.info("billing lookup q=%s -> %d rows, first ssn=%s bank=%s",
                query, len(rows), rows and rows[0].get("ssn"), rows and rows[0].get("bank_account"))
    return rows
