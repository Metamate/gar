---
title: Overview
description: The 12 course sessions, their games and main topics.
---

The course spans 12 sessions, each building a classic game. Every session has one main
topic, supported by a few related ones. The [course project](../project/) runs alongside,
in your own time.

| Session | Game | Main topic | Patterns | Also |
| --- | --- | --- | --- | --- |
| 01 | [Pong](../sessions/01-pong/) | The game loop | Game Loop, Update Method | delta time, input, drawing, AABB collision |
| 02 | [Flappy Bird](../sessions/02-flappy-bird/) | Structuring the code | State (game states), Singleton | a core library (GARCore), textures & parallax, procedural generation, keyboard & mouse input |
| 03 | [Snake](../sessions/03-snake/) | Assets as data | — | texture atlases, sprites & animation, fixed-tick movement, input as actions & buffering |
| 04 | [Sokoban](../sessions/04-sokoban/) | Command and undo | Command | levels as text files, rules apart from drawing, unit tests |
| 05 | [Pac-Man](../sessions/05-pac-man/) | The State pattern | State, Strategy | State vs. Strategy, pathfinding with A\*, testing each ghost |
| 06 | [Super Mario Bros](../sessions/06-super-mario-bros/) | The game world | Strategy (level makers), State (the player) | platformer physics & tile collision, debug drawing |
| 07 | [The Legend of Zelda](../sessions/07-the-legend-of-zelda/) | Events | Observer | C# events and lambdas, an event queue, hitboxes, tweening, composition vs. inheritance |
| 08 | [Angry Birds](../sessions/08-angry-birds/) | Using a physics library | Adapter, Facade, Prototype | physics world vs. game world, contact events, destroying safely |
| 09 | [Plants vs. Zombies](../sessions/09-plants-vs-zombies/) | Components | Component, Type Object | game types as data, picking, testing a component |
| 10 | [Pokemon](../sessions/10-pokemon/) | Scenes and UI | State (a stack), Service Locator | UI widgets, separating UI from game data, save/load |
| 11 | [Geometry Wars](../sessions/11-geometry-wars/) | Components and systems | Object Pool, Flyweight | components vs. systems, dependency injection & testing with fakes |
| 12 | [Vampire Survivors](../sessions/12-vampire-survivors/) | Performance | Spatial Partition, Data Locality | profiling, data-oriented design, [course recap](../recap/) |

## The Session Pages

Every session page has the same parts. **Prepare** lists chapters and tutorials to read
beforehand. The main part builds the game, with exercises in between. Pong and Flappy
Bird start from an empty project; from Snake on, you start from a working codebase, explore
it and extend it. **Apply It to Your Project** takes the session's patterns into your own
[course project](../project/), and **Check Yourself** has short questions, linked to the
[exam](../exam/) questions they prepare you for.

## GARCore

Reusable code moves from the individual games into **GARCore**, a shared class library that
starts in [Flappy Bird](../sessions/02-flappy-bird/) and grows into a small game framework,
with screen scaling, input, sprites, animation, tilemaps, state machines and more. Deciding
what belongs in the core and what belongs in the game is an architectural decision in
itself, and it comes up again in every session.
