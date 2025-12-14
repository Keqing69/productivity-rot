import pyautogui
import subprocess
import time
import sys

from pynput import keyboard, mouse

# ------------------- SETTINGS -------------------
TIKTOK_URL = "https://www.tiktok.com"
BROWSER_APP = "Safari"
SECOND_MONITOR_OFFSET = 2000
CHECK_INTERVAL = 0.25  # schnell genug, ohne zu stressen

# Wie exakt? 0 = knallhart, 3-8 ist in der Praxis stabiler wegen Rendering/AA.
TOLERANCE = 6
# ------------------------------------------------


def is_process_running(app_name: str) -> bool:
    res = subprocess.run(
        ["pgrep", "-x", app_name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return res.returncode == 0


def move_front_window_to_second_monitor():
    cmd = (
        f'tell application "System Events" to set position of front window of process "{BROWSER_APP}" '
        f'to {{{SECOND_MONITOR_OFFSET}, 0}}'
    )
    subprocess.run(["osascript", "-e", cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def open_tiktok():
    print("\n🚀 Trigger da -> TikTok auf")
    subprocess.run(["open", "-a", BROWSER_APP, TIKTOK_URL],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(0.6)
    try:
        move_front_window_to_second_monitor()
    except Exception:
        pass


def kill_safari():
    print("\n🛑 Trigger weg -> TikTok zu (Safari kill)")
    subprocess.run(["killall", BROWSER_APP],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def rgb_close(a, b, tol: int) -> bool:
    return (abs(a[0] - b[0]) <= tol and
            abs(a[1] - b[1]) <= tol and
            abs(a[2] - b[2]) <= tol)


def safe_pixel_at(x: int, y: int):
    """
    Robust: Erst 1x1 Region, falls macOS/pyautogui meckert, fallback auf Full-Screenshot.
    """
    try:
        img = pyautogui.screenshot(region=(x, y, 1, 1))
        return img.getpixel((0, 0))[:3]
    except Exception:
        full = pyautogui.screenshot()
        w, h = full.size
        x2 = min(max(0, x), w - 1)
        y2 = min(max(0, y), h - 1)
        return full.getpixel((x2, y2))[:3]


def main():
    # Screen-Recording Rechte testen, sonst jagst du Phantom-Fehler
    try:
        _ = pyautogui.screenshot(region=(0, 0, 10, 10))
    except Exception as e:
        print("\n❌ Screenshot blockiert.")
        print("macOS: Datenschutz & Sicherheit -> Bildschirmaufnahme für Terminal/Python aktivieren.")
        print("Fehler:", e)
        sys.exit(1)

    print("Kalibrierung:")
    print("1) Maus auf den Trigger-Punkt bewegen")
    print("2) STRG+U drücken (armed)")
    print("3) Linksklick auf genau den Punkt")
    print("Stop jederzeit: STRG+H\n")

    state = {
        "ctrl_down": False,
        "armed": False,
        "quit": False,
        "picked": False,
        "pick_x": None,
        "pick_y": None,
        "pick_rgb": None,
    }

    def on_press(key):
        # CTRL tracken
        if key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            state["ctrl_down"] = True

        # STRG+H = quit
        # (manchmal kommt ctrl+h als backspace, wir nehmen beides)
        if state["ctrl_down"]:
            try:
                if hasattr(key, "char") and key.char == "h":
                    state["quit"] = True
                    return False
            except Exception:
                pass

        if key == keyboard.Key.backspace and state["ctrl_down"]:
            state["quit"] = True
            return False

        # STRG+U = armed
        if state["ctrl_down"]:
            try:
                if hasattr(key, "char") and key.char == "u":
                    state["armed"] = True
                    print("\n🎯 Armed: jetzt Linksklick auf den Punkt...")
            except Exception:
                pass

    def on_release(key):
        if key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            state["ctrl_down"] = False

    kb_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

    def on_click(x, y, button, pressed):
        if pressed and button == mouse.Button.left and state["armed"] and not state["picked"]:
            px, py = int(x), int(y)
            rgb = safe_pixel_at(px, py)
            state["picked"] = True
            state["pick_x"] = px
            state["pick_y"] = py
            state["pick_rgb"] = rgb
            print(f"\n✅ Picked @ ({px}, {py}) Farbe: {rgb}")
            return False  # stop mouse listener

    ms_listener = mouse.Listener(on_click=on_click)

    kb_listener.start()
    ms_listener.start()

    # Warten bis picked oder quit
    while not state["picked"] and not state["quit"]:
        time.sleep(0.05)

    if state["quit"]:
        print("\nSTRG+H erkannt. Ende.")
        try:
            ms_listener.stop()
        except Exception:
            pass
        try:
            kb_listener.stop()
        except Exception:
            pass
        sys.exit(0)

    # Listener stoppen
    try:
        kb_listener.stop()
    except Exception:
        pass

    x = state["pick_x"]
    y = state["pick_y"]
    target = state["pick_rgb"]

    print("\n--- LIVE MONITOR ---")
    print(f"Position: ({x}, {y})")
    print(f"Trigger-Farbe: {target} | Tolerance: ±{TOLERANCE}")
    print("Stop: STRG+H\n")

    # Runtime Quit wieder per non-blocking Keyboard (pynput) im Loop:
    quit_flag = {"quit": False, "ctrl": False}

    def loop_on_press(key):
        if key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            quit_flag["ctrl"] = True

        if quit_flag["ctrl"]:
            try:
                if hasattr(key, "char") and key.char == "h":
                    quit_flag["quit"] = True
                    return False
            except Exception:
                pass

        if key == keyboard.Key.backspace and quit_flag["ctrl"]:
            quit_flag["quit"] = True
            return False

    def loop_on_release(key):
        if key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            quit_flag["ctrl"] = False

    loop_kb = keyboard.Listener(on_press=loop_on_press, on_release=loop_on_release)
    loop_kb.start()

    tiktok_opened_by_us = False

    while True:
        if quit_flag["quit"]:
            print("\nSTRG+H erkannt. Ende.")
            sys.exit(0)

        current = safe_pixel_at(x, y)
        match = rgb_close(current, target, TOLERANCE)

        if match and not tiktok_opened_by_us:
            open_tiktok()
            tiktok_opened_by_us = True

        elif (not match) and tiktok_opened_by_us:
            # nur einmal schließen, dann Ruhe
            if is_process_running(BROWSER_APP):
                kill_safari()
            tiktok_opened_by_us = False

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
