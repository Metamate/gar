param(
  [string]$Exe,
  [string[]]$Events = @(),        # "seconds action arg...": "1.5 down right", "3 up right", "2 tap enter",
                                  # "4 mdown 120 500", "4.5 mmove 60 540", "5 mup", "6 click 300 400" (client pixels)
  [double]$Start = 2,             # seconds after launch when capturing starts
  [double]$Duration = 5,          # seconds of capture
  [int]$IntervalMs = 80,
  [string]$OutDir
)
# Plays a timed script of key and mouse events on a game while capturing its window at a steady rate.
Add-Type @"
using System;
using System.Runtime.InteropServices;
public static class R {
  [DllImport("user32.dll")] public static extern void keybd_event(byte vk, byte scan, uint flags, UIntPtr extra);
  [DllImport("user32.dll")] public static extern void mouse_event(uint flags, int dx, int dy, uint data, UIntPtr extra);
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr hdc, uint flags);
  [DllImport("user32.dll")] public static extern bool GetClientRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool ClientToScreen(IntPtr h, ref POINT p);
  public struct RECT { public int L, T, R, B; }
  public struct POINT { public int X, Y; }
}
"@
Add-Type -AssemblyName System.Drawing
$codes = @{ enter = @(0x0D, 0x1C, 0); space = @(0x20, 0x39, 0); right = @(0x27, 0x4D, 1); left = @(0x25, 0x4B, 1);
  up = @(0x26, 0x48, 1); down = @(0x28, 0x50, 1); w = @(0x57, 0x11, 0); a = @(0x41, 0x1E, 0); s = @(0x53, 0x1F, 0);
  d = @(0x44, 0x20, 0); z = @(0x5A, 0x2C, 0); y = @(0x59, 0x15, 0); r = @(0x52, 0x13, 0); f = @(0x46, 0x21, 0); f3 = @(0x72, 0x3D, 0); f1 = @(0x70, 0x3B, 0);
  d1 = @(0x31, 0x02, 0); d2 = @(0x32, 0x03, 0); d3 = @(0x33, 0x04, 0); d4 = @(0x34, 0x05, 0); d5 = @(0x35, 0x06, 0); d6 = @(0x36, 0x07, 0) }
New-Item -ItemType Directory -Force $OutDir | Out-Null
Get-ChildItem $OutDir -Filter *.png | Remove-Item
$p = Start-Process -FilePath $Exe -WorkingDirectory (Split-Path $Exe) -PassThru
Start-Sleep -Milliseconds 2500
$p.Refresh()
$h = $p.MainWindowHandle
[R]::keybd_event(0x12, 0x38, 0, [UIntPtr]::Zero); [R]::keybd_event(0x12, 0x38, 2, [UIntPtr]::Zero)
[R]::SetForegroundWindow($h) | Out-Null
Start-Sleep -Milliseconds 300

function Key($name, $up) { $c = $codes[$name]; $f = [uint32]$c[2]; if ($up) { $f = $f -bor 2 }; [R]::keybd_event([byte]$c[0], [byte]$c[1], $f, [UIntPtr]::Zero) }
function Cursor($x, $y) { $pt = New-Object R+POINT; $pt.X = [int]$x; $pt.Y = [int]$y; [R]::ClientToScreen($h, [ref]$pt) | Out-Null; [R]::SetCursorPos($pt.X, $pt.Y) | Out-Null }
function Grab($file) {
  $rc = New-Object R+RECT; [R]::GetClientRect($h, [ref]$rc) | Out-Null
  $bmp = New-Object System.Drawing.Bitmap ([Math]::Max(1, $rc.R)), ([Math]::Max(1, $rc.B))
  $g = [System.Drawing.Graphics]::FromImage($bmp); $hdc = $g.GetHdc()
  [R]::PrintWindow($h, $hdc, 3) | Out-Null
  $g.ReleaseHdc($hdc); $bmp.Save($file); $g.Dispose(); $bmp.Dispose()
}

$queue = [System.Collections.Generic.List[object]]::new()
foreach ($e in $Events) { $parts = $e.Split(' '); $queue.Add(@{ t = [double]$parts[0]; a = $parts[1]; args = $parts[2..($parts.Length - 1)] }) }
$sorted = $queue | Sort-Object { $_.t }
$clock = [Diagnostics.Stopwatch]::StartNew()
$i = 0; $frame = 0; $nextShot = $Start
while ($clock.Elapsed.TotalSeconds -lt $Start + $Duration) {
  $now = $clock.Elapsed.TotalSeconds
  while ($i -lt $sorted.Count -and $sorted[$i].t -le $now) {
    $ev = $sorted[$i]; $i++
    switch ($ev.a) {
      'down' { Key $ev.args[0] $false }
      'up' { Key $ev.args[0] $true }
      'tap' { Key $ev.args[0] $false; Start-Sleep -Milliseconds 60; Key $ev.args[0] $true }
      'mdown' { Cursor $ev.args[0] $ev.args[1]; [R]::mouse_event(0x02, 0, 0, 0, [UIntPtr]::Zero) }
      'mmove' { Cursor $ev.args[0] $ev.args[1] }
      'mup' { [R]::mouse_event(0x04, 0, 0, 0, [UIntPtr]::Zero) }
      'click' { Cursor $ev.args[0] $ev.args[1]; [R]::mouse_event(0x02, 0, 0, 0, [UIntPtr]::Zero); Start-Sleep -Milliseconds 50; [R]::mouse_event(0x04, 0, 0, 0, [UIntPtr]::Zero) }
    }
  }
  if ($now -ge $nextShot) {
    Grab (Join-Path $OutDir ('f{0:D3}.png' -f $frame)); $frame++
    $nextShot = $Start + $frame * $IntervalMs / 1000.0
  }
  Start-Sleep -Milliseconds 5
}
foreach ($name in $codes.Keys) { Key $name $true }
if (-not $p.HasExited) { Stop-Process $p -Force; "captured $frame frames" } else { "EXITED early, $frame frames" }
