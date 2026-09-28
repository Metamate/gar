---
title: Exercise Answers
description: Instructor-only notes on what a good answer to each exercise contains. Not published.
draft: true
---

:::caution
This page is a **draft**: it is visible when running `astro dev`, but excluded from the
production build. The exercises stay unsolved in the public repos; this page says what a good
answer contains, and what to look out for, for whoever checks the work.
:::

## 01 Pong

Exercises 0 to 7 are the build steps: step `PongN` in gar-games is a solution to exercise N.
Look for delta time in every movement (not a fixed step per frame), clamping that uses the
paddle's height, and the bounce angle from where the ball hits the paddle rather than a
flipped velocity only. The optional steps 8 to 11 are `Pong8` to `Pong11`.

## 02 Flappy Bird

The build exercises match steps: 1 and 2 are `Flappy0` (its `GMDCore` is the library), 3 is
`Flappy3`, 4 is `Flappy4` and `Flappy5`, 5 is `Flappy8`, 6 is `Flappy9`, 7 is `Flappy12`.

- **1, a class library:** the reference points from the game to GMDCore, never back; `Core`
  mentions nothing about Flappy Bird.
- **5, hitboxes:** "more forgiving" means a hitbox a few pixels smaller than the sprite.
- **6, a state machine:** each state resets itself in `Enter`; `Game1` only forwards
  `Update` and `Draw`.
- **7, audio as a Singleton:** a private constructor and one static instance. Good answers
  also say what it costs: every caller now depends on the concrete `Audio` class.

## 03 Snake

- **1, data, not code:** the beetle needs only XML (two regions, one animation) and the
  animation name in C#, if the mouse is swapped for it. A beetle next to the mouse needs
  real C#: `Game1` handles the mouse by name (its field, its respawn, its collision), so its
  rules live in `Game1`, not in the data. The insight to look for: data describes *what
  things look like*; behaviour is still code.
- **2, speed up:** the tick length belongs to the snake's movement (or to a game-rules
  class), changed where eating is handled; a minimum stops it at a playable speed.
- **3, new input:** `GamePadInfo` mirrors `KeyboardInfo` (this frame's and last frame's
  state). In the game, only `GameController` changes: that is the point of actions.
- **4, pause:** a `Paused` action in `GameController`; while paused, the tick doesn't
  advance and the input buffer isn't filled, or turns queue up and fire on resume.
- **5, a fixed timer (stretch):** `FixedTimer` holds the accumulator and an interval and
  calls an `Action` per tick; the snake subscribes. Watch for a timer that drops the
  remainder (`_elapsed = 0` instead of `-= interval`).
- **Rebinding (optional):** only `GameController` (and a settings file) changes; the snake
  and the game never notice.

## 04 Sokoban

- **1, a new level:** the game could list the level files in the folder instead of
  `LevelCount`. Solvable: by playing it through, or by a solver; a level is only known to
  be solvable once someone has solved it.
- **2, two more tests:** one test pushes a box off a goal and asserts `IsSolved` is false;
  the other walks onto a goal and checks the position. Both must fail when `Move` is broken.
- **3, test first (ice):** tests written before the code, seen failing first. A box can't be
  pushed onto `~`; the player can walk on it. `LevelView` draws tile 9 for ice.
- **4, replay:** reset the level, then re-execute the history's commands on a timer. The
  commands already know how to execute: no new move code.
- **5, restart as a command:** the command remembers the level as it was (a snapshot of
  positions) so that undo can restore it.
- **6, snapshot undo (stretch):** less code and harder to get wrong, but memory grows with
  every move and the whole level is copied each time. Commands are smaller and also
  support replay.

## 05 Pac-Man

- **1, a new mode:** one new class (`FrozenState`) and one line where the ghost is eaten,
  against seven places in `Pacman1`'s enum version.
- **2, a new personality:** a new `ITargetStrategy` that remembers Pac-Man's recent tiles
  (a queue); the test comes first and fails until the strategy exists. The atlas needs two
  regions and an animation.
- **3, frightened in the house:** `InHouseState` needs a frightened flag or timer, and draws
  blue while it runs, without leaving the house.
- **4, fruit:** a class of its own (or in `World`, which knows the dot count and the
  timer); not in `Maze`, which is the level's layout.
- **5, tunnel (stretch):** the maze knows which tiles are tunnel; the ghost (or its state)
  decides the speed there.
- **Pathfinding (optional):** a breadth-first search from the ghost's tile to the target
  over open tiles, returning the first step. It takes the short way round walls where the
  greedy choice doesn't.

## 06 Super Mario Bros

- **1, a chunk level maker:** a new `LevelMakerBase` subclass reading chunk files, placed
  end to end; each level a few chunks longer. The Strategy pattern is what makes it a
  drop-in.
- **2, moving platforms:** no single right place. Common: the player remembers the
  platform it stands on and moves with it before its own movement. Good answers say why
  their choice.
- **3, powerups:** a component or a state-like object with a timer on the player, rather
  than flags such as `isInvincible` and `isBig` on `Player`.
- **4, debug drawing:** coyote time shows as the frames where the probe finds no ground but
  a jump still works (about 0.1 s).
- **Auto-tiling (optional):** look at left and right neighbours: both solid gives the
  middle, only the right solid gives the left end, and so on. Tilemap-level logic that any
  level maker gets for free.
- **A scene graph (optional):** world position = parent's world position + local position;
  when the platform moves, the child moves with it without any code in the player.

## 07 The Legend of Zelda

- **Event-driven:**
  - `OnPlayerDied`: `Room` fires it, `Dungeon` forwards it, `PlayState` changes to game
    over.
  - Enemy death: `Room` checks `enemy.Health <= 0` and removes the enemy in its update loop.
    An `EnemyDied` event would let a score, a sound or a key drop react without `Room`
    knowing them.
  - Sounds: `SoundManager.PlaySound` is called from `Room`, `Dungeon` and
    `PlayerSwingSwordState`. With events, gameplay announces what happened and one
    listener picks the sounds.
- **Composition:** the hierarchy explodes into combinations (a flying shooter, an exploding
  walker). With composition, an enemy has a movement part and zero or more abilities; a
  shooting behaviour attaches to any enemy.
- **Keys and locked doors:** the key drop is an event subscriber; the lock is data in
  `door_layouts.xml` and a flag on the doorway; the key count lives on the player.
- **A dungeon map (optional):** the dungeon records visited rooms; a map state pushed on a
  key press draws them.

## 08 Angry Birds

- **1, a new level:** the level needs no code; the new prefab is one entry in `Prefabs`.
- **2, a new bird:** a prefab for the heavy bird, and the level format lists birds by name
  (`birds red red heavy`), read in `Level`.
- **3, explosive:** the facade gets something like `ApplyImpulse(body, impulse)` or
  `Explode(center, radius, strength)`, in pixels; Box2D types stay inside `Physics`.
- **4, unit test the conversion:** round trip pixels to metres and back; y flips; zero
  stays zero. The `InternalsVisibleTo` line is needed because `Units` is internal.
- **5, swap the library (stretch):** only the `Physics` folder changes. That is the answer
  the adapter was built for.

## 09 Plants vs. Zombies

- **1, new types:** only JSON (and the atlas regions for the Tall-nut); no code.
- **2, Snow Pea:** a `Slow` (or `Chill`) effect carried by the pea's `Projectile`, applied
  to the zombie's `Walker` on hit, with a timer; the data marks the plant's shooter as cold.
- **3, Pumpkin:** `Armour` can be reused as is for the health; drawing it needs a different
  position (around the plant, not on a head).
- **4, a shovel:** a seed-bar entry that isn't a plant: picking a cell then removes the plant
  there instead of planting one. Picking is already there.
- **5, a component registry (stretch):** gains: new components without touching
  `PlantType.Create`. Loses: the compiler no longer checks the data's shape, so a typo in
  a component name is a runtime error.

## 10 Pokemon

- **1, overworld encounters:** `PlayerWalkState` rolls in tall grass; the stack then holds
  `PlayState`, a fade, and `BattleState` (with the menu on top once it shows). When a
  battle ends, the battle states pop and `PlayState` is on top again, unchanged.
- **2, battles:** `BattleMenuState` → `TakeTurnState` (damage in `Mon`) → back to the menu,
  or victory or defeat when one side's HP is 0.
- **3, data-driven definitions:** the new species is JSON only. Types need a field in the
  record, in `PokemonSpecies`, and a multiplier in the damage formula.
- **4, save and load:** save data, not objects (species name, level, HP, position), as
  records; the round-trip test compares a saved and loaded record.
- **5, pause:** a `PauseState` pushed on a key and popped on the same key.
- **Catching (optional):** a Catch option in `BattleMenuState`, a chance from the monster's
  HP, and a field menu state; `Party` gains an add method.

## 11 Geometry Wars

- **1, composition:** the new enemy is only a recipe in `EntityFactory`; the shield is one
  component that listens to (or intercepts) damage.
- **2, component or system?** Pressing the key and "one per life" belong to the player
  (a component, or the session's state); destroying every enemy on screen spans many
  entities, so it belongs in a system.
- **3, dependency injection:** the service is added to `PlayContext` and passed in; the
  classes that shake receive it. With a Service Locator, they would reach for it instead,
  and their constructors wouldn't show it.
- **4, test with a fake:** the fake records spawn calls; the test asserts two bullets. The
  spread uses `Random.Shared`, so the test checks the count, not the angles, unless the
  randomness is passed in too.
- **5, measure pooling:** without the pool, allocated bytes and gen-0 collections per second
  rise clearly while firing.

## 12 Vampire Survivors

- **1, tune the grid:** smaller cells mean more cells to visit; bigger cells mean more
  enemies per cell to check. The cells can't be smaller than the biggest overlap distance,
  or pairs in neighbouring cells are missed.
- **2, bolts as arrays?** Usually not worth it: there are few bolts. It would be with
  thousands of them.
- **3, the next bottleneck:** at 20,000 the profiler points at the next phase; any change
  must keep `Survivors.Tests` green.
- **4, a new enemy kind:** a new `EnemyKind` value with its speed, health and sprite; the
  spawner places a group together. The struct-of-arrays layout doesn't change.
- **5, parallel separation (stretch):** two threads writing the same enemy is a race. Fixes:
  each thread only writes enemies in its own rows, or computes pushes into a separate buffer
  that is applied afterwards.
