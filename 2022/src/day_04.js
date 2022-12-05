const fs = require("fs");

function parse(line) {
  return line.split(",").map((p) => p.split("-").map((c) => parseInt(c)));
}

function contains(a, b) {
  return a[0] >= b[0] && a[1] <= b[1];
}

function overlaps(a, b) {
  return a[1] >= b[0] && b[1] >= a[0];
}

function solve1(input) {
  const lines = input.trim().split("\n");

  count = 0;
  for (const line of lines) {
    const [a, b] = parse(line);
    if (contains(a, b) || contains(b, a)) {
      count++;
    }
  }

  return count;
}

function solve2(input) {
  const lines = input.trim().split("\n");

  count = 0;
  for (const line of lines) {
    const [a, b] = parse(line);
    if (overlaps(a, b)) {
      count++;
    }
  }

  return count;
}

console.log(solve1(fs.readFileSync("input/04.test", "utf8")));
console.log(solve1(fs.readFileSync("input/04.input", "utf8")));

console.log(solve2(fs.readFileSync("input/04.test", "utf8")));
console.log(solve2(fs.readFileSync("input/04.input", "utf8")));
