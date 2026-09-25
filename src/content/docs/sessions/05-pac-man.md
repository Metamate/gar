---
title: 05 Pac-Man
description: The State pattern through the ghosts' modes, the Strategy pattern through their targeting, and how the two differ.
sidebar:
  order: 5
---

## Today's Goal

Make **Pac-Man**: eat every dot in the maze while four ghosts hunt you. Eat a power pellet,
and for a few seconds the hunters become the hunted.

The ghosts are what make Pac-Man interesting to build. Each ghost switches between modes
(waiting in the house, scattering, chasing, frightened, eaten), and each mode changes how it
moves and what happens when it touches Pac-Man. The main topic is the **State** pattern,
which turns each mode into an object. Along the way:

- The **Strategy** pattern: each ghost chases in its own way
- State vs. Strategy: similar code, different reasons
- Unit tests for each ghost's targeting, one strategy at a time

**Source code:** [gar-games/05-pacman](https://github.com/Metamate/gar-games/tree/main/05-pacman)

| Step | Topic |
| --- | --- |
| `Pacman0` | The maze and Pac-Man |
| `Pacman1` | Ghosts, with their modes as an enum |
| `Pacman2` | The State pattern: each mode becomes a class |
| `Pacman3` | The Strategy pattern: each ghost chases in its own way |
| `Pacman4` | The whole game: lives, death, levels and game states (the finished game) |
| `Pacman.Tests` | Unit tests for the targeting strategies, the ghost states and Pac-Man's movement |

## Prepare

- [State](https://gameprogrammingpatterns.com/state.html) (up to and including "The State
  Pattern")
- [Strategy](https://refactoring.guru/design-patterns/strategy)
- Optional: [The Pac-Man Dossier](https://pacman.holenet.info/), chapter 3 ("Maze Logic
  101") and 4 ("Meet the Ghosts"): how the original ghosts really work

## The Maze

_Step `Pacman0`_

The maze is a text file, like [Sokoban's levels](../04-sokoban/#levels-as-data):

```text title="maze.txt (the top)"
############################
#............##............#
#.####.#####.##.#####.####.#
#o####.#####.##.#####.####o#
```

`#` is a wall, `.` a dot and `o` a power pellet. `-` is the door of the ghost house and `H`
its inside; `P` marks where Pac-Man starts, and `b`, `p`, `i` and `c` the four ghosts. A row
that is open at both ends is a tunnel: leaving on one side enters on the other.

As in Sokoban, the rules are separate from the drawing. `Maze`, `PacMan` and `World` hold the
game; `MazeView` and `PacManView` draw it. The walls aren't even images: `MazeView` draws a
blue line along every side of a wall tile that faces an open tile.

### Moving through the maze

Pac-Man doesn't move freely like Pong's ball. He moves from the centre of one tile to the
centre of the next, and only at a tile centre can he turn. The ghosts move the same way, so
this lives in a shared base class, `Actor`:

```csharp title="Actor.cs"
public void Move(float distance)
{
    while (true)
    {
        Vector2 goal = Maze.Center(_target);
        float left = Vector2.Distance(Position, goal);
        if (left > distance)
        {
            Position += (goal - Position) / left * distance;
            return;
        }

        // Arrived at a tile centre: wrap through the tunnel, and choose the next direction.
        distance -= left;
        _target = maze.Wrap(_target);
        Position = Maze.Center(_target);
        Heading = ChooseDirection(_target);
        if (Heading == Direction.None)
            return;
        _target += Heading;
    }
}

protected abstract Point ChooseDirection(Point tile);
```

Pac-Man and the ghosts only differ in how they choose. Pac-Man turns where the player asked,
if he can:

```csharp title="PacMan.cs"
protected override Point ChooseDirection(Point tile)
{
    if (Wanted != Direction.None && !Maze.BlocksPacMan(tile + Wanted))
        return Wanted;
    if (!Maze.BlocksPacMan(tile + Heading))
        return Heading;
    return Direction.None;
}
```

`Wanted` is kept until Pac-Man can turn that way. Press up a little before a corner, and he
turns up when he gets there. That's [input buffering](../03-snake/#input-buffering), as in
Snake, but here it's what makes the controls feel good.

## Ghosts, With an Enum

_Step `Pacman1`_

Each ghost is always in one of five **modes**:

| Mode | What the ghost does | Touching Pac-Man |
| --- | --- | --- |
| In the house | Waits, then leaves through the door | — |
| Scatter | Heads for its own corner of the maze | Pac-Man is caught |
| Chase | Hunts Pac-Man | Pac-Man is caught |
| Frightened | Turns blue, slows down and wanders at random | The ghost is eaten |
| Eaten | Only the eyes, racing back to the house | — |

```mermaid
stateDiagram-v2
    [*] --> InHouse
    InHouse --> Scatter : left the house
    Scatter --> Chase : schedule
    Chase --> Scatter : schedule
    Scatter --> Frightened : power pellet
    Chase --> Frightened : power pellet
    Frightened --> Scatter : time's up
    Frightened --> Chase : time's up
    Frightened --> Eaten : touched Pac-Man
    Eaten --> InHouse : back in the house
```

Scatter and chase take turns on a fixed **schedule** (`ModeSchedule`): 7 seconds of scatter,
20 of chase, and so on. That's why the ghosts sometimes seem to give up the hunt: without the
scatter phases, the game would be too hard.

However a ghost moves, it decides at each tile centre the same way. It never turns back, and
of the directions left, it takes the one whose next tile is closest to a **target tile**
(in a straight line). The mode decides the target: its corner in scatter, Pac-Man in chase,
the house when eaten. Frightened ghosts have no target, and pick at random.

The simplest way to build the modes is an enum, and that's what `Pacman1` does:

```csharp title="Ghost.cs (Pacman1)"
public enum GhostMode { InHouse, Scatter, Chase, Frightened, Eaten }

public void Update(float deltaSeconds)
{
    switch (Mode)
    {
        case GhostMode.InHouse:
            _houseTimer += deltaSeconds;
            if (_houseTimer < _releaseDelay)
                return;
            Move(HouseSpeed * deltaSeconds);
            if (!Maze.IsInHouse(Tile))
                SetMode(ScheduledMode());
            break;
        case GhostMode.Scatter:
        case GhostMode.Chase:
            Move(Speed * deltaSeconds);
            break;
        case GhostMode.Frightened:
            // ...
    }
}
```

It works. But look at the whole class:

- **Every method switches over the mode:** `Update`, `ChooseDirection`, `OnPowerPellet`,
  `Touch`, `Look`, and `SetMode` for what happens when a mode starts. To understand
  frightened ghosts, you read a piece of seven methods.
- **Fields that belong to one mode:** `_houseTimer` only matters in the house,
  `_frightenedTimer` only when frightened, `_enteringHouse` only when eaten. They're all
  there all the time, and nothing stops a mode from using another mode's field.
- **A new mode touches everything:** add a mode where ghosts are frozen for a moment, and
  every `switch` needs a new case. Miss one, and the compiler won't tell you.

This is the same problem as Pong's string-based game state, and it gets worse with every
mode.

## The State Pattern

_Step `Pacman2`_

> Allow an object to alter its behavior when its internal state changes. The object will
> appear to change its class.
> _(Design Patterns, Gamma et al.)_

In [Flappy Bird](../02-flappy-bird/#state-machines) we made each state of the _game_ an
object. The State pattern does the same for an _object_ in the game: each of a ghost's modes
becomes a class, and the ghost forwards everything that depends on the mode to its current
state.

```mermaid
classDiagram
    class Ghost {
        +GhostState State
        +ChangeState(state)
        +Update(deltaSeconds)
        +OnPowerPellet()
        +Touch() TouchResult
    }
    class GhostState {
        <<abstract>>
        +Enter(ghost)
        +Exit(ghost)
        +Update(ghost, deltaSeconds)*
        +ChooseDirection(ghost, options)* Point
        +OnPhaseChanged(ghost)
        +OnPowerPellet(ghost)
        +OnTouch(ghost) TouchResult
    }
    Ghost --> GhostState : current
    GhostState <|-- InHouseState
    GhostState <|-- ScatterState
    GhostState <|-- ChaseState
    GhostState <|-- FrightenedState
    GhostState <|-- EatenState
```

```csharp title="Ghost.cs"
public void ChangeState(GhostState state)
{
    State?.Exit(this);
    State = state;
    State.Enter(this);
}

public void Update(float deltaSeconds) => State.Update(this, deltaSeconds);
public void OnPowerPellet() => State.OnPowerPellet(this);
public TouchResult Touch() => State.OnTouch(this);
```

Everything about being frightened now lives in one class, including its own timer:

```csharp title="FrightenedState.cs"
public class FrightenedState : GhostState
{
    public const float Seconds = 6;
    private float _elapsed;

    // Every ghost turns around when it becomes frightened: a sign for the player.
    public override void Enter(Ghost ghost) => ghost.Reverse();

    public override void Update(Ghost ghost, float deltaSeconds)
    {
        _elapsed += deltaSeconds;
        ghost.Move(Speed * deltaSeconds);
        if (_elapsed >= Seconds)
            ghost.ChangeState(ghost.ScheduledState());
    }

    public override Point ChooseDirection(Ghost ghost, IReadOnlyList<Point> options)
        => options[ghost.World.Random.Next(options.Count)];

    public override TouchResult OnTouch(Ghost ghost)
    {
        ghost.ChangeState(new EatenState());
        return TouchResult.GhostEaten;
    }
}
```

Things to notice:

- **The states decide the transitions.** `FrightenedState` knows it ends after six seconds,
  and that being touched makes the ghost `EatenState`. `Ghost` doesn't know which states
  exist.
- **The same event, handled differently.** `World` tells every ghost about a power pellet,
  and doesn't care what each one does with it. Scatter and chase become frightened; a
  frightened ghost starts its time over; eaten ghosts and ghosts in the house ignore it (the
  base class does nothing by default).
- **`Enter` and `Exit`** give each state a place to start and clean up. Turning around when
  frightened is part of becoming frightened, so it's in `Enter`.
- **Each state is small.** The five state classes are together about as long as the enum
  version of `Ghost`, but each one can be read on its own.

Compare the diff between `Pacman1` and `Pacman2`: `World` didn't change at all. Only the
inside of `Ghost` did.

## The Strategy Pattern

_Step `Pacman3`_

Until now, all four ghosts chase the same way: straight at Pac-Man. They end up in a line
behind him, which is easy to escape. In the original game, each ghost has its own
personality, and that's all in how it picks its target while chasing:

| Ghost | Strategy | Target while chasing |
| --- | --- | --- |
| Blinky (red) | `ChasePacMan` | Pac-Man's tile |
| Pinky (pink) | `AmbushAhead` | Four tiles ahead of Pac-Man |
| Inky (cyan) | `FlankWithBlinky` | Take the tile two ahead of Pac-Man, and double the line from Blinky to it |
| Clyde (orange) | `ChaseUntilClose` | Pac-Man, until within eight tiles; then his own corner |

Together, they trap Pac-Man: Blinky follows him, Pinky cuts him off, and Inky closes in
from the other side of Blinky.

> Define a family of algorithms, encapsulate each one, and make them interchangeable.
> _(Design Patterns, Gamma et al.)_

```csharp title="ITargetStrategy.cs"
public interface ITargetStrategy
{
    Point ChooseTarget(Ghost ghost, World world);
}
```

```csharp title="AmbushAhead.cs"
// Pinky: four tiles ahead of Pac-Man, to cut him off.
public class AmbushAhead : ITargetStrategy
{
    public Point ChooseTarget(Ghost ghost, World world)
    {
        Point facing = world.PacMan.Facing;
        return world.PacMan.Tile + new Point(facing.X * 4, facing.Y * 4);
    }
}
```

Each ghost gets its strategy when `World` creates it, and `ChaseState` asks the ghost's
strategy for the target:

```csharp title="World.cs"
Pinky = new Ghost(this, "pinky", Maze.StartOf('p'), new Point(2, -3), 0, new AmbushAhead());
```

```csharp title="ChaseState.cs"
public override Point ChooseDirection(Ghost ghost, IReadOnlyList<Point> options)
    => ghost.Closest(ghost.Targeting.ChooseTarget(ghost, ghost.World), options);
```

`ChaseState` works for every ghost, and doesn't know which strategies exist. A fifth ghost
with a new personality is one new class and one line in `World`. You'll meet the pattern
again in [Super Mario Bros](../06-super-mario-bros/#strategy-pattern-level-makers), where
interchangeable level makers build different kinds of levels.

## State vs. Strategy

Draw the class diagrams of the two patterns, and they look the same: an object holds a
reference to an interface, and forwards work to it. The difference is in **why** and
**when** the object behind the interface changes.

| | State | Strategy |
| --- | --- | --- |
| In Pac-Man | The ghost's mode | The ghost's targeting |
| Who picks it | The states themselves, as the game goes on | Whoever creates the ghost (`World`) |
| How often it changes | All the time | Never, once chosen |
| Knows the others? | Yes: a state creates the next state | No: strategies don't know each other |
| The question it answers | "What am I doing right now?" | "How do I do this?" |

The two work together here: the **state** decides _whether_ the ghost is chasing, and the
**strategy** decides _how_ it chases.

## Testing the Ghosts

_Project `Pacman.Tests`_

A targeting strategy is a small class with one method: put Pac-Man somewhere, and check
which tile the ghost aims for. Each strategy can be tested on its own, as in
[Sokoban](../04-sokoban/#unit-tests):

```csharp title="TargetingTests.cs"
[Fact]
public void Inky_doubles_the_line_from_Blinky_to_two_tiles_ahead_of_Pac_Man()
{
    _world.PacMan.Place(new Point(5, 1), Direction.Right);
    _world.Blinky.Place(new Point(3, 3), Direction.Left);

    // Two tiles ahead of Pac-Man is (7, 1). From Blinky that's (+4, -2), doubled: (11, -1).
    Assert.Equal(new Point(11, -1), TargetOf(_world.Inky));
}
```

Inky's rule is the hardest to get right by playing: you can't see his target. The test
checks it with numbers you can work out on paper.

The states are tested the same way: put a ghost in a state, make something happen, and check
the state it ends up in (`GhostStateTests`). The tests use a small maze of their own
(`TestMaze`) and a seeded `Random`, so frightened ghosts wander the same way every run.

## The Whole Game

_Step `Pacman4`_

`Pacman4` adds three lives, Pac-Man's death, and a new level when the dots are gone. The flow
of the game uses the State pattern too, as a state machine like
[Flappy Bird's](../02-flappy-bird/#state-machines):

```mermaid
stateDiagram-v2
    [*] --> Ready
    Ready --> Play : after 2 seconds
    Play --> Dying : caught
    Play --> Ready : maze cleared
    Dying --> Ready : lives left
    Dying --> GameOver : no lives left
    GameOver --> Ready : Enter
```

So there are two levels of state machine in one game: the game's states (ready, play, dying,
game over) and each ghost's states. The ghosts only get updated in `PlayState`, so while
Pac-Man is dying, the ghosts' states are simply paused.

## Exercises

Start from `Pacman4`.

1. **A new mode:** when Pac-Man eats a ghost, the game freezes for half a second in the
   original, and shows the points. Add a short `PausedState` for the eaten ghost before
   `EatenState`. Which classes did you change? Compare with adding it to `Pacman1`'s enum.
2. **A new personality:** add a fifth ghost with its own `ITargetStrategy`, e.g. one that
   targets the tile Pac-Man was at five seconds ago. Write a test for it first.
3. **Frightened in the house:** in the original, ghosts waiting in the house also turn blue
   after a power pellet (but stay in the house). Change `InHouseState` to do that. What does
   the state need to remember?
4. **Fruit:** after 70 dots, a fruit appears below the house for ten seconds. Where does
   that rule belong: in `World`, in `Maze`, or in a class of its own?
5. **Tunnel (stretch):** in the original, ghosts slow down in the tunnel. Which class should
   know that the ghost is in the tunnel, and which should know how fast to go there?

## Apply It to Your Project

- Which objects in your game have modes? Are they flags, an enum, or state objects?
- Where do you have a `switch` (or an `if` chain) over a mode in more than one method?
- Is there a behaviour that differs per object, but never changes for one object? That's a
  strategy.

## Check Yourself

<details>
<summary>What problems does the enum version of the ghost have?</summary>

Every method switches over the mode, so one mode's behaviour is spread over many methods.
Fields that belong to one mode exist in all of them, and adding a mode means finding and
changing every `switch`.

</details>

<details>
<summary>In the State pattern, who decides when to change state?</summary>

Usually the states themselves: a state knows which events end it, and which state comes
next. The object that holds the state only forwards to it, and doesn't need to know which
states exist.

</details>

<details>
<summary>What are Enter and Exit for?</summary>

Setting up and cleaning up a state, in one place, whichever state came before or comes
after. Here, `FrightenedState.Enter` turns the ghost around.

</details>

<details>
<summary>State and Strategy have the same structure. How do they differ?</summary>

A state changes during the object's life, often chosen by the states themselves. A strategy
is chosen from outside, usually once, and strategies don't know about each other.

</details>

Related exam questions: [2](../../exam/#2-state-pattern--state-stack).
