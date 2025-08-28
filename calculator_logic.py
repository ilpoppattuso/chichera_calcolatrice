# calculator_logic.py
import math
import re
from fractions import Fraction

def sin_deg(x): return math.sin(math.radians(x))
def cos_deg(x): return math.cos(math.radians(x))
def tan_deg(x): return math.tan(math.radians(x))

class CalculatorLogic:
    def __init__(self):
        self.expression_list = []
        self.display_list = []
        self.display_string = "0"
        self.last_answer = 0
        self.last_numeric_result = 0
        self.result_display_mode = 'fraction'
        self.angle_mode = 'deg'
        self.memory = 0
        self.parenthesis_open = 0
        self.in_error_state = False
        self.is_approximate = False
        self.cursor_pos = 0

    def reset(self):
        self.expression_list = []; self.display_list = []; self.display_string = "0"
        self.parenthesis_open = 0
        self.last_numeric_result = 0; self.in_error_state = False
        self.is_approximate = False; self.cursor_pos = 0
        print("Logic Reset")

    def _update_display_string(self):
        if not self.display_list:
            self.display_string = ""
            return
        self.display_string = "".join(self.display_list)

    def _insert_item(self, logic_item, display_item):
        self.expression_list.insert(self.cursor_pos, logic_item)
        self.display_list.insert(self.cursor_pos, display_item)
        self.cursor_pos += 1

    def _format_number(self, number):
        self.is_approximate = False
        number_str = str(number)
        if 'e' in number_str:
             self.is_approximate = True
             return "{:.2e}".format(number)

        if abs(number) >= 1e8 or (abs(number) < 1e-5 and number != 0):
            self.is_approximate = True
            return "{:.2e}".format(number)

        if '.' in number_str:
            if len(number_str.replace('.', '').replace('-', '')) > 8:
                self.is_approximate = True
                return "{:.2e}".format(number)
        
        original_str = str(round(number, 8))
        if len(original_str.replace('.', '').replace('-', '')) > 10:
            self.is_approximate = True
            number = round(number, 6)

        if self.result_display_mode == 'decimal':
            return str(number)
        try:
            frac = Fraction(number).limit_denominator(10000)
            if frac.denominator == 1: return str(frac.numerator)
            formatted_frac = f"{frac.numerator}/{frac.denominator}"
            if len(formatted_frac) > 12:
                self.is_approximate = True
                return str(round(number, 6))
            return formatted_frac
        except (ValueError, OverflowError):
            return str(round(number, 10))
    
    def handle_key(self, key):
        if self.in_error_state and key != 'ac': return
        self.is_approximate = False

        if key in "0123456789.":
            if self.expression_list and self.cursor_pos > 0 and self.expression_list[self.cursor_pos-1].replace('.', '', 1).isdigit():
                if key == '.' and '.' in self.expression_list[self.cursor_pos-1]: return
                self.expression_list[self.cursor_pos-1] += key; self.display_list[self.cursor_pos-1] += key
            else:
                self._insert_item(key, key)
        
        elif key in "+-*/^":
            op_map_logic = {'^': '**'}; op_map_display = {'*': '×', '/': '÷', '^': '^'}
            self._insert_item(op_map_logic.get(key, key), op_map_display.get(key, key))
        
        elif key in ('sqr', 'inv', 'fact'):
            if self.cursor_pos > 0:
                prev_index = self.cursor_pos - 1
                logic_item = self.expression_list[prev_index]
                display_item = self.display_list[prev_index]
                if key == 'sqr': self.expression_list[prev_index] = f'({logic_item})**2'; self.display_list[prev_index] = f'({display_item})²'
                elif key == 'inv': self.expression_list[prev_index] = f'({logic_item})**-1'; self.display_list[prev_index] = f'({display_item})⁻¹'
                elif key == 'fact': self.expression_list[prev_index] = f'math.factorial({logic_item})'; self.display_list[prev_index] = f'{display_item}!'
        
        elif key in ('sqrt', 'log10', 'ln', 'exp', 'sin', 'cos', 'tan', 'log_base'):
            if key in ('sin', 'cos', 'tan'):
                logic_func = f'{key}('
            else:
                func_map_logic = {'sqrt': 'math.sqrt(', 'log10': 'math.log10(', 'ln': 'math.log(', 'exp': 'math.exp(', 'log_base': 'math.log('}
                logic_func = func_map_logic[key]
            
            display_map = {'sqrt': '√(', 'log10': 'log(', 'ln': 'ln(', 'exp': 'e(', 'sin': 'sin(', 'cos': 'cos(', 'tan': 'tan(', 'log_base': 'log('}
            self._insert_item(logic_func, display_map[key]); self.parenthesis_open += 1

        elif key == "(": self._insert_item("(", "("); self.parenthesis_open += 1
        elif key == ")":
            if self.parenthesis_open > 0: self._insert_item(")", ")"); self.parenthesis_open -= 1
        elif key == ",": self._insert_item(",", ",")
        elif key == "pi": self._insert_item(str(math.pi), 'π')
        elif key == 'e': self._insert_item(str(math.e), 'e')
        elif key == "ans": self._insert_item(str(self.last_answer), 'Ans')

        elif key == 'left': self.cursor_pos = max(0, self.cursor_pos - 1)
        elif key == 'right': self.cursor_pos = min(len(self.display_list), self.cursor_pos + 1)
        elif key == "backspace":
            if self.cursor_pos > 0:
                popped_item = self.expression_list.pop(self.cursor_pos - 1); self.display_list.pop(self.cursor_pos - 1)
                self.cursor_pos -= 1
                if popped_item.endswith('('): self.parenthesis_open -= 1
                elif popped_item == ')': self.parenthesis_open += 1
        
        elif key == "=": self.evaluate()
        elif key == "ac": self.reset()
        elif key == "f_d":
            if self.expression_list and len(self.expression_list) == 1:
                if self.result_display_mode == 'fraction': self.result_display_mode = 'decimal'
                else: self.result_display_mode = 'fraction'
                self.display_string = self._format_number(self.last_numeric_result)
                self.display_list = [self.display_string]
                return
        
        elif key == "drg":
            modes = ['deg', 'rad', 'grad']; current_index = modes.index(self.angle_mode)
            self.angle_mode = modes[(current_index + 1) % len(modes)]

        self._update_display_string()

    def evaluate(self):
        eval_string = "".join(self.expression_list) + ")" * self.parenthesis_open
        if not eval_string: return
        
        try:
            pattern = r'math\.log\(([^,]+?),([^)]+?)\)'
            eval_string = re.sub(pattern, r'math.log(\2,\1)', eval_string)
        except Exception as e:
            print(f"Errore durante la sostituzione del log: {e}")

        safe_globals = {'math': math}
        if self.angle_mode == 'deg':
            safe_globals.update({'sin': sin_deg, 'cos': cos_deg, 'tan': tan_deg})
        else:
            safe_globals.update({'sin': math.sin, 'cos': math.cos, 'tan': math.tan})

        try:
            if "/0" in eval_string.replace(".0", "") and not "/0." in eval_string: raise ZeroDivisionError
            result = eval(eval_string, safe_globals)

            # --- NUOVA CORREZIONE ---
            # Gestisce gli errori di precisione dei float. Se un risultato è 
            # estremamente vicino a zero (es. sin(pi)), lo imposta a 0.
            if abs(result) < 1e-10:
                result = 0
            # --- FINE CORREZIONE ---

            if math.isinf(result) or math.isnan(result): raise ValueError
            self.last_numeric_result = result; self.last_answer = result
            display_result = self._format_number(result)
            self.display_string = display_result; self.expression_list = [str(result)]
            self.display_list = [display_result]; self.cursor_pos = len(self.display_list)
            self.parenthesis_open = 0; self.in_error_state = False
        except ZeroDivisionError: self.display_string = "undef"; self.in_error_state = True
        except ValueError: self.display_string = "∄"; self.in_error_state = True
        except (SyntaxError, TypeError) as e: self.display_string = "Syntax ERROR"; self.in_error_state = True; print(f"Syntax/Type Error: {e} in '{eval_string}'")
        except OverflowError: self.display_string = "Overflow"; self.in_error_state = True
        except Exception as e: self.display_string = "ERROR"; self.in_error_state = True; print(f"Evaluation Error: {e}")
        
        if self.in_error_state:
            self.expression_list = []; self.display_list = []; self.parenthesis_open = 0; self.cursor_pos = 0