from collections import defaultdict
class TokenTable:
    def __init__(self):
        self.order = ['STRING', 'NUMBER', 'SYMBOL', 'IDENTIFIER', 'RESERVEDWORD']
        self.tokens = defaultdict(list)

    def add_token(self, token_type, value):
        self.tokens[token_type].append(value)

    def _hash(self, value):
        return sum(ord(c) for c in value) % 1000

    def generate_table(self):
        sorted_table = []
        for token_type in self.order:
            if token_type in self.tokens:
                sorted_values = sorted(set(self.tokens[token_type]), key=lambda x: (x, [ord(c) for c in x]))
                for val in sorted_values:
                    sorted_table.append((token_type, val, self._hash(val)))
        return sorted_table