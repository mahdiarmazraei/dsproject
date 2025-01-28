from collections import defaultdict


class CPPGrammar:
    def __init__(self):
        # تعریف تولیدات (Production Rules) برای دستور زبان
        # هر نماد غیر پایانی (Non-terminal) به تولیدات خود (کدام نمادها می‌توانند به آن تبدیل شوند) اشاره دارد
        self.productions = {
            'Start': [['S', 'N', 'M']],  # Start -> S N M
            'S': [['#include', 'HEADER'], ['ε']],  # S -> #include HEADER | ε (ε به معنای تولید تهی است)
            'N': [['using', 'namespace', 'std', ';'], ['ε']],  # N -> using namespace std ; | ε
            'M': [['int', 'main', '(', ')', '{', 'T', 'V', '}']],  # M -> int main ( ) { T V }
            'T': [  # T -> Id T | L T | Loop T | Input T | Output T | ε
                ['Id', 'T'], ['L', 'T'], ['Loop', 'T'],
                ['Input', 'T'], ['Output', 'T'], ['ε']
            ],
            'V': [['return', '0', ';'], ['ε']],  # V -> return 0 ; | ε
            'Id': [['int', 'L'], ['float', 'L']],  # Id -> int L | float L
            'L': [['IDENTIFIER', 'Assign', 'Z']],  # L -> IDENTIFIER Assign Z
            'Z': [[',', 'IDENTIFIER', 'Assign', 'Z'], [';']],  # Z -> , IDENTIFIER Assign Z | ;
            'Assign': [['=', 'Operation'], ['ε']],  # Assign -> = Operation | ε
            'Operation': [['NUMBER', 'P'], ['IDENTIFIER', 'P']],  # Operation -> NUMBER P | IDENTIFIER P
            'P': [['O', 'W', 'P'], ['ε']],  # P -> O W P | ε
            'O': [['+'], ['-'], ['*']],  # O -> + | - | *
            'W': [['NUMBER'], ['IDENTIFIER']],  # W -> NUMBER | IDENTIFIER
            'Loop': [['while', '(', 'Expression', ')', '{', 'T', '}']],  # Loop -> while ( Expression ) { T }
            'Expression': [['Operation', 'K', 'Operation']],  # Expression -> Operation K Operation
            'K': [['=='], ['>='], ['<='], ['!=']],  # K -> == | >= | <= | !=
            'Input': [['cin', '>>', 'IDENTIFIER', 'F', ';']],  # Input -> cin >> IDENTIFIER F ;
            'F': [['>>', 'IDENTIFIER', 'F'], ['ε']],  # F -> >> IDENTIFIER F | ε
            'Output': [['cout', '<<', 'C', 'H', ';']],  # Output -> cout << C H ;
            'H': [['<<', 'C', 'H'], ['ε']],  # H -> << C H | ε
            'C': [['STRING'], ['IDENTIFIER'], ['NUMBER']]  # C -> STRING | IDENTIFIER | NUMBER
        }

        # نماد شروع (Start Symbol)
        self.start = 'Start'

        # تعریف نمادهای پایانی (Terminals) که می‌توانند در تولیدات ظاهر شوند
        # این مجموعه شامل تمامی واژگان اصلی زبان است که نمی‌توانند بیشتر تجزیه شوند
        self.terminals = {
            '#include', 'int', 'float', 'void', 'return', 'if', 'while',
            'cin', 'cout', 'continue', 'break', 'include', 'using',
            'iostream', 'namespace', 'std', 'main', 'IDENTIFIER', 'NUMBER',
            '(', ')', '{', '}', '[', ']', ',', ';', '+', '-', '*', '/',
            '==', '!=', '>=', '<=', '=', '>>', '<<', 'STRING', '0', 'HEADER', 'ε'
        }

        # تعریف نمادهای غیر پایانی (Non-terminals) که در تولیدات ظاهر می‌شوند
        # این نمادها باید به تولیدات دیگر خود تبدیل شوند
        self.non_terminals = set(self.productions.keys())

        # دیکشنری برای ذخیره مجموعه‌های FIRST و FOLLOW برای هر نماد غیر پایانی
        self.first = {}  # مجموعه‌های FIRST برای هر نماد غیر پایانی
        self.follow = {}  # مجموعه‌های FOLLOW برای هر نماد غیر پایانی

        # جدول تجزیه (Parse Table) که برای تجزیه ورودی استفاده خواهد شد
        self.parse_table = defaultdict(dict)

        # محاسبه مجموعه‌های FIRST و FOLLOW
        self.compute_first()
        self.compute_follow()

        # ساخت جدول تجزیه با استفاده از مجموعه‌های FIRST و FOLLOW
        self.build_parse_table()

    def compute_first(self):
        # محاسبه مجموعه FIRST برای هر نماد غیر پایانی
        # مجموعه FIRST نشان‌دهنده نمادهایی است که می‌توانند در ابتدای یک دنباله از نمادهای غیر پایانی ظاهر شوند
        for nt in self.non_terminals:
            self.first[nt] = set()  # برای هر نماد غیر پایانی، مجموعه FIRST آن را خالی می‌کنیم

        updated = True
        while updated:
            updated = False
            for nt in self.non_terminals:
                for prod in self.productions[nt]:
                    # اولین نماد در تولید (Production) را می‌گیریم
                    first_symbol = prod[0]
                    if first_symbol in self.terminals:
                        # اگر اولین نماد یک نماد پایانی باشد، آن را به مجموعه FIRST اضافه می‌کنیم
                        if first_symbol not in self.first[nt]:
                            self.first[nt].add(first_symbol)
                            updated = True
                    else:
                        # اگر اولین نماد یک نماد غیر پایانی باشد، مجموعه FIRST آن را می‌گیریم
                        prev_len = len(self.first[nt])
                        # مجموعه FIRST نماد غیر پایانی را با مجموعه FIRST نماد اول تولید به‌روزرسانی می‌کنیم
                        self.first[nt].update(self.first[first_symbol] - {'ε'})
                        if len(self.first[nt]) > prev_len:
                            updated = True
                        # اگر 'ε' در مجموعه FIRST نماد اول وجود داشته باشد، ادامه تولیدات بررسی می‌شود
                        if 'ε' in self.first[first_symbol]:
                            for sym in prod[1:]:
                                if sym in self.terminals:
                                    # اگر نماد بعدی پایانی باشد، به مجموعه FIRST اضافه می‌شود
                                    if sym not in self.first[nt]:
                                        self.first[nt].add(sym)
                                        updated = True
                                    break
                                else:
                                    # اگر نماد بعدی غیر پایانی باشد، مجموعه FIRST آن را اضافه می‌کنیم
                                    prev_len = len(self.first[nt])
                                    self.first[nt].update(self.first[sym] - {'ε'})
                                    if len(self.first[nt]) > prev_len:
                                        updated = True
                                    if 'ε' not in self.first[sym]:
                                        break
                            else:
                                # اگر تمامی نمادها 'ε' بودند، 'ε' را به مجموعه FIRST اضافه می‌کنیم
                                if 'ε' not in self.first[nt]:
                                    self.first[nt].add('ε')
                                    updated = True

    def compute_follow(self):
        # محاسبه مجموعه FOLLOW برای هر نماد غیر پایانی
        # مجموعه FOLLOW نشان‌دهنده نمادهایی است که می‌توانند در انتهای یک دنباله از نمادهای غیر پایانی قرار گیرند
        for nt in self.non_terminals:
            self.follow[nt] = set()  # برای هر نماد غیر پایانی، مجموعه FOLLOW آن را خالی می‌کنیم
        self.follow[self.start].add('$')  # نماد شروع باید '$' را در مجموعه FOLLOW خود داشته باشد

        updated = True
        while updated:
            updated = False
            for nt in self.non_terminals:
                for prod in self.productions[nt]:
                    for i, sym in enumerate(prod):
                        if sym in self.non_terminals:
                            # اگر نماد فعلی یک نماد غیر پایانی باشد، باید دنباله‌های بعدی آن را بررسی کنیم
                            next_syms = prod[i + 1:]
                            first_next = self.get_first_of_sequence(next_syms)  # FIRST دنباله بعدی را می‌گیریم
                            prev_len = len(self.follow[sym])
                            # مجموعه FOLLOW نماد را با FIRST دنباله بعدی به‌روزرسانی می‌کنیم
                            self.follow[sym].update(first_next - {'ε'})
                            if len(self.follow[sym]) > prev_len:
                                updated = True
                            # اگر 'ε' در FIRST دنباله بعدی باشد یا دنباله بعدی تهی باشد، باید FOLLOW نماد غیر پایانی اصلی را هم اضافه کنیم
                            if 'ε' in first_next or len(next_syms) == 0:
                                prev_len = len(self.follow[sym])
                                self.follow[sym].update(self.follow[nt])
                                if len(self.follow[sym]) > prev_len:
                                    updated = True

    def get_first_of_sequence(self, seq):
        # محاسبه مجموعه FIRST برای یک دنباله از نمادها
        # این متد به‌طور خاص برای گرفتن FIRST دنباله‌های دیگر استفاده می‌شود
        first = set()
        for sym in seq:
            if sym in self.terminals:
                first.add(sym)
                break  # اگر نماد پایانی باشد، از اینجا می‌رویم
            else:
                first.update(self.first[sym] - {'ε'})  # مجموعه FIRST نمادهای غیر پایانی را اضافه می‌کنیم
                if 'ε' not in self.first[sym]:
                    break  # اگر 'ε' نباشد، از همین‌جا تمام می‌شود
        else:
            first.add('ε')  # اگر تمام نمادها 'ε' باشند، آن را اضافه می‌کنیم
        return first

    def build_parse_table(self):
        # ساخت جدول تجزیه با استفاده از مجموعه‌های FIRST و FOLLOW
        # این جدول برای تعیین کدام تولید برای نمادهای خاص در زمان تجزیه استفاده می‌شود
        for nt in self.non_terminals:
            for prod in self.productions[nt]:
                first_alpha = self.get_first_of_sequence(prod)  # مجموعه FIRST برای هر تولید
                for term in first_alpha - {'ε'}:
                    # برای هر نماد از FIRST که 'ε' نباشد، آن را به جدول تجزیه اضافه می‌کنیم
                    self.parse_table[nt][term] = prod
                if 'ε' in first_alpha:
                    for term in self.follow[nt]:
                        # اگر 'ε' در FIRST باشد، FOLLOW را هم بررسی کرده و به جدول اضافه می‌کنیم
                        self.parse_table[nt][term] = prod
                if 'ε' in first_alpha and '$' in self.follow[nt]:
                    # اگر 'ε' و '$' در FOLLOW باشد، به جدول برای علامت پایان ('$', '$') هم اضافه می‌کنیم
                    self.parse_table[nt]['$'] = prod
