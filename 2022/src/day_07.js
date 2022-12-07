/**
 * Day 7: No Space Left On Device
 *
 * A very simple FS representation. In order to not confuse my brain
 * too much (and size I was concerned about the shell re-entering
 * directories or part 2 requiring different processing logic), we do
 * this in two passes:
 *
 * 1. Parse shell output to reconstruct the FS structure. This is a
 * flat map, indexed on the path, making lookup simple.
 * 2. Walk the FS, accumulating sizes.
 */
const fs = require("fs");
const path = require("path");

function parse(input) {
  const lines = input.trim().split("\n");

  let p = [""];
  const tree = { "": [] };
  let l = 0;
  while (l < lines.length) {
    if (lines[l][0] == "$") {
      [, cmd, arg] = lines[l].split(" ");
      switch (cmd) {
        case "cd":
          if (arg == "..") {
            p.pop();
          } else if (arg == "/") {
            p = [""];
          } else {
            p.push(arg);
            if (!tree[p.join("/")]) {
              tree[p.join("/")] = [];
            }
          }
          l++;
          break;
        case "ls":
          l++;
          while (lines[l] && lines[l][0] != "$") {
            const [size, fname] = lines[l].split(" ");
            if (size == "dir") {
              tree[p.join("/")].push({ type: "d", name: fname });
            } else {
              tree[p.join("/")].push({
                type: "f",
                name: fname,
                size: parseInt(size),
              });
            }
            l++;
          }
          break;
      }
    }
  }

  return tree;
}

function walk(tree, path, acc) {
  for (const entry of tree[path]) {
    if (entry.type == "d") {
      const new_path = [path, entry.name].join("/");
      acc[new_path] = 0;
      acc[path] += walk(tree, new_path, acc);
    } else {
      acc[path] += entry.size;
    }
  }

  return acc[path];
}

function solve1(input) {
  const tree = parse(input);

  const acc = { "": 0 };
  walk(tree, "", acc);

  const limit = 100000;
  let sum = 0;
  for (const path of Object.keys(acc)) {
    if (acc[path] <= limit) {
      sum += acc[path];
    }
  }

  return sum;
}

function solve2(input) {
  const tree = parse(input);

  const acc = { "": 0 };
  walk(tree, "", acc);

  const total = 70000000;
  const target = 30000000;
  const used = acc[""];
  const free = total - used;
  const need = target - free;

  let best = "";
  for (const path of Object.keys(acc)) {
    if (acc[path] >= need) {
      if (acc[path] < acc[best]) {
        best = path;
      }
    }
  }
  return acc[best];
}

const input_base = path.basename(__filename, ".js").split("_")[1];
console.log(solve1(fs.readFileSync(`input/${input_base}.test`, "utf8")));
console.log(solve1(fs.readFileSync(`input/${input_base}.input`, "utf8")));

console.log(solve2(fs.readFileSync(`input/${input_base}.test`, "utf8"), 14));
console.log(solve2(fs.readFileSync(`input/${input_base}.input`, "utf8"), 14));
