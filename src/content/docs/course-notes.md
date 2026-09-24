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
question pool (question 9 added for Geometry Wars). Projects must document at least three
patterns.

- **CS50 GD50:** the game line-up follows CS50's Introduction to Game Development closely.
  Check its license and credit it where assets or structure are derived from it.

## Session Plan

Decided in September 2026. The 2026 midterm evaluation said the pace was too fast, so
every session is now a game session with **one main topic** and 2–3 supporting ones (see
the [schedule](../schedule/)). The course project is done in the students' own time: the
[project page](../project/) holds the kick-off, milestone, self-review, release and exam
guidance. The official [syllabus](../syllabus/) stays as it is. The last lesson of session
12 walks through the [course recap](../recap/).

Session pages for the new games (Sokoban, Pac-Man, Angry Birds, Plants vs. Zombies,
Vampire Survivors) are placeholders marked "In development" until their games exist.

| # | Game | Main topic | Supporting |
| --- | --- | --- | --- |
| 1 | Pong | The game loop | delta time, input, drawing, AABB, Update Method |
| 2 | Flappy Bird | Organizing a growing game | class library, game states, textures & parallax, procedural generation, Singleton, keyboard & mouse input |
| 3 | Snake | Assets as data | atlases, sprites & animation, fixed-tick movement (the timestep in practice), input as actions & buffering |
| 4 | Sokoban (new) | Command pattern (undo/redo) | levels as data (tilemaps), rules separated from rendering (testable) |
| 5 | Pac-Man (new) | State pattern | Strategy (per-ghost targeting), State vs. Strategy |
| 6 | Super Mario Bros | Physics & tile collision | camera, debug drawing, level makers (Strategy again) |
| 7 | Angry Birds (new) | Integrating a third-party library (Adapter/Facade) | physics world vs. game world, contact events & safe destruction, Prototype (prefabs) |
| 8 | The Legend of Zelda | Composition vs. inheritance | Observer & events, hitboxes, tweening |
| 9 | Plants vs. Zombies (new) | Component pattern | Type Object, game types as data, picking (screen → grid) |
| 10 | Pokemon | Scenes & UI | state stack, separating UI from game data, Service Locator, save/load |
| 11 | Geometry Wars | Components vs. systems | dependency injection vs. Service Locator, Object Pool, Flyweight |
| 12 | Vampire Survivors (new) | Performance: the same genre built data-first | data-oriented design, spatial partitioning, profiling, course recap |

Threads that run through the plan (the recap page lists them for students):

- **Game families:** free movement (1–2), grids (3–5), tile worlds and physics (6–10),
  free movement at scale (11–12). Each game reuses most of the previous one's code.
- **Build vs. buy:** hand-written platformer physics (6), then a physics library (7).
- **Data:** assets as data (3) → levels as data (4) → game types as data (9) → save/load (10).
- **Entities:** composition vs. inheritance (8) → components (9) → components vs. systems
  (11) → data-oriented design (12, same genre as 11 built a second way).
- **Dependencies:** Singleton (2) → Service Locator (10) → dependency injection (11).
- **Coordinate spaces:** virtual resolution (2) → camera (6) → physics units (7) → picking (9).
- **Pattern pairs:** State vs. Strategy (5), Prototype (7) vs. Type Object (9), Object Pool
  vs. Flyweight (11).
- **Recurring:** a Mermaid class diagram on every session page, "Apply It to Your Project"
  in every session, and a refactoring exercise from Sokoban onwards (the UML, analysis and
  refactoring competences the project sessions used to cover). No references to other
  engines: the students haven't met Unity yet.

Notes for building it:

- **Physics library:** [Box2D.NET](https://github.com/ikpil/Box2D.NET) 3.1 (C# port of Box2D
  v3.1, MIT, targets .NET 10) works with MonoGame 3.8.5 (checked with a falling box and its
  contact event). Chosen over Aether.Physics2D for v3's stable stacking, events read after
  the step, and a foreign C-style API that makes the Adapter lesson concrete. Keep the Angry
  Birds steps focused on the adapter, syncing and events, not physics tuning. Write a small
  debug renderer for it (or make it an exercise).
- **Changes to existing sessions:** Command moves from Snake to Sokoban (done: Snake is now
  `Snake0`–`Snake9`, a real Snake with fixed-tick movement, input as actions and buffering;
  its room is still drawn from a tilemap, as asset data, while Sokoban uses the grid as game
  state); mouse input moves into Flappy's
  `InputManager` (done); debug drawing moves to Mario (done: `DebugDraw` in GMDCore, `F1`
  from `Platformer2`); State is introduced in Pac-Man and reinforced in Mario (page done); tweening moves from Pokemon to Zelda (done: `Zelda5`'s room shift
  uses `TweenManager`, which now enters GMDCore with Zelda); data definitions move from
  Pokemon to Plants vs. Zombies (Pokemon page and deck done); data-oriented design, spatial partitioning and profiling
  move from Geometry Wars to Vampire Survivors (done: Geometry Wars now teaches components
  vs. systems and dependency injection; the removed DOD, spatial partitioning and profiling
  text and slides are in git history, and the Component pattern intro slides too, for the
  new decks). All existing sessions are now reshaped.
- **GMDCore lineage** follows the new order; new games join it in session order.
- **Exam pool:** add Prototype and Adapter; split question 9 between Geometry Wars
  (components vs. systems) and Vampire Survivors (performance). The "Covered in" lines
  already point at the new sessions.
- **Sokoban vs. Snake:** Sokoban is the textbook Command/undo game. Snake's continuous
  movement makes undo pointless (replay works instead).

## Materials

- **Slides:** edited decks live in `slides/` (version controlled), named by session number.
  A deck moves there from `in-progress/slides-ppt/` (the untouched originals, not in git)
  the first time it is edited.
- **Code:** one repository, [gar-games](https://github.com/Metamate/gar-games), with one
  folder per game, numbered by session (`01-pong`, `03-snake`, …). It replaced the separate
  `gmd2-*` repositories (started from a single commit; no imported history). Every game is
  split into step
  projects (`Snake0`,
  `Snake1`, …; one per exercise for Pong and Flappy, one per concept for the rest), with
  the finished game as the last step. Steps share one final `GMDCore`, and the README has
  a table of steps. The site page and the deck name the step for each topic.
- **Content pipeline:** all repos use the MonoGame 3.8.5 content builder (C# build rules in
  `Content/Builder/Builder.cs`, no `.mgcb`) and target .NET 10. `Content/Content.csproj`
  and `Content/BuildContent.targets` are identical in every repo. The targets file restores
  and runs the builder, copies the output, and makes asset changes trigger a rebuild. In
  every repo, all steps share one `Content/Assets` folder; a step's `Content.Load` calls
  show which assets it uses. Where an asset changes between steps, keep both versions and
  swap them in code (Pong: `arial` → `font` in `Pong3`).
- **GMDCore lineage:** GMDCore is one library that grows through the course: Flappy →
  Snake → Platformer → Zelda → Pokemon → Geometry Wars. Each repo's `GMDCore` keeps the
  previous session's core and adds to it or deliberately changes it; nothing is dropped,
  even if the game doesn't use it. Each README has a "New in GMDCore" section, and
  `python tools/check.py` in gar-games lists the differences between games (and fails if a
  file was removed, or if the build files differ between games). The GitHub build runs it.
  Each game folder stays self-contained, like a single-game repo and like gar-starter, so
  the two build files are duplicated on purpose; the check keeps them identical.
- **Project files:** keep every `.csproj` to the essentials (output type, framework,
  `MonoGamePlatform`, package/project references, the content import). No icons, app
  manifests or publish settings; publish options go on the `dotnet publish` command line.
- **Starting a new project:** MonoGame's `dotnet new` templates (3.8.5.1) still create MGCB
  projects, so students start from our own template repo,
  [gar-starter](https://github.com/Metamate/gar-starter) (Flappy exercise 2, the
  project page): one empty `MyGame` project plus the `Content` builder, with general rules for
  images, fonts, sounds, music and JSON/XML. Keep its `Content.csproj` and
  `BuildContent.targets` identical to the course repos. Revisit when MonoGame ships its new
  Empty template (MonoGame/MonoGame.EmptyGame.CSharp).

## Slide & Code TODOs

- **05 Mario:** the `GameController` is deliberately _not_ the Command pattern; keep the
  discussion slide.
- **Keep exercises unsolved:** Pokemon save/load (exercise 4), the Geometry Wars
  allocation counter (exercise 2) and spatial grid (exercise 3) stay out of the repos, so the
  finished games don't give away the answers. Shaders in Geometry Wars are a showcase only.
- **Tilemap:** Snake introduces a tilemap of plain tile IDs; the Platformer upgrades it to
  `Tile` values (graphic ID plus `IsSolid`) with collision helpers and a `Position`.
  Game-specific layers (the Platformer's toppers, Pokemon's tall grass) are separate
  tilemaps drawn on top.

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
| [Refactoring](https://refactoring.guru) | 04 Sokoban, then an exercise in every session |
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
