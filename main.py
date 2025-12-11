import pyautogui
import subprocess
import time
import sys

# --- DEINE GEMESSENEN WERTE ---
CHECK_X = 1258
CHECK_Y = 899

# Deine "Stop"-Farbe (KI arbeitet)
# Wir nutzen exakt deine Werte
TARGET_COLOR = (30, 31, 32) 

# Da 30 und 19 sehr nah beieinander liegen, darf die Toleranz fast Null sein.
# Wir erlauben maximal 2 Punkte Abweichung.
TOLERANCE = 2
# ------------------------------

# Settings
TIKTOK_URL = "https://www.tiktok.com"
BROWSER_APP = "Safari"
SECOND_MONITOR_OFFSET = 2000 
CHECK_INTERVAL = 0.5

def open_tiktok():
    try:
        subprocess.check_output(["pgrep", "-x", BROWSER_APP])
    except:
        print(f"\n🚀 TARGET ERKANNT ({TARGET_COLOR}) -> TikTok auf")
        subprocess.run(["open", "-a", BROWSER_APP, TIKTOK_URL])
        time.sleep(0.5)
        try:
            cmd = f'tell application "System Events" to set position of front window of process "{BROWSER_APP}" to {{{SECOND_MONITOR_OFFSET}, 0}}'
            subprocess.run(["osascript", "-e", cmd])
        except:
            pass

def kill_safari():
    try:
        subprocess.check_output(["pgrep", "-x", BROWSER_APP])
        print(f"\n🛑 FARBE WEG -> TikTok zu")
        subprocess.run(["killall", BROWSER_APP])
    except:
        pass

def start_rot():
    print(f"--- EXACT COORDINATE MODE ---")
    print(f"Überwache: {CHECK_X}, {CHECK_Y}")
    print(f"Suche Farbe: {TARGET_COLOR}")
    print("-----------------------------")

    while True:
        try:
            # Wir prüfen exakt deine Werte
            matches = pyautogui.pixelMatchesColor(CHECK_X, CHECK_Y, TARGET_COLOR, tolerance=TOLERANCE)

            if matches:
                # Treffer!
                sys.stdout.write(f"\r[🧠 WORKING] Farbe stimmt exakt.   ")
                sys.stdout.flush()
                open_tiktok()
            else:
                # Kein Treffer
                sys.stdout.write(f"\r[✅ IDLE] Farbe ist anders.       ")
                sys.stdout.flush()
                kill_safari()

            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            print("\nBye.")
            sys.exit()
        except Exception:
            pass

if __name__ == "__main__":
    start_rot()