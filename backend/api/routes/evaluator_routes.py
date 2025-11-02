from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional 

from evaluator import BalanceEvaluator
from models.puzzle_model import PuzzleDB

router = APIRouter()
db = PuzzleDB()

class PGNRequest(BaseModel):
    pgn: str

@router.post("/evaluate")
def evaluate_pgn(request: PGNRequest):
    evaluator = BalanceEvaluator(depth=10, balance_threshold=40.0, min_delta=0.0)
    results = evaluator.find_balancing_moves(request.pgn)
    return {"count": len(results), "results": results}

@router.get("/puzzles/random")
def get_random_puzzles(limit: int = 1):
    """
    Fetch a random puzzle or multiple puzzles.
    """
    puzzles = db.fetch_random(limit=limit)
    return {"count": len(puzzles), "results": puzzles}

@router.get("/puzzles")
def list_puzzles(game_id: Optional[str] = None, limit: int = 20, offset: int = 0):
    """
    Fetch puzzles optionally filtered by game_id.
    Pagination is done with limit and offset.
    """
    with db._connect() as conn:
        cur = conn.cursor()
        if game_id:
            cur.execute(
                "SELECT * FROM puzzles WHERE game_id = ? LIMIT ? OFFSET ?",
                (game_id, limit, offset),
            )
        else:
            cur.execute(
                "SELECT * FROM puzzles LIMIT ? OFFSET ?",
                (limit, offset),
            )
        cols = [col[0] for col in cur.description]
        results = [dict(zip(cols, row)) for row in cur.fetchall()]
    return {"count": len(results), "results": results}