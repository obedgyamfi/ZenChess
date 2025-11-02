# loader.py
import requests
from backend.evaluator import BalanceEvaluator


class GameLoader:
    def __init__(self, username: str, max_games: int = 10):
        self.username = username
        self.max_games = max_games
        self.evaluator = BalanceEvaluator(depth=10, balance_threshold=40.0, min_delta=0.0)

    def fetch_games(self):
        """Fetch PGN games for a user from Lichess."""
        url = f"https://lichess.org/api/games/user/{self.username}"
        params = {
            "max": self.max_games,
            "analysed": "true",
            "moves": "true",
            "tags": "true",
            "pgnInJson": "false",
        }
        headers = {"Accept": "application/x-chess-pgn"}
        print(f"Fetching up to {self.max_games} games for user: {self.username}")
        r = requests.get(url, headers=headers, params=params, timeout=30)
        r.raise_for_status()
        # Games are separated by blank lines
        pgns = [g.strip() for g in r.text.split("\n\n\n") if g.strip()]
        print(f"Fetched {len(pgns)} games.")
        return pgns

    def process_games(self):
        """Fetch games, process them, and store puzzles in the database."""
        games = self.fetch_games()
        total_puzzles = 0

        for idx, pgn_text in enumerate(games, start=1):
            print(f"\nProcessing game {idx}/{len(games)}...")
            results = self.evaluator.find_balancing_moves(pgn_text)
            # records = results.get("results", [])
            records = results if isinstance(results, list) else results.get("results", [])
            print(f"  Found {len(records)} puzzle candidates.")

            for rec in records:
                try:
                    self.evaluator.db.insert_puzzle(
                        rec["game_id"],
                        rec["move_number"],
                        rec["fen_before"],
                        rec["move_uci"],
                        rec["eval_before"],
                        rec["eval_after"],
                    )
                    total_puzzles += 1
                except Exception as e:
                    print(f"  [DB insert failed] {e}")

        print(f"\n✅ Finished. Added {total_puzzles} new puzzles.")
        return total_puzzles


def load_games(username: str, max_games: int = 10):
    """Convenience function for direct import or CLI use."""

    loader = GameLoader(username=username, max_games=max_games)
    
    # Clear the database before loading new puzzles 
    loader.evaluator.db.clear_puzzles()

    return loader.process_games()


if __name__ == "__main__":
    # Example: load_games("MagnusCarlsen", 5)
    import sys
    if len(sys.argv) < 2:
        print("Usage: python loader.py <lichess_username> [max_games]")
        sys.exit(1)
    username = sys.argv[1]
    max_games = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    load_games(username, max_games)
