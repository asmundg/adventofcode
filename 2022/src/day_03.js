const fs = require("fs");

function calc(char) {
  const code = char.charCodeAt(0);
  return code >= 97 ? code - 96 : code - 38;
}

function solve1(input) {
  const lines = input.trim().split("\n");

  let sum = 0;
  for (const line of lines) {
    const [a, b] = [
      line.substr(0, line.length / 2),
      new Set(line.substr(line.length / 2)),
    ];
    const common = [...a].filter((c) => b.has(c))[0];
    const value = calc(common);
    sum += value;
  }
  return sum;
}

function solve2(input) {
  const lines = input.trim().split("\n");

  let sum = 0;
  let acc = [];
  for (const line of lines) {
    acc.push(new Set(line));
    if (acc.length === 3) {
      const common = [...acc[0]].filter(
        (c) => acc[1].has(c) && acc[2].has(c)
      )[0];
      const value = calc(common);
      sum += value;
      acc = [];
    }
  }
  return sum;
}

console.log(solve1(fs.readFileSync("input/03.test", "utf8")));
console.log(solve1(fs.readFileSync("input/03.input", "utf8")));

console.log(solve2(fs.readFileSync("input/03.test", "utf8")));
console.log(solve2(fs.readFileSync("input/03.input", "utf8")));
