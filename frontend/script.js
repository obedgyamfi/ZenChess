// let board = null;
// let game = new Chess();
// let currentPuzzle = null;

// async function loadPuzzle() {
//   const res = await fetch("http://127.0.0.1:8000/api/v1/puzzles/random");
//   const data = await res.json();
//   currentPuzzle = data;

//   // Set up board
//   game.load(data.fen_before);
//   board.position(data.fen_before);
//   document.getElementById("feedback").textContent = "Your turn — guess the hidden move!";
// }

// async function onDrop(source, target) {
//   const move = game.move({ from: source, to: target, promotion: 'q' });
//   if (!move) return 'snapback';

//   const body = JSON.stringify({ pgn: game.pgn() });
//   const res = await fetch("http://127.0.0.1:8000/api/v1/evaluate", {
//     method: "POST",
//     headers: { "Content-Type": "application/json" },
//     body
//   });
//   const result = await res.json();

//   if (result.count > 0)
//     document.getElementById("feedback").textContent = "✅ Balanced move!";
//   else
//     document.getElementById("feedback").textContent = "❌ Not balanced — try again!";

//   game.undo();
//   board.position(game.fen());
// }

// document.getElementById("newPuzzle").addEventListener("click", loadPuzzle);

// window.onload = () => {
//   board = Chessboard('board', {
//     draggable: true,
//     position: 'start',
//     onDrop
//   });
//   loadPuzzle();
// };
