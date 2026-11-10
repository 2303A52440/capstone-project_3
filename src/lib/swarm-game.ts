// Pure game rules for "Swarm Dispatch": robots move one cell per tick at the same time.
export type Cell = [number, number];
export interface RobotDef {
  start: Cell;
  dock: Cell;
}
export interface Level {
  id: number;
  name: string;
  brief: string;
  map: string[]; // '#' = shelf, '.' = floor
  robots: RobotDef[];
}

export const LEVELS: Level[] = [
  {
    id: 1,
    name: "First Delivery",
    brief: "One robot, one dock. Draw a route around the shelves.",
    map: ["....#...", ".##.#...", ".##.....", "....##.."],
    robots: [{ start: [0, 0], dock: [7, 3] }],
  },
  {
    id: 2,
    name: "Crossroads",
    brief: "Two robots reach the middle at the same moment. Make one of them wait.",
    map: ["###.###", "###.###", ".......", "###.###", "###.###"],
    robots: [
      { start: [1, 2], dock: [6, 2] },
      { start: [3, 0], dock: [3, 4] },
    ],
  },
  {
    id: 3,
    name: "Narrow Aisle",
    brief: "Robots can't pass through each other. Use the side bay to let one go by.",
    map: ["#####.###", "........."],
    robots: [
      { start: [0, 1], dock: [8, 1] },
      { start: [8, 1], dock: [0, 1] },
    ],
  },
  {
    id: 4,
    name: "Rush Hour",
    brief: "Three robots, crossing traffic. Plan who goes first.",
    map: [".........", ".##.#.##.", ".........", ".##.#.##.", "........."],
    robots: [
      { start: [0, 0], dock: [8, 4] },
      { start: [8, 0], dock: [0, 4] },
      { start: [4, 0], dock: [4, 4] },
    ],
  },
  {
    id: 5,
    name: "Full Swarm",
    brief: "Four robots, every route crosses. The whole warehouse is counting on you.",
    map: ["..........", ".##.##.##.", "..........", ".##.##.##.", "..........", ".##.##.##.", ".........."],
    robots: [
      { start: [0, 0], dock: [9, 6] },
      { start: [9, 0], dock: [0, 6] },
      { start: [0, 6], dock: [9, 0] },
      { start: [9, 6], dock: [0, 0] },
    ],
  },
];

export const key = (c: Cell) => `${c[0]},${c[1]}`;
export const same = (a: Cell, b: Cell) => a[0] === b[0] && a[1] === b[1];

export function isFloor(level: Level, c: Cell) {
  const row = level.map[c[1]];
  return !!row && c[0] >= 0 && c[0] < row.length && row[c[0]] === ".";
}

/** A legal next cell: same cell (wait) or one orthogonal step onto floor. */
export function canStep(level: Level, from: Cell, to: Cell) {
  const d = Math.abs(from[0] - to[0]) + Math.abs(from[1] - to[1]);
  return d <= 1 && isFloor(level, to);
}

export const posAt = (path: Cell[], t: number): Cell => path[Math.min(t, path.length - 1)]!;

export type Crash =
  | { kind: "same-cell"; t: number; a: number; b: number; cell: Cell }
  | { kind: "swap"; t: number; a: number; b: number; cell: Cell };

/** Steps the robots need: the time after which every robot stays parked forever. */
export function makespan(paths: Cell[][]) {
  return Math.max(0, ...paths.map((p) => p.length - 1));
}

/** First collision, if any. Robots that finished their route stay where they stopped. */
export function findCrash(paths: Cell[][]): Crash | null {
  const T = makespan(paths);
  for (let t = 0; t <= T; t++) {
    for (let a = 0; a < paths.length; a++) {
      for (let b = a + 1; b < paths.length; b++) {
        const pa = posAt(paths[a]!, t);
        const pb = posAt(paths[b]!, t);
        if (same(pa, pb)) return { kind: "same-cell", t, a, b, cell: pa };
        if (t > 0 && same(pa, posAt(paths[b]!, t - 1)) && same(pb, posAt(paths[a]!, t - 1)) && !same(pa, pb))
          return { kind: "swap", t, a, b, cell: pa };
      }
    }
  }
  return null;
}

/** Total moves: for each robot, the step at which it last arrives at its final cell. */
export function sumOfCosts(paths: Cell[][]) {
  return paths.reduce((s, p) => {
    let n = p.length - 1;
    while (n > 0 && same(p[n - 1]!, p[p.length - 1]!)) n--;
    return s + n;
  }, 0);
}

export function allDocked(level: Level, paths: Cell[][]) {
  return level.robots.every((r, i) => same(posAt(paths[i]!, 1e9), r.dock));
}

export type Result =
  | { ok: true; cost: number; stars: number }
  | { ok: false; reason: "crash"; crash: Crash }
  | { ok: false; reason: "undocked"; robots: number[] };

export function evaluate(level: Level, paths: Cell[][], par: number, usedHint: boolean): Result {
  const crash = findCrash(paths);
  if (crash) return { ok: false, reason: "crash", crash };
  const missing = level.robots.map((r, i) => (same(posAt(paths[i]!, 1e9), r.dock) ? -1 : i)).filter((i) => i >= 0);
  if (missing.length) return { ok: false, reason: "undocked", robots: missing };
  const cost = sumOfCosts(paths);
  let stars = cost <= par ? 3 : cost <= par + 3 ? 2 : 1;
  if (usedHint) stars = Math.min(stars, 2);
  return { ok: true, cost, stars };
}

// ---------- Shared search helpers ----------
const DIRS: Cell[] = [[0, 0], [1, 0], [-1, 0], [0, 1], [0, -1]];

function planOne(level: Level, r: RobotDef, others: Cell[][], maxT = 60): Cell[] | null {
  const occupied = (c: Cell, t: number) => others.some((p) => same(posAt(p, t), c));
  const swapped = (from: Cell, to: Cell, t: number) =>
    others.some((p) => same(posAt(p, t), from) && same(posAt(p, t - 1), to));
  const othersEnd = makespan(others);
  const h = (c: Cell) => Math.abs(c[0] - r.dock[0]) + Math.abs(c[1] - r.dock[1]);
  type N = { c: Cell; t: number; g: number; f: number; prev: N | null };
  const open: N[] = [{ c: r.start, t: 0, g: 0, f: h(r.start), prev: null }];
  const seen = new Set<string>();
  while (open.length) {
    open.sort((x, y) => x.f - y.f || y.t - x.t);
    const n = open.shift()!;
    const sk = `${key(n.c)}@${n.t}`;
    if (seen.has(sk)) continue;
    seen.add(sk);
    if (same(n.c, r.dock)) {
      let safe = true;
      for (let t = n.t + 1; t <= othersEnd + 1; t++) if (occupied(n.c, t)) safe = false;
      if (safe) {
        const out: Cell[] = [];
        for (let m: N | null = n; m; m = m.prev) out.unshift(m.c);
        return out;
      }
    }
    if (n.t >= maxT) continue;
    for (const d of DIRS) {
      const c: Cell = [n.c[0] + d[0], n.c[1] + d[1]];
      const t = n.t + 1;
      if (!isFloor(level, c) || occupied(c, t) || swapped(n.c, c, t)) continue;
      const g = same(c, r.dock) && same(n.c, r.dock) ? n.g : n.g + 1;
      open.push({ c, t, g, f: t + h(c), prev: n });
    }
  }
  return null;
}

function permutations(n: number): number[][] {
  if (n === 1) return [[0]];
  return permutations(n - 1).flatMap((p) => Array.from({ length: n }, (_, i) => [...p.slice(0, i), n - 1, ...p.slice(i)]));
}

/** Prioritized planning — fallback only, if CBS exceeds its node budget. */
export function solvePrioritized(level: Level): Cell[][] | null {
  let best: Cell[][] | null = null;
  for (const order of permutations(level.robots.length)) {
    const planned: Cell[][] = [];
    const result: Cell[][] = new Array(level.robots.length);
    let ok = true;
    for (const i of order) {
      const p = planOne(level, level.robots[i]!, planned);
      if (!p) { ok = false; break; }
      planned.push(p);
      result[i] = p;
    }
    if (ok && !findCrash(result) && (!best || sumOfCosts(result) < sumOfCosts(best))) best = result;
  }
  return best;
}

// ---------- MAPF: Conflict-Based Search (CBS) ----------
export type Constraint =
  | { robot: number; kind: "vertex"; cell: Cell; t: number }
  | { robot: number; kind: "edge"; from: Cell; to: Cell; t: number };

/** Low level: space-time A* for one robot that respects CBS constraints. */
export function lowLevel(level: Level, ri: number, cons: Constraint[], maxT = 60): Cell[] | null {
  const r = level.robots[ri]!;
  const mine = cons.filter((c) => c.robot === ri);
  const vBlocked = (c: Cell, t: number) => mine.some((k) => k.kind === "vertex" && k.t === t && same(k.cell, c));
  const eBlocked = (a: Cell, b: Cell, t: number) =>
    mine.some((k) => k.kind === "edge" && k.t === t && same(k.from, a) && same(k.to, b));
  const lastDockBan = Math.max(0, ...mine.filter((k) => k.kind === "vertex" && same(k.cell, r.dock)).map((k) => k.t));
  const h = (c: Cell) => Math.abs(c[0] - r.dock[0]) + Math.abs(c[1] - r.dock[1]);
  type N = { c: Cell; t: number; f: number; prev: N | null };
  const open: N[] = [{ c: r.start, t: 0, f: h(r.start), prev: null }];
  const seen = new Set<string>();
  while (open.length) {
    open.sort((x, y) => x.f - y.f || y.t - x.t);
    const n = open.shift()!;
    const sk = `${key(n.c)}@${n.t}`;
    if (seen.has(sk)) continue;
    seen.add(sk);
    if (same(n.c, r.dock) && n.t >= lastDockBan) {
      const out: Cell[] = [];
      for (let m: N | null = n; m; m = m.prev) out.unshift(m.c);
      return out;
    }
    if (n.t >= maxT) continue;
    for (const d of DIRS) {
      const c: Cell = [n.c[0] + d[0], n.c[1] + d[1]];
      const t = n.t + 1;
      if (!isFloor(level, c) || vBlocked(c, t) || eBlocked(n.c, c, t)) continue;
      open.push({ c, t, f: t + h(c), prev: n });
    }
  }
  return null;
}

/** High level: CBS over the constraint tree, ordered by sum of costs. Optimal for sum-of-costs. */
export function solveCBS(level: Level, maxNodes = 4000): { paths: Cell[][]; expanded: number } | null {
  const n = level.robots.length;
  type CT = { cons: Constraint[]; paths: Cell[][]; cost: number };
  const root: Cell[][] = [];
  for (let i = 0; i < n; i++) {
    const p = lowLevel(level, i, []);
    if (!p) return null;
    root.push(p);
  }
  const open: CT[] = [{ cons: [], paths: root, cost: sumOfCosts(root) }];
  let expanded = 0;
  while (open.length && expanded < maxNodes) {
    open.sort((a, b) => a.cost - b.cost);
    const node = open.shift()!;
    expanded++;
    const crash = findCrash(node.paths);
    if (!crash) return { paths: node.paths, expanded };
    for (const robot of [crash.a, crash.b]) {
      let c: Constraint;
      if (crash.kind === "same-cell") c = { robot, kind: "vertex", cell: crash.cell, t: crash.t };
      else {
        const p = node.paths[robot]!;
        c = { robot, kind: "edge", from: posAt(p, crash.t - 1), to: posAt(p, crash.t), t: crash.t };
      }
      const cons = [...node.cons, c];
      const np = lowLevel(level, robot, cons);
      if (!np) continue;
      const paths = node.paths.slice();
      paths[robot] = np;
      open.push({ cons, paths, cost: sumOfCosts(paths) });
    }
  }
  return null;
}

/** Solver used for par scores and hints: CBS, with prioritized planning as a safety net. */
export function solve(level: Level): Cell[][] | null {
  return solveCBS(level)?.paths ?? solvePrioritized(level);
}
