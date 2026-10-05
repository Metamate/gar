---
title: Course Development Notes
description: Instructor-only notes, conventions and ideas. Not published.
draft: true
---

:::caution
This page is a **draft**: it is visible when running `astro dev`, but excluded from the
production build. Keep instructor notes here, not on the public pages.
:::

## Open Decisions

The course is English only, and the [Exam](../exam/) page is the authoritative question
pool (questions 0–10). Projects must document at least three patterns.

- **No CS50 GD50 credit:** the course is its own: our own names, rules, exercises and
  sounds, with Press Start 2P (SIL OFL) as the font. The art is our own or Kenney's (CC0);
  see Art below.

## Session Plan

Every session is a game session with **one main topic** and 2–3 supporting ones (see the
[overview](../overview/)); the 2026 midterm evaluation said the pace was too fast. The course project is done in the students' own time: the
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
| 00 Course Intro + 01 Pong | ~40 + ~200 | +60 | the intro deck first, then 7 build steps; virtual resolution and steps 8–11 are demos |
| 02 Flappy Bird | ~200 | +20 | 6 build steps; four stretches are demos with a try-it |
| 03 Snake | ~205 | +25 | 5 short tasks after the demos |
| 04 Sokoban | ~185 | +5 | 5 short tasks; Command for undo and for input |
| 05 Pac-Man | ~185 | +5 | 5 short tasks; routing is Strategy a second time |
| 06 Super Mario Bros | ~205 | +25 | 6 short tasks; physics first; player states only say what's new after Pac-Man |
| 07 The Legend of Zelda | ~195 | +15 | 3 short tasks; events are the main topic, composition closes the session |
| 08 Angry Birds | ~175 | −5 | 5 short tasks, and the physics samples |
| 09 Plants vs. Zombies | ~175 | −5 | 5 short tasks, one a test with `Pvz.Tests` |
| 10 Pokemon | ~165 | −15 | trace-it tasks, and 4 short tasks (samples, stack, tweens, locator) |
| 11 Geometry Wars | ~150 | −30 | 4 short tasks; the spare time goes to the project |
| 12 Vampire Survivors | ~170 | −10 | 4 short tasks; the course recap also takes time |

- **Pong and Flappy Bird:** students build the core steps in class and continue at home;
  the steps that are plumbing or repeat an idea (Pong's screen scaling, modes and sound, Flappy's images, gravity and input, spawning and
  extra states) are shown as demos with a try-it, and the next build exercise starts from
  the step the demo ended on. Nothing is marked as homework in advance. With the midterm
  evaluation in mind, cover the concept slides in class even when the building runs
  behind: they are what the next session builds on.
- **Rhythm:** every session alternates listening and doing. Every session from Pong on has
  a short task (5–7 minutes, in pairs) after its demos, on the step just shown; the
  longest stretch of listening is about 30 minutes. The final exercises continue at home
  when a session runs long.
- **Exercise answers:** what a good answer to each exercise contains is kept outside the
  public repositories (`projects/gar-private/exercise-answers.md` on the teacher's machine),
  so the exercises stay unsolved for students.
- **Spare time** in the later sessions goes to the exercises and to project work in class,
  which the syllabus includes. No material is added to fill it.
- **Slides keep to the topic:** no milestones, due dates, "last week" or other course
  admin. The project page, the overview and the teacher carry those. "Apply It to Your
  Project" stays: it applies the day's topic, not the project's schedule.
- **Course intro:** `00 Course Intro` opens the first session, before Pong: the teacher,
  the course, the games, how a session runs, the project and the exam in brief, and where
  things are. Only what holds all year; it ends with a live tour of the site.

| # | Game | Main topic | Patterns | Supporting |
| --- | --- | --- | --- | --- |
| 1 | Pong | The game loop | Game Loop, Update Method | delta time, input, drawing, AABB collision |
| 2 | Flappy Bird | Structuring the code | State (game states), Singleton | a core library (GARCore), textures & parallax, procedural generation, keyboard & mouse input |
| 3 | Snake | Assets as data | — | texture atlases, sprites & animation, fixed-tick movement, input as actions & buffering |
| 4 | Sokoban | Undo and replay | Command | levels as text files, rules apart from drawing, unit tests |
| 5 | Pac-Man | Changing behaviour | State, Strategy | State vs. Strategy, a second strategy for routes, testing each ghost |
| 6 | Super Mario Bros | The game world | Strategy (level makers), State (the player) | platformer physics & tile collision, debug drawing |
| 7 | The Legend of Zelda | Events | Observer | C# events and lambdas, an event queue, hitboxes, tweening, composition vs. inheritance |
| 8 | Angry Birds | Using a physics library | Adapter, Facade, Prototype | physics world vs. game world, contact events, destroying safely |
| 9 | Plants vs. Zombies | Components | Component, Type Object | game types as data, picking, testing a component |
| 10 | Pokemon | Scenes and UI | State (a stack), Service Locator | UI widgets, separating UI from game data, save/load |
| 11 | Geometry Wars | Components and systems | Object Pool, Flyweight | components vs. systems, dependency injection & testing with fakes |
| 12 | Vampire Survivors | Performance | Spatial Partition, Data Locality | profiling, data-oriented design, course recap |

Threads that run through the plan (the recap page lists them for students):

- **Game families:** free movement (1–2), grids (3–5), tile worlds and physics (6–10),
  free movement at scale (11–12). Each game reuses most of the previous one's code.
- **Build vs. buy:** hand-written platformer physics (6), then a physics library (8).
- **Data:** assets as data (3) → levels as data (4) → enemies as data (7) → prefabs (8) →
  game types as data (9) → save/load (10).
- **Entities:** composition vs. inheritance (7) → components (9) → components vs. systems
  (11) → data-oriented design (12, same genre as 11 built a second way).
- **Dependencies:** Singleton (2) → Service Locator (10) → dependency injection (11).
- **Coordinate spaces:** virtual resolution (1) → window to game coordinates (2) → camera (6) → physics units (8) → picking (9).
- **Pattern pairs:** State vs. Strategy (5), Prototype (8) vs. Type Object (9), Object Pool
  vs. Flyweight (11).
- **Order of 07 and 08:** Zelda comes before Angry Birds. Zelda teaches events, and Angry Birds' contact events use them; Mario's
  core leads straight into Zelda's; and Angry Birds' Prototype sits next to Plants vs.
  Zombies' Type Object.
- **Recurring:** a Mermaid class diagram on every session page, "Apply It to Your Project"
  in every session, and a design or refactoring exercise in most sessions from Sokoban on
  (they carry the syllabus's UML, analysis and refactoring competences). No references to other
  engines: the students haven't met Unity yet.

Notes for building it:

- **Physics library:** [Box2D.NET](https://github.com/ikpil/Box2D.NET) 3.1 (C# port of Box2D
  v3.1, MIT, targets .NET 10) works with MonoGame 3.8.5 (checked with a falling box and its
  contact event). Chosen over Aether.Physics2D for v3's stable stacking, events read after
  the step, and a foreign C-style API that makes the Adapter lesson concrete. Keep the Angry
  Birds steps focused on the adapter, syncing and events, not physics tuning.
- **GARCore lineage** follows the session order (see Materials).
- **Exam pool:** Strategy is a sub-question of 2, Adapter/Facade of 7, Type Object and
  Prototype of 8. Components & systems are question 9 and memory & performance question 10,
  so students draw from 1–10.
- **Testing thread:** unit testing is introduced from scratch in Sokoban (students meet
  testing in another course the same semester, but not concretely). After that, tests only
  appear where they show off the session's topic, never as a test project in every game:
  Pac-Man (each ghost strategy tested on its own), Plants vs. Zombies (`Pvz.Tests`:
  components tested on their own, just before the self-review), Pokemon (a save/load round-trip test,
  part of the unsolved save/load exercise), Geometry Wars (`GeometryWars.Tests`: fakes
  passed in through DI) and Vampire Survivors (the spatial grid checked against brute
  force). Mario, Zelda and Angry Birds have none. In the project, tests
  are recommended at the self-review, not required (the syllabus doesn't mention testing).
- **Sokoban vs. Snake:** Sokoban is the textbook Command/undo game. Snake's continuous
  movement makes undo pointless (replay works instead).

## Materials

- **Slides:** the decks live in `slides/` (version controlled), named by session number.
- **Figures:** the concept drawings on the pages and the decks are our own, drawn by `tools/figures`: one Python
  function per figure, in `sessionNN.py`. `python tools/figures/build.py` writes each as an SVG in
  `src/assets/sessionNN/` for the site and as a PNG in `tools/figures/out/` for the decks. One dark panel,
  the site's orange for what the figure is about, teal for what it is compared with. A figure goes on a
  slide at nearly full width, so its text stays readable when projected. Figures that show a game's art
  read it from gar-games, cloned next to this repository.
- **Code:** one repository, [gar-games](https://github.com/Metamate/gar-games), with one
  folder per game, numbered by session (`01-pong`, `03-snake`, …). Every game is
  split into step projects (`Snake0`,
  `Snake1`, …; one per exercise for Pong and Flappy, one per concept for the rest), with
  the finished game as the last step. Steps share one final `GARCore`, and the README has
  a table of steps. The site page and the deck name the step for each topic.
- **Content pipeline:** every game uses the MonoGame 3.8.5 content builder (C# build rules in
  `Content/Builder/Builder.cs`, no `.mgcb`) and target .NET 10. `Content/Content.csproj`
  and `Content/BuildContent.targets` are identical in every game. The targets file restores
  and runs the builder, copies the output, and makes asset changes trigger a rebuild. In
  every game, all steps share one `Content/Assets` folder; a step's `Content.Load` calls
  show which assets it uses. Where an asset changes between steps, keep both versions and
  swap them in code (Pong: `sans` → `font` in `Pong3`).
- **GARCore lineage:** GARCore is one library that grows through the course, in session
  order: Flappy Bird → Snake (Sokoban and Pac-Man unchanged) → Mario → Zelda (Angry Birds
  and Plants vs. Zombies unchanged) → Pokemon → Geometry Wars (Vampire
  Survivors unchanged). Game-specific code (the Box2D adapter, the components in Plants vs.
  Zombies) stays in the game, so later cores don't inherit it. Each game's `GARCore` keeps
  the previous session's core and adds to it or deliberately changes it; nothing is dropped,
  even if the game doesn't use it. Each README has a "New in GARCore" section, and
  `python tools/check.py` in gar-games lists the differences between games (and fails if a
  file was removed, or if the build files differ between games). The GitHub build runs it.
  Each game folder stays self-contained, like a single-game repo and like gar-starter, so
  the two build files are duplicated on purpose; the check keeps them identical.
- **Project files:** keep every `.csproj` to the essentials (output type, framework,
  `MonoGamePlatform`, package/project references, the content import). No icons, app
  manifests or publish settings; publish options go on the `dotnet publish` command line.
- **Starting a new project:** MonoGame's `dotnet new` templates (3.8.5.1) still create MGCB
  projects, so students start from our own template repo,
  [gar-starter](https://github.com/Metamate/gar-starter) (Flappy exercise 1, the
  project page): one empty `MyGame` project plus the `Content` builder, with general rules for
  images, fonts, sounds, music and JSON/XML. Keep its `Content.csproj` and
  `BuildContent.targets` identical to the course's games. Revisit when MonoGame ships its new
  Empty template (MonoGame/MonoGame.EmptyGame.CSharp).

## Slide & Code Conventions

- **06 Mario:** the `GameController` is deliberately _not_ the Command pattern; keep the
  discussion slide.
- **Keep exercises unsolved:** Pokemon save/load (exercise 3) and the Geometry Wars pooling
  measurement (exercise 5) stay out of the repos, so the finished games don't give away the
  answers. Shaders in Geometry Wars are a showcase only.
- **Tilemap:** Snake introduces a tilemap of plain tile IDs; Mario upgrades it to
  `Tile` values (graphic ID plus `IsSolid`) with collision helpers and a `Position`.
  Game-specific layers (Mario's toppers, Pokemon's tall grass) are separate
  tilemaps drawn on top.
- **Art:** each game has a look of its own that fits the original, with no shared style
  between games. Seven use asset packs by Kenney (CC0), credited in the game's README:
  Sokoban (Sokoban Pack), Super Mario Bros (Pixel Platformer), The Legend of Zelda (Tiny
  Dungeon), Angry Birds (Physics Assets), Plants vs. Zombies (Tiny Town and Tiny Dungeon, as a castle
  defended against goblins), Pokemon (Monochrome RPG) and Vampire Survivors
  (1-Bit Pack). The other five have our own art: Pong, Flappy Bird, Snake (lit dots on a
  dark screen, as on the phones it became famous on), Pac-Man (a beetle chased by four one-eyed wisps, in
  the original ghosts' colours, which the lesson names them by) and
  Geometry Wars. Where a pack lacks something a game needs (a ducking frame, a sword
  swing, a slingshot, hearts, a floor switch, a goblin), it is made from the pack's own pieces and colours. Pokemon's
  monsters are our designs, in the pack's four shades, and its trainer's side and back views
  are made from the pack's front-facing one. Zelda's hero gets his side and back views the
  same way.
- **Pixel art:** inside a game, every sprite, tile and background uses the same art-pixel
  size and the same style; between games both may differ. Pixel art is drawn with
  `SamplerState.PointClamp` (or `PointWrap`), never stretched by a fraction (Plants vs.
  Zombies breathes by rising one art pixel), and cameras move in whole pixels. Every game
  opens in a 1280 × 720 window, and its view follows its art. Pixel art is scaled by a whole
  number: 320 × 180 at 4× (Pong, Snake, Zelda, Pokemon), 426 × 240 at 3× (Mario, whose
  platforms need the height; a one-pixel bar is left on each side), 640 × 360 at 2× (Flappy
  Bird), and 1280 × 720 at 1× (the rest; Pac-Man's maze stands in the middle of it). Two
  games have smooth art: Angry Birds (Kenney's Physics Assets, drawn with linear sampling
  because its pieces rotate) and Geometry Wars' glow. The recordings follow the same rule: `makegif.py` scales with
  nearest neighbour, to a width where one art pixel is a whole number of GIF pixels.
- **Text:** one font, `retro.ttf`, crisp at multiples of 8 pixels. A `.spritefont`'s size is
  in points, a third larger than pixels, so the sizes are 6, 12, 18, 24 … points for 8, 16,
  24, 32 … pixels. Text is always drawn at scale 1, on whole pixels: a game that needs two
  sizes has two fonts (Pong's `font` and `font-big`), and never scales one. On screen, HUD text is
  16 or 32 pixels, and the title screen's name is 64 pixels with 32-pixel lines under it, in
  every game: at 1× that is the 48- and 24-point fonts, at 4× the 12- and 6-point ones. Over a busy background, text gets a dark shadow. Messages are sentences with
  single spaces. (Snake draws its score with digits from its atlas, and Pokemon draws its
  own bitmap fonts, from `fonts/*_atlas.png`.)
- **Screens and keys:** every game opens on the same title screen: the game drawn behind a
  dark band across the middle, and on the band the game's name, its controls in one dimmer
  line ("Arrows: move   Space: jump"), and "Press Enter". GARCore's `TitleScreen` draws it
  from Snake on, in plain code: three `MeasureString` calls, a rectangle and three
  `DrawString` calls. Pong and Flappy Bird come before that and draw the same layout
  themselves at fixed positions (in `Game1` and in `TitleState`), a band and three centred
  lines, so the title takes no more code than its session can carry; Pokemon has
  its own for its bitmap fonts. Nothing in a game may use a concept before the session that
  teaches it, even in a helper: no delegates before Zelda. The text is white,
  or the game's own light colour where the game has a fixed palette (Snake, Pokemon). The
  controls are shown there and nowhere else: no key hints in the HUD. In a game with game
  states, the title is a state that draws a play state without updating it; in Pong, Snake
  and Sokoban it is a flag in `Game1`, since a state machine only for a title would add
  architecture that isn't the session's topic. Enter starts, continues and restarts (end
  screens say "Press Enter to …"), Esc quits, R restarts the level where there are levels,
  P pauses where there is a pause, F1 toggles debug drawing, F3 the profiler.
- **Naming:** a game's folder is its full name, as in its site page's URL
  (`06-super-mario-bros`), and so is its solution (`SuperMarioBros.slnx`). Step projects
  use a short form of the game's name (`Mario0`, `Birds0`, `Pvz0`), never a genre.

## Where Content Goes

Each piece of content has one home; the others link to it. If a fact changes, only one
file should need editing.

| | Deck | Session page | Game README |
| --- | --- | --- | --- |
| For | The class, live, with the teacher talking | A student alone, before and after class, and for the exam | Someone with the repo open |
| Answers | What are we doing now? | Why does this work, and when would I use it? | How do I run this, and where is X? |
| Holds | The session's flow, the goal demo, diagrams, a few key excerpts, discussion questions, exercise prompts | Concepts and patterns with trade-offs, readings, exercises, Apply it, Check yourself, links to key files | The steps, what's new in GARCore, a code map, tests and tools, content, controls, running, credits |
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
- All twelve decks follow this. Every slide has speaker notes written for
  presenting: what to say, what to ask (with the expected answer), and how to run each demo;
  the Check yourself slides carry the site's answers.

## General Notes

- Use consistent, simple UML diagrams (Mermaid is supported on the site).
- End each game session with "what moved into GARCore this week, and why?"

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
| SOLID principles | Woven into sessions; no standalone lecture |
| Proxy, Iterator, Builder | Probably out of scope |
| Game math (sin/cos, atan2, lerp, radians, normalization) | Short primer in Pong/Flappy |
| [Refactoring](https://refactoring.guru) | 04 Sokoban, then an exercise in every session |
| Pathfinding (A\*), steering behaviours | A\* is in Pac-Man's code behind `IRouteStrategy`, as optional reading: the session teaches the strategy and leaves the algorithm out. Steering: Geometry Wars (seek & flee is in its code) |
| ECS in practice (e.g. MonoGame.Extended) | Geometry Wars, briefly |

## Ideas for Games

- **Space Invaders / Asteroids:** object pool, spatial partitioning, Prototype (splitting
  asteroids)
- **Tetris:** pure grid logic
- **Tower defence / turn-based strategy:** mouse input, Type Object, pathfinding
- Minecraft, Terraria, Stardew Valley: probably too big, but good for inspiration
