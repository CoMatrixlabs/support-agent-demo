"""Customer-accounts database access.

A thin SQLite layer holding customer accounts across multiple tenants. Every read is
parameterized and scoped to the caller's tenant. Sensitive columns (ssn, bank_account,
card_number) exist so the demo can show masking vs. leakage — real deployments would
tokenize these at rest.
"""
from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager

_DSN = os.environ.get("SUPPORT_AGENT_DSN", "customer_accounts.db")

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
CREATE INDEX IF NOT EXISTS idx_customers_tenant ON customers(tenant_id);
"""


@contextmanager
def connect():
    con = sqlite3.connect(_DSN)
    con.row_factory = sqlite3.Row
    try:
        yield con
    finally:
        con.close()


def find_customers(tenant_id: int, name_like: str) -> list[dict]:
    """Look up accounts for ONE tenant by (partial) name. Parameterized + tenant-scoped."""
    with connect() as con:
        cur = con.execute(
            "SELECT id, tenant_id, name, email, ssn, bank_account, card_number, balance_cents "
            "FROM customers WHERE tenant_id = ? AND name LIKE ? ORDER BY name",
            (tenant_id, f"%{name_like}%"),
        )
        return [dict(r) for r in cur.fetchall()]


def update_email(tenant_id: int, customer_id: int, new_email: str) -> int:
    """Effectful write — used only behind the approval gate. Tenant-scoped."""
    with connect() as con:
        cur = con.execute(
            "UPDATE customers SET email = ? WHERE tenant_id = ? AND id = ?",
            (new_email, tenant_id, customer_id),
        )
        con.commit()
        return cur.rowcount
