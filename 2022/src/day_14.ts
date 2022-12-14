/**
 * Day 14: Regolith Reservoir
 *
 * We only really need to track the filled spaces, i.e. the
 * coordinates where there is 'something'. This avoid the issue of
 * tracking empty space in an infinitely expanding grid.
 *
 * Falling off the world is detected heuristically when the sand is
 * lower than the lowest known obstacle. This is modified slightly for
 * part 2, where there is always an obstacle at max_y + 2
 *
 * The render function wasn't strictly necessary, but this task just
 * begs for a visualisation.
 */

import * as fs from "fs";
import * as path from "path";

function parse(input: string): {
  box: Record<string, string>;
  constraints: { min_y: number; max_y: number; min_x: number; max_x: number };
} {
  const paths = input
    .trim()
    .split("\n")
    .map((l) =>
      l.split(" -> ").map((c) => c.split(",").map((n) => parseInt(n, 10)))
    );

  let [min_x, max_x, min_y, max_y] = [paths[0][0][0], 0, paths[0][0][1], 0];
  const box = paths.reduce((box, path) => {
    for (let i = 0; i < path.length - 1; i++) {
      const [[a_x, a_y], [b_x, b_y]] = [path[i], path[i + 1]];
      min_x = Math.min(min_x, a_x, b_x);
      max_x = Math.max(max_x, a_x, b_x);
      min_y = Math.min(min_y, a_y, b_y);
      max_y = Math.max(max_y, a_y, b_y);

      if (a_x == b_x) {
        for (let y = Math.min(a_y, b_y); y <= Math.max(a_y, b_y); y++) {
          box[`${y}.${a_x}`] = "#";
        }
      } else {
        for (let x = Math.min(a_x, b_x); x <= Math.max(a_x, b_x); x++) {
          box[`${a_y}.${x}`] = "#";
        }
      }
    }
    return box;
  }, {} as Record<string, string>);

  return { box, constraints: { min_y, max_y, min_x, max_x } };
}

function render(
  box: Record<string, string>,
  {
    min_y,
    max_y,
    min_x,
    max_x,
  }: { min_y: number; max_y: number; min_x: number; max_x: number }
): void {
  for (let y = min_y; y <= max_y; y++) {
    let l = "";
    for (let x = min_x; x <= max_x; x++) {
      l += box[`${y}.${x}`] || " ";
    }
    console.log(l);
  }
}

function solve1(input: string): number {
  const {
    box,
    constraints: { min_x, max_x, min_y, max_y },
  } = parse(input);

  let fell_off = false;
  let loops = 0;
  while (!fell_off) {
    fell_off = true;
    let sand = [0, 500];
    while (sand[0] <= max_y) {
      if (!box[`${sand[0] + 1}.${sand[1]}`]) {
        sand[0]++;
      } else if (!box[`${sand[0] + 1}.${sand[1] - 1}`]) {
        sand[0]++;
        sand[1]--;
      } else if (!box[`${sand[0] + 1}.${sand[1] + 1}`]) {
        sand[0]++;
        sand[1]++;
      } else {
        loops += 1;
        fell_off = false;
        box[`${sand[0]}.${sand[1]}`] = "o";
        break;
      }
    }

    process.env.DEBUG && render(box, { min_y, max_y, min_x, max_x });
  }

  return loops;
}

function solve2(input: string): number {
  let {
    box,
    constraints: { min_x, max_x, min_y, max_y },
  } = parse(input);

  let loops = 0;
  while (!box[`${0}.${500}`]) {
    let sand = [0, 500];
    while (true) {
      if (sand[0] < max_y + 1 && !box[`${sand[0] + 1}.${sand[1]}`]) {
        sand[0]++;
      } else if (sand[0] < max_y + 1 && !box[`${sand[0] + 1}.${sand[1] - 1}`]) {
        sand[0]++;
        sand[1]--;
      } else if (sand[0] < max_y + 1 && !box[`${sand[0] + 1}.${sand[1] + 1}`]) {
        sand[0]++;
        sand[1]++;
      } else {
        loops += 1;
        min_x = Math.min(min_x, sand[1]);
        max_x = Math.max(max_x, sand[1]);
        box[`${sand[0]}.${sand[1]}`] = "o";
        break;
      }
    }

    process.env.DEBUG &&
      render(box, { min_y: 0, max_y: max_y + 2, min_x, max_x });
  }

  return loops;
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
