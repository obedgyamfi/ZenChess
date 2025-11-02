# backend/test_db_run.py
from models.puzzle_model import PuzzleDB

db = PuzzleDB()

db.insert_puzzle(
    game_id="demo_001",
    move_number=31,
    fen="r2qrbk1/1bpn1p2/p2p1npp/1p2p3/3PP3/2P1BNNP/PPB2PP1/R2QR1K1 b - - 1 16",
    move_uci="g5e3",
    eval_before=66.0,
    eval_after=-30.0,
)

print(db.fetch_random())
