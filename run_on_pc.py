# run_on_pc.py

import pygame
from calculator_logic import CalculatorLogic
from virtual_keypad import VirtualKeypad

# --- Impostazioni dell'emulatore ---
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 520
BG_COLOR = (20, 20, 30)
RECT_COLOR = (200, 200, 200)
TEXT_COLOR = (255, 255, 255)
CURSOR_BLINK_RATE_MS = 500

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Emulatore Calcolatrice Scientifica")
    
    try:
        font_display = pygame.font.SysFont("DejaVu Sans", 28)
        font_small = pygame.font.SysFont("DejaVuSans", 14)
        print("Font 'DejaVu Sans' caricato.")
    except Exception as e:
        print(f"Attenzione: Font 'DejaVu Sans' non trovato ({e}).")
        font_display = pygame.font.SysFont(None, 36)
        font_small = pygame.font.SysFont(None, 20)
    
    calculator = CalculatorLogic()
    keypad = VirtualKeypad(position=(15, 100), key_size=(58, 40)) 
    clock = pygame.time.Clock()

    # Logica Cursore Intelligente
    editing_mode = False

    running = True
    while running:
        key_pressed = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: running = False
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER: key_pressed = "="
                elif event.key == pygame.K_BACKSPACE: key_pressed = "backspace"
                elif event.key == pygame.K_DELETE: key_pressed = "ac"
                elif event.key == pygame.K_LEFT: key_pressed = "left"
                elif event.key == pygame.K_RIGHT: key_pressed = "right"
                else: key_pressed = event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                key_pressed = keypad.handle_click(event.pos)

        if key_pressed:
            # Attiva la modalità editing solo con tasti di modifica
            if key_pressed in ('left', 'right', 'backspace'):
                editing_mode = True
            # Disattiva la modalità editing dopo un calcolo o un reset
            elif key_pressed in ('=', 'ac'):
                editing_mode = False

            calculator.handle_key(key_pressed)

        # --- Sezione Disegno ---
        screen.fill(BG_COLOR)
        display_rect = pygame.Rect(10, 10, SCREEN_WIDTH - 20, 60)
        pygame.draw.rect(screen, (0,0,0), display_rect)
        pygame.draw.rect(screen, RECT_COLOR, display_rect, 2)

        mode_surf = font_small.render(calculator.angle_mode.upper(), True, RECT_COLOR)
        screen.blit(mode_surf, (15, 15))

        if calculator.is_approximate:
            approx_surf = font_small.render("≈", True, RECT_COLOR)
            screen.blit(approx_surf, (15, 40))

        text_surface = font_display.render(calculator.display_string, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(midright=(SCREEN_WIDTH - 15, display_rect.centery + 5))
        screen.blit(text_surface, text_rect)
        
        show_blink = (pygame.time.get_ticks() // CURSOR_BLINK_RATE_MS) % 2 == 1
        if editing_mode and show_blink and not calculator.in_error_state:
            try:
                text_after_cursor = "".join(calculator.display_list[calculator.cursor_pos:])
                width_after_cursor = font_display.size(text_after_cursor)[0]
                cursor_x = text_rect.right - width_after_cursor
                cursor_rect = pygame.Rect(cursor_x, text_rect.top, 2, text_rect.height)
                pygame.draw.rect(screen, TEXT_COLOR, cursor_rect)
            except Exception as e:
                print(f"Errore rendering cursore: {e}")

        keypad.draw(screen)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    main()