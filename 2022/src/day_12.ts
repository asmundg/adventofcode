/**
 * Day 12: Hill Climbing Algorithm
 *
 * It's A* day!
 */

import * as fs from "fs";
import * as path from "path";

function reconstruct_path(
  cameFrom: Map<string, string>,
  current: string
): string[] {
  const totalPath = [current];
  while (cameFrom.has(current)) {
    current = cameFrom.get(current)!;
    totalPath.unshift(current);
  }

  return totalPath;
}

function neighbours(node: string, map: string[]): string[] {
  const [y, x] = node.split(",").map((x) => parseInt(x));
  return [
    [y + 1, x],
    [y - 1, x],
    [y, x + 1],
    [y, x - 1],
  ]
    .filter(
      (n) => n[0] >= 0 && n[0] < map.length && n[1] >= 0 && n[1] < map[0].length
    )
    .filter((n) => {
      const char = map[n[0]][n[1]];
      const val = char == "E" ? "z".charCodeAt(0) : char.charCodeAt(0);
      return map[y][x] == "S" || val <= map[y][x].charCodeAt(0) + 1;
    })
    .map((n) => n.join(","));
}

// A*
function a_star(start: string, goal: string, map: string[]): string[] {
  const openSet: string[] = [start];
  const cameFrom = new Map<string, string>();

  const gScore = new Map<string, number>();
  gScore.set(start, 0);

  const fScore = new Map<string, number>();
  fScore.set(start, 1);

  while (openSet.length > 0) {
    const current = openSet.reduce(
      (lowest, cur) => (fScore.get(cur)! < fScore.get(lowest)! ? cur : lowest),
      openSet[0]
    )!;
    openSet.splice(openSet.indexOf(current), 1);

    if (current == goal) {
      return reconstruct_path(cameFrom, current);
    }

    for (const neighbor of neighbours(current, map)) {
      const tentative_gScore = gScore.get(current)! + 1;
      if (!gScore.has(neighbor) || tentative_gScore < gScore.get(neighbor)!) {
        cameFrom.set(neighbor, current);
        gScore.set(neighbor, tentative_gScore);
        fScore.set(neighbor, tentative_gScore + 1);
        if (!openSet.some((x) => x == neighbor)) {
          openSet.push(neighbor);
        }
      }
    }
  }

  throw new Error("No path found");
}

function solve(input: string): number {
  const map = input.trim().split("\n");
  const start_idx = map
    .join("")
    .split("")
    .findIndex((x) => x == "S");
  const start = `${Math.floor(start_idx / map[0].length)},${
    start_idx % map[0].length
  }`;

  const goal_idx = map
    .join("")
    .split("")
    .findIndex((x) => x == "E");
  const goal = `${Math.floor(goal_idx / map[0].length)},${
    goal_idx % map[0].length
  }`;

  return a_star(start, goal, map).length - 1;
}

function solve2(input: string): number {
  const map = input.trim().split("\n");
  const goal_idx = map
    .join("")
    .split("")
    .findIndex((x) => x == "E");
  const goal = `${Math.floor(goal_idx / map[0].length)},${
    goal_idx % map[0].length
  }`;

  let best = 10000;
  for (let y = 0; y < map.length; y++) {
    for (let x = 0; x < map[0].length; x++) {
      if (map[y][x] == "S" || map[y][x] == "a") {
        try {
          const length = a_star(`${y},${x}`, goal, map).length - 1;
          if (length < best) {
            best = length;
          }
        } catch {
          // There may be starting points that we can't exit
        }
      }
    }
  }

  return best;
}

const input_base = path.resolve(
  __dirname,
  "input",
  `${__filename.split("_")[1].split(".")[0]}`
);
console.log(solve(fs.readFileSync(`${input_base}.test`, "utf8")));
console.log(solve(fs.readFileSync(`${input_base}.input`, "utf8")));

console.log(solve2(fs.readFileSync(`${input_base}.test`, "utf8")));
console.log(solve2(fs.readFileSync(`${input_base}.input`, "utf8")));
