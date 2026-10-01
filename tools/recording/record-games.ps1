param([string[]]$Games = @('pong', 'flappy', 'snake', 'sokoban', 'pacman', 'mario', 'zelda', 'birds', 'pvz', 'pokemon', 'gw', 'vs'))
# Records the animated game images for the session pages and the decks' Today's Goal slides.
# Build the finished steps in gar-games first (Debug). Each game is played by a bot, which
# captures the game's window ten times a second into tools/recording/out/frames-<game>.
#
# A run isn't the same twice, so the GIF is made by hand afterwards: look through the frames,
# pick a stretch that reads well, and give it to makegif.py. The lines at the bottom of each
# recipe show the stretch and the settings used last time. Then copy the GIF over the one in
# src/assets/sessionNN/, and replace the picture on the deck's Today's Goal slide.
# Each GIF's width turns one art pixel into a whole number of GIF pixels, so it stays sharp.

$here = $PSScriptRoot
$out = Join-Path $here 'out'
New-Item -ItemType Directory -Force $out | Out-Null
function Bot($script, $name, $seconds) { python (Join-Path $here $script) (Join-Path $out "frames-$name") $seconds }

# Two players who follow the ball, and sometimes get there late.
#   makegif.py out/pong.gif 640 100 none out/frames-pong/f{110..249}.png
if ($Games -contains 'pong') { Bot 'pong_bot.py' 'pong' 26 }

# longest_play.py lists the frames of the longest flight; the GIF is twelve seconds of it.
#   makegif.py out/flappy-bird.gif 640 100 none (the frames longest_play.py prints, 60 to 180)
if ($Games -contains 'flappy') { Bot 'flappy_bot.py' 'flappy' 45 }

# The snake goes for the food, and keeps out of pockets it can't get out of.
#   makegif.py out/snake.gif 640 100 none out/frames-snake/f{040..189}.png
if ($Games -contains 'snake') {
  python (Join-Path $here 'snake_bot.py') (Join-Path $here '..\..\..\gar-games\03-snake\Snake9\bin\Debug\net10.0\Snake9.exe') (Join-Path $out 'frames-snake') 22 100
}

# Solves the first three levels, with an undo and a redo. The crop leaves out the empty sides.
#   makegif.py out/sokoban.gif 640 100 320,96,960,636 10 out/frames-sokoban/f{000..158}.png
if ($Games -contains 'sokoban') { python (Join-Path $here 'sokoban_bot.py') (Join-Path $out 'frames-sokoban') }

# Eats dots and keeps away from the ghosts. It still loses lives: pick a stretch between two.
#   makegif.py out/pac-man.gif 640 100 none out/frames-pacman/f{212..345}.png
if ($Games -contains 'pacman') { Bot 'pacman_bot.py' 'pacman' 40 }

# Runs through the level and back. longest_play.py lists the longest run without a fall.
# The game is 426 wide at 3x, with a one-pixel bar on each side: the crop drops the bars, and
# 852 is two GIF pixels to an art pixel.
#   makegif.py out/super-mario-bros.gif 852 100 1,0,1279,720 (the first 120 frames longest_play.py prints)
if ($Games -contains 'mario') { Bot 'mario_bot.py' 'mario' 70 }

# Fights, steps on the switch, and walks on to the next room.
#   makegif.py out/the-legend-of-zelda.gif 640 100 none out/frames-zelda/f{000..125}.png
if ($Games -contains 'zelda') { Bot 'zelda_bot.py' 'zelda' 50 }

# Three aimed shots at the first hut.
#   makegif.py out/angry-birds.gif 640 100 none 8 out/frames-birds/f{002..140}.png
if ($Games -contains 'birds') { python (Join-Path $here 'birds_bot.py') (Join-Path $out 'frames-birds') }

# Eighty seconds of play: the last fourteen have the most on the lawn.
#   makegif.py out/plants-vs-zombies.gif 640 100 none out/frames-pvz/f{660..799}.png
if ($Games -contains 'pvz') { Bot 'pvz_bot.py' 'pvz' 80 }

# From the town into the grass, and the first battle.
#   makegif.py out/pokemon.gif 640 100 none out/frames-pokemon/f{040..189}.png
if ($Games -contains 'pokemon') { Bot 'pokemon_bot.py' 'pokemon' 70 }

# The glow is lost in a GIF's palette, so the site gets a lossy WebP
# (public/animations/geometry-wars.webp), and the deck a GIF with a full palette.
#   makewebp.py out/geometry-wars.webp 960 100 70 out/frames-gw/f{205..259}.png
#   makegif-small.py out/geometry-wars.gif 640 100 1 256 smooth out/frames-gw/f{205..259}.png
if ($Games -contains 'gw') { Bot 'gw_bot.py' 'gw' 40 }

# A level-up menu dims the screen: pick a stretch without one.
#   makegif-small.py out/vampire-survivors.gif 640 100 1 64 out/frames-vs/f{313..385}.png
if ($Games -contains 'vs') { Bot 'survivors_bot.py' 'vs' 45 }
