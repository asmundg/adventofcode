const fs = require("fs");
const path = require("path");

function parse(input) {
  return input.trim().split("\n");
}

function solve(input, marker_length = 4) {
  packets = parse(input);

  res = [];
  for (p of packets) {
    chars = [];
    for (let i = 0; i < p.length; i++) {
      chars.push(p[i]);

      if (chars.length == marker_length + 1) {
        chars.shift();
        if ([...new Set(chars)].length == marker_length) {
          res.push(i + 1);
          break;
        }
      }
    }
  }

  return res;
}

const input_base = path.basename(__filename, ".js").split("_")[1];
console.log(solve(fs.readFileSync(`input/${input_base}.test`, "utf8")));
console.log(solve(fs.readFileSync(`input/${input_base}.input`, "utf8")));

console.log(solve(fs.readFileSync(`input/${input_base}.test`, "utf8"), 14));
console.log(solve(fs.readFileSync(`input/${input_base}.input`, "utf8"), 14));
