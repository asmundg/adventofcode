/**
 * Day 11: Monkey in the Middle
 *
 * Mostly a parsing problem.
 *
 * Part 2 relies on a little bith of crucial math that I fortunately
 * learned in the 2020 AoC. :)
 */

import * as fs from "fs";
import * as path from "path";

interface Monkey {
  items: number[];
  op: "+" | "*";
  op_r: "old" | number;
  test: number;
  true_branch: number;
  false_branch: number;
  inspected: number;
}

function parse(input: string): Monkey[] {
  const raw_monkeys = input.trim().split("\n\n");

  const monkeys: Monkey[] = [];

  let i = 0;
  for (const raw_monkey of raw_monkeys) {
    const [, start_line, op_line, test_line, true_line, false_line] =
      raw_monkey.split("\n");
    const items = start_line
      .split("Starting items: ")[1]
      .split(", ")
      .map((item) => parseInt(item, 10));

    const [, op, op_r] = op_line.match(
      /  Operation: new = old (\+|\*) (old|[0-9]+)/
    )!;
    const [, test] = test_line
      .match(/  Test: divisible by ([0-9]+)/)!
      .map((n) => +n);
    const [, true_branch] = true_line
      .match(/    If true: throw to monkey ([0-9]+)/)!
      .map((n) => +n);
    const [, false_branch] = false_line
      .match(/    If false: throw to monkey ([0-9]+)/)!
      .map((n) => +n);

    if (op != "+" && op != "*") {
      throw new Error(`Invalid op: ${op} in ${op_line}`);
    }

    monkeys.push({
      items,
      op,
      op_r: op_r == "old" ? "old" : parseInt(op_r, 10),
      test,
      true_branch,
      false_branch,
      inspected: 0,
    });
  }

  return monkeys;
}

function solve(input: string, rounds = 20, reduce_worry = true): number {
  const monkeys = parse(input);

  // We only care if the item value is divisible by one of the test
  // values. Which means we only need to track the modulo of the
  // product of all the divisiors.
  const period = monkeys.reduce((acc, monkey) => acc * monkey.test, 1);

  for (let round = 0; round < rounds; round++) {
    for (let monkey of monkeys) {
      while (monkey.items.length) {
        const item = monkey.items.shift()!;
        const old = monkey.op_r == "old" ? item : monkey.op_r;
        const new_val =
          Math.floor(
            (monkey.op == "+" ? item + old : item * old) /
              (reduce_worry ? 3 : 1)
          ) % period;

        if (new_val % monkey.test == 0) {
          monkeys[monkey.true_branch].items.push(new_val);
        } else {
          monkeys[monkey.false_branch].items.push(new_val);
        }
        monkey.inspected++;
      }
    }
  }

  const inspected = monkeys
    .map((monkey) => monkey.inspected)
    .sort((a, b) => b - a);
  return inspected[0] * inspected[1];
}

const input_base = path.resolve(
  __dirname,
  "input",
  `${__filename.split("_")[1].split(".")[0]}`
);
console.log(solve(fs.readFileSync(`${input_base}.test`, "utf8")));
console.log(solve(fs.readFileSync(`${input_base}.input`, "utf8")));

console.log(solve(fs.readFileSync(`${input_base}.test`, "utf8"), 10000, false));
console.log(
  solve(fs.readFileSync(`${input_base}.input`, "utf8"), 10000, false)
);
