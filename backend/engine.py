import chess.engine 
from pathlib import Path 

ENGINE_PATH = Path(__file__).resolve().parent.parent / "engine" / "stockfish" / "stockfish.exe"

class ChessEngine:
    def __init__(self, engine_path: str = str(ENGINE_PATH)):
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)

    def evaluate_position(self, fen: str, depth: int = 12) -> float:
        """
        Evaluate a chess position.
        Returns the centipawn score (positive = white better, negative = black better)
        """
        board = chess.Board(fen)
        info = self.engine.analyse(board, limit=chess.engine.Limit(depth=depth))
        score = info["score"].white().score(mate_score=100000)
        # Convert None (mate cases) to large values 
        return float(score) if score is not None else 0.0 
    
    def close(self):
        self.engine.quit()