import re
from collections import deque, defaultdict

class DFATokenizer:
    def __init__(self):
        self.state = 'start'
        self.tokens = []
        self.current_token = ''
        self.symbols = {
            'single': {'(', ')', '{', '}', '[', ']', ',', ';', '+', '-', '*', '/', '='},
            'multi': {'==', '!=', '>=', '<=', '>>', '<<', '||', '&&'}
        }

    def transition(self, char):
        if self.state == 'start':
            if char == '#':
                self.begin_token('preprocessor')
            elif char.isalpha() or char == '_':
                self.begin_token('identifier')
            elif char.isdigit():
                self.begin_token('number')
            elif char == '"':
                self.begin_token('string')
            elif char in self.symbols['single']:
                self.emit_token('symbol', char)
            elif char in ['<', '>', '!', '|', '&']:
                self.begin_token('potential_multi')
            elif char.isspace():
                pass
            else:
                raise ValueError(f'Invalid character: {char}')

        elif self.state == 'identifier':
            if char.isalnum() or char == '_':
                self.current_token += char
            else:
                self.check_reserved()
                self.reset_and_process(char)

        elif self.state == 'number':
            if char.isdigit():
                self.current_token += char
            else:
                self.emit_token('number')
                self.reset_and_process(char)

        elif self.state == 'string':
            if char == '"':
                self.emit_token('string')
            else:
                self.current_token += char

        elif self.state == 'potential_multi':
            combined = self.current_token + char
            if combined in self.symbols['multi']:
                self.emit_token('symbol', combined)
            else:
                self.emit_token('symbol', self.current_token)
                self.reset_and_process(char)

        elif self.state == 'preprocessor':
            if char == '>':
                self.emit_token('symbol', '>')
            elif char == '<':
                self.emit_token('symbol', '<')
            elif char.isspace():
                self.check_reserved()
                self.state = 'start'

    def tokenize(self, code):
        for char in code:
            self.transition(char)
        return self.tokens

    def begin_token(self, new_state):
        self.state = new_state
        self.current_token = ''

    def emit_token(self, token_type, value=None):
        value = value or self.current_token
        self.tokens.append((token_type.upper(), value))
        self.reset()

    def check_reserved(self):
        reserved = {'int', 'float', 'void', 'return', 'if', 'while',
                   'cin', 'cout', 'continue', 'break', 'include',
                   'using', 'iostream', 'namespace', 'std', 'main'}
        if self.current_token in reserved:
            self.emit_token('RESERVEDWORD')
        elif self.state == 'preprocessor':
            self.emit_token('HEADER')

    def reset_and_process(self, char):
        self.reset()
        self.transition(char)

    def reset(self):
        self.state = 'start'
        self.current_token = ''