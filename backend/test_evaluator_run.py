from evaluator import BalanceEvaluator

pgn_sample = """
[Event "Example Game"]
[Site "ZenChess"]
[Date "2025.11.02"]
[Round "1"]
[White "Alpha"]
[Black "Beta"]
[Result "*"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 d6 8. c3 O-O
9. h3 Nb8 10. d4 Nbd7 11. Nbd2 Bb7 12. Bc2 Re8 13. Nf1 Bf8 14. Ng3 g6 15. Bg5 h6
16. Be3 Bg7 17. Qd2 h5 *
"""

if __name__ == "__main__":
    evaluator = BalanceEvaluator(depth=10, balance_threshold=40.0, min_delta=0.0)
    results = evaluator.find_balancing_moves(pgn_sample)
    print(f"Found {len(results)} balancing moves:\n")
    print({"count": len(results), "results": results})
    # for r in results:
        # print(f"Move {r['move_number']}: {r['move_san']} | {r['eval_before']} → {r['eval_after']}")

