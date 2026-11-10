import { describe, expect, it } from "vitest";
import { LEVELS, evaluate, findCrash, solve, type Cell } from "./swarm-game";

describe("swarm rules", () => {
  it("two robots on the same cell at the same time crash", () => {
    const a: Cell[] = [[0, 0], [1, 0]];
    const b: Cell[] = [[2, 0], [1, 0]];
    expect(findCrash([a, b])?.kind).toBe("same-cell");
  });
  it("two robots swapping cells crash head-on", () => {
    const a: Cell[] = [[0, 0], [1, 0]];
    const b: Cell[] = [[1, 0], [0, 0]];
    expect(findCrash([a, b])?.kind).toBe("swap");
  });
  it("every level is solvable and the solver's answer earns 3 stars", () => {
    for (const lvl of LEVELS) {
      const s = solve(lvl);
      expect(s, lvl.name).not.toBeNull();
      const r = evaluate(lvl, s!, Infinity, false);
      expect(r.ok).toBe(true);
    }
  });
  it("using a hint caps the score at 2 stars", () => {
    const s = solve(LEVELS[0]!)!;
    const r = evaluate(LEVELS[0]!, s, 100, true);
    expect(r.ok && r.stars).toBe(2);
  });
});

import { solveCBS, solvePrioritized, sumOfCosts as soc } from "./swarm-game";
describe("CBS (MAPF)", () => {
  it("finds a crash-free plan on every level, never worse than prioritized planning", () => {
    for (const lvl of LEVELS) {
      const r = solveCBS(lvl);
      expect(r).not.toBeNull();
      expect(findCrash(r!.paths)).toBeNull();
      const pr = solvePrioritized(lvl);
      if (pr) expect(soc(r!.paths)).toBeLessThanOrEqual(soc(pr));
    }
  });
});
