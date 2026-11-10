import { useCallback, useEffect, useMemo, useState } from "react";
import { Bot, BookOpen, Lightbulb, Play, RotateCcw, Undo2, Pause, Star, ChevronLeft, Trophy, Lock, CheckCircle2, ShieldCheck, SkipForward, Flag } from "lucide-react";
import { Button } from "@/components/ui/button";
import { WarehousePreview } from "@/components/WarehousePreview";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import {
  LEVELS, canStep, evaluate, findCrash, makespan, posAt, same, solve, sumOfCosts,
  type Cell, type Level, type Result,
} from "@/lib/swarm-game";

const ROBOT_COLORS = ["var(--robot-1)", "var(--robot-2)", "var(--robot-3)", "var(--robot-4)"];
const ROBOT_NAMES = ["Zip", "Bolt", "Sparky", "Rosie"];
const last = (p: Cell[]) => posAt(p, 1e9);
const STORAGE = "swarm-dispatch-stars";

function StarRow({ n, size = 20 }: { n: number; size?: number }) {
  return (
    <div className="flex gap-1">
      {[1, 2, 3].map((i) => (
        <Star key={i} size={size} className={i <= n ? "fill-primary text-primary" : "text-muted-foreground/40"} />
      ))}
    </div>
  );
}

function RulesDialog({ open, onOpenChange }: { open: boolean; onOpenChange: (o: boolean) => void }) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-lg">
        <DialogHeader>
          <DialogTitle className="text-2xl">How to play</DialogTitle>
          <DialogDescription>Get every robot to its matching dock without a single crash.</DialogDescription>
        </DialogHeader>
        <ol className="space-y-3 text-sm">
          {[
            ["Pick a robot", "Click a robot (or press 1–4). Its dock is the dashed ring in the same color."],
            ["Draw its route", "Click the squares next to the end of its route, or use the arrow keys. Shelves block the way."],
            ["Wait when needed", "Click the route's last square again (or press Space) to make the robot pause for one tick."],
            ["Press Dispatch", "All robots move at the same time, one square per tick."],
          ].map(([t, d], i) => (
            <li key={t} className="flex gap-3">
              <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-primary font-mono text-sm font-bold text-primary-foreground">{i + 1}</span>
              <span><strong className="text-foreground">{t}.</strong> <span className="text-muted-foreground">{d}</span></span>
            </li>
          ))}
        </ol>
        <div className="rounded-lg border border-destructive/40 bg-destructive/10 p-3 text-sm">
          <p className="font-semibold text-destructive">Crashes end the run:</p>
          <ul className="mt-1 list-disc pl-5 text-muted-foreground">
            <li>Two robots on the same square at the same tick.</li>
            <li>Two robots swapping squares head-on.</li>
          </ul>
        </div>
        <div className="rounded-lg border border-primary/40 bg-primary/10 p-3 text-sm text-muted-foreground">
          <p className="font-semibold text-primary">Stars</p>
          Fewer total moves = more stars. Match the expert score for ⭐⭐⭐. Using a hint caps you at ⭐⭐.
          Backspace undoes a step, Enter dispatches.
        </div>
        <DialogFooter>
          <Button onClick={() => onOpenChange(false)}>Got it!</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

function Board({
  level, paths, selected, t, running, crash, onCell, onSelect,
}: {
  level: Level; paths: Cell[][]; selected: number; t: number | null; running: boolean;
  crash: { cell: Cell } | null; onCell: (c: Cell) => void; onSelect: (i: number) => void;
}) {
  const cols = level.map[0]?.length ?? 1;
  const rows = level.map.length;
  const size = `min(64px, calc((100vw - 3rem) / ${cols}))`;
  const pathIndex = useMemo(() => {
    const m = new Map<string, number>();
    paths[selected]?.forEach((c, i) => m.set(`${c[0]},${c[1]}`, i));
    return m;
  }, [paths, selected]);

  return (
    <div
      className="relative mx-auto rounded-xl border-2 border-border bg-card p-1 shadow-2xl"
      style={{ width: `calc(${size} * ${cols} + 0.5rem + 4px)` }}
    >
      <div className="grid" style={{ gridTemplateColumns: `repeat(${cols}, ${size})`, gridTemplateRows: `repeat(${rows}, ${size})` }}>
        {level.map.flatMap((row, y) =>
          row.split("").map((ch, x) => {
            const idx = pathIndex.get(`${x},${y}`);
            const sel = paths[selected];
            const end = !!sel && same(last(sel), [x, y]);
            const reachable = !running && !!sel && canStep(level, last(sel), [x, y]);
            return (
               <Button variant="ghost"
                key={`${x}-${y}`}
                type="button"
                aria-label={ch === "#" ? `shelf ${x},${y}` : `cell ${x},${y}`}
                disabled={ch === "#" || running}
                onClick={() => onCell([x, y])}
                 className={`relative m-px h-auto rounded-md p-0 transition-colors ${
                  ch === "#"
                    ? "bg-shelf shadow-inner"
                    : `bg-floor ${reachable ? "hover:bg-secondary ring-1 ring-inset ring-primary/30" : ""}`
                }`}
              >
                {ch === "#" && <span className="absolute inset-1 rounded-sm border-y-2 border-background/30" />}
                {idx !== undefined && idx > 0 && !running && (
                  <span
                    className="absolute inset-0 m-auto flex h-1/2 w-1/2 items-center justify-center rounded-full font-mono text-[10px] font-bold text-background"
                    style={{ background: ROBOT_COLORS[selected], opacity: end ? 1 : 0.55 }}
                  >
                     {idx}{sel && idx > 0 && same(sel[idx] ?? [x, y], sel[idx - 1] ?? [x, y]) ? "Ⅱ" : ""}
                  </span>
                )}
               </Button>
            );
          }),
        )}
      </div>
      {/* other robots' routes */}
      <svg className="pointer-events-none absolute inset-1" style={{ width: `calc(${size} * ${cols})`, height: `calc(${size} * ${rows})` }} viewBox={`0 0 ${cols} ${rows}`}>
        {paths.map((p, i) =>
          p.length > 1 ? (
            <polyline key={i} points={p.map((c) => `${c[0] + 0.5},${c[1] + 0.5}`).join(" ")} fill="none"
              stroke={ROBOT_COLORS[i]} strokeWidth={i === selected ? 0.08 : 0.05} strokeDasharray={i === selected ? "0" : "0.15 0.1"}
              opacity={running ? 0.25 : i === selected ? 0.9 : 0.45} strokeLinecap="round" strokeLinejoin="round" />
          ) : null,
        )}
        {level.robots.map((r, i) => (
          <circle key={i} cx={r.dock[0] + 0.5} cy={r.dock[1] + 0.5} r={0.36} fill="none" stroke={ROBOT_COLORS[i]} strokeWidth={0.06} strokeDasharray="0.12 0.08" />
        ))}
      </svg>
      {/* robots */}
      {level.robots.map((r, i) => {
        const at = t === null ? r.start : posAt(paths[i] ?? [r.start], t);
        const docked = t !== null && same(at, r.dock);
        return (
          <Button variant="ghost"
            key={i}
            type="button"
            aria-label={`robot ${ROBOT_NAMES[i]}`}
            disabled={running}
            onClick={() => onSelect(i)}
            className="absolute left-1 top-1 flex items-center justify-center p-0 transition-transform duration-300 ease-in-out"
            style={{ width: size, height: size, transform: `translate(calc(${size} * ${at[0]}), calc(${size} * ${at[1]}))` }}
          >
            <span
              className={`flex h-[72%] w-[72%] items-center justify-center rounded-xl border-2 shadow-lg ${i === selected && !running ? "border-foreground scale-110" : "border-background/60"} ${docked ? "animate-bounce" : ""}`}
              style={{ background: ROBOT_COLORS[i] }}
            >
              <Bot className="!h-3/5 !w-3/5 text-background" />
            </span>
          </Button>
        );
      })}
      {crash && (
        <div className="pointer-events-none absolute left-1 top-1 flex items-center justify-center"
          style={{ width: size, height: size, transform: `translate(calc(${size} * ${crash.cell[0]}), calc(${size} * ${crash.cell[1]}))` }}>
          <span className="crash-pop absolute h-full w-full rounded-full bg-destructive/60" />
          <span className="relative text-2xl">💥</span>
        </div>
      )}
    </div>
  );
}

function PlayScreen({ level, onExit, onWin, onNext, hasNext }: {
  level: Level; onExit: () => void; onWin: (stars: number) => void; onNext: () => void; hasNext: boolean;
}) {
  const solution = useMemo(() => solve(level), [level]);
  const par = solution ? sumOfCosts(solution) : Infinity;
  const fresh = useCallback(() => level.robots.map((r) => [r.start] as Cell[]), [level]);
  const [paths, setPaths] = useState<Cell[][]>(fresh);
  const [selected, setSelected] = useState(0);
  const [t, setT] = useState<number | null>(null);
  const [result, setResult] = useState<Result | null>(null);
  const [hintUsed, setHintUsed] = useState(false);
  const [message, setMessage] = useState<string>(level.brief);
  const [paused, setPaused] = useState(false);
  const [speed, setSpeed] = useState(1);
  const running = t !== null && result === null;
  const plannedCrash = useMemo(() => findCrash(paths), [paths]);
  const readyCount = level.robots.filter((r, i) => same(last(paths[i] ?? [r.start]), r.dock)).length;
  const stopAt = plannedCrash ? plannedCrash.t : makespan(paths);

  const reset = () => {
    setPaths(fresh()); setT(null); setResult(null); setSelected(0); setHintUsed(false); setPaused(false); setMessage(level.brief);
  };
  useEffect(reset, [level]); // eslint-disable-line react-hooks/exhaustive-deps

  const editing = () => { if (t !== null) { setT(null); setResult(null); } };

  const extend = (to: Cell) => {
    editing();
    setPaths((ps) => ps.map((p, i) => {
      if (i !== selected) return p;
      const end = last(p);
      if (!canStep(level, end, to) || p.length > 40) return p;
      return [...p, to];
    }));
  };
  const undo = () => { editing(); setPaths((ps) => ps.map((p, i) => (i === selected && p.length > 1 ? p.slice(0, -1) : p))); };

  const onCell = (c: Cell) => {
    if (running) return;
    const robot = level.robots.findIndex((r) => same(r.start, c));
    const p = paths[selected];
    if (!p) return;
    const end = last(p);
    if (robot >= 0 && robot !== selected && !(canStep(level, end, c) && !same(end, c))) {
      setSelected(robot); setMessage(`${ROBOT_NAMES[robot]} selected. Draw a route to its dashed dock.`); return;
    }
    if (canStep(level, end, c)) return extend(c);
    // Clicking an earlier square on the route trims back to it.
    const idx = p.findIndex((q) => same(q, c));
    if (idx >= 0) { editing(); setPaths((ps) => ps.map((q, i) => (i === selected ? q.slice(0, idx + 1) : q))); }
  };

  const dispatch = () => {
    if (running) return;
    setResult(null); setPaused(false); setT(0); setMessage("Robots on the move…");
  };

  const finish = () => {
    const final = evaluate(level, paths, par, hintUsed);
    setResult(final); setPaused(false);
    if (final.ok) { onWin(final.stars); setMessage("All docked!"); }
    else if (final.reason === "crash") {
      const c = final.crash;
      setMessage(`💥 ${ROBOT_NAMES[c.a]} and ${ROBOT_NAMES[c.b]} ${c.kind === "swap" ? "tried to swap places head-on" : "hit the same square"} at tick ${c.t}. Add a wait or reroute.`);
    } else setMessage(`${final.robots.map((i) => ROBOT_NAMES[i]).join(", ")} didn't reach the dock. Extend the route.`);
  };

  useEffect(() => {
    if (!running || paused || t === null) return;
    const timer = setTimeout(() => {
      if (t >= stopAt) finish();
      else setT(t + 1);
    }, 600 / speed);
    return () => clearTimeout(timer);
  }, [running, paused, t, stopAt, speed, paths, hintUsed, par]); // eslint-disable-line react-hooks/exhaustive-deps

  const selectRobot = (i: number) => {
    if (running) return;
    setSelected(i); setMessage(`${ROBOT_NAMES[i]} selected. Draw a route to its dashed dock.`);
  };

  const checkRoutes = () => {
    const check = evaluate(level, paths, par, hintUsed);
    if (check.ok) setMessage(`Clear to dispatch! All ${readyCount} routes are safe. ${check.stars} stars within reach.`);
    else if (check.reason === "crash") setMessage(`Conflict at tick ${check.crash.t}: ${ROBOT_NAMES[check.crash.a]} and ${ROBOT_NAMES[check.crash.b]}. Add a wait before the crossing or change a route.`);
    else setMessage(`Still to route: ${check.robots.map((i) => ROBOT_NAMES[i]).join(", ")}.`);
  };

  const hint = () => {
    if (!solution) return;
    editing();
    setHintUsed(true);
    setPaths((ps) => ps.map((p, i) => (i === selected ? solution[i] ?? p : p)));
    setMessage(`Hint: here is an expert route for ${ROBOT_NAMES[selected]}. (Max ⭐⭐ this round.)`);
  };

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (running || (e.target as HTMLElement)?.closest("[role=dialog]")) return;
      const path = paths[selected];
      if (!path) return;
      const end = last(path);
      const map: Partial<Record<string, Cell>> = { ArrowUp: [0, -1], ArrowDown: [0, 1], ArrowLeft: [-1, 0], ArrowRight: [1, 0], " ": [0, 0] };
      const d = map[e.key];
      if (d) { e.preventDefault(); extend([end[0] + d[0], end[1] + d[1]]); }
      else if (e.key === "Backspace") { e.preventDefault(); undo(); }
      else if (e.key === "Enter") { e.preventDefault(); dispatch(); }
      else if (/^[1-4]$/.test(e.key) && +e.key <= level.robots.length) selectRobot(+e.key - 1);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  });

  const crashInfo = result && !result.ok && result.reason === "crash" ? result.crash : null;
  const visibleCrash = crashInfo ?? (!running && t === null ? plannedCrash : null);

  return (
    <div className="mx-auto flex max-w-5xl flex-col gap-5 px-4 py-6">
      <div className="flex items-center justify-between gap-3">
        <Button variant="ghost" onClick={onExit}><ChevronLeft /> Levels</Button>
        <div className="text-center">
          <p className="font-mono text-xs uppercase tracking-widest text-muted-foreground">Level {level.id}</p>
          <h2 className="text-2xl font-bold">{level.name}</h2>
        </div>
        <div className="text-right font-mono text-xs text-muted-foreground">
          <div>Moves <span className="text-lg font-bold text-foreground">{sumOfCosts(paths)}</span></div>
          <div>Expert {par}</div>
        </div>
      </div>

      <div className={`border-l-4 px-4 py-3 text-sm ${crashInfo ? "border-destructive bg-destructive/10" : "border-primary bg-primary/5"}`} aria-live="polite">
        {message}
      </div>

      <div className="flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-sm">
        <span className={readyCount === level.robots.length ? "text-success" : "text-muted-foreground"}><Flag className="mr-1 inline h-4 w-4" />{readyCount}/{level.robots.length} routes docked</span>
        <span className={plannedCrash ? "text-destructive" : "text-success"}>{plannedCrash ? `Conflict · tick ${plannedCrash.t}` : "No route conflicts"}</span>
        <span className="font-mono text-muted-foreground">{running ? `Tick ${t}/${stopAt}` : `${makespan(paths)} ticks`}</span>
      </div>

      <div className="flex flex-wrap justify-center gap-2">
        {level.robots.map((r, i) => {
          const path = paths[i] ?? [r.start];
          const docked = same(last(path), r.dock);
          return (
            <Button variant="outline" key={i} type="button" onClick={() => selectRobot(i)} disabled={running} aria-pressed={i === selected}
              className={`h-10 gap-2 border-2 px-3 text-sm font-semibold transition ${i === selected ? "border-foreground bg-secondary" : "border-border"}`}>
              <span className="h-3 w-3 rounded-full" style={{ background: ROBOT_COLORS[i] }} />
              {i + 1}. {ROBOT_NAMES[i]}
              <span className="font-mono text-xs text-muted-foreground">{docked ? <CheckCircle2 className="text-success" /> : `${path.length - 1} steps`}</span>
            </Button>
          );
        })}
      </div>

      <Board level={level} paths={paths} selected={selected} t={t} running={running} crash={visibleCrash} onCell={onCell} onSelect={selectRobot} />

      <div className="flex flex-wrap justify-center gap-2">
        <Button size="lg" onClick={running ? () => setPaused((p) => !p) : dispatch} className="font-bold">
          {running && !paused ? <Pause /> : <Play />} {running ? paused ? "Resume" : "Pause" : "Dispatch"}
        </Button>
        {running && <Button variant="secondary" onClick={() => { setPaused(true); if (t !== null && t >= stopAt) finish(); else setT((tick) => (tick ?? 0) + 1); }}><SkipForward /> Step</Button>}
        <Button variant="secondary" onClick={undo} disabled={running}><Undo2 /> Undo</Button>
        <Button variant="secondary" onClick={() => { const path = paths[selected]; if (path) extend(last(path)); }} disabled={running}><Pause /> Wait</Button>
        <Button variant="secondary" onClick={checkRoutes} disabled={running}><ShieldCheck /> Check</Button>
        <Button variant="secondary" onClick={hint} disabled={running || !solution}><Lightbulb /> Hint</Button>
        <Button variant="ghost" onClick={reset}><RotateCcw /> Restart</Button>
      </div>

      <div className="flex items-center justify-center gap-1" aria-label="Playback speed">
        <span className="mr-2 text-xs text-muted-foreground">Speed</span>
        {[0.5, 1, 2].map((n) => <Button key={n} size="sm" variant={speed === n ? "secondary" : "ghost"} aria-pressed={speed === n} onClick={() => setSpeed(n)}>{n}×</Button>)}
      </div>

      <Dialog open={!!result?.ok} onOpenChange={(o) => !o && setResult(null)}>
        <DialogContent className="text-center sm:max-w-sm">
          <DialogHeader className="items-center">
            <Trophy className="h-12 w-12 text-primary" />
            <DialogTitle className="text-2xl">Delivery complete!</DialogTitle>
            <DialogDescription>
              {result?.ok && `${result.cost} moves · expert ${par}`}
            </DialogDescription>
          </DialogHeader>
          <div className="flex justify-center">{result?.ok && <StarRow n={result.stars} size={36} />}</div>
          {result?.ok && result.stars < 3 && (
            <p className="text-sm text-muted-foreground">{hintUsed ? "Try it without a hint for 3 stars." : "Fewer waits and shorter routes earn more stars."}</p>
          )}
          <DialogFooter className="sm:justify-center">
            <Button variant="secondary" onClick={reset}>Replay</Button>
            {hasNext ? <Button onClick={onNext}>Next level</Button> : <Button onClick={onExit}>All levels</Button>}
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}

export function SwarmGame() {
  const [stars, setStars] = useState<Record<number, number>>({});
  const [levelIdx, setLevelIdx] = useState<number | null>(null);
  const [rules, setRules] = useState(false);

  useEffect(() => {
    try {
      setStars(JSON.parse(localStorage.getItem(STORAGE) || "{}"));
      if (!localStorage.getItem(STORAGE)) setRules(true);
    } catch { /* ignore */ }
  }, []);
  const saveStars = (id: number, n: number) => {
    setStars((s) => {
      const next = { ...s, [id]: Math.max(s[id] || 0, n) };
      localStorage.setItem(STORAGE, JSON.stringify(next));
      return next;
    });
  };
  const total = Object.values(stars).reduce((a, b) => a + b, 0);
  const activeLevel = levelIdx === null ? undefined : LEVELS[levelIdx];
  const nextUnfinished = LEVELS.findIndex((l) => !stars[l.id]);

  return (
    <div className="min-h-screen">
      <header className="flex items-center justify-between border-b border-border px-5 py-3">
        <Button variant="ghost" type="button" onClick={() => setLevelIdx(null)} className="h-auto gap-2 px-0 hover:bg-transparent">
          <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary"><Bot className="h-5 w-5 text-primary-foreground" /></span>
          <span className="text-lg font-extrabold tracking-tight">Swarm Dispatch</span>
        </Button>
        <div className="flex items-center gap-3">
          <span className="flex items-center gap-1 font-mono text-sm"><Star size={16} className="fill-primary text-primary" /> {total}/{LEVELS.length * 3}</span>
          <Button variant="outline" size="sm" onClick={() => setRules(true)}><BookOpen /> Rules</Button>
        </div>
      </header>

      {levelIdx === null ? (
        <main className="mx-auto max-w-5xl px-5 py-8">
          <section className="flex flex-wrap items-end justify-between gap-5 border-b border-border pb-7">
            <div>
              <p className="font-mono text-xs uppercase tracking-widest text-accent">Dispatch control</p>
              <h1 className="mt-2 text-4xl font-black sm:text-5xl">Swarm Dispatch</h1>
              <p className="mt-3 text-muted-foreground">{Object.keys(stars).length}/{LEVELS.length} deliveries complete · {total} stars earned</p>
            </div>
            <div className="flex flex-wrap gap-3">
              <Button size="lg" className="font-bold" onClick={() => setLevelIdx(nextUnfinished >= 0 ? nextUnfinished : 0)}>
                <Play /> {total ? "Continue shift" : "Start shift"}
              </Button>
              <Button size="lg" variant="secondary" onClick={() => setRules(true)}><BookOpen /> How to play</Button>
            </div>
          </section>

          <section className="mt-7 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {LEVELS.map((l, i) => {
              const previous = LEVELS[i - 1];
              const locked = !!previous && !stars[previous.id];
              return (
                <Button variant="outline" key={l.id} type="button" disabled={locked} onClick={() => setLevelIdx(i)}
                  className="group block h-auto whitespace-normal rounded-lg border border-border bg-card p-5 text-left transition hover:-translate-y-1 hover:border-primary hover:bg-card hover:text-foreground disabled:opacity-50 disabled:hover:translate-y-0 disabled:hover:border-border">
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-xs text-muted-foreground">LEVEL {l.id}</span>
                    {locked ? <Lock size={16} className="text-muted-foreground" /> : <StarRow n={stars[l.id] || 0} size={16} />}
                  </div>
                  <div className="mt-4 flex h-44 items-center justify-center"><div className="w-full"><WarehousePreview level={l} /></div></div>
                  <h3 className="mt-2 text-xl font-bold group-hover:text-primary">{l.name}</h3>
                  <p className="mt-1 text-sm text-muted-foreground">{l.brief}</p>
                  <div className="mt-3 flex gap-1">
                    {l.robots.map((_, r) => <span key={r} className="h-2.5 w-2.5 rounded-full" style={{ background: ROBOT_COLORS[r] }} />)}
                  </div>
                </Button>
              );
            })}
          </section>
        </main>
      ) : activeLevel ? (
        <PlayScreen
          key={levelIdx}
          level={activeLevel}
          onExit={() => setLevelIdx(null)}
          onWin={(n) => saveStars(activeLevel.id, n)}
          hasNext={levelIdx < LEVELS.length - 1}
          onNext={() => setLevelIdx(levelIdx + 1)}
        />
      ) : null}
      <RulesDialog open={rules} onOpenChange={setRules} />
    </div>
  );
}
