import pyautogui
import time

print("--- COLOR PICKER ---")
print("Bewege die Maus über den BLAUEN SENDEN-PFEIL.")
print("Drücke STRG+C, wenn du den Wert hast.")
print("-----------------------------------------")

try:
    while True:
        # Wo ist die Maus?
        x, y = pyautogui.position()
        
        # Welche Farbe hat der Pixel da?
        # (Auf Mac Retina Displays muss man manchmal tricksen, aber pyautogui regelt das meistens)
        try:
            r, g, b = pyautogui.pixel(x, y)
            print(f"X={x}, Y={y} | RGB=({r}, {g}, {b})     ", end="\r")
        except Exception:
            pass
            
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nAbbruch.")