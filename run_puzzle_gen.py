# run_puzzle_gen.py
import os
import sys
from pathlib import Path

# --- Ensure project root is importable ---
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# --- Set working directory to project root ---
os.chdir(BASE_DIR)

# --- Import and run the loader ---
from backend.data.lichess_puzzle_gen import load_games

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate chess puzzles from Lichess games."
    )
    parser.add_argument("username", type=str, help="Lichess username")
    parser.add_argument(
        "max_games", type=int, nargs="?", default=5, help="Number of games to process"
    )
    args = parser.parse_args()

    print(f"Fetching {args.max_games} games for user: {args.username}")
    load_games(args.username, args.max_games)
    print("\n✅ Puzzle generation completed successfully!")
