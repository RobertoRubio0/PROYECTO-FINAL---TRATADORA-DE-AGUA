import pyautogui
import time

print("Mueve el mouse. Presiona Ctrl+C para salir.\n")

while True:
    x, y = pyautogui.position()
    print(f"Coordenadas: ({x}, {y})")
    time.sleep(0.1)
