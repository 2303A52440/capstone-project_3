import { createFileRoute } from "@tanstack/react-router";
import { SwarmGame } from "@/components/SwarmGame";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Swarm Dispatch — Warehouse Robot Puzzle" },
      { name: "description", content: "Plan routes for a swarm of warehouse robots and dispatch them without a single crash." },
      { property: "og:title", content: "Swarm Dispatch — Warehouse Robot Puzzle" },
      { property: "og:description", content: "Plan robot routes, add waits, dodge head-on collisions and earn 3 stars." },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: SwarmGame,
});
