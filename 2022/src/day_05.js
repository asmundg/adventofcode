const fs = require("fs");
const path = require("path");

function parse(input) {
  const lines = input.trimEnd().split("\n");

  let line_no = 0;
  let read_stacks = false;
  stacks = new Array(Math.ceil(lines[0].length / 4)).fill(0).map(() => []);
  while (!read_stacks) {
    for (let char = 1; char < lines[0].length; char += 4) {
      if (lines[line_no][char].match(/[0-9]+/)) {
        read_stacks = true;
        break;
      }

      stack_idx = Math.floor(char / 4);
      if (lines[line_no][char] === " ") {
        continue;
      } else {
        stacks[stack_idx].push(lines[line_no][char]);
      }
    }

    line_no += 1;
  }

  line_no += 1;
  return [
    stacks,
    lines.slice(line_no).map((line) =>
      line
        .split(" ")
        .filter((s) => /[0-9]+/.test(s))
        .map((s) => parseInt(s))
    ),
  ];
}

function solve1(input) {
  const [stacks, moves] = parse(input);
  for (const [nums, src, target] of moves) {
    for (let n = 0; n < nums; n++) {
      char = stacks[src - 1].shift();
      stacks[target - 1].unshift(char);
    }
  }

  return stacks.reduce((acc, stack) => (acc += stack[0]), "");
}

function solve2(input) {
  const [stacks, moves] = parse(input);
  for (const [nums, src, target] of moves) {
    const crates = stacks[src - 1].splice(0, nums);
    stacks[target - 1].unshift(...crates);
  }

  return stacks.reduce((acc, stack) => (acc += stack[0]), "");
}

const input_base = path.basename(process.argv[1], ".js").split("_")[1];
console.log(solve1(fs.readFileSync(`input/${input_base}.test`, "utf8")));
console.log(solve1(fs.readFileSync(`input/${input_base}.input`, "utf8")));

console.log(solve2(fs.readFileSync(`input/${input_base}.test`, "utf8")));
console.log(solve2(fs.readFileSync(`input/${input_base}.input`, "utf8")));
