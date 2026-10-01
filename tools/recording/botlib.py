"""What the game-playing bots share: starting a game, pressing its keys, moving its mouse, and
capturing its window at a steady rate while a bot plays.

A bot is a function that gets the latest capture of the window and the seconds played, and
presses keys. run() calls it as often as it can, and saves a frame every interval."""
import ctypes, os, subprocess, time
from ctypes import wintypes
from winshot import grab, window_of

user32 = ctypes.windll.user32
GAMES = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'gar-games'))

# virtual key, scan code, extended
KEYS = {'enter': (0x0D, 0x1C, 0), 'space': (0x20, 0x39, 0), 'left': (0x25, 0x4B, 1), 'up': (0x26, 0x48, 1),
        'right': (0x27, 0x4D, 1), 'down': (0x28, 0x50, 1), 'esc': (0x1B, 0x01, 0), 'f1': (0x70, 0x3B, 0), 'f3': (0x72, 0x3D, 0)}
for i, ch in enumerate('1234567890'):
    KEYS[ch] = (0x30 + (i + 1) % 10, 0x02 + i, 0)


def _key(name):
    if name in KEYS:
        return KEYS[name]
    vk = ord(name.upper())
    return vk, user32.MapVirtualKeyW(vk, 0), 0


class Game:
    def __init__(self, folder, step, wait=2.5):
        d = os.path.join(GAMES, folder, step, 'bin', 'Debug', 'net10.0')
        self.proc = subprocess.Popen([os.path.join(d, step + '.exe')], cwd=d)
        self.hwnd = None
        for _ in range(60):
            time.sleep(0.2)
            self.hwnd = window_of(self.proc.pid)
            if self.hwnd:
                break
        time.sleep(wait)
        user32.keybd_event(0x12, 0x38, 0, 0)        # Windows only hands over the focus after a key press
        user32.keybd_event(0x12, 0x38, 2, 0)
        user32.SetForegroundWindow(self.hwnd)
        time.sleep(0.4)
        self._held = set()
        self._cursor = wintypes.POINT()
        user32.GetCursorPos(ctypes.byref(self._cursor))

    # keys
    def down(self, name):
        if name not in self._held:
            vk, scan, ext = _key(name)
            user32.keybd_event(vk, scan, ext, 0)
            self._held.add(name)

    def up(self, name):
        if name in self._held:
            vk, scan, ext = _key(name)
            user32.keybd_event(vk, scan, ext | 2, 0)
            self._held.discard(name)

    def hold(self, *names):
        """Hold exactly these keys of the ones this bot has pressed."""
        for name in list(self._held):
            if name not in names:
                self.up(name)
        for name in names:
            self.down(name)

    def tap(self, name, seconds=0.03):
        vk, scan, ext = _key(name)
        user32.keybd_event(vk, scan, ext, 0)
        time.sleep(seconds)
        user32.keybd_event(vk, scan, ext | 2, 0)

    # mouse, in the window's own pixels
    def move(self, x, y):
        pt = wintypes.POINT(int(x), int(y))
        user32.ClientToScreen(self.hwnd, ctypes.byref(pt))
        user32.SetCursorPos(pt.x, pt.y)

    def mouse_down(self):
        user32.mouse_event(2, 0, 0, 0, 0)

    def mouse_up(self):
        user32.mouse_event(4, 0, 0, 0, 0)

    def click(self, x, y):
        self.move(x, y)
        time.sleep(0.05)
        self.mouse_down()
        time.sleep(0.05)
        self.mouse_up()

    def grab(self):
        return grab(self.hwnd)

    def run(self, bot, seconds, out, interval=0.1, start=0.0):
        """Calls bot(image, seconds played) in a loop, and saves a frame every interval from start on."""
        os.makedirs(out, exist_ok=True)
        for f in os.listdir(out):
            if f.endswith('.png'):
                os.remove(os.path.join(out, f))
        t0 = time.time()
        frame, next_shot = 0, start
        while True:
            t = time.time() - t0
            if t >= seconds:
                break
            img = self.grab()
            if t >= next_shot:
                img.save(os.path.join(out, f'f{frame:03d}.png'))
                frame += 1
                next_shot += interval
            if bot(img, t) is False:
                break
            time.sleep(0.004)
        return frame

    def close(self):
        for name in list(self._held):
            self.up(name)
        self.mouse_up()
        self.proc.kill()
        user32.SetCursorPos(self._cursor.x, self._cursor.y)
