# Swarm Dispatch

A robot-routing puzzle game. You are the dispatcher for a warehouse fleet: draw a
route for each robot so every one of them reaches its charging bay without two
robots ever crashing into each other.

Built from an Autonomous Collaborative Robot Swarm project (Conflict-Based
Search) and refactored into a playable, rules-first puzzle game.

## Play

```sh
npm i
npm run dev
```

Open the printed local address. A How-to-play dialog opens the first time you
visit, and every level shows a tip.

## Rules

- The grid is a warehouse: `#` is a shelf (impassable), `.` is floor.
- Each robot has a start cell and a charging bay. Draw a route by clicking or
  dragging over floor cells, or with the arrow keys.
- One route step moves a robot one cell. Every robot moves at the same time,
  one step per tick. A robot that is done waits in its bay.
- Two robots on the same cell at the same time crash. So do two robots that
  swap cells head-on in one tick.
- Every robot must end in its own bay.
- Score: 3 stars if your total steps beat the level's target, 2 stars if you are
  within 3 extra steps, 1 star otherwise. Using a hint caps you at 2 stars.
- The target is the true minimum, computed by the solver, so 3 stars means you
  matched the best possible plan.

## Levels

1. First Delivery — one robot, learn the controls
2. Crossroads — two robots meet head-on
3. Narrow Aisle — one-way passage, timing matters
4. Rush Hour — three robots, real coordination
5. Full Swarm — four robots, the whole floor

Stars and unlocked levels are stored in your browser's localStorage under
`swarm-dispatch-stars`.

## In-game tools

- **Check** validates your routes without dispatching.
- **Conflict · tick N** warns you before you dispatch, and says which tick crashes.
- **Hint** reveals a solver-made route for the selected robot.
- **Pause / Step / Speed** (0.5×, 1×, 2×) while the fleet runs.

## Solver: MAPF with Conflict-Based Search

Multi-Agent Path Finding (MAPF) is the problem: find crash-free routes for all
robots at once. The game solves it with Conflict-Based Search (CBS).

- **Low level** — space-time A* plans one robot's route while obeying the
  constraints CBS has given it.
- **High level** — CBS picks the first conflict (two robots on one cell, or a
  head-on swap), splits into two children, and adds a constraint keeping one
  robot out of that cell at that time. It expands the cheapest node first, so
  the plan it returns is optimal for sum-of-costs.
- **Fallback** — prioritized planning (robots one at a time) runs only if CBS
  exceeds its node budget.

CBS supplies both the 3-star targets and the hints.

## Layout

- `src/lib/swarm-game.ts` — game rules and solver as pure functions: levels,
  movement and crash checks, scoring, and the CBS/MAPF solver.
- `src/lib/swarm-game.test.ts` — rules and solver tests.
- `src/components/SwarmGame.tsx` — the game UI; it only renders and calls the
  rules module.
- `src/components/WarehousePreview.tsx` — mini warehouse thumbnails on the
  level cards.
- `src/styles.css` — the dark warehouse theme and design tokens.

## Tests

```sh
npm test
```

Covers same-cell crashes, head-on swap crashes, every level being solvable, the
solver's plan earning 3 stars, hints capping the score, and CBS never doing
worse than the fallback planner.

## Built with

TanStack Start, TypeScript, React, Tailwind CSS v4, shadcn/ui, Vitest.
