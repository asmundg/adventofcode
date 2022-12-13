/**
 * Day 13: Distress Signal
 *
 * We're implementing compare today. I considered writing the parser
 * as well, but since this is valid JSON, the temptation to use the
 * existing parser was too great.
 *
 * Implementing part 1 using compare semantics (<0, 0, >0) means we
 * can trivially solve part 2 with an array sort.
 */

import * as fs from "fs";
import * as path from "path";

type Value = number | number[] | Value[];

function compare(a: Value, b: Value): number {
  if (Number.isInteger(a) && Number.isInteger(b)) {
    return (a as number) - (b as number);
  } else if (Array.isArray(a) && Array.isArray(b)) {
    let idx = 0;
    while (true) {
      if (idx >= a.length && idx < b.length) {
        return -1;
      } else if (idx < a.length && idx >= b.length) {
        return 1;
      } else if (idx >= a.length && idx >= b.length) {
        return 0;
      }

      const sub = compare(a[idx], b[idx++]);
      if (sub != 0) {
        return sub;
      }
    }
  } else if (Array.isArray(a) && Number.isInteger(b)) {
    return compare(a, [b]);
  } else if (Number.isInteger(a) && Array.isArray(b)) {
    return compare([a], b);
  }

  throw new Error(`Invalid input ${a} ${b}`);
}

function solve1(input: string): number {
  const pairs = input
    .trim()
    .split("\n\n")
    .map((p) => p.split("\n").map((l) => JSON.parse(l))) as [Value, Value][];

  return pairs.reduce(
    (acc, [a, b], i) => (compare(a, b) < 0 ? acc + i + 1 : acc),
    0
  );
}

function solve2(input: string): number {
  const packets = input
    .trim()
    .split("\n")
    .filter((l) => !!l)
    .map((l) => JSON.parse(l));
  packets.push([[2]]);
  packets.push([[6]]);

  const sorted = packets.sort((a, b) => compare(a, b));
  return (
    (sorted.findIndex((e) => e.toString() == [2].toString()) + 1) *
    (sorted.findIndex((e) => e.toString() == [6].toString()) + 1)
  );
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
