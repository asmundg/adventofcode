/**
 * Day 8: Treetop Tree House
 *
 * Off-by-one city!
 *
 * This is a simple neighbour walk of an array. I was a bit worried
 * about complexity getting out of hand, so did some additional work
 * to reduce the number of passes needed.
 *
 * I didn't check how costly brute force is, but we can reduce the
 * cost of part 2 significantly by only considering the tallest
 * trees. If you can see to an edge, there's no point in considering
 * trees closer to that edge.
 */
const fs = require("fs");
const path = require("path");

function parse(input) {
  return input
    .trim()
    .split("\n")
    .map((line) => line.split("").map((c) => parseInt(c)));
}

function height_map(trees) {
  const tallest_top = new Array(trees.length)
    .fill(0)
    .map((_) => new Array(trees[0].length).fill(0));
  const tallest_bottom = new Array(trees.length)
    .fill(0)
    .map((_) => new Array(trees[0].length).fill(0));
  const tallest_left = new Array(trees.length)
    .fill(0)
    .map((_) => new Array(trees[0].length).fill(0));
  const tallest_right = new Array(trees.length)
    .fill(0)
    .map((_) => new Array(trees[0].length).fill(0));

  for (let y = 0; y < trees.length; y++) {
    let tallest = 0;
    for (let x = 0; x < trees.length; x++) {
      if (trees[y][x] > tallest) {
        tallest = trees[y][x];
      }
      tallest_left[y][x] = tallest;
    }

    tallest = 0;
    for (let x = trees.length - 1; x >= 0; x--) {
      if (trees[y][x] > tallest) {
        tallest = trees[y][x];
      }
      tallest_right[y][x] = tallest;
    }
  }

  for (let x = 0; x < trees[0].length; x++) {
    let tallest = 0;
    for (let y = 0; y < trees.length; y++) {
      if (trees[y][x] > tallest) {
        tallest = trees[y][x];
      }
      tallest_top[y][x] = tallest;
    }

    tallest = 0;
    for (let y = trees[0].length - 1; y >= 0; y--) {
      if (trees[y][x] > tallest) {
        tallest = trees[y][x];
      }
      tallest_bottom[y][x] = tallest;
    }
  }

  return [tallest_left, tallest_right, tallest_top, tallest_bottom];
}

function tallest(input) {
  const trees = parse(input);
  const [tallest_left, tallest_right, tallest_top, tallest_bottom] =
    height_map(trees);
  const visible = new Set();

  for (let y = 0; y < trees.length; y++) {
    for (let x = 0; x < trees.length; x++) {
      if (x == 0 || trees[y][x] > tallest_left[y][x - 1]) {
        visible.add(`${y}.${x}`);
      }
      if (x == trees[0].length - 1 || trees[y][x] > tallest_right[y][x + 1]) {
        visible.add(`${y}.${x}`);
      }
      if (y == 0 || trees[y][x] > tallest_top[y - 1][x]) {
        visible.add(`${y}.${x}`);
      }
      if (y == trees.length - 1 || trees[y][x] > tallest_bottom[y + 1][x]) {
        visible.add(`${y}.${x}`);
      }
    }
  }

  return visible;
}

function solve1(input) {
  return tallest(input).size;
}

function solve2(input) {
  const trees = parse(input);
  const tallest_trees = tallest(input);

  let best = 0;
  for (const tree of tallest_trees) {
    const [y, x] = tree.split(".").map((c) => parseInt(c));
    if (y == 0 || y == trees.length - 1 || x == 0 || x == trees[0].length - 1) {
      continue;
    }

    let score = 1;

    // right
    let count = 1;
    for (; x + count < trees[0].length - 1; count++) {
      if (trees[y][x + count] >= trees[y][x]) {
        break;
      }
    }
    score *= count;

    // left
    count = 1;
    for (; x - count > 0; count++) {
      if (trees[y][x - count] >= trees[y][x]) {
        break;
      }
    }
    score *= count;

    // down
    count = 1;
    for (; y + count < trees.length - 1; count++) {
      if (trees[y + count][x] >= trees[y][x]) {
        break;
      }
    }
    score *= count;

    // up
    count = 1;
    for (; y - count > 0; count++) {
      if (trees[y - count][x] >= trees[y][x]) {
        break;
      }
    }
    score *= count;

    if (score > best) {
      best = score;
    }
  }

  return best;
}

const input_base = path.basename(__filename, ".js").split("_")[1];
console.log(solve1(fs.readFileSync(`input/${input_base}.test`, "utf8")));
console.log(solve1(fs.readFileSync(`input/${input_base}.input`, "utf8")));

console.log(solve2(fs.readFileSync(`input/${input_base}.test`, "utf8"), 14));
console.log(solve2(fs.readFileSync(`input/${input_base}.input`, "utf8"), 14));
