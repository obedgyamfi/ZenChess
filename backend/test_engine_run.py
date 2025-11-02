from engine import ChessEngine

if __name__ == "__main__":
    engine = ChessEngine()
    # Start position (balanced)
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    score = engine.evaluate_position(fen)
    print(f"Evaluation of start position: {score} centipawns")
    engine.close()
