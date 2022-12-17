/**
 * Day 17:
 */

import * as fs from "fs";
import * as path from "path";

const figures = [
  ["####"],

  [".#.", "###", ".#."],

  ["..#", "..#", "###"],

  ["#", "#", "#", "#"],

  ["##", "##"],
].map((f) => f.map((r) => r.split("")));

function collides(
  stack: string[][],
  figure: string[][],
  [left, bottom]: number[]
): boolean {
  const rows = [];
  if (process.env.DEBUG) {
    for (let y = 0; y < stack.length; y++) {
      const line = [];
      for (let x = 0; x < stack[y].length; x++) {
        line.push(stack[y][x]);
      }
      rows.push(line);
    }
  }

  let collision = false;
  for (let y = 0; y < figure.length; y++) {
    for (let x = 0; x < figure[y].length; x++) {
      if (figure[figure.length - y - 1][x] === "#") {
        if (stack[bottom + y][left + x] !== ".") {
          collision = true;
        }
        if (process.env.DEBUG) {
          rows[bottom + y][left + x] = "@";
        }
      }
    }
  }

  if (process.env.DEBUG) {
    console.log(
      rows
        .reverse()
        .map((row) => row.join(""))
        .join("\n")
    );
    console.log(collision ? "collision!" : "ok");
  }

  return collision;
}

function blit(
  stack: string[][],
  figure: string[][],
  [left, bottom]: [number, number]
): string[][] {
  for (let y = 0; y < figure.length; y++) {
    for (let x = 0; x < figure[y].length; x++) {
      if (figure[figure.length - y - 1][x] === "#") {
        stack[bottom + y][left + x] = "#";
      }
    }
  }

  return stack;
}

function top(stack: string[][]): number {
  for (let i = 1; i < stack.length; i++) {
    if (stack[stack.length - i].some((c) => c === "#")) {
      return stack.length - i;
    }
  }
  return 0;
}

function solve(input: string, target: number): number {
  const jets = input.trim().split("");
  let jet_pos = 0;
  let block = 0;
  let stack: string[][] = [["+", ...Array(7).fill("-"), "+"]];

  while (block < target) {
    if (block % 100000 == 0) {
      console.log(block);
    }

    let bottom_pos = top(stack) + 4;
    let left_pos = 3;
    const figure = figures[block % figures.length];

    const grow = bottom_pos + figure.length - stack.length;
    for (let i = 0; i < grow; i++) {
      stack.push(["|", ...Array(7).fill("."), "|"]);
    }

    while (true) {
      const shift = jets[jet_pos] === ">" ? 1 : -1;
      jet_pos = (jet_pos + 1) % jets.length;
      if (!collides(stack, figure, [left_pos + shift, bottom_pos])) {
        left_pos += shift;
      }
      if (!collides(stack, figure, [left_pos, bottom_pos - 1])) {
        bottom_pos -= 1;
      } else {
        stack = blit(stack, figure, [left_pos, bottom_pos]);
        block++;
        break;
      }
    }
  }

  return top(stack);
}

const input_base = path.resolve(
  __dirname,
  "input",
  `${__filename.split("_")[1].split(".")[0]}`
);

console.log(solve(fs.readFileSync(`${input_base}.test`, "utf8"), 2022));
console.log(solve(fs.readFileSync(`${input_base}.input`, "utf8"), 2022));

console.log(
  solve(fs.readFileSync(`${input_base}.test`, "utf8"), 1000000000000)
);
// console.log(solve2(fs.readFileSync(`${input_base}.input`, "utf8")));
