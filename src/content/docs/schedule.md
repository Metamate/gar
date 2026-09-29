---
title: Schedule
description: Overview of the 12 course sessions.
---

The course spans 12 sessions, each building a classic game. Every session has one main
topic, the problem it solves, and the patterns that solve it, supported by a few related
ones. The [course project](../project/) runs alongside, in your own time.

| Session | Game | Main topic | Patterns | Also |
| --- | --- | --- | --- | --- |
| 01 | [Pong](../sessions/01-pong/) | The game loop | Game Loop, Update Method | delta time, input, drawing, AABB collision |
| 02 | [Flappy Bird](../sessions/02-flappy-bird/) | Organizing a growing game | State (game states), Singleton | a core library (GARCore), textures & parallax, procedural generation, keyboard & mouse input |
| 03 | [Snake](../sessions/03-snake/) | Assets as data | — | texture atlases, sprites & animation, fixed-tick movement, input as actions & buffering |
| 04 | [Sokoban](../sessions/04-sokoban/) | Actions you can undo, replay and rebind | Command | levels as text files, rules apart from drawing, unit tests |
| 05 | [Pac-Man](../sessions/05-pac-man/) | Behaviour that changes with the situation | State, Strategy | State vs. Strategy, testing each ghost |
| 06 | [Super Mario Bros](../sessions/06-super-mario-bros/) | The game world: tiles, entities and a camera | Strategy (level makers), State (the player) | platformer physics & tile collision, debug drawing |
| 07 | [The Legend of Zelda](../sessions/07-the-legend-of-zelda/) | Reacting to events without knowing who reacts | Observer | C# events and lambdas, an event queue, hitboxes, tweening, composition vs. inheritance |
| 08 | [Angry Birds](../sessions/08-angry-birds/) | A library behind your own interface | Adapter, Facade, Prototype | physics world vs. game world, contact events, destroying safely |
| 09 | [Plants vs. Zombies](../sessions/09-plants-vs-zombies/) | Game objects built from parts | Component, Type Object | game types as data, picking, testing a component |
| 10 | [Pokemon](../sessions/10-pokemon/) | Scenes and UI: screens that stack | State (a stack), Service Locator | UI widgets, separating UI from game data, save/load |
| 11 | [Geometry Wars](../sessions/11-geometry-wars/) | Where behaviour lives in a big game | Object Pool, Flyweight | components vs. systems, dependency injection & testing with fakes |
| 12 | [Vampire Survivors](../sessions/12-vampire-survivors/) | Performance at scale | Spatial Partition, Data Locality | profiling, data-oriented design, [course recap](../recap/) |