"""Seed the baseline database + help corpus with non-sensitive demo data.

The baseline agent holds NO customer PII — just order status rows and help articles.
(The demo PR is what introduces a customer-accounts table with SSN/bank/card.)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app import db  # noqa: E402

ORDERS = [
    ("ORD-1001", 1, "shipped", "2 days"),
    ("ORD-1002", 1, "processing", "5 days"),
    ("ORD-2001", 2, "delivered", "-"),
    ("ORD-2002", 2, "processing", "4 days"),
]

DOCS = [
    {"doc_id": "kb-t1-billing", "tenant_id": 1, "classification": "standard",
     "title": "Billing cycle FAQ", "body": "Invoices generate on the 1st. Contact support to change your billing email."},
    {"doc_id": "kb-t1-shipping", "tenant_id": 1, "classification": "standard",
     "title": "Shipping & tracking", "body": "Track an order with its order id. Most orders ship within 2 business days."},
    {"doc_id": "kb-t2-billing", "tenant_id": 2, "classification": "standard",
     "title": "Globex billing FAQ", "body": "Globex invoices are net-30. Reach support for plan changes."},
]


def main() -> None:
    with db.connect() as con:
        con.executescript(db.SCHEMA)
        con.execute("DELETE FROM orders")
        con.executemany(
            "INSERT INTO orders (order_id, tenant_id, status, eta) VALUES (?,?,?,?)", ORDERS)
        con.commit()
    docs_dir = Path(__file__).resolve().parent / "docs"
    docs_dir.mkdir(exist_ok=True)
    for d in DOCS:
        (docs_dir / f"{d['doc_id']}.json").write_text(json.dumps(d, indent=2))
    print(f"seeded {len(ORDERS)} orders, {len(DOCS)} help docs (no PII)")


if __name__ == "__main__":
    main()
