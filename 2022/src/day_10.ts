/**
 * Day 10: Cathode-Ray Tube
 *
 * 2019 redux! This is _almost_ purely mechanical, but the 1-indexed
 * cycles and 0-indexed pixels in part 2 was a bit annoying to get
 * right. The fact that we want the register value _during_ the cycle
 * also takes a bit of careful reading.
 */
import * as fs from "fs";
import * as path from "path";

type op = ["noop"] | ["addx", number];

function parse(input: string): op[] {
  return input
    .trim()
    .split("\n")
    .map((line) => {
      const [op, n] = line.split(" ");
      if (op == "noop") {
        return ["noop"];
      } else if (op == "addx") {
        return ["addx", parseInt(n)];
      } else {
        throw new Error(`invalid op ${op}`);
      }
    });
}

function render({
  cycle,
  x,
  screen,
}: {
  cycle: number;
  x: number;
  screen: string[];
}): void {
  const line = Math.floor((cycle - 1) / 40);
  if (screen.length < line + 1) {
    screen.push("");
  }

  const pixel_pos = (cycle - 1) % 40;
  screen[line] += pixel_pos >= x - 1 && pixel_pos <= x + 1 ? "#" : ".";
}

function step({
  cycle,
  x,
  screen,
}: {
  cycle: number;
  x: number;
  screen: string[];
}): number {
  const sample_cycles = new Set([20, 60, 100, 140, 180, 220]);
  render({ cycle, x, screen });
  if (sample_cycles.has(cycle)) {
    return cycle * x;
  } else {
    return 0;
  }
}

function solve(input: string): number {
  const ops = parse(input);
  let sum = 0;
  let cycle = 0;
  let x = 1;
  const screen: string[] = [];
  for (const [op, n] of ops) {
    if (op == "noop") {
      cycle += 1;
      sum += step({ cycle, x, screen });
    } else if (op == "addx") {
      cycle += 1;
      sum += step({ cycle, x, screen });

      cycle += 1;
      sum += step({ cycle, x, screen });

      x += n;
    }
  }

  console.log(screen.join("\n"));
  return sum;
}

const input_base = path.resolve(
  __dirname,
  "input",
  `${__filename.split("_")[1].split(".")[0]}`
);
console.log(solve(fs.readFileSync(`${input_base}.test`, "utf8")));
console.log(solve(fs.readFileSync(`${input_base}.input`, "utf8")));
