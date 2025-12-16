# Comments made by AI
# Purpose:
# - Calibrate a single "trigger" pixel on your screen (picked via CTRL+U then left-click).
# - While running, continuously check that pixel's RGB color.
# - If the pixel matches (within tolerance), open TikTok in Safari and move the window to monitor 2.
# - If the pixel stops matching, close Safari (kill Safari process).
# - Quit anytime with CTRL+H.

import pyautogui
import subprocess
import time
import sys

from pynput import keyboard, mouse

# ------------------- SETTINGS -------------------
TIKTOK_URL = "https://www.tiktok.com"
BROWSER_APP = "Safari"

# X-offset where the second monitor begins (adjust to your setup)
SECOND_MONITOR_OFFSET = 2000

# How often to check the pixel (fast enough without stressing the system)
CHECK_INTERVAL = 0.25

# Color matching strictness:
# 0 = exact match, 3-8 is usually more stable due to rendering / anti-aliasing
TOLERANCE = 6
# ------------------------------------------------


def is_process_running(app_name: str) -> bool:
    """Check if a process with the exact name is currently running (macOS)."""
    res = subprocess.run(
        ["pgrep", "-x", app_name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return res.returncode == 0


def move_front_window_to_second_monitor():
    """Move the front window of the browser process to the second monitor via AppleScript."""
    cmd = (
        f'tell application "System Events" to set position of front window of process "{BROWSER_APP}" '
        f'to {{{SECOND_MONITOR_OFFSET}, 0}}'
    )
    subprocess.run(["osascript", "-e", cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def open_tiktok():
    """Open TikTok in the configured browser and try to move it to monitor 2."""
    print("\n🚀 Trigger detected -> opening TikTok")
    subprocess.run(
        ["open", "-a", BROWSER_APP, TIKTOK_URL],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(0.6)  # let the window spawn
    try:
        move_front_window_to_second_monitor()
    except Exception:
        # If window moving fails, we still keep TikTok open
        pass


def kill_safari():
    """Close the browser by killing its process."""
    print("\n🛑 Trigger gone -> closing TikTok (killing Safari)")
    subprocess.run(
        ["killall", BROWSER_APP],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def rgb_close(a, b, tol: int) -> bool:
    """Return True if two RGB tuples are within a tolerance per channel."""
    return (abs(a[0] - b[0]) <= tol and
            abs(a[1] - b[1]) <= tol and
            abs(a[2] - b[2]) <= tol)


def safe_pixel_at(x: int, y: int):
    """
    Robust pixel read:
    - First try a tiny 1x1 screenshot region at (x, y).
    - If macOS / pyautogui complains, fall back to a full screenshot and clamp coords.
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
    # Verify screen recording permission early, otherwise you will chase phantom errors
    try:
        _ = pyautogui.screenshot(region=(0, 0, 10, 10))
    except Exception as e:
        print("\n❌ Screenshot blocked.")
        print("macOS: Privacy & Security -> enable Screen Recording for Terminal/Python.")
        print("Error:", e)
        sys.exit(1)

    print("Calibration:")
    print("1) Move your mouse to the trigger point")
    print("2) Press CTRL+U (armed)")
    print("3) Left-click exactly on the point")
    print("Stop anytime: CTRL+H\n")

    # Shared state for the calibration step
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
        # Track CTRL state
        if key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            state["ctrl_down"] = True

        # CTRL+H = quit
        # (sometimes ctrl+h is reported as backspace, we support both)
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

        # CTRL+U = arm the mouse pick
        if state["ctrl_down"]:
            try:
                if hasattr(key, "char") and key.char == "u":
                    state["armed"] = True
                    print("\n🎯 Armed: now left-click the point...")
            except Exception:
                pass

    def on_release(key):
        if key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            state["ctrl_down"] = False

    # Keyboard listener for calibration hotkeys
    kb_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

    def on_click(x, y, button, pressed):
        # Once armed, a single left click captures pixel position + RGB and stops the mouse listener
        if pressed and button == mouse.Button.left and state["armed"] and not state["picked"]:
            px, py = int(x), int(y)
            rgb = safe_pixel_at(px, py)
            state["picked"] = True
            state["pick_x"] = px
            state["pick_y"] = py
            state["pick_rgb"] = rgb
            print(f"\n✅ Picked @ ({px}, {py}) Color: {rgb}")
            return False  # stop mouse listener

    # Mouse listener for the single pick click
    ms_listener = mouse.Listener(on_click=on_click)

    kb_listener.start()
    ms_listener.start()

    # Wait until we have a picked pixel or quit was requested
    while not state["picked"] and not state["quit"]:
        time.sleep(0.05)

    if state["quit"]:
        print("\nCTRL+H detected. Exiting.")
        try:
            ms_listener.stop()
        except Exception:
            pass
        try:
            kb_listener.stop()
        except Exception:
            pass
        sys.exit(0)

    # Stop calibration keyboard listener
    try:
        kb_listener.stop()
    except Exception:
        pass

    x = state["pick_x"]
    y = state["pick_y"]
    target = state["pick_rgb"]

    print("\n--- LIVE MONITOR ---")
    print(f"Position: ({x}, {y})")
    print(f"Trigger color: {target} | Tolerance: ±{TOLERANCE}")
    print("Stop: CTRL+H\n")

    # Separate non-blocking quit listener for the runtime loop
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

    # We only close Safari if we opened it due to the trigger, to avoid killing it unnecessarily
    tiktok_opened_by_us = False

    while True:
        if quit_flag["quit"]:
            print("\nCTRL+H detected. Exiting.")
            sys.exit(0)

        current = safe_pixel_at(x, y)
        match = rgb_close(current, target, TOLERANCE)

        # Trigger appears -> open TikTok once
        if match and not tiktok_opened_by_us:
            open_tiktok()
            tiktok_opened_by_us = True

        # Trigger disappears -> close Safari once
        elif (not match) and tiktok_opened_by_us:
            if is_process_running(BROWSER_APP):
                kill_safari()
            tiktok_opened_by_us = False

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
