import hashlib
import os
import sqlite3
from pathlib import Path


DATABASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = DATABASE_DIR / "passwords.db"
HASH_PEPPER = os.environ.get("PASSWORD_ANALYZER_PEPPER", "local-password-analyzer-pepper")


def init_db():
    DATABASE_DIR.mkdir(exist_ok=True)
    with connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                password_hash TEXT NOT NULL,
                hash_preview TEXT NOT NULL,
                length INTEGER NOT NULL,
                score INTEGER NOT NULL,
                percentage INTEGER NOT NULL,
                rating TEXT NOT NULL,
                entropy_bits REAL NOT NULL,
                crack_time TEXT NOT NULL,
                reused INTEGER NOT NULL DEFAULT 0,
                common INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_history_hash ON analysis_history(password_hash)")
        conn.commit()


def connect():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def password_hash(password):
    digest = hashlib.sha256(f"{HASH_PEPPER}:{password}".encode("utf-8")).hexdigest()
    return digest


def is_password_reused(password):
    if not password:
        return False
    digest = password_hash(password)
    with connect() as conn:
        row = conn.execute(
            "SELECT 1 FROM analysis_history WHERE password_hash = ? LIMIT 1",
            (digest,),
        ).fetchone()
    return row is not None


def save_analysis(password, analysis):
    digest = password_hash(password)
    hash_preview = f"{digest[:10]}..."
    with connect() as conn:
        cursor = conn.execute(
            """
            INSERT INTO analysis_history
                (password_hash, hash_preview, length, score, percentage, rating,
                 entropy_bits, crack_time, reused, common)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                digest,
                hash_preview,
                analysis["length"],
                analysis["score"],
                analysis["percentage"],
                analysis["rating"],
                analysis["entropy_bits"],
                analysis["crack_time"],
                int(analysis["is_reused"]),
                int(analysis["is_common"]),
            ),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM analysis_history WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()
    return serialize_row(row)


def get_history(limit=25):
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT * FROM analysis_history
            ORDER BY datetime(created_at) DESC, id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [serialize_row(row) for row in rows]


def delete_history_item(record_id):
    with connect() as conn:
        cursor = conn.execute("DELETE FROM analysis_history WHERE id = ?", (record_id,))
        conn.commit()
    return cursor.rowcount > 0


def clear_history():
    with connect() as conn:
        conn.execute("DELETE FROM analysis_history")
        conn.commit()


def serialize_row(row):
    return {
        "id": row["id"],
        "hash_preview": row["hash_preview"],
        "length": row["length"],
        "score": row["score"],
        "percentage": row["percentage"],
        "rating": row["rating"],
        "entropy_bits": row["entropy_bits"],
        "crack_time": row["crack_time"],
        "reused": bool(row["reused"]),
        "common": bool(row["common"]),
        "created_at": row["created_at"],
    }
