---
title: 04 Project Kick-Off
description: Groups, game concept, repository setup and a first architecture sketch.
sidebar:
  order: 4
---

## Today's Goal

Get your [course project](../../project/) started: form groups, choose a game, set up
version control, and sketch a first architecture.

## Choosing a Game

- Take inspiration from classic games. Most of what you need has been covered in the
  first three sessions, and the rest arrives over the coming weeks.
- **Be mindful of scope (creep).** A small, finished game with clean architecture beats a
  large, unfinished one.
- You don't need to know all the details before you start. Iterate and experiment.

Write a **one-page concept**: title, core gameplay loop, controls, and a list of the
systems you expect to need (e.g. scenes, tilemap, enemies with AI, UI, save data).

## Version Control Setup

Spend 15 minutes setting up the repository:

- Create the project from a copy of the empty `Pong0` project and the `Content` builder
  (reuse GMDCore if you like).
- Add a `.gitignore` for .NET (`bin/`, `obj/`, `.vs/`, …).
- Create a GitHub remote and add your group members as collaborators.
- Upload the repository link to itslearning.

## First Architecture Sketch

Before writing code, sketch your game's main classes and how they relate (a simple class
diagram is enough):

- Which **states/scenes** does your game have, and how does it move between them?
- Which code belongs in a **reusable core**, and which is specific to your game?
- Where does **input** go, and which **actions** does it trigger?

Keep the sketch. You will update it at the [project checkpoint](../07-project-work/).

## Project Work

Work on your project. Each group gets short feedback on its game idea and scope.
