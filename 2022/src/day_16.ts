/**
 * Day 16: Proboscidea Volcanium
 *
 * I was fully convinced that I had made a fundamental mistake, since
 * the runtime for part2 is well above 5 minutes. So I ended up
 * cheating a bit here.
 *
 * Turns out brute forcing is the thing to do. Just generate all
 * possible paths. We only care about valves that provide flow, so we
 * need to find the shortest paths between them, ignoring "empty" tunnels.
 *
 * I'm beginning to miss python now.
 */

import * as fs from "fs";
import * as path from "path";

type Graph = Record<
  string,
  {
    rate: number;
    min_edges: Record<string, number>;
    edges: string[];
  }
>;

function parse(input: string): Graph {
  const graph = input
    .trim()
    .split("\n")
    .map(
      (s) =>
        s.match(
          /Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? (.*)/
        )!
    )
    .reduce((graph, [_, id, rate, edges]) => {
      graph[id] = {
        rate: parseInt(rate),
        edges: edges.split(", "),
        min_edges: {},
      };
      return graph;
    }, {} as Graph);

  Object.keys(graph).forEach(
    (node) => (graph[node].min_edges = dijkstra(graph, node))
  );
  return graph;
}

// spanning tree
function dijkstra(graph: Graph, start: string): Record<string, number> {
  const unvisited = new Set<string>(Object.keys(graph));
  const costs = Object.keys(graph).reduce((o, k) => {
    o[k] = 10000;
    return o;
  }, {} as Record<string, number>);
  costs[start] = 0;

  while (unvisited.size) {
    const node = [...unvisited]
      .filter((node) => costs[node] !== undefined)
      .sort((a, b) => costs[a] - costs[b])[0];
    unvisited.delete(node);
    const cost = costs[node]!;

    graph[node].edges.forEach((edge) => {
      const new_cost = cost + 1;
      if (costs[edge] === undefined || new_cost < costs[edge]) {
        costs[edge] = new_cost;
      }
    });
  }

  return Object.entries(costs).reduce((o, [node, cost]) => {
    graph[node].rate > 0 && cost > 0 && (o[node] = cost);
    return o;
  }, {} as Record<string, number>);
}

function all_paths(graph: Graph, t: number): string[][] {
  const paths: string[][] = [];
  function dfs(node: string, t: number, graph: Graph, visited: string[]) {
    if (t <= 0) {
      return;
    }

    for (const [id, edge] of Object.entries(graph[node].min_edges).filter(
      ([id, edge]) => !visited.find((n) => n == id) && t - edge - 1 > 0
    )) {
      dfs(id, t - edge - 1, graph, [...visited, id]);
    }

    paths.push(visited);
  }

  dfs("AA", t, graph, []);
  return paths;
}

function path_score(path: string[], t: number, graph: Graph): number {
  const pairs = ["AA", ...path]
    .map((a, i) => [a, path[i]] as const)
    .slice(0, -1);
  let score = 0;
  for (const [a, b] of pairs) {
    t -= graph[a].min_edges[b] + 1;
    score += t * graph[b].rate;
  }
  return score;
}

function* combinations<T>(array: T[], n: number): Generator<T[]> {
  if (n === 1) {
    for (const a of array) {
      yield [a];
    }
    return;
  }

  for (let i = 0; i <= array.length - n; i++) {
    for (const c of combinations(array.slice(i + 1), n - 1)) {
      yield [array[i], ...c];
    }
  }
}

function solve1(input: string): number {
  const graph = parse(input);
  const paths = all_paths(graph, 30);
  return paths
    .map((path) => path_score(path, 30, graph))
    .reduce((max, cur) => Math.max(max, cur), 0);
}

function solve2(input: string): number {
  const graph = parse(input);
  const paths = all_paths(graph, 26);
  let best = 0;
  for (const [a, b] of combinations(paths, 2)) {
    if (a.filter((node) => new Set(b).has(node)).length == 0) {
      const score = path_score(a, 26, graph) + path_score(b, 26, graph);
      if (score > best) {
        best = score;
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

console.log(solve1(fs.readFileSync(`${input_base}.test`, "utf8")));
console.log(solve1(fs.readFileSync(`${input_base}.input`, "utf8")));

console.log(solve2(fs.readFileSync(`${input_base}.test`, "utf8")));
console.log(solve2(fs.readFileSync(`${input_base}.input`, "utf8")));
