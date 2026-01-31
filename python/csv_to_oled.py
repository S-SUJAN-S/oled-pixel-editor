import csv
import tkinter as tk
from tkinter import filedialog
import pyperclip

WIDTH = 128
HEIGHT = 64

ARDUINO_TEMPLATE = """#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define SCREEN_ADDRESS 0x3C

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

{bitmap}

void setup() {{
  Wire.begin(D2, D1); // SDA, SCL
  if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {{
    while (1);
  }}
  display.clearDisplay();
  display.drawBitmap(0, 0, myBitmap, 128, 64, 1);
  display.display();
}}

void loop() {{
}}
"""

def pick_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

def load_csv(path):
    pixels = []
    with open(path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            clean = []
            for x in row:
                try:
                    v = float(x.strip())
                    clean.append(1 if v > 0.5 else 0)
                except:
                    pass
            if clean:
                pixels.append(clean)
    return pixels

def convert_to_binary_bitmap(pixels):
    out = []
    out.append("const unsigned char myBitmap[] PROGMEM = {\n")

    for page in range(HEIGHT // 8):
        for x in range(WIDTH):
            byte = 0
            for bit in range(8):
                y = page * 8 + bit
                if pixels[y][x]:
                    byte |= (1 << bit)
            out.append(f"0b{byte:08b}, ")
        out.append("\n")

    out.append("};\n")
    return "".join(out)

def main():
    path = pick_file()
    if not path:
        print("No file selected")
        return

    pixels = load_csv(path)

    if len(pixels) != HEIGHT or len(pixels[0]) != WIDTH:
        print("ERROR: CSV must be 64 rows x 128 columns")
        return

    bitmap = convert_to_binary_bitmap(pixels)
    full_code = ARDUINO_TEMPLATE.format(bitmap=bitmap)

    pyperclip.copy(full_code)
    print("FULL Arduino sketch (BINARY FORMAT) copied to clipboard")

if __name__ == "__main__":
    main()
