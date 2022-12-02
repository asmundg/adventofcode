const fs = require("fs");

// Rock: A, X
// Paper: B, Y
// Scissors: C, Z
map = { X: "A", Y: "B", Z: "C" };
correct_selection = { A: "B", B: "C", C: "A" };
incorrect_selection = { A: "C", B: "A", C: "B" };
values = { A: 1, B: 2, C: 3 };
result_scores = [0, 3, 6];

function calc(theirs, mine) {
  return (
    values[mine] +
    (mine == correct_selection[theirs]
      ? result_scores[2]
      : theirs == mine
      ? result_scores[1]
      : result_scores[0])
  );
}

function solve1(input) {
  const lines = input.trim().split("\n");

  let score = 0;
  for (const line of lines) {
    [theirs, mine] = line.split(" ");
    mine = map[mine];

    score += calc(theirs, mine);
  }

  return score;
}

function solve2(input) {
  const lines = input.trim().split("\n");

  let score = 0;
  for (const line of lines) {
    let [theirs, mine] = line.split(" ");
    switch (mine) {
      case "X":
        mine = incorrect_selection[theirs];
        break;
      case "Y":
        mine = theirs;
        break;
      case "Z":
        mine = correct_selection[theirs];
        break;
    }
    score += calc(theirs, mine);
  }

  return score;
}

console.log(solve1(fs.readFileSync("input/02.test", "utf8")));
console.log(solve1(fs.readFileSync("input/02.input", "utf8")));

console.log(solve2(fs.readFileSync("input/02.test", "utf8")));
console.log(solve2(fs.readFileSync("input/02.input", "utf8")));
