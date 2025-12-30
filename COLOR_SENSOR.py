# Librerías
import subprocess
import time
import re
import serial

import pygetwindow as gw
import pyautogui
import pytesseract
from PIL import Image


# Configuración serial
ser = serial.Serial(
    port='COM9',
    baudrate=9600,
    timeout=1
)


time.sleep(2)
print("Conectado al Arduino")


# Abrir SCRCPY
subprocess.Popen(
    r"C:\Users\jrobe\Downloads\scrcpy-win64-v3.3.3\scrcpy-win64-v3.3.3\scrcpy.exe"
)

time.sleep(3)

windows = gw.getWindowsWithTitle("M2003J15SC")

if not windows:
    print("No se encontró la ventana del teléfono")
    exit()

w = windows[0]
w.moveTo(1044, 0)
w.resizeTo(1365 - 1044, 719)


# OCR CONFIG
zona = (1156, 630, 93, 18)

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

regex_rgb = re.compile(
    r"^\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*$"
)

# Lectura RGB
def leer_rgb():
    img = pyautogui.screenshot(region=zona)
    img = img.resize((img.width * 4, img.height * 4), Image.LANCZOS)

    texto = pytesseract.image_to_string(
        img, config="--psm 7"
    ).strip()

    match = regex_rgb.match(texto)
    if not match:
        return None

    R, G, B = map(int, match.groups())

    # Formateo de datos
    if not (0 <= R <= 255 and 0 <= G <= 255 and 0 <= B <= 255):
        return None

    return R, G, B

def calcular_ir(R, G, B):
    total = R + G + B
    if total == 0:
        return 0.0
    return R / total

ultimo_ir = 0.0

# Main
while True:
    if ser.in_waiting:
        linea = ser.readline().decode(errors="ignore").strip()

        if linea == "REQ_IR":
            rgb = leer_rgb()

            if rgb:
                R, G, B = rgb
                ir = calcular_ir(R, G, B)

                if ir is not None:
                    ultimo_ir = ir

            # Envío de datos
            mensaje = f"IR,{ultimo_ir:.3f}\n"
            ser.write(mensaje.encode())
            print("Python envió:", mensaje.strip())

    time.sleep(0.05)