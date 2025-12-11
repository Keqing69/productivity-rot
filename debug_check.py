import pyautogui
import time
import sys

# --- KONFIGURATION ---
IMG_START = "trigger_start.png"
IMG_STOP  = "trigger_stop.png"
CONFIDENCE = 0.8  
# ---------------------

print("--- DIAGNOSE V2 ---")
print("Ziel: Es darf IMMER nur EINS von beiden gefunden werden.")
print("Drücke STRG+C zum Beenden.\n")

while True:
    try:
        # Wir suchen...
        start_loc = pyautogui.locateOnScreen(IMG_START, confidence=CONFIDENCE, grayscale=False)
        stop_loc  = pyautogui.locateOnScreen(IMG_STOP, confidence=CONFIDENCE, grayscale=False)

        # Logik-Check
        status = ""
        
        if start_loc and stop_loc:
            # SUPER GAU: Beides gefunden
            status = "⚠️ FEHLER: Finde BEIDE Bilder gleichzeitig! Deine Screenshots sind nicht eindeutig genug."
        elif start_loc:
            status = f"✅ START erkannt (KI arbeitet) | X={start_loc.left}"
        elif stop_loc:
            status = f"🛑 STOP erkannt (KI fertig)   | X={stop_loc.left}"
        else:
            status = "👀 Suche... (Nichts gefunden)"

        # Zeile überschreiben
        sys.stdout.write(f"\r{status.ljust(80)}")
        sys.stdout.flush()
        
        time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n\nDiagnose beendet.")
        break
    except Exception as e:
        # Hier geben wir den 'rohen' Fehler aus, damit wir sehen was los ist
        print(f"\nCRITICAL ERROR: {repr(e)}")
        time.sleep(1)