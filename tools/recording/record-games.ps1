param([string[]]$Games = @('snake', 'sokoban', 'pacman', 'birds', 'pvz', 'gw', 'vs'))
# Records the animated game images for the session pages and the decks' Today's Goal slides.
# Build the finished steps in gar-games first (Debug). Each recipe plays the game with a
# timed script of keys or mouse moves and captures frames; makegif.py turns them into a GIF.
# Output: tools/recording/out/<game>.gif. Copy it over src/assets/sessionNN/<name>.gif.

$here = $PSScriptRoot
$gamesRoot = Resolve-Path (Join-Path $here '..\..\..\gar-games')
$out = Join-Path $here 'out'
New-Item -ItemType Directory -Force $out | Out-Null
function Exe($folder, $step) { Join-Path $gamesRoot "$folder\$step\bin\Debug\net10.0\$step.exe" }
function Record($name, $exe, $start, $duration, $events) {
  & (Join-Path $here 'record.ps1') -Exe $exe -Start $start -Duration $duration -IntervalMs 100 -OutDir (Join-Path $out "frames-$name") -Events $events
}

if ($Games -contains 'snake') {
  # The snake moves five cells a second, too fast for a fixed script: snake_bot.py reads the
  # screen and steers towards the bat. It can still die now and then, so pick a stretch of
  # frames without a restart (the snake is back to three segments after one).
  python (Join-Path $here 'snake_bot.py') (Exe '03-snake' 'Snake9') (Join-Path $out 'frames-snake') 14 100
  python (Join-Path $here 'makegif.py') (Join-Path $out 'snake.gif') 640 130 none 6 (Join-Path $out 'frames-snake\f*.png')
}
if ($Games -contains 'sokoban') {
  # Solve level 1, go to level 2, push, undo, redo, and solve it.
  $ev = @('0.6 tap right', '1.0 tap right', '1.6 tap enter', '2.4 tap up', '2.9 tap z', '3.4 tap y')
  $t = 3.9
  foreach ($m in 'down', 'right', 'right', 'up', 'up', 'left', 'left', 'left', 'down', 'right', 'right', 'right', 'up', 'right', 'down') {
    $ev += ('{0:0.00} tap {1}' -f $t, $m); $t += 0.35 }
  Record 'sokoban' (Exe '04-sokoban' 'Sokoban4') 2.0 8.2 $ev
  python (Join-Path $here 'makegif.py') (Join-Path $out 'sokoban.gif') 640 100 '240,120,1040,570' 12 (Join-Path $out 'frames-sokoban\f*.png')
}
if ($Games -contains 'pacman') {
  # Pac-Man is caught after about six seconds: keep the frames before that.
  Record 'pacman' (Exe '05-pacman' 'Pacman4') 2.0 8 @('0.2 tap left', '1.5 tap left', '3.0 tap up', '4.2 tap up', '5.2 tap right', '6.2 tap up', '7.0 tap left')
  python (Join-Path $here 'makegif.py') (Join-Path $out 'pacman.gif') 448 100 none 8 (Join-Path $out 'frames-pacman\f0[0-5][0-9].png') (Join-Path $out 'frames-pacman\f060.png')
}
if ($Games -contains 'birds') {
  # Grab the bird on the slingshot at (220, 520), pull back slowly, and let go.
  $ev = @('0.6 mdown 220 520')
  for ($k = 1; $k -le 10; $k++) { $ev += ('{0:0.00} mmove {1} {2}' -f (0.6 + 0.07 * $k), (220 - 5 * $k), (520 + [math]::Round(2.8 * $k))) }
  $ev += '2.0 mup'
  Record 'birds' (Exe '07-angry-birds' 'Birds4') 0.3 6 $ev
  python (Join-Path $here 'makegif.py') (Join-Path $out 'angry-birds.gif') 640 100 none 10 (Join-Path $out 'frames-birds\f00[5-9].png') (Join-Path $out 'frames-birds\f0[1-5][0-9].png')
}
if ($Games -contains 'pvz') {
  # Plant a sunflower and a peashooter, then capture once several zombies are on the lawn.
  Record 'pvz' (Exe '09-plants-vs-zombies' 'Pvz4') 44 7 @('0.5 click 182 70', '0.9 click 310 425', '1.4 click 274 70', '1.8 click 410 425', '2.2 mmove 700 700')
  python (Join-Path $here 'makegif.py') (Join-Path $out 'plants-vs-zombies.gif') 640 100 none (Join-Path $out 'frames-pvz\f*.png')
}
if ($Games -contains 'gw') {
  # Move with WASD and fire with the arrow keys, turning every second. Busy: a smaller GIF.
  $ev = @('0.3 tap enter'); $t = 0.5
  for ($k = 0; $k -lt 16; $k++) {
    $a = @('right', 'down', 'left', 'up')[$k % 4]; $m = @('w', 'd', 's', 'a')[$k % 4]
    $ev += ('{0:0.00} down {1}' -f $t, $a); $ev += ('{0:0.00} up {1}' -f ($t + 0.95), $a)
    $ev += ('{0:0.00} down {1}' -f $t, $m); $ev += ('{0:0.00} up {1}' -f ($t + 0.6), $m); $t += 1.0 }
  Record 'gw' (Exe '11-geometry-wars' 'GeometryWars6') 8 6 $ev
  python (Join-Path $here 'makegif-small.py') (Join-Path $out 'geometry-wars.gif') 480 200 2 64 (Join-Path $out 'frames-gw\f01[0-9].png') (Join-Path $out 'frames-gw\f0[2-5][0-9].png')
}
if ($Games -contains 'vs') {
  # Walk in a square, pick upgrade 1 whenever a level-up menu opens, capture after half a minute.
  # A level-up menu can still land in the capture: check the frames and drop those.
  $ev = @(); $t = 0.5
  for ($k = 0; $k -lt 50; $k++) { $key = @('d', 's', 'a', 'w')[$k % 4]; $ev += ('{0:0.00} down {1}' -f $t, $key); $ev += ('{0:0.00} up {1}' -f ($t + 0.9), $key); $t += 1.0 }
  for ($u = 1.0; $u -lt 44; $u += 1.7) { $ev += ('{0:0.00} tap d1' -f $u) }
  Record 'vs' (Exe '12-vampire-survivors' 'Survivors4') 38 7 $ev
  python (Join-Path $here 'makegif-small.py') (Join-Path $out 'vampire-survivors.gif') 560 150 1 64 (Join-Path $out 'frames-vs\f*.png')
}
