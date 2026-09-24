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

- **CS50 GD50:** the game line-up follows CS50's Introduction to Game Development closely.
  Check its license and credit it where assets or structure are derived from it.

## Planned Session Plan

Decided (September 2026), not yet on the public pages. The 2026 midterm evaluation said
the pace was too fast, so every session becomes a game session with **one main topic**
and 2–3 supporting ones. The course project is done in the students' own time: the
[project page](../project/) takes over the kick-off, milestone, release and review
guidance. The official [syllabus](../syllabus/) stays as it is.

| # | Game | Main topic | Supporting |
| --- | --- | --- | --- |
| 1 | Pong | The game loop | delta time, input, drawing, AABB, Update Method |
| 2 | Flappy Bird | Organizing a growing game (reusable core, game states) | textures & parallax, procedural generation, Singleton |
| 3 | Snake | Assets as data (atlases & animations in XML) | sprites & animation, grid movement on a fixed tick |
| 4 | Sokoban (new) | Command pattern (with undo/redo) | levels as data (tilemaps), rules separated from rendering |
| 5 | Pac-Man (new) | State pattern | Strategy (per-ghost targeting), State vs. Strategy |
| 6 | Super Mario Bros | Physics & tile collision | camera, debug drawing, level makers (Strategy again) |
| 7 | The Legend of Zelda | Composition vs. inheritance | Observer & events, hitboxes, tweening |
| 8 | Plants vs. Zombies (new) | Component pattern | Type Object, game types as data, mouse input |
| 9 | Pokemon | Scenes & UI (state stack, GUI) | separating UI from game data, Service Locator, save/load |
| 10 | Angry Birds (new) | Integrating a third-party library (Adapter/Facade) | physics world vs. game world, collision callbacks as events, Prototype |
| 11 | Geometry Wars | Components vs. systems | dependency injection vs. Service Locator, Object Pool, Flyweight, particles as a system |
| 12 | Vampire Survivors (new) | Performance (data-oriented design) | spatial partitioning, profiling |

Threads that run through the plan:

- **Game families:** free movement (1–2), grids (3–5), tile worlds (6–9), physics and free
  movement at scale (10–12). Each game reuses most of the previous one's code.
- **Data:** assets as data (3) → levels as data (4) → game types as data (8) → save/load (9).
- **Entities:** inheritance strains (7) → components (8) → components vs. systems (11) →
  data-oriented design (12).
- **Dependencies:** Singleton (2) → Service Locator (9) → dependency injection (11).
- **Pattern pairs:** State vs. Strategy (5), Type Object (8) vs. Prototype (10), Object Pool
  vs. Flyweight (11).
- **Recurring:** a Mermaid class diagram on every session page, "Apply It to Your Project"
  in every session, and a refactoring exercise from Sokoban onwards (UML, analysis and
  refactoring competences, previously covered by the project sessions).

Notes for building it:

- **Physics library:** `Aether.Physics2D.MG` 2.2.0 (C# port of Box2D, namespace
  `nkast.Aether.Physics2D`) works with MonoGame 3.8.5 on .NET 10 (checked with a falling
  box and a collision callback). Keep the Angry Birds steps focused on the adapter, syncing
  and events, not physics tuning.
- **Changes to existing sessions:** Command moves from Snake to Sokoban (tilemaps too);
  Observer stays in Zelda; debug drawing moves to Mario; State is introduced in Pac-Man
  and reinforced in Mario; tweening moves from Pokemon to Zelda; data definitions move
  from Pokemon to Plants vs. Zombies; data-oriented design, spatial partitioning and
  profiling move from Geometry Wars to Vampire Survivors.
- **GMDCore lineage** follows the new order; new games join it in session order.
- **Exam pool:** add Prototype and Adapter; split question 9 between Geometry Wars
  (components vs. systems) and Vampire Survivors (performance).
- **Sokoban vs. Snake:** Sokoban is the textbook Command/undo game. Snake's continuous
  movement makes undo pointless (replay works instead).

## Materials

- **Slides:** edited decks live in `slides/` (version controlled), named by session number.
  A deck moves there from `in-progress/slides-ppt/` (the untouched originals, not in git)
  the first time it is edited.
- **No deck for 07:** the old Project Work session only exists as a PDF
  (`in-progress/slides/07 Project Work.pdf`). The site's Project Checkpoint page replaces
  it; its value vs. reference types slides are dropped (assumed prior knowledge).
- **Code:** the `gmd2-*` repos. Every repo is split into step projects (`Snake0`,
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
  `python tools/core-lineage.py` lists the differences between sessions (and fails if a
  file was removed). Run it after changing any `GMDCore`.
- **Project files:** keep every `.csproj` to the essentials (output type, framework,
  `MonoGamePlatform`, package/project references, the content import). No icons, app
  manifests or publish settings; publish options go on the `dotnet publish` command line.
- **Starting a new project:** MonoGame's `dotnet new` templates (3.8.5.1) still create MGCB
  projects, so students start from our own template repo,
  [gar-starter](https://github.com/Metamate/gar-starter) (Flappy exercise 2, project
  kick-off): one empty `MyGame` project plus the `Content` builder, with general rules for
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
