import time
from luma.core.interface.serial import spi
from luma.lcd.device import ili9341
from luma.core.render import canvas
from PIL import ImageDraw, ImageFont

from calculator_logic import CalculatorLogic

# --- Funzione Helper per leggere un singolo tasto ---
def getkey():
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    # AGGIUNGI QUESTE DUE RIGHE
    if ord(ch) == 127: # Questo è il codice ASCII per il tasto Backspace/Canc
        return "backspace"
    
    if ord(ch) == 13: return '='
    return ch

def main():
    # --- Configurazione Hardware ---
    serial = spi(port=0, device=0, gpio_DC=22, gpio_RST=27)
    device = ili9341(serial, rotate=2) # rotate=2 per 180 gradi
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
    except IOError:
        font = ImageFont.load_default()

    calculator = CalculatorLogic()
    
    print("Avvio Calcolatrice. 'q' per uscire.")
    running = True
    while running:
        # Disegno con Luma
        with canvas(device) as draw:
            draw.rectangle((10, 10, device.width - 10, 60), outline="white", fill="black")
            text_width, text_height = draw.textsize(calculator.display_value, font=font)
            draw.text(
                (device.width - text_width - 15, 15),
                calculator.display_value,
                fill="white",
                font=font
            )
        
        key = getkey()
        if key.lower() == 'q':
            running = False
        else:
            calculator.handle_key(key)

    print("Applicazione terminata.")

if __name__ == "__main__":
    main()