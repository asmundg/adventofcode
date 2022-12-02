const fs = require("fs");

function calc(input) {
  const lines = input.split("\n");
  elves = [];

  current = 0;
  for (line of lines) {
    if (line == "") {
      elves.push(current);
      current = 0;
    } else {
      current += parseInt(line);
    }
  }
  elves.push(current);

  return elves.sort((a, b) => a - b);
}

function solve1(input) {
  res = calc(input);
  return res[res.length - 1];
}

function solve2(input) {
  res = calc(input);
  return res[res.length - 1] + res[res.length - 2] + res[res.length - 3];
}

console.log(solve1(fs.readFileSync("input/01.test", "utf8")));
console.log(solve1(fs.readFileSync("input/01.input", "utf8")));

console.log(solve2(fs.readFileSync("input/01.test", "utf8")));
console.log(solve2(fs.readFileSync("input/01.input", "utf8")));
