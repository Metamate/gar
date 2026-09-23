---
title: 07 Project Checkpoint
description: Midway project status, architecture review of your own game, and project work.
sidebar:
  order: 7
---

## Today's Goal

Take stock of your [project](../../project/) halfway through, and make sure its
architecture is heading in a good direction before it grows further.

## Checkpoint Deliverables

Bring the following to class (commit them to your repository):

1. **A playable core loop.** It doesn't need to be pretty, but the central mechanic should
   work.
2. **An updated class diagram** of your game's main classes (update your sketch from the
   [kick-off](../04-project-kick-off/)). Mermaid in your README works well.
3. **A list of patterns** you use or plan to use, and where.
4. **An event map:** the meaningful moments in your game, who fires them and who reacts
   (see [Zelda](../06-the-legend-of-zelda/)).

## Status Round

Each group gives a short status (about 5 minutes):

- What works? What is next?
- Show your class diagram. Where is the code most tangled?
- What is your biggest risk (scope, a technical problem, the group)?

## Self-Review Questions

Go through these with your group:

- Is `Game1` (or any other class) doing too much?
- Are game states handled by a state machine, or by flags and `if`-chains?
- Do gameplay classes read the keyboard directly?
- Which classes know about each other that shouldn't need to?
- Which values are hardcoded that should be data?

## Project Work

Use the rest of the session on your project. Pick one issue from the self-review and fix
it today.
