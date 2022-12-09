/**
 * Day 9: Rope Bridge
 *
 * Rather simple coordinate manipulation. It doesn't really get more
 * complex by adding more knots in part 2, since that just breaks down
 * to performing the same logic for additional pairs of knots.
 */
import * as fs from "fs";
import * as path from "path";

type Point = [number, number];

function parse(input: string) {
  return input
    .trim()
    .split("\n")
    .map((line) => {
      const [d, n] = line.split(" ");
      return [d, parseInt(n, 10)];
    });
}

function touches(h: Point, t: Point): boolean {
  return (
    t[0] >= h[0] - 1 && t[0] <= h[0] + 1 && t[1] >= h[1] - 1 && t[1] <= h[1] + 1
  );
}

function follow(h: Point, t: Point): Point {
  if (touches(h, t)) {
    return t;
  }

  const new_t0 = t[0] == h[0] ? t[0] : h[0] > t[0] ? t[0] + 1 : t[0] - 1;
  const new_t1 = t[1] == h[1] ? t[1] : h[1] > t[1] ? t[1] + 1 : t[1] - 1;
  return [new_t0, new_t1];
}

function solve(input: string, n_knots: number) {
  const moves = parse(input);
  const knots: [number, number][] = new Array(n_knots)
    .fill(0)
    .map((_) => [0, 0]);
  const visits = new Set();

  for (const [d, n] of moves) {
    for (let i = 0; i < n; i++) {
      switch (d) {
        case "U":
          knots[0][0]--;
          break;
        case "D":
          knots[0][0]++;
          break;
        case "L":
          knots[0][1]--;
          break;
        case "R":
          knots[0][1]++;
          break;
        default:
          throw new Error("Unknown direction");
      }
      for (let k = 1; k < n_knots; k++) {
        knots[k] = follow(knots[k - 1], knots[k]);
      }
      visits.add(`${knots[n_knots - 1][0]}.${knots[n_knots - 1][1]}`);
    }
  }

  return visits.size;
}

function solve1(input: string) {
  return solve(input, 2);
}

function solve2(input: string) {
  return solve(input, 10);
}

const input_base = path.resolve(
  __dirname,
  "input",
  `${__filename.split("_")[1].split(".")[0]}`
);
console.log(solve1(fs.readFileSync(`${input_base}.test`, "utf8")));
console.log(solve1(fs.readFileSync(`${input_base}.input`, "utf8")));

console.log(solve2(fs.readFileSync(`${input_base}.test`, "utf8")));
console.log(solve2(fs.readFileSync(`${input_base}.input`, "utf8")));
