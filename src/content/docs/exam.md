---
title: Exam
description: Exam format and the full pool of exam questions.
---

## Format

Individual oral exam, **20 minutes including grading**, without preparation. See the
[syllabus](../syllabus/#exam) for the formal description.

1. You draw a number from **1–10**.
2. The exam starts with **question 0** (your project), followed by the question you drew.
3. That gives about **7–8 minutes per question**.

The sub-questions are prompts to guide the conversation, not a checklist you must get
through in full.

If you can't answer part of the question you drew using your own game project, you are
welcome to refer to the games from the course. You may use their source code at the exam:
all of them are in [gar-games](https://github.com/Metamate/gar-games), one folder per game.

## Questions

### 0. Present Your Game Project

- Present your game project.
- Briefly describe the gameplay and systems in the game.
- What is the overall architecture?
- Which design patterns does the project use? Choose one and describe its implementation
  in detail. It must be a different pattern from the one in the question (1–10) you drew.

### 1. Game Loop & Update Method

_Covered in: [01 Pong](../sessions/01-pong/), [03 Snake](../sessions/03-snake/),
[11 Geometry Wars](../sessions/11-geometry-wars/)_

1. Explain the structure of a traditional game loop. What are the responsibilities of the
   `Update` and `Draw` phases, and why are they usually kept separate?
2. What problems arise with a fixed-step versus a variable-step game loop, and what role
   does delta time play in `Update`?
3. How is the game loop implemented in MonoGame, and where does your project hook into it?
4. Show a place in your project where the Update Method pattern is applied to a collection
   of game objects. What are the trade-offs of each entity implementing an `Update(dt)`
   method?

### 2. State Pattern & State Stack

_Covered in: [02 Flappy Bird](../sessions/02-flappy-bird/),
[05 Pac-Man](../sessions/05-pac-man/),
[06 Super Mario Bros](../sessions/06-super-mario-bros/),
[10 Pokemon](../sessions/10-pokemon/)_

1. Explain the State pattern. What problem does it solve compared to using `if`/`switch`
   statements on an enum or boolean flags?
2. Draw (or describe) a state diagram for an entity or scene in your project, and explain
   how transitions are triggered.
3. How are `Enter()` and `Exit()` methods useful, and what kinds of bugs occur if you forget
   to call them?
4. What is a state stack, and how does it differ from a simple finite state machine? Give
   an example where pushing/popping states is more appropriate than replacing them.

### 3. Singleton & Service Locator

_Covered in: [02 Flappy Bird](../sessions/02-flappy-bird/),
[10 Pokemon](../sessions/10-pokemon/), [11 Geometry Wars](../sessions/11-geometry-wars/)_

1. Explain the Singleton pattern. Why is it both widespread and controversial in game
   development?
2. Which concrete problems does the Service Locator pattern solve, and how does it differ
   from a Singleton in terms of coupling and testability?
3. Show how `GameServices` (or a similar locator) is used in your project. Which services
   have you registered, and why?
4. Discuss the trade-offs: when would you prefer dependency injection (passing references
   in through constructors) over a Service Locator?

### 4. Command Pattern & Input Handling

_Covered in: [01 Pong](../sessions/01-pong/), [02 Flappy Bird](../sessions/02-flappy-bird/),
[03 Snake](../sessions/03-snake/), [04 Sokoban](../sessions/04-sokoban/)_

1. Explain the Command pattern. What is the core idea, and what are its main benefits in a
   game context? How can commands support undo and redo, and what must a command remember
   to be undone?
2. Explain how input is handled at the lowest level in MonoGame (polling
   `Keyboard.GetState()` / `Mouse.GetState()`). What problems arise if you poll directly
   inside gameplay code?
3. How would you (or how did you) build an input abstraction layer on top of polling, and
   where does the Command pattern fit in?
4. Demonstrate or sketch a refactoring in your project where input handling could be
   improved using commands.

### 5. Observer Pattern, Events & UI

_Covered in: [07 Angry Birds](../sessions/07-angry-birds/),
[08 The Legend of Zelda](../sessions/08-the-legend-of-zelda/),
[10 Pokemon](../sessions/10-pokemon/)_

1. Explain the Observer pattern. How is it implemented in C# with `event` and `delegate`
   (or `Action<T>`)?
2. Why is Observer particularly well suited to UI code?
3. Show a place in your project where you use events. Who is the publisher, who are the
   subscribers, and what would the alternative (polling / direct calls) look like?
4. What are common pitfalls when using events in games?

### 6. Sprites, Texture Atlases, Animation & Rendering

_Covered in: [01 Pong](../sessions/01-pong/), [02 Flappy Bird](../sessions/02-flappy-bird/),
[03 Snake](../sessions/03-snake/)_

1. Explain how 2D rendering works in MonoGame: what is a `SpriteBatch`, and what happens
   between `Begin()` and `End()`?
2. What is a texture atlas (sprite sheet), and why is it preferable to loading many
   individual texture files?
3. How is a frame-based animation system typically structured? Sketch (or describe) a
   class diagram for an `AnimatedSprite`, and explain how it switches between frames over
   time.
4. How does your project organize sprite assets, and what would need to change to support,
   for example, a new animated enemy?

### 7. Tilemaps, Collision Detection & Procedural Generation

_Covered in: [01 Pong](../sessions/01-pong/), [02 Flappy Bird](../sessions/02-flappy-bird/),
[04 Sokoban](../sessions/04-sokoban/),
[06 Super Mario Bros](../sessions/06-super-mario-bros/),
[07 Angry Birds](../sessions/07-angry-birds/),
[08 The Legend of Zelda](../sessions/08-the-legend-of-zelda/),
[12 Vampire Survivors](../sessions/12-vampire-survivors/)_

1. Explain how a tile-based level is represented in memory, and how rendering a tilemap
   differs from rendering individual sprites.
2. Describe at least two approaches to 2D collision detection (e.g. AABB, circle-circle,
   tile-grid lookup). What are the trade-offs between performance and precision?
3. How can collision detection be made efficient when there are many entities?
4. Explain a procedural generation technique you have used or studied (e.g. infinite
   scrolling with obstacles).
5. How would you bring a physics library into a game without the rest of the code depending
   on it? Explain the Adapter and Facade patterns, and what problems they solve.

### 8. Data-Driven Design & Serialization

_Covered in: [03 Snake](../sessions/03-snake/), [04 Sokoban](../sessions/04-sokoban/),
[07 Angry Birds](../sessions/07-angry-birds/), [09 Plants vs. Zombies](../sessions/09-plants-vs-zombies/),
[10 Pokemon](../sessions/10-pokemon/)_

1. What does it mean for a game to be data-driven? Compare hardcoded gameplay values with
   externalized data (JSON, configuration files).
2. What are the benefits of data-driven design for designers, testers and programmers?
   What are the costs?
3. How is serialization used in your project (save/load, level files, entity
   configurations)? Walk through how an object is turned into bytes and back again.
4. Identify a part of your project that is currently hardcoded but would benefit from
   being data-driven. What would the data file look like, and what code would need to
   change?
5. Explain the Prototype pattern. How can prototypes (prefabs) and data files be used to
   build levels, and what must you watch out for when copying objects?

### 9. Components & Systems

_Covered in: [08 The Legend of Zelda](../sessions/08-the-legend-of-zelda/),
[09 Plants vs. Zombies](../sessions/09-plants-vs-zombies/),
[11 Geometry Wars](../sessions/11-geometry-wars/)_

1. Explain the Component pattern. What problems with deep inheritance hierarchies does it
   solve, and what does it cost?
2. How do components of the same entity work together, and how do they find out about other
   entities?
3. When should behaviour live in a system rather than in a component? Give an example.
4. Show a class in your project that does several unrelated things. How could it be split
   into components, and what would you gain?

### 10. Memory & Performance

_Covered in: [11 Geometry Wars](../sessions/11-geometry-wars/),
[12 Vampire Survivors](../sessions/12-vampire-survivors/)_

1. Explain the difference between an Array of Structs and a Struct of Arrays. Why can the
   memory layout of game data affect performance?
2. Explain spatial partitioning. What problem does a uniform grid solve, and when would
   checking every pair still be the better choice?
3. Explain the Object Pool and Flyweight patterns. What problem does each solve, and how do
   they differ?
4. Show a place in your project that would become a bottleneck with many more entities
   (e.g. allocations, collision checks). How would you measure it, and how would you fix
   it?
