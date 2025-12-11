import pyautogui
import time
import sys

print("--- ZONEN KALIBRIERUNG ---")
print("Wir definieren jetzt den Bereich, in dem Python suchen soll.")
print("Das ist meistens das Eingabefeld unten, wo der Senden/Stop Button ist.")
print("------------------------------------------------")

try:
    input("1. Bewege die Maus zur Linken Oberen Ecke des Eingabefeldes und drücke ENTER...")
    x1, y1 = pyautogui.position()
    print(f"   -> Punkt 1 gespeichert: {x1}, {y1}")

    input("2. Bewege die Maus zur Rechten Unteren Ecke des Eingabefeldes und drücke ENTER...")
    x2, y2 = pyautogui.position()
    print(f"   -> Punkt 2 gespeichert: {x2}, {y2}")

    # Breite und Höhe berechnen
    width = x2 - x1
    height = y2 - y1

    print("\n------------------------------------------------")
    print("✅ PERFEKT! Hier ist dein Code für die main.py:")
    print("------------------------------------------------")
    print(f"SEARCH_REGION = ({x1}, {y1}, {width}, {height})")
    print("------------------------------------------------")
    print("Kopiere die Zeile oben und ersetze sie in deiner main.py!")

except KeyboardInterrupt:
    print("\nAbbruch.")