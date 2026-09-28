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
question pool (questions 0–10). Projects must document at least three patterns.

- **CS50 GD50:** decided in September 2026 not to credit it. The course is its own: our
  own art, sounds, names, rules and exercises, with Press Start 2P (SIL OFL) as the font.

## Session Plan

Decided in September 2026. The 2026 midterm evaluation said the pace was too fast, so
every session is now a game session with **one main topic** and 2–3 supporting ones (see
the [schedule](../schedule/)). The course project is done in the students' own time: the
[project page](../project/) holds the kick-off, milestone, self-review, release and exam
guidance. The official [syllabus](../syllabus/) stays as it is. The last lesson of session
12 walks through the [course recap](../recap/).

Every session has its game in gar-games, its page and its deck.

## Session Timing

Each session is 4 blocks of 45 minutes: 180 minutes. Estimated from the decks in September
2026 (concept slide 3 min, demo 6, pair activity 10, exploring a codebase 12, a Pong or
Flappy build step 12, an exercise slide 20, Check Yourself 10, Apply 8). Rough, but the
same rules for every session.

| Session | Estimate | vs. 180 | Notes |
| --- | --- | --- | --- |
| 01 Pong | ~270 | +90 | course intro (~40) and 12 build steps (~145) |
| 02 Flappy Bird | ~255 | +75 | 14 build steps (~170) |
| 03 Snake | ~210 | +30 | 5 short tasks after the demos |
| 04 Sokoban | ~175 | −5 | 4 short tasks |
| 05 Pac-Man | ~165 | −15 | 4 short tasks |
| 06 Super Mario Bros | ~225 | +45 | 7 short tasks |
| 07 Angry Birds | ~165 | −15 | 4 short tasks |
| 08 The Legend of Zelda | ~180 | 0 | 1 short task |
| 09 Plants vs. Zombies | ~165 | −15 | 4 short tasks |
| 10 Pokemon | ~140 | −40 | already alternates (trace-it tasks) |
| 11 Geometry Wars | ~135 | −45 | 2 short tasks |
| 12 Vampire Survivors | ~170 | −10 | 4 short tasks; the course recap also takes time |

- **Pong and Flappy Bird:** students start the build steps in class and continue at home;
  few will finish in class. Nothing is marked as homework in advance. With the midterm evaluation in mind, cover the concept slides in
  class even when the building runs behind: they are what the next session builds on.
- **Rhythm:** every session alternates listening and doing. Sessions 03–09, 11 and 12
  have a short task (5–7 minutes, in pairs) after each demo, on the step just shown; the
  longest stretch of listening is about 30 minutes. The final
  exercises continue at home when a session runs long.
- **Spare time** in the later sessions goes to the exercises and to project work in class,
  which the syllabus includes, rather than to more material.
- Re-estimate after running a session: `timing.py` in the working notes did the counting.

| # | Game | Main topic | Supporting |
| --- | --- | --- | --- |
| 1 | Pong | The game loop | delta time, input, drawing, AABB, Update Method |
| 2 | Flappy Bird | Organizing a growing game | class library, game states, textures & parallax, procedural generation, Singleton, keyboard & mouse input |
| 3 | Snake | Assets as data | atlases, sprites & animation, fixed-tick movement (the timestep in practice), input as actions & buffering |
| 4 | Sokoban (new) | Command pattern (undo/redo) | levels as text files, rules separated from rendering (tested with xUnit) |
| 5 | Pac-Man (new) | State pattern | Strategy (per-ghost targeting), State vs. Strategy, targeting tests |
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
  in every session, and a design or refactoring exercise in most sessions from Sokoban on
  (the UML, analysis and refactoring competences the project sessions used to cover). No references to other
  engines: the students haven't met Unity yet.

Notes for building it:

- **Physics library:** [Box2D.NET](https://github.com/ikpil/Box2D.NET) 3.1 (C# port of Box2D
  v3.1, MIT, targets .NET 10) works with MonoGame 3.8.5 (checked with a falling box and its
  contact event). Chosen over Aether.Physics2D for v3's stable stacking, events read after
  the step, and a foreign C-style API that makes the Adapter lesson concrete. Keep the Angry
  Birds steps focused on the adapter, syncing and events, not physics tuning. Write a small
  debug renderer for it (or make it an exercise).
- **Changes to existing sessions:** all done. Command moved from Snake to Sokoban, mouse
  input into Flappy's `InputManager`, debug drawing to Mario, State to Pac-Man (reinforced
  in Mario), tweening from Pokemon to Zelda, data definitions from Pokemon to Plants vs.
  Zombies, and data-oriented design, spatial partitioning and profiling from Geometry Wars
  to Vampire Survivors.
- **GMDCore lineage** follows the session order (see Materials).
- **Exam pool:** Prototype and Adapter/Facade are sub-questions of 8 and 7 (done); question 9 is split into 9 (components &
  systems) and 10 (memory & performance), so students draw from 1–10 (done).
- **Testing thread:** unit testing is introduced from scratch in Sokoban (students meet
  testing in another course the same semester, but not concretely). After that, tests only
  appear where they show off the session's topic, never as a test project in every game:
  Pac-Man (each ghost strategy tested on its own), Pokemon (a save/load round-trip test,
  part of the unsolved save/load exercise), Geometry Wars (`GeometryWars.Tests`: fakes
  passed in through DI) and Vampire Survivors (the spatial grid checked against brute
  force). Mario, Angry Birds, Zelda and Plants vs. Zombies have none. In the project, tests
  are recommended at the self-review, not required (the syllabus doesn't mention testing).
- **Sokoban vs. Snake:** Sokoban is the textbook Command/undo game. Snake's continuous
  movement makes undo pointless (replay works instead).

## Materials

- **Slides:** edited decks live in `slides/` (version controlled), named by session number.
  A deck moves there from `in-progress/slides-ppt/` (the untouched originals, not in git)
  the first time it is edited.
- **Code:** one repository, [gar-games](https://github.com/Metamate/gar-games), with one
  folder per game, numbered by session (`01-pong`, `03-snake`, …). It replaced the separate
  `gmd2-*` repositories (started from a single commit; no imported history). Every game is
  split into step projects (`Snake0`,
  `Snake1`, …; one per exercise for Pong and Flappy, one per concept for the rest), with
  the finished game as the last step. Steps share one final `GMDCore`, and the README has
  a table of steps. The site page and the deck name the step for each topic.
- **Content pipeline:** every game uses the MonoGame 3.8.5 content builder (C# build rules in
  `Content/Builder/Builder.cs`, no `.mgcb`) and target .NET 10. `Content/Content.csproj`
  and `Content/BuildContent.targets` are identical in every game. The targets file restores
  and runs the builder, copies the output, and makes asset changes trigger a rebuild. In
  every game, all steps share one `Content/Assets` folder; a step's `Content.Load` calls
  show which assets it uses. Where an asset changes between steps, keep both versions and
  swap them in code (Pong: `sans` → `font` in `Pong3`).
- **GMDCore lineage:** GMDCore is one library that grows through the course, in session
  order: Flappy → Snake (Sokoban and Pac-Man unchanged) → Platformer (Angry Birds
  unchanged) → Zelda (Plants vs. Zombies unchanged) → Pokemon → Geometry Wars (Vampire
  Survivors unchanged). Game-specific code (the Box2D adapter, the components in Plants vs.
  Zombies) stays in the game, so later cores don't inherit it. Each game's `GMDCore` keeps
  the previous session's core and adds to it or deliberately changes it; nothing is dropped,
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
  `BuildContent.targets` identical to the course's games. Revisit when MonoGame ships its new
  Empty template (MonoGame/MonoGame.EmptyGame.CSharp).

## Slide & Code TODOs

- **06 Mario:** the `GameController` is deliberately _not_ the Command pattern; keep the
  discussion slide.
- **Keep exercises unsolved:** Pokemon save/load (exercise 4) and the Geometry Wars pooling
  measurement (exercise 5) stay out of the repos, so the finished games don't give away the
  answers. Shaders in Geometry Wars are a showcase only.
- **Tilemap:** Snake introduces a tilemap of plain tile IDs; the Platformer upgrades it to
  `Tile` values (graphic ID plus `IsSolid`) with collision helpers and a `Position`.
  Game-specific layers (the Platformer's toppers, Pokemon's tall grass) are separate
  tilemaps drawn on top.
- **Repo naming pass (later):** make the game folder and project names consistent. `06-platformer` / `Platformer0` is the only generic name (the others name the game), and some use shortened names (`Birds`, `Pvz`, `Survivors`) while others use the full name (`GeometryWars`, `Pokemon`). Renaming touches the site, the decks, the READMEs and CI.

## Where Content Goes

Each piece of content has one home; the others link to it. If a fact changes, only one
file should need editing.

| | Deck | Session page | Game README |
| --- | --- | --- | --- |
| For | The class, live, with the teacher talking | A student alone, before and after class, and for the exam | Someone with the repo open |
| Answers | What are we doing now? | Why does this work, and when would I use it? | How do I run this, and where is X? |
| Holds | The session's flow, the goal demo, diagrams, a few key excerpts, discussion questions, exercise prompts | Concepts and patterns with trade-offs, readings, exercises, Apply it, Check yourself, links to key files | The steps, what's new in GMDCore, a code map, tests and tools, content, controls, running, credits |
| Leaves out | Explanations that only work when read | Run instructions, file-by-file tours, the step list | Explaining patterns or design reasoning |

- The step list lives in the README; a session page names the steps each section is about.
- A session page shows short snippets that illustrate a concept; a README points to files
  and says what they hold.
- Decks and session pages cover the **same essentials in a different form**: every essential
  appears in both, no paragraph does. In class, a concept is problem first (show it break,
  ask how to fix it, then name the pattern), then one headline sentence, a visual (diagram,
  code, labelled screenshot) and a question. The site has the full explanation.
- A dense bullet slide is a sign its text belongs on the site, or in the speaker notes as
  talking points. Exercise slides give a one-line goal; the instructions are on the site.
- Decks end with a few of the site's "Check yourself" questions, asked live.
- All twelve decks follow this since September 2026. Every slide has speaker notes written for
  presenting: what to say, what to ask (with the expected answer), and how to run each demo;
  the Check yourself slides carry the site's answers.

## General Notes

- Use consistent, simple UML diagrams (Mermaid is supported on the site).
- The graphics are redone in one simple classic style (our own art, generated sounds,
  Press Start 2P). The games can still become less 1:1 compared to CS50.
- End each game session with "what moved into GMDCore this week, and why?"

## Topic Backlog

Topics not assigned to a session. Prefer _naming_ patterns that already exist in the course
code over adding new sessions.

| Topic | Possible home |
| --- | --- |
| [Dirty Flag](https://gameprogrammingpatterns.com/dirty-flag.html) | Screen scale / camera matrix recalculation |
| Abstract Factory vs. Factory Method | Geometry Wars `EntityFactory` |
| [Subclass Sandbox](https://gameprogrammingpatterns.com/subclass-sandbox.html) | Zelda/Mario entity base classes |
| Decorator | Mario powerups |
| Event bus / message bus | Zelda, alongside Event Queue |
| MVVM / MVP | Pokemon UI (currently only mentioned) |
| SOLID principles | Weave into sessions rather than a standalone lecture |
| Proxy, Iterator, Builder | Probably out of scope |
| Game math (sin/cos, atan2, lerp, radians, normalization) | Short primer in Pong/Flappy |
| [Refactoring](https://refactoring.guru) | 04 Sokoban, then an exercise in every session |
| Pathfinding (A\*), steering behaviours | Zelda or Geometry Wars (seek & flee is in the GW code) |
| ECS in practice (e.g. MonoGame.Extended) | Geometry Wars, briefly |

## Ideas for Games

- **Space Invaders / Asteroids:** object pool, spatial partitioning, Prototype (splitting
  asteroids)
- **Tetris:** pure grid logic
- **Tower defence / turn-based strategy:** mouse input, Type Object, pathfinding
- Minecraft, Terraria, Stardew Valley: probably too big, but good for inspiration
