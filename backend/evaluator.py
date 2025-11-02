import chess.pgn 
from io import StringIO
from engine import ChessEngine 

class BalanceEvaluator:
    def __init__(self, depth: int = 12, balance_threshold: float = 50.0):
        """
        :param depth: Engine search depth 
        :param balance_threshold: Centipawn threshold for considering position balance
        """
        self.engine = ChessEngine()
        self.depth = depth 
        self.balance_threshold = balance_threshold

    def is_balanced(self, score: float) -> bool:
        """Return True if position is approximately balanced."""
        return abs(score) <= self.balance_threshold
    
    def find_balancing_moves(self, pgn_text: str):
        """
        Parse a PGN game and find moves that balance the position.
        Returns a list of (move_number, fen_before, fen_after, score_before, score_after)
        """
        game = chess.pgn.read_game(StringIO(pgn_text))
        board = game.board()

        results = [] 
        previous_score = None 

        for move_number, move in enumerate(game.mainline_moves(), start=1):
            fen_before = board.fen()
            score_before = self.engine.evaluate_position(fen_before, depth=self.depth)

            board.push(move)
            fen_after = board.fen()
            score_after = self.engine.evaluate_position(fen_after, depth=self.depth)

            # Detect balancing transition 
            if (
                previous_score is not None 
                and not self.is_balanced(previous_score)
                and self.is_balanced(score_after)
            ):
                results.append({
                    "move_number": move_number,
                    "fen_before": fen_before,
                    "fen_after": fen_after, 
                    "score_before": previous_score,
                    "score_after": score_after,
                    "move_san": board.san(move) if move in board.legal_moves else move.uci()
                })

            previous_score = score_after
        
        self.engine.close()
        return results
        
