import pyautogui
import time

print("--- PYTHON KAMERA ---")
print("1. Schieb das KI-Fenster auf den Monitor, wo es bleiben soll.")
print("2. Mach die KI bereit (sodass man Start oder Stop sieht).")
print("3. Du hast 5 Sekunden Zeit...")

time.sleep(5)

# Screenshot machen und speichern
# Das Bild wird 'screen_dump.png' heißen
img = pyautogui.screenshot()
img.save("screen_dump.png")

print("✅ FOTO GEMACHT: 'screen_dump.png'")
print("WICHTIG: Öffne dieses Bild und schneide die Buttons DORT aus.")
print("Benutze NICHT Cmd+Shift+4 für den Ausschnitt!")