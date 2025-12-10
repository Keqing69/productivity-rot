import pyautogui
import subprocess
import time
import sys

# --- KONFIGURATION ---
TRIGGER_IMAGE = "trigger.png"     # Dein Screenshot vom Stop-Button
CONFIDENCE = 0.8                  # 0.8 = Toleranz für Bildvergleich
CHECK_INTERVAL = 0.5              # Check alle 0.5 Sekunden
TIKTOK_URL = "https://www.tiktok.com"
BROWSER_APP = "Safari"            # Wir zielen auf Safari
# ---------------------

def is_safari_running():
    try:
        # Pgrep prüft, ob der Safari-Prozess läuft
        subprocess.check_output(["pgrep", "-x", BROWSER_APP])
        return True
    except subprocess.CalledProcessError:
        return False

def open_tiktok():
    # Wir öffnen Safari nur, wenn es nicht eh schon offen ist (um Spam zu vermeiden)
    if not is_safari_running():
        print(f"🧠 KI arbeitet -> 🚀 Starte Safari mit TikTok")
        subprocess.run(["open", "-a", BROWSER_APP, TIKTOK_URL])

def kill_safari():
    # Gnadenloser Kill Command
    if is_safari_running():
        print(f"✅ KI fertig -> 💀 Kille Safari")
        subprocess.run(["pkill", "-x", BROWSER_APP])

def start_rot():
    print(f"--- PROJECT PRODUCTIVITY ROT (SAFARI EDITION) ---")
    print(f"Suche nach Stop-Button in '{TRIGGER_IMAGE}'...")
    print("Drücke STRG+C zum Beenden.")

    was_working = False

    while True:
        try:
            # Suche das Stop-Symbol auf dem Screen
            # confidence=0.8 braucht 'opencv-python' library
            location = pyautogui.locateOnScreen(TRIGGER_IMAGE, confidence=CONFIDENCE, grayscale=True)

            if location:
                # KI ARBEITET (Symbol gefunden)
                if not was_working:
                    open_tiktok()
                    was_working = True
            else:
                # KI FERTIG (Symbol weg)
                if was_working:
                    kill_safari()
                    was_working = False

            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            print("\n👋 Ende.")
            sys.exit()
        except Exception as e:
            # Fehler ignorieren (z.B. wenn Bild kurz nicht gefunden wird)
            pass

if __name__ == "__main__":
    start_rot()