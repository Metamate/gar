# Recording the game images

The animated images at the top of the session pages and on the decks' Today's Goal slides
are recorded from the finished games in gar-games.

Every game is played by a bot. Build the games first, then run, for example:

```
pwsh tools/recording/record-games.ps1 -Games pong,zelda
```

The bot plays the finished game and captures its window ten times a second into
`tools/recording/out/frames-<game>` (not in git). A run isn't the same twice, so the last step
is by hand: look through the frames, pick a stretch that reads well, and make the GIF from it
with `makegif.py` (or `makegif-small.py` for busy scenes, with fewer colours). The recipes in
`record-games.ps1` show the stretch and the settings used last time. Then copy the GIF over
the one in `src/assets/sessionNN/`, and replace the picture on the deck's Today's Goal slide.
The home page's stills in `src/assets/home/` are single frames from the same recordings.

The bots share `botlib.py` (start a game, press its keys, move its mouse, capture its window)
and `winshot.py` (the capture: the game's own pixels only, never the rest of the screen). Most
of them read the picture to decide what to do:

| Bot | How it plays |
| --- | --- |
| `pong_bot.py` | Both paddles move to where the ball will cross their line, sometimes late |
| `flappy_bot.py` | Finds every pipe's gap, and checks each flap by flying on in its head |
| `snake_bot.py` | Steers to the food, and keeps out of pockets smaller than the snake |
| `sokoban_bot.py` | Solves the levels from their text files with a breadth-first search |
| `pacman_bot.py` | Walks to the cheapest dot, where steps near a ghost cost more |
| `mario_bot.py` | Reads the ground's height, and jumps at pits, steps, slimes and boxes |
| `zelda_bot.py` | Lines up with the nearest monster, swings, then takes the switch and the door |
| `birds_bot.py` | Works out the pull for each shot from the slingshot's numbers |
| `pvz_bot.py` | Places chests, picks up the gold, and puts an archer in each goblin's row |
| `pokemon_bot.py` | A timed walk into the tall grass, with Enter pressed all along |
| `gw_bot.py` | Moves away from what comes close, and aims at the nearest enemy |
| `survivors_bot.py` | Walks where the swarm is thinnest, and takes the first upgrade |

`record.ps1` is the older tool, which plays a timed script of keys and mouse moves.
`longest_play.py` picks the longest stretch without a death (Flappy Bird, Mario).

`makegif.py` scales with nearest neighbour, which keeps pixel art sharp: each recipe's width
turns one art pixel into a whole number of GIF pixels. The site converts the GIFs to animated
WebP losslessly (see `image` in `astro.config.mjs`); lossy WebP blurs pixel art and adds block
artefacts. After changing that setting, delete `node_modules/.astro/assets`, or the build
reuses the old images.

Geometry Wars is the exception: its glow doesn't survive a GIF palette. `makewebp.py` makes a
full-colour, lossy WebP for the site, which serves it as it is from
`public/animations/geometry-wars.webp`; the deck gets a 256-colour GIF.
