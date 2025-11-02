import sqlite3
import json
from pathlib import Path
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float 
from db.database import Base

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "puzzles.db"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)


class PuzzleDB:
    """Handles SQLite operations for ZenChess puzzles."""

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS puzzles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    game_id TEXT,
                    move_number INTEGER,
                    fen TEXT,
                    move_uci TEXT,
                    eval_before REAL,
                    eval_after REAL,
                    delta REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()

    def insert_puzzle(self, game_id, move_number, fen, move_uci, eval_before, eval_after):
        """Insert a new puzzle record."""
        delta = round(abs(eval_after - eval_before), 2)
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO puzzles
                (game_id, move_number, fen, move_uci, eval_before, eval_after, delta)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (game_id, move_number, fen, move_uci, eval_before, eval_after, delta),
            )
            conn.commit()

    def fetch_random(self, limit=1):
        """Fetch a random set of puzzles."""
        with self._connect() as conn:
            cur = conn.execute(
                "SELECT * FROM puzzles ORDER BY RANDOM() LIMIT ?", (limit,)
            )
            cols = [col[0] for col in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]

    def export_to_json(self, output_path=None):
        """Export all puzzles to JSON."""
        if not output_path:
            output_path = DATA_DIR / "exports" / "puzzles.json"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with self._connect() as conn:
            cur = conn.execute("SELECT * FROM puzzles")
            cols = [col[0] for col in cur.description]
            data = [dict(zip(cols, row)) for row in cur.fetchall()]

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return output_path

