/**
 * Day 15: Beacon Exclusion Zone
 *
 * Some simple range math today, to avoid blowing up heap space by
 * storing individual coordinates.
 *
 * Doing the usual approach and calculating the complete data
 * structure was also a mistake here, as part 2 blows up the heap,
 * even with ranges. The trick was to realize that I should rewind
 * completely and calculate one line at a time. Which is what part 1
 * very explicitly tells you to do, as a matter of fact.
 *
 * Once we look at each line, it's trivial to control both
 * computational and spatial complexity. Neither part 1 nor part 2
 * ever requires looking at more than the current line.
 */

import * as fs from "fs";
import * as path from "path";

type Sensor = [[number, number], [number, number]];

function parse(input: string): Sensor[] {
  const sensors = input
    .trim()
    .split("\n")
    .map((l) =>
      l
        .match(
          "Sensor at x=(-?[0-9]+), y=(-?[0-9]+): closest beacon is at x=(-?[0-9]+), y=(-?[0-9]+)"
        )!
        .slice(1, 5)
        .map((n) => parseInt(n))
    );
  return sensors.map((s) => [
    [s[1], s[0]],
    [s[3], s[2]],
  ]);
}

function line_range(sensors: Sensor[], target_y: number): [number, number][] {
  const line: [number, number][] = [];
  sensors.forEach(([[s_y, s_x], [b_y, b_x]]) => {
    const dist = Math.abs(Math.abs(s_x - b_x) + Math.abs(s_y - b_y));
    if (s_y - dist > target_y || s_y + dist < target_y) {
      // no coverage
      return;
    }

    const d_y = Math.abs(s_y - target_y);
    line.push([s_x - (dist - Math.abs(d_y)), s_x + dist - Math.abs(d_y)]);
  });

  // Merge overlapping ranges
  const sorted = line.sort(([a_min, _a_max], [b_min, _b_max]) => a_min - b_min);
  const final = [sorted[0]];
  sorted.forEach(([min, max]) => {
    const [target_min, target_max] = final[final.length - 1];
    if (min <= target_max && max >= target_min) {
      const [new_min, new_max] = [
        Math.min(min, target_min),
        Math.max(max, target_max),
      ];
      final.splice(final.length - 1, 1, [new_min, new_max]);
    } else {
      final.push([min, max]);
    }
  });

  return final;
}

function solve1(input: string, target: number): number {
  const sensors = parse(input);

  return line_range(sensors, target).reduce(
    (acc, [v_min, v_max]) => acc + (v_max - v_min),
    0
  );
}

function solve2(input: string, min: number, max: number): number {
  const sensors = parse(input);

  for (let i = min; i < max; i++) {
    const line = line_range(sensors, i);
    if (line.length > 1) {
      return i + (line[0][1] + 1) * 4000000;
    }
  }

  throw new Error("No solution found");
}

const input_base = path.resolve(
  __dirname,
  "input",
  `${__filename.split("_")[1].split(".")[0]}`
);
console.log(solve1(fs.readFileSync(`${input_base}.test`, "utf8"), 10));
console.log(solve1(fs.readFileSync(`${input_base}.input`, "utf8"), 2000000));

console.log(solve2(fs.readFileSync(`${input_base}.test`, "utf8"), 0, 20));
console.log(solve2(fs.readFileSync(`${input_base}.input`, "utf8"), 0, 4000000));
