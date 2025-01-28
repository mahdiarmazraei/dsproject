import re
from collections import deque, defaultdict

# ------------------ بخش ۱: پیاده سازی Lexical Analyzer با DFA ------------------
class DFATokenizer:
    def __init__(self):
        self.state = 'start'
        self.tokens = []
        self.current_token = ''
        self.symbols = {
            'single': {'(', ')', '{', '}', '[', ']', ',', ';', '+', '-', '*', '/', '='},
            'multi': {'==', '!=', '>=', '<=', '>>', '<<', '||', '&&'}
        }