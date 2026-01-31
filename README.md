# OLED Pixel Editor

A browser-based pixel editor for 128×64 OLED displays with a Python tool that converts CSV designs into an Arduino-ready binary bitmap for the ESP8266.

## Live Demo
https://oled-pixel-editor.netlify.app/

## Workflow
1. Open `index.html` in a browser.
2. Draw your design and export as CSV.
3. Run: python python/csv_to_oled.py
4. Select the CSV file.
5. The full Arduino sketch for the ESP8266 is copied to your clipboard.
6. Paste into Arduino IDE and upload to your OLED.

## Requirements
- Python 3.8+
- `pyperclip` (`pip install pyperclip`)
- Tkinter (usually included with Python)

## Hardware
- 128×64 OLED (SSD1306)
- ESP8266

