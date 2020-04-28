# Py-Snake

> A python implementation of the video game classic Snake via Python's Pygame library

## Overview

This is a recreation in Python of Snake in which the player assumes the role of a snake
whose sole objective is to consume randomly placed food blocks. Each consumed food block
increases the snake's size by 1 block. A [demo](#demo) of a simple AI implementation is shown below.

## How to Play

### As a Human Player

- start the game:

```{bash}
python -m game
```

- Use the `Up`, `Down`, `Left`, `Right` arrow-keys to control the snake

### As an AI Player

- start the game:

```{bash}
python -m game --ai_player
```

## Demo

The visual below is the `AIPlayer` traversing the board using Dijkstra's Algorithm
to navigate via the shortest path.

![demo]

While the bot does well navigating early on, it will eventually encounter scenarios
like those shown below. The red `X` marks the previous food location. After travellign to
and consuming the food at the red `X`, the snake had (unknowingly) blocked off the other
half of the board and failed to solve for a new path to the next food block.

![ai_flaw]

[demo]: demo.gif "Game Demo"
[ai_flaw]: ai-flaw.png "AI Flaw"
