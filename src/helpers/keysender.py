import time
from threading import RLock
from pynput.keyboard import Key,Controller as KeyboardController
import win32gui, win32con


class KeySender:
    def __init__(self, window_name=None):
        self._kill_pill = False
        self._lines = []
        self._lock = RLock()
        self._window = window_name
        self._kc = KeyboardController()

    def type(self, line):
        with self._lock:
            self._lines.append(line)

    def shortcut(self):
        with self._lock:
            with self._kc.pressed(Key.ctrl_r):
                with self._kc.pressed(Key.shift_r):
                    self._kc.press(Key.f10)
                    self._kc.release(Key.f10)

    def destroy(self):
        self._kill_pill = True

    def main_loop(self):
        while not self._kill_pill:
            if len(self._lines):
                hwnd = win32gui.FindWindow(None, self._window)
                line = self._lines.pop()
                try:
                    if hwnd:
                        win32gui.SetForegroundWindow(hwnd)
                    else:
                        print("Could not find game Window.")
                        continue
                except:
                    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    win32gui.SetForegroundWindow(hwnd)
                    print("Fixed window.")
                with self._lock:
                    self._kc.type(line)
            time.sleep(0.1)
