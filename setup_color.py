import pyautogui
import time

print("--- PIXEL JÄGER ---")
print("1. Sorge dafür, dass der BLAUE STOP-BUTTON (KI arbeitet) sichtbar ist.")
print("2. Bewege die Maus genau auf die blaueste Stelle des Buttons.")
print("3. Warte 5 Sekunden...")
print("-------------------")

time.sleep(5)

x, y = pyautogui.position()
try:
    # Versucht Farbe zu holen (klappt auf Mac manchmal nur via Screenshot-Trick)
    # Wir nutzen hier den Screenshot-Trick intern, um sicherzugehen
    color = pyautogui.screenshot().getpixel((x, y))
    
    print("\n✅ TREFFER!")
    print(f"CHECK_X = {x}")
    print(f"CHECK_Y = {y}")
    print(f"TARGET_COLOR = {color}")
    print("\nKopiere diese 3 Zeilen in die main.py!")
except Exception as e:
    print(f"Fehler: {e}")