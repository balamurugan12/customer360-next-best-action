"""Local demo action ledger. Records decisions; never contacts customers."""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_PATH = Path(__file__).resolve().parents[1] / "runtime" / "actions.sqlite3"
STATUSES = ("Accepted", "Declined", "Resolved", "No improvement")


def connect(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, timeout=10)
    connection.execute(
        """CREATE TABLE IF NOT EXISTS action_events (
        id INTEGER PRIMARY KEY, customer_id TEXT NOT NULL, action TEXT NOT NULL,
        owner TEXT NOT NULL, risk_score INTEGER NOT NULL, status TEXT NOT NULL,
        notes TEXT NOT NULL, evidence_ids TEXT NOT NULL, created_at TEXT NOT NULL)"""
    )
    return connection


def record_event(customer_id, action, risk_score, status, notes, evidence_ids, path=DEFAULT_PATH):
    if status not in STATUSES:
        raise ValueError("Unknown action status")
    if status in ("Declined", "Resolved", "No improvement") and not notes.strip():
        raise ValueError("Add a reason or outcome note.")
    with connect(path) as connection:
        connection.execute("BEGIN IMMEDIATE")
        previous = connection.execute(
            "SELECT status FROM action_events WHERE customer_id=? AND action=? ORDER BY id DESC LIMIT 1",
            (customer_id, action["action"]),
        ).fetchone()
        if status in ("Resolved", "No improvement") and (not previous or previous[0] != "Accepted"):
            raise ValueError("Accept the recommendation before recording an outcome.")
        if previous and previous[0] == status:
            raise ValueError("This status is already recorded.")
        connection.execute(
            "INSERT INTO action_events (customer_id, action, owner, risk_score, status, notes, evidence_ids, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (customer_id, action["action"], action["owner"], int(risk_score), status,
             notes.strip(), json.dumps(list(evidence_ids)), datetime.now(timezone.utc).isoformat()),
        )


def read_events(path=DEFAULT_PATH):
    with connect(path) as connection:
        connection.row_factory = sqlite3.Row
        return [dict(row) for row in connection.execute("SELECT * FROM action_events ORDER BY id DESC")]
