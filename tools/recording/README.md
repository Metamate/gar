# Recording the game images

The animated images at the top of the session pages and on the decks' Today's Goal slides
are recorded from the finished games in gar-games.

- `record.ps1` starts a game, plays a timed script of key presses and mouse moves, and
  captures its window at a steady rate (Windows, PowerShell 7).
- `makegif.py` turns the frames into a GIF, with an optional crop and a pause on the last
  frame. `makegif-small.py` makes a lighter one for busy scenes (fewer frames and colours).
- `record-games.ps1` has the recipes for Snake, Sokoban, Pac-Man, Angry Birds, Plants vs.
  Zombies, Pokemon, Geometry Wars and Vampire Survivors. Build the games first, then run, for example:

  ```
  pwsh tools/recording/record-games.ps1 -Games birds,pvz
  ```

  The GIFs land in `tools/recording/out/` (not in git). Look through the frames before using
  one: a death or a menu can end up in the capture. Then copy the GIF over the one in
  `src/assets/sessionNN/`, and replace the picture on the deck's Today's Goal slide.

Snake is played by `snake_bot.py`, which reads the screen each frame and steers towards the
bat, because the snake moves too fast for a fixed script. Pong, Flappy Bird, Super Mario
Bros and Zelda were recorded by hand. The site converts the GIFs to animated WebP, which is usually much smaller.
