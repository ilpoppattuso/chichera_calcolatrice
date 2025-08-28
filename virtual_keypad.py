# virtual_keypad.py
import pygame

class VirtualKeypad:
    def __init__(self, position, key_size=(50, 40)):
        self.pos = position
        self.key_size = key_size
        self.font = pygame.font.SysFont("DejaVuSans", 20)
        self.buttons = []

        # CORREZIONE: Layout della tastiera corretto e riorganizzato.
        # Aggiunto il tasto '÷' e rimosso il doppio 'Ans'.
        key_layout = [
            [('AC', 'ac'), ('←', 'left'), ('→', 'right'), ('DEL', 'backspace'), ('DRG', 'drg')],
            [('F↔D', 'f_d'), ('sin', 'sin'), ('cos', 'cos'), ('tan', 'tan'), ('xʸ', '^')],
            [('x²', 'sqr'), ('√', 'sqrt'), ('x⁻¹', 'inv'), ('n!', 'fact'), ('log₁₀', 'log10')],
            [('ln', 'ln'), ('eˣ', 'exp'), ('logₐb', 'log_base'), ('(', '('), (')', ')')],
            [('π', 'pi'), ('7', '7'), ('8', '8'), ('9', '9'), ('÷', '/')],
            [('e', 'e'), ('4', '4'), ('5', '5'), ('6', '6'), ('×', '*')],
            [('Ans', 'ans'), ('1', '1'), ('2', '2'), ('3', '3'), ('-', '-')],
            [('0', '0'), ('.', '.'), (',', ','), ('+', '+'), ('=', '=')]
        ]
        
        self._create_buttons(key_layout)

    def _create_buttons(self, layout):
        start_x, start_y = self.pos
        key_w, key_h = self.key_size
        margin = 5
        for row_idx, row in enumerate(layout):
            for col_idx, key_data in enumerate(row):
                label, key_id = key_data
                x = start_x + col_idx * (key_w + margin)
                y = start_y + row_idx * (key_h + margin)
                rect = pygame.Rect(x, y, key_w, key_h)
                self.buttons.append({'rect': rect, 'label': label, 'id': key_id})

    def draw(self, surface):
        for btn in self.buttons:
            pygame.draw.rect(surface, (80, 80, 80), btn['rect'])
            pygame.draw.rect(surface, (120, 120, 120), btn['rect'], 2)
            
            text_surf = self.font.render(btn['label'], True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=btn['rect'].center)
            surface.blit(text_surf, text_rect)

    def handle_click(self, pos):
        for btn in self.buttons:
            if btn['rect'].collidepoint(pos):
                return btn['id']
        return None