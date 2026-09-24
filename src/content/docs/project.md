---
title: Project
description: The course project — a 2D game built with MonoGame.
---

For the GAR course project, you will be implementing a 2D game using the MonoGame Framework.

**Group size:** 1–3 students

The goal of the project is to create a simple 2D game that uses best practices for
organizing and architecting a game project. That is, the project must include gameplay
systems and design elements solved through patterns and principles taught in the course.
You have free choice in which type of game you create, as long as you keep the above in
mind.

The project is done in your own time, alongside the sessions. Each session ends with
questions that bring the day's patterns into your project.

## Requirements

The source code of the project must be versioned using git and hosted on GitHub. By the
final course session, the root of the repository must contain a `README.md` with:

- A title and a brief description of the project
- A "how to play" section (input, actions, game modes, etc.)
- An **architecture** section with:
  - A class diagram of the game's main classes (e.g. using [Mermaid](https://mermaid.js.org/syntax/classDiagram.html))
  - The design patterns from the course that the game uses (at least three), each with a
    short explanation and a link to where it is implemented
- A brief video demonstration of the project (hosted on YouTube)
- A link to a downloadable, playable Windows build of the project (hosted on itch.io)

## Milestones

Keep a steady pace. Aim to reach each milestone by the session listed:

| By session | Milestone |
| --- | --- |
| [04 Sokoban](../sessions/04-sokoban/) | Groups formed, [game concept](#getting-started) written, repository created and link uploaded to itslearning |
| [06 Super Mario Bros](../sessions/06-super-mario-bros/) | Playable core loop, first class diagram |
| [09 Plants vs. Zombies](../sessions/09-plants-vs-zombies/) | [Self-review](#self-review) done: updated class diagram, list of patterns, event map, at least one refactoring |
| [11 Geometry Wars](../sessions/11-geometry-wars/) | [Release build](#release) on itch.io, README started |
| [12 Vampire Survivors](../sessions/12-vampire-survivors/) | Final README complete, repository link uploaded to itslearning |

## Getting Started

**Choose a game.** Take inspiration from classic games, like the ones in the course.

- **Be mindful of scope (creep).** A small, finished game with clean architecture beats a
  large, unfinished one.
- You don't need to know all the details before you start. Iterate and experiment.

Write a **one-page concept**: title, core gameplay loop, controls, and a list of the
systems you expect to need (e.g. scenes, tilemap, enemies with AI, UI, save data).

**Set up the repository:**

- Create the repository from the [gar-starter](https://github.com/Metamate/gar-starter)
  template (**Use this template** on GitHub): an empty game set up with the content
  builder. Its README shows how to rename it and add GMDCore if you want to reuse it.
- Check that build output stays out of git: the template's `.gitignore` already ignores
  `bin/`, `obj/`, `.vs/`, ….
- Add your group members as collaborators, and upload the repository link to itslearning.

**Sketch the architecture** before writing much code (a simple class diagram is enough):

- Which **states/scenes** does your game have, and how does it move between them?
- Which code belongs in a **reusable core**, and which is specific to your game?
- Where does **input** go, and which **actions** does it trigger?

## Self-Review

Halfway through, take stock before the game grows further. Update your class diagram,
list the patterns you use or plan to use (and where), and write an **event map**: the
meaningful moments in your game, who fires them and who reacts (see
[Zelda](../sessions/08-the-legend-of-zelda/)). Then go through these questions with your
group:

- Is `Game1` (or any other class) doing too much?
- Are game states handled by a state machine, or by flags and `if`-chains?
- Do gameplay classes read the keyboard directly?
- Which classes know about each other that shouldn't need to?
- Which values are hardcoded that should be data?

Pick at least one issue and fix it. In your commit message, describe the design problem
and how the change solves it. This makes good material to talk about at the exam.

**Review with another group (recommended).** Swap repositories with another group, start
from their README and class diagram, and answer:

1. Can you understand the overall architecture? Does the code match the diagram?
2. Where would you add a new screen, enemy or level? How many files would need to change?
3. Which patterns do you recognize? Are they used where they help, or just to have them?
4. What are your **top three** concrete improvements, most valuable first?

Write your answers as a GitHub issue in their repository.

## Release

- Make a **Release** build, not a Debug build.
- Publish **self-contained** so players don't need to install .NET:
  `dotnet publish -c Release -r win-x64 --self-contained`.
- Test the build on a machine (or a clean folder) that has never run your game.
- Upload a Windows build to [itch.io](https://itch.io). See MonoGame's
  [packaging](https://docs.monogame.net/articles/tutorials/building_2d_games/25_packaging_game)
  and [publishing](https://docs.monogame.net/articles/tutorials/building_2d_games/26_publish_to_itch)
  guides.

Prioritize what makes the game feel finished: a title screen, a way to win or lose and to
restart, sound and music, and no crashes on the common paths. Cut features before you cut
polish.

## The Project at the Exam

The game project is the reference and talking point at the [exam](../exam/). It can be
worked on up until the day of the exam, but you are expected to have a working version of
the game by the final session of the course.

Prepare by going through each exam question with your project open:

- For each question, find the place(s) in your code you would show. If your project
  doesn't cover a sub-question, find an example in one of the course games instead (the
  [course recap](../recap/) shows where each topic appears).
- Practice explaining your architecture in about 5 minutes, using your class diagram.
- Choose the pattern you will present in detail in question 0, plus a backup in case you
  draw the question that covers it.
- Be ready to modify code live: a small change such as adding a state, an event or a
  command.
