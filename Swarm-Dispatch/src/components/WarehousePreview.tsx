import { Bot } from "lucide-react";
import { type Level, same } from "@/lib/swarm-game";

export function WarehousePreview({ level }: { level: Level }) {
  return (
    <div className="warehouse-preview" style={{ gridTemplateColumns: `repeat(${level.map[0]?.length ?? 1}, 1fr)` }} aria-hidden="true">
      {level.map.flatMap((row, y) => row.split("").map((cell, x) => {
        const robot = level.robots.findIndex((r) => same(r.start, [x, y]));
        const dock = level.robots.findIndex((r) => same(r.dock, [x, y]));
        return <span key={`${x}-${y}`} className={`warehouse-mini-cell ${cell === "#" ? "bg-shelf" : "bg-floor"}`}>
          {dock >= 0 && <span className={`warehouse-mini-dock robot-tone-${dock + 1}`} />}
          {robot >= 0 && <Bot className={`warehouse-mini-robot robot-tone-${robot + 1}`} />}
        </span>;
      }))}
    </div>
  );
}