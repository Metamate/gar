---
title: Course Development Notes
description: Instructor-only notes, TODOs and ideas. Not published.
draft: true
---

:::caution
This page is a **draft**: it is visible when running `astro dev`, but excluded from the
production build. Keep instructor notes here, not on the public pages.
:::

## Open Decisions

Decided: the course is English only, and the [Exam](../exam/) page is the authoritative
question pool (question 9 added for session 09). Projects must document at least three
patterns.

- **Pacing:** the 2026 midterm evaluation said the pace was too fast, with a lot of content
  per session, and the level was split 50/50 between too high and about right. The slide
  numbering (01 Pong, 03 Flappy, 05 Snake) suggests Pong and Flappy each needed two
  sessions. The schedule has one session each; if they need two again, merge 10 Release
  and 11 Architecture Review.
- **Snake vs. Sokoban:** Sokoban is the textbook Command/undo game. Snake's continuous
  movement makes undo pointless (replay works instead).
- **CS50 GD50:** the game line-up follows CS50's Introduction to Game Development closely.
  Check its license and credit it where assets or structure are derived from it.

## Materials

- **Slides:** edited decks live in `slides/` (version controlled), named by session number.
  A deck moves there from `in-progress/slides-ppt/` (the untouched originals, not in git)
  the first time it is edited.
- **Code:** the `gmd2-*` repos. Every game should follow the Pong/Flappy layout: one project
  per step (`Snake0`, `Snake1`, …), each with its own `Content`, all sharing one final
  `GMDCore`, and a README table of steps. The site page and the deck name the step for
  each topic.
- **Still single-project:** Geometry Wars. (Snake, Platformer, Zelda and Pokemon are split into steps.)
- **Content pipeline:** all repos use the MonoGame 3.8.5 content builder (C# build rules in
  `Content/Builder/Builder.cs`, no `.mgcb`) and target .NET 10. `Content/BuildContent.targets`
  is identical in every repo; Pong and Flappy steps set `ContentAssets` to their own `Assets`
  folder, the other repos share `Content/Assets`.
- **Starting a new project:** MonoGame's `dotnet new` templates (3.8.5.1) still create MGCB
  projects, so students start from a copy of `Pong0` plus the `Content` folder (Pong page,
  Flappy exercise 2, project kick-off). Revisit when MonoGame ships its new Empty template
  (MonoGame/MonoGame.EmptyGame.CSharp), or consider a small starter repo of our own.

## Slide & Code TODOs

- **01 Pong:** update the slides to cover the Update Method pattern properly (Encapsulation
  exercise), plus fixed vs. variable timestep and double buffering (now on the site).
- **02 Flappy:** update the implementation to contain a Singleton example, and use it to
  contrast static classes vs. Singleton (`Art`, `Core.Input`).
- **03 Snake:** done. Split into `Snake0`–`Snake8` (`steps` branch in `gmd2-snake`, not yet
  pushed); site page and `slides/03 Snake.pptx` updated to match.
- **05 Mario:** the `GameController` is deliberately _not_ the Command pattern; keep the
  discussion slide.
- **07 Project Work slides:** drop the value vs. reference types slides (assumed prior knowledge).
- **08 Pokemon:** add a save/load exercise to the repo (party + position to JSON).
- **09 Geometry Wars:** add a spatial grid broad phase (or leave as exercise), and an
  allocation/GC counter overlay for the profiling exercise. Shaders are now a showcase only.
- Make "Tilemap" more generic early on. In the platformer and Zelda it contains a lot of
  game-specific decisions.

## General Notes

- Use consistent, simple UML diagrams (Mermaid is supported on the site).
- Redo graphics and make the games less 1:1 compared to CS50.
- End each game session with "what moved into GMDCore this week, and why?"

## Topic Backlog

Topics not assigned to a session. Prefer _naming_ patterns that already exist in the course
code over adding new sessions.

| Topic | Possible home |
| --- | --- |
| [Dirty Flag](https://gameprogrammingpatterns.com/dirty-flag.html) | Screen scale / camera matrix recalculation |
| [Prototype](https://gameprogrammingpatterns.com/prototype.html), Abstract Factory vs. Factory Method | Geometry Wars `EntityFactory` |
| [Subclass Sandbox](https://gameprogrammingpatterns.com/subclass-sandbox.html) | Zelda/Mario entity base classes |
| Decorator | Mario powerups |
| Event bus / message bus | Zelda, alongside Event Queue |
| MVVM / MVP | Pokemon UI (currently only mentioned) |
| SOLID principles | Weave into sessions rather than a standalone lecture |
| Adapter, Proxy, Facade, Iterator, Builder | Probably out of scope |
| Game math (sin/cos, atan2, lerp, radians, normalization) | Short primer in Pong/Flappy |
| Debugging (debug overlay, hitbox drawing) | GMDCore, early |
| [Refactoring](https://refactoring.guru) | 11 Architecture Review |
| Pathfinding (A\*), steering behaviours | Zelda or Geometry Wars (seek & flee is in the GW code) |
| ECS in practice (e.g. MonoGame.Extended) | Geometry Wars, briefly |

## Ideas for Games

- **Space Invaders / Asteroids:** object pool, spatial partitioning, Prototype (splitting
  asteroids)
- **Pac-Man:** per-ghost AI as State/Strategy, pathfinding
- **Tetris:** pure grid logic
- **Sokoban:** Command pattern with undo
- **Vampire Survivors-like:** alternative to Geometry Wars (components, pooling, spatial
  hash, Type Object enemies, Decorator upgrades)
- **Tower defence / turn-based strategy:** mouse input, Type Object, pathfinding
- Minecraft, Terraria, Stardew Valley: probably too big, but good for inspiration
