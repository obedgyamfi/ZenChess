import chess.pgn
from io import StringIO
from typing import List, Dict, Any, Optional

from engine import ChessEngine
from models.puzzle_model import PuzzleDB


class BalanceEvaluator:
    def __init__(
        self,
        depth: int = 12,
        balance_threshold: float = 50.0,
        min_delta: float = 30.0,
    ):
        """
        :param depth: Engine search depth
        :param balance_threshold: centipawn threshold to consider a position 'balanced'
        :param min_delta: minimum absolute change (centipawns) between before/after to record
        """
        self.engine = ChessEngine()
        self.depth = depth
        self.balance_threshold = balance_threshold
        self.min_delta = min_delta
        self.db = PuzzleDB()

    def is_balanced(self, score: Optional[float]) -> bool:
        """Return True if position is approximately balanced (or if score is None)."""
        if score is None:
            return True
        return abs(score) <= self.balance_threshold

    def find_balancing_moves(self, pgn_text: str) -> Dict[str, Any]:
        """
        Parse a PGN game and find moves that balance the position.
        Returns a list of records:
        {
          "game_id", "move_number", "fen_before", "fen_after",
          "eval_before", "eval_after", "delta", "move_uci", "move_san"
        }
        """
        game = chess.pgn.read_game(StringIO(pgn_text))
        if game is None:
            return {"results": []}

        board = game.board()
        results: List[Dict[str, Any]] = []

        for ply_index, move in enumerate(game.mainline_moves(), start=1):
            fen_before = board.fen()
            eval_before = self.engine.evaluate_position(fen_before, depth=self.depth)

            # SAN must be computed while move is legal on this board (so compute before push)
            try:
                move_san = board.san(move)
            except Exception:
                move_san = move.uci()

            # Apply move
            board.push(move)

            fen_after = board.fen()
            eval_after = self.engine.evaluate_position(fen_after, depth=self.depth)

            # Detection condition:
            # - before was unbalanced
            # - after is balanced
            # - the change magnitude is >= min_delta (optional)
            delta = None
            if eval_before is not None and eval_after is not None:
                delta = round(abs(eval_after - eval_before), 2)
            else:
                # handle mate/None cases conservatively
                delta = None

            print(f"Move {ply_index}: {move_san} | eval_before={eval_before}, eval_after={eval_after}, delta={delta}")


            before_unbalanced = not self.is_balanced(eval_before)
            after_balanced = self.is_balanced(eval_after)
            sufficient_delta = (delta is None) or (delta >= self.min_delta)

            if before_unbalanced and after_balanced and sufficient_delta:
                record = {
                    "game_id": game.headers.get("Event", "Unknown"),
                    "move_number": ply_index,
                    "fen_before": fen_before,
                    "fen_after": fen_after,
                    "eval_before": eval_before,
                    "eval_after": eval_after,
                    "delta": delta,
                    "move_uci": move.uci(),
                    "move_san": move_san,
                }

                # Save to DB
                try:
                    self.db.insert_puzzle(
                        record["game_id"],
                        record["move_number"],
                        record["fen_before"],
                        record["move_uci"],
                        record["eval_before"],
                        record["eval_after"],
                    )
                except Exception as e:
                    # non-fatal: log or print in dev; don't crash the whole run
                    print(f"[Warning] DB insert failed: {e}")

                results.append(record)

        # leave engine alive if you plan to reuse the evaluator; otherwise close.
        # self.engine.close()
        return results
