# Current Content

## 01 Pong

Today's goal: "Make it work".

We end up with a working, very basic Pong game. The implementation will be "naive" in the sense that it doesn't consider good practices in terms of architecture and design, but it keeps things simple and gets us to a working prototype relatively quickly.

By the end of the session, we will have a game with:

- An update loop
- Primitive graphics
- Collision detection
- Hardcoded input
- Crude state management
- Homemade 8-bit Audio

Contents:

- MonoGame & Tooling
- Game Loop
- Content Pipeline
- Drawing to the Screen
- DeltaTime & Velocity
- Game State
- Encapsulation
- Update Method ← SHOULD maybe update in slides
- Collision Detection
- Sound Effects

Resources:

- [01: What Is MonoGame?](https://docs.monogame.net/articles/tutorials/building_2d_games/01_what_is_monogame)
- [02: Getting Started](https://docs.monogame.net/articles/tutorials/building_2d_games/02_getting_started)
- [03: The Game1 File](https://docs.monogame.net/articles/tutorials/building_2d_games/03_the_game1_file)
- [Game Loop](https://gameprogrammingpatterns.com/game-loop.html)
- [Update Method](https://gameprogrammingpatterns.com/update-method.html)
- [Source Code](https://github.com/Metamate/gmd2-pong)

## 02 Flappy Bird

Today’s goal: Make a “Flappy Bird” clone.

We will go through some new important concepts such as class libraries and interfaces, and figure out how to work with textures. We will also touch on some new design patterns such as State Pattern and Singleton.

Contents:

- Game Architecture & Performance
- Class Libraries
- Images (Sprites)
- Infinite Scrolling
- Procedural Generation
- Interfaces
- State Machines
- Singleton Pattern   ← SHOULD update impl to contain example

Resources:

- [04: Creating a Class Library](https://docs.monogame.net/articles/tutorials/building_2d_games/04_creating_a_class_library)
- [05: Content Pipeline](https://docs.monogame.net/articles/tutorials/building_2d_games/05_content_pipeline)
- [06: Working with Textures](https://docs.monogame.net/articles/tutorials/building_2d_games/06_working_with_textures)
- [Interfaces](https://www.w3schools.com/cs/cs_interface.php)
- [Architecture, Performance & Games](https://gameprogrammingpatterns.com/architecture-performance-and-games.html)
- [Singleton Pattern](https://gameprogrammingpatterns.com/singleton.html)
- [Source Code](https://github.com/Metamate/gmd2-flappy)

## 03 Snake

Today’s goal: Make a Snake game!

This time, we will be starting out with quite a bit of working code. That is, we won’t create everything from scratch. We will instead focus on a few select areas of the game and codebase:

- Texture Atlases
- Sprites & Animation
- Command Pattern
- Collision Detection
- Tilemaps

Contents:

- Sprite Sheets / Texture Atlases
- Sprites & Animation
- Input + Input buffering
- Command Pattern  ← Implementation and game can be improved
- Tile maps

Resources:

- [07: Optimizing Texture Rendering](https://docs.monogame.net/articles/tutorials/building_2d_games/07_optimizing_texture_rendering)
- [08: The Sprite Class](https://docs.monogame.net/articles/tutorials/building_2d_games/08_the_sprite_class)
- [09: The AnimatedSprite Class](https://docs.monogame.net/articles/tutorials/building_2d_games/09_the_animatedsprite_class)
- [10: Handling Input](https://docs.monogame.net/articles/tutorials/building_2d_games/10_handling_input)
- [11: Input Management](https://docs.monogame.net/articles/tutorials/building_2d_games/11_input_management)
- [12: Collision Detection](https://docs.monogame.net/articles/tutorials/building_2d_games/12_collision_detection)
- [13: Working With Tilemaps](https://docs.monogame.net/articles/tutorials/building_2d_games/13_working_with_tilemaps)
- [Command Pattern](https://gameprogrammingpatterns.com/command.html)
- [Source Code](https://github.com/Metamate/gmd2-snake)

## 04 Super Mario Bros

Today’s goal: Make a 2D Platformer.

We will see the fundamental steps involved in creating a basic Super Mario Bros. clone, with a focus on:

- Procedural Level Generation
- State Pattern
- Camera
- Platformer Physics
- Basic AI

Contents:

- Procedural Level Generation
- Scenes
- Level loading from JSON/XML/Tiled
- Camera
- Platformer Physics
- Basic AI
- Powerups
- State Pattern

Resources:

- [14: Sound Effects and Music](https://docs.monogame.net/articles/tutorials/building_2d_games/14_soundeffects_and_music)
- [15: Audio Controller](https://docs.monogame.net/articles/tutorials/building_2d_games/15_audio_controller)
- [16: Working with SpriteFonts](https://docs.monogame.net/articles/tutorials/building_2d_games/16_working_with_spritefonts)
- [17: Scenes](https://docs.monogame.net/articles/tutorials/building_2d_games/17_scenes)
- [18: Texture Sampling](https://docs.monogame.net/articles/tutorials/building_2d_games/18_texture_sampling)
- [State Pattern](https://gameprogrammingpatterns.com/state.html)
- [Source Code](https://github.com/Metamate/gmd2-platformer)

## 05 Zelda

Today’s goal: Make a top-down dungeon crawler.

We will see the fundamental steps involved in creating a primitive The Legend of Zelda clone, with a focus on:

- Assets and Tooling
- Dungeon Generation
- Hitboxes/Hurtboxes
- Observer Pattern (Delegates & Events)
- Screen Scrolling
- Data Driven Design

Contents:

- Top-Down Perspective
- Infinite Dungeon Generation
- Hitboxes/Hurtboxes
- Screen Scrolling
- Data-Driven Design
- Observer Pattern
- Events

Resources:

- [Observer Pattern](https://gameprogrammingpatterns.com/observer.html)
- [C# Delegates](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/delegates/)
- [C# Action Delegate](https://learn.microsoft.com/en-us/dotnet/api/system.action)
- [Source Code](https://github.com/Metamate/gmd2-zelda)

## 06 Pokemon

Today’s goal: Make a turn-based RPG game

We will see the fundamental steps involved in creating a primitive Pokemon clone, with a focus on:

- State Stack
- Tweening
- GUIs
- Turn-Based Systems
- RPG Mechanics
- Service Locator

Contents:

- StateStacks / Pushdown automata
- Turn-Based Systems
- Custom UI
- GUIs, UI Library (Gum)
- RPG Mechanics
- UI Architecture / Separating UI from data/logic (MVVM?, MVP?)
- Service Locator

Resources:

- [19: User Interface Fundamentals](https://docs.monogame.net/articles/tutorials/building_2d_games/19_user_interface_fundamentals)
- [20: Implementing UI with Gum](https://docs.monogame.net/articles/tutorials/building_2d_games/20_implementing_ui_with_gum)
- [21: Customizing Gum UI](https://docs.monogame.net/articles/tutorials/building_2d_games/21_customizing_gum_ui)
- [Pushdown Automata](https://gameprogrammingpatterns.com/state.html#pushdown-automata)
- [Service Locator](https://gameprogrammingpatterns.com/service-locator.html)
- [Components & Services](https://gavsdevblog.wordpress.com/2016/09/04/monogame-components-and-services)
- [Source Code](https://github.com/Metamate/gmd2-pokemon)

## 07 Geometry Wars

Today’s goal: Make a top-down shooter

We will see the fundamental steps involved in creating a primitive Geometry Wars clone, with a focus on:

- Component Pattern
- Data Oriented Design
- Object Pool Pattern
- Flyweight Pattern
- Shaders

Contents:

- Component Pattern
  - Inheritance vs composition
- Shaders & Effects
  - Transitions
  - Color Swapping
  - Sprite Vertex Manipulation
  - 2D Lights
  - Shadows
- Particles
- AI (seek & flee)
- Data Oriented Design
- Performance + profiling (basic stopwatch stuff, allocations, etc.)
- Data Locality
- Flyweight Pattern
- Object Pool

Resources:

- [24: Shaders](https://docs.monogame.net/articles/tutorials/building_2d_games/24_shaders/)
- [Component Pattern](https://gameprogrammingpatterns.com/component.html)
- [Data Oriented Design](https://www.youtube.com/watch?v=WwkuAqObplU)
- [Data Locality](https://gameprogrammingpatterns.com/data-locality.html)
- [Flyweight](https://gameprogrammingpatterns.com/flyweight.html)
- [Object Pool](https://gameprogrammingpatterns.com/object-pool.html)
- [Source Code](https://github.com/Metamate/gmd2-geometrywars)

## 08 Project Work

Resources:

- [25: Packaging Your Game for Distribution](https://docs.monogame.net/articles/tutorials/building_2d_games/25_packaging_game)
- [26: Publishing Your Game to itch.io](https://docs.monogame.net/articles/tutorials/building_2d_games/26_publish_to_itch)
- [27: Conclusion and Next Steps](https://docs.monogame.net/articles/tutorials/building_2d_games/27_conclusion)


## Resources and topics currently not associated with a session (not sure whether to include)

- [Dirty Flag](https://gameprogrammingpatterns.com/dirty-flag.html)
- [Event Queue](https://gameprogrammingpatterns.com/event-queue.html)
- Event Bus + messaging systems/message bus (this is sort of the same?)
- [Prototype](https://gameprogrammingpatterns.com/prototype.html)
  - Abstract Factory Pattern vs Factory Method?
- [Model-View-ViewModel](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93viewmodel)
- [Subclass Sandbox](https://gameprogrammingpatterns.com/subclass-sandbox.html)
- [Type Object](https://gameprogrammingpatterns.com/type-object.html)
- [Refactoring](https://refactoring.guru)

## General Notes

- Use consistent, simple UML diagrams
- Redo graphics and make the games less 1-1 compared to cs50
- Redistribution of topics for better flow (maybe some topics/games over multiple sessions)
- Look into making “Tilemap” more generic early on (in Platformer and Zelda they contain a lot of “game” specific decisions)