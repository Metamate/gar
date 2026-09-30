# Recording the game images

The animated images at the top of the session pages and on the decks' Today's Goal slides
are recorded from the finished games in gar-games.

- `record.ps1` starts a game, plays a timed script of key presses and mouse moves, and
  captures its window at a steady rate (Windows, PowerShell 7).
- `makegif.py` turns the frames into a GIF, with an optional crop and a pause on the last
  frame. `makegif-small.py` makes a lighter one for busy scenes (fewer frames and colours).
- `record-games.ps1` has the recipes for Flappy Bird, Snake, Sokoban, Pac-Man, Super Mario Bros, Zelda, Angry
  Birds, Plants vs. Zombies, Pokemon, Geometry Wars and Vampire Survivors. Build the games first, then run, for example:

  ```
  pwsh tools/recording/record-games.ps1 -Games birds,pvz
  ```

  The GIFs land in `tools/recording/out/` (not in git). Look through the frames before using
  one: a death or a menu can end up in the capture. Then copy the GIF over the one in
  `src/assets/sessionNN/`, and replace the picture on the deck's Today's Goal slide.

Snake and Flappy Bird are played by bots, `snake_bot.py` and `flappy_bot.py`, which read the
game's window each frame (`winshot.py`, the game's own pixels only) and steer or flap, because
both games move too fast for a fixed script. Pong was recorded by hand. For Super Mario Bros,
`longest_play.py` picks the longest stretch without a death from a half-minute run.

`makegif.py` scales with nearest neighbour, which keeps pixel art sharp: each recipe's width
turns one art pixel into a whole number of GIF pixels. The site converts the GIFs to animated
WebP losslessly (see `image` in `astro.config.mjs`); lossy WebP blurs pixel art and adds block
artefacts. After changing that setting, delete `node_modules/.astro/assets`, or the build
reuses the old images.

Geometry Wars is the exception: its glow doesn't survive a GIF palette. `makewebp.py` makes a
full-colour, lossy WebP for the site, which serves it as it is from
`public/animations/geometry-wars.webp`; the deck gets a 256-colour GIF.
