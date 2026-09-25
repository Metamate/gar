---
title: Course Recap
description: Every pattern and topic in the course, the games that use it, and the exam questions it prepares you for.
---

The patterns and topics from all twelve games in one place: where each one is introduced,
where it comes back, and which [exam question](../exam/) it belongs to. We go through it
in the last lesson of [session 12](../sessions/12-vampire-survivors/), and it is a good
starting point for exam preparation (see [the project at the exam](../project/#the-project-at-the-exam)).

## Patterns

| Pattern | Introduced in | Also in | Exam |
| --- | --- | --- | --- |
| Update Method | [01 Pong](../sessions/01-pong/) | every game | [1](../exam/#1-game-loop--update-method) |
| State (game states) | [02 Flappy Bird](../sessions/02-flappy-bird/) | every game from here | [2](../exam/#2-state-pattern--state-stack) |
| Singleton | [02 Flappy Bird](../sessions/02-flappy-bird/) | | [3](../exam/#3-singleton--service-locator) |
| Command | [04 Sokoban](../sessions/04-sokoban/) | | [4](../exam/#4-command-pattern--input-handling) |
| State (entities) | [05 Pac-Man](../sessions/05-pac-man/) | [06 Super Mario Bros](../sessions/06-super-mario-bros/), [08 The Legend of Zelda](../sessions/08-the-legend-of-zelda/) | [2](../exam/#2-state-pattern--state-stack) |
| Strategy | [05 Pac-Man](../sessions/05-pac-man/) | [06 Super Mario Bros](../sessions/06-super-mario-bros/) | |
| Adapter & Facade | [07 Angry Birds](../sessions/07-angry-birds/) | | [7](../exam/#7-tilemaps-collision-detection--procedural-generation) |
| Prototype | [07 Angry Birds](../sessions/07-angry-birds/) | | [8](../exam/#8-data-driven-design--serialization) |
| Observer | [08 The Legend of Zelda](../sessions/08-the-legend-of-zelda/) | [10 Pokemon](../sessions/10-pokemon/), [11 Geometry Wars](../sessions/11-geometry-wars/) | [5](../exam/#5-observer-pattern-events--ui) |
| Component | [09 Plants vs. Zombies](../sessions/09-plants-vs-zombies/) | [11 Geometry Wars](../sessions/11-geometry-wars/) | [9](../exam/#9-components--systems) |
| Type Object | [09 Plants vs. Zombies](../sessions/09-plants-vs-zombies/) | [10 Pokemon](../sessions/10-pokemon/) | [8](../exam/#8-data-driven-design--serialization) |
| State stack | [10 Pokemon](../sessions/10-pokemon/) | [11 Geometry Wars](../sessions/11-geometry-wars/) | [2](../exam/#2-state-pattern--state-stack) |
| Service Locator | [10 Pokemon](../sessions/10-pokemon/) | | [3](../exam/#3-singleton--service-locator) |
| Object Pool | [11 Geometry Wars](../sessions/11-geometry-wars/) | | [10](../exam/#10-memory--performance) |
| Flyweight | [11 Geometry Wars](../sessions/11-geometry-wars/) | | [10](../exam/#10-memory--performance) |

## Threads Through the Course

Some ideas grow over several games. Following one thread is a good way to prepare an exam
answer.

- **Game loop & time:** the game loop ([01](../sessions/01-pong/)) → fixed-tick movement
  ([03](../sessions/03-snake/)) → the physics step ([07](../sessions/07-angry-birds/)) →
  tweening ([08](../sessions/08-the-legend-of-zelda/)) → a fixed-timestep core
  ([11](../sessions/11-geometry-wars/)). Exam [1](../exam/#1-game-loop--update-method).
- **Input:** keyboard and mouse ([02](../sessions/02-flappy-bird/)) → input as actions
  ([03](../sessions/03-snake/)) → commands with undo ([04](../sessions/04-sokoban/)) →
  picking ([09](../sessions/09-plants-vs-zombies/)). Exam
  [4](../exam/#4-command-pattern--input-handling).
- **Data:** assets as data ([03](../sessions/03-snake/)) → levels as data
  ([04](../sessions/04-sokoban/)) → game types as data ([09](../sessions/09-plants-vs-zombies/))
  → save/load ([10](../sessions/10-pokemon/)). Exam [8](../exam/#8-data-driven-design--serialization).
- **Entities:** inheritance ([06](../sessions/06-super-mario-bros/)) → composition vs.
  inheritance ([08](../sessions/08-the-legend-of-zelda/)) → components
  ([09](../sessions/09-plants-vs-zombies/)) → components vs. systems
  ([11](../sessions/11-geometry-wars/)) → data-oriented design
  ([12](../sessions/12-vampire-survivors/)). Exam [9](../exam/#9-components--systems),
  [10](../exam/#10-memory--performance).
- **Dependencies:** Singleton ([02](../sessions/02-flappy-bird/)) → Service Locator
  ([10](../sessions/10-pokemon/)) → dependency injection ([11](../sessions/11-geometry-wars/)).
  Exam [3](../exam/#3-singleton--service-locator).
- **Testing:** rules apart from drawing, and unit tests ([04](../sessions/04-sokoban/)) →
  ghost strategies tested one by one ([05](../sessions/05-pac-man/)) → a save/load
  round trip ([10](../sessions/10-pokemon/)) → fakes passed in through dependency injection
  ([11](../sessions/11-geometry-wars/)) → the fast spatial grid checked against the slow,
  obvious search ([12](../sessions/12-vampire-survivors/)).
- **Collision:** AABB ([01](../sessions/01-pong/)) → grid lookups ([04](../sessions/04-sokoban/))
  → tile collision ([06](../sessions/06-super-mario-bros/)) → a physics library
  ([07](../sessions/07-angry-birds/)) → hitboxes ([08](../sessions/08-the-legend-of-zelda/)) →
  spatial partitioning ([12](../sessions/12-vampire-survivors/)). Exam
  [7](../exam/#7-tilemaps-collision-detection--procedural-generation).
- **Coordinate spaces:** virtual resolution ([02](../sessions/02-flappy-bird/)) → world vs.
  camera ([06](../sessions/06-super-mario-bros/)) → physics units vs. pixels
  ([07](../sessions/07-angry-birds/)) → screen to grid ([09](../sessions/09-plants-vs-zombies/)).
- **Rendering:** drawing & the content pipeline ([01](../sessions/01-pong/)) → textures
  ([02](../sessions/02-flappy-bird/)) → atlases, sprites & animation
  ([03](../sessions/03-snake/)) → debug drawing ([06](../sessions/06-super-mario-bros/)).
  Exam [6](../exam/#6-sprites-texture-atlases-animation--rendering).
- **Performance:** the fixed timestep ([01](../sessions/01-pong/)) → Object Pool and
  Flyweight ([11](../sessions/11-geometry-wars/)) → profiling, spatial partitioning and
  data-oriented design ([12](../sessions/12-vampire-survivors/)). Exam
  [10](../exam/#10-memory--performance).
- **GMDCore:** every game adds to the same core library. Each repository's README lists
  what is new in `GMDCore` since the previous game.
