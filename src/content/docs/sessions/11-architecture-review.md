---
title: 11 Architecture Review
description: Peer review of another group's game architecture, and refactoring based on the feedback.
sidebar:
  order: 11
---

## Today's Goal

Read another group's code, analyze its architecture and propose improvements, then use
the feedback you receive to refactor your own. This is exactly what the exam asks of you:
explaining an architecture, and discussing its strengths, weaknesses and trade-offs.

## Peer Review

Groups are paired up. Each group reviews the other's repository for about 45 minutes.

Start from the README and the class diagram, then read the code. Answer these questions:

1. **Overview:** Can you understand the overall architecture from the README and diagram?
   Does the code match the diagram?
2. **Game loop & states:** How are game states or scenes handled? Where would you add a new
   screen?
3. **Coupling:** Pick one class. What does it depend on? Could any of those dependencies be
   removed with an interface, an event or a service?
4. **Patterns:** Which patterns from the course do you recognize? Are they used where they
   help, or just to have them?
5. **Data:** What is hardcoded that could be data-driven?
6. **Change:** Pick a plausible new feature (a new enemy, a new level, a new input device).
   How many files would need to change?
7. **Suggestions:** Give your **top three** concrete improvements, most valuable first.

Write your answers as a GitHub issue in the other group's repository.

## Discussion

Each pair of groups spends about 15 minutes going through the reviews together. Focus on
_why_ a change would help, and what it would cost.

## Refactor

Use the rest of the session to act on at least one suggestion you received. In your commit
message, describe the design problem and how the change solves it. This makes good
material to talk about at the exam.
