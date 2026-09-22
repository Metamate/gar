---
title: 03 Snake
description: Organizing and designing our game as it grows.
sidebar:
  order: 3
---

- Sprite Sheets
- Procedural Layouts
- Levels
- Scene Management ? (basically state pattern)
- Input
- Command Pattern
- Player Health
- Persistent Save Data
- [Component Pattern](https://gameprogrammingpatterns.com/component.html)
- [Components](https://gavsdevblog.wordpress.com/2016/09/04/monogame-components-and-services/)
- Inheritance vs Composition

## Today's Goal

Organizing and designing our game as it grows.

## Input

Separating physical inputs (Space Bar, 'A' button) from logical actions ("Jump", "Fire").

- Keyboard, mouse, gamepad input models
- Polling vs event-driven
- Binding input to actions
- [Command Pattern](https://gameprogrammingpatterns.com/command.html)
- Input buffering

## Inheritance vs Composition

Why deep inheritance hierarchies (e.g., Object -> Entity -> Movable -> Enemy -> Orc) become
unmanageable.

Component Pattern: The shift from "is-a" to "has-a" relationships.
