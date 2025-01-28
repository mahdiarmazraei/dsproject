import re
from collections import deque, defaultdict

class DFATokenizer:
    def __init__(self):
        # وضعیت فعلی تجزیه را به حالت شروع تعیین می‌کند
        self.state = 'start'
        # لیستی برای ذخیره توکن‌های شناسایی‌شده
        self.tokens = []
        # توکن جاری که در حال تشکیل است
        self.current_token = ''
        # دیکشنری که نمادهای تک و چندکلمه‌ای را تعریف می‌کند
        self.symbols = {
            'single': {'(', ')', '{', '}', '[', ']', ',', ';', '+', '-', '*', '/', '='},
            'multi': {'==', '!=', '>=', '<=', '>>', '<<', '||', '&&'}
        }

    def transition(self, char):
        # در اینجا، وضعیت‌ها و نحوه انتقال بین آن‌ها برای هر کاراکتر ورودی مشخص می‌شود

        if self.state == 'start':
            # اگر کاراکتر '# ' باشد، وارد وضعیت پیش‌پردازنده می‌شویم
            if char == '#':
                self.begin_token('preprocessor')
            # اگر کاراکتر حرف باشد یا زیرخط (_) باشد، وارد وضعیت شناسه می‌شویم
            elif char.isalpha() or char == '_':
                self.begin_token('identifier')
            # اگر کاراکتر عدد باشد، وارد وضعیت عدد می‌شویم
            elif char.isdigit():
                self.begin_token('number')
            # اگر کاراکتر " باشد، وارد وضعیت رشته می‌شویم
            elif char == '"':
                self.begin_token('string')
            # اگر کاراکتر نماد تک باشد (مثل پرانتز، کاما و ...)، توکن نماد تولید می‌کنیم
            elif char in self.symbols['single']:
                self.emit_token('symbol', char)
            # اگر کاراکتر یکی از این کاراکترها باشد، احتمالاً نماد چندکلمه‌ای داریم
            elif char in ['<', '>', '!', '|', '&']:
                self.begin_token('potential_multi')
            # اگر کاراکتر فاصله باشد، هیچ عملی انجام نمی‌دهیم
            elif char.isspace():
                pass
            else:
                raise ValueError(f'Invalid character: {char}')  # اگر کاراکتر معتبر نباشد، خطا می‌دهیم

        elif self.state == 'identifier':
            # اگر کاراکتر ورودی برای تشکیل شناسه مناسب باشد (حروف یا عدد یا زیرخط)، شناسه را می‌سازیم
            if char.isalnum() or char == '_':
                self.current_token += char
            else:
                # در غیر این صورت، چک می‌کنیم که آیا شناسه کلمه رزرو شده است یا نه
                self.check_reserved()
                # پس از اتمام شناسه، آن را پردازش می‌کنیم و وضعیت را تغییر می‌دهیم
                self.reset_and_process(char)

        elif self.state == 'number':
            # در صورتی که در حالت عدد باشیم و کاراکتر عددی باشد، عدد را ادامه می‌دهیم
            if char.isdigit():
                self.current_token += char
            else:
                # در غیر این صورت، توکن عددی را تولید می‌کنیم
                self.emit_token('number')
                # وضعیت را بازنشانی کرده و کاراکتر جدید را پردازش می‌کنیم
                self.reset_and_process(char)

        elif self.state == 'string':
            # اگر در وضعیت رشته باشیم و کاراکتر " باشد، رشته به پایان می‌رسد
            if char == '"':
                self.emit_token('string')
            else:
                # در غیر این صورت، کاراکتر را به رشته اضافه می‌کنیم
                self.current_token += char

        elif self.state == 'potential_multi':
            # اگر در وضعیت نماد چندکلمه‌ای باشیم، کاراکتر جدید را با توکن فعلی ترکیب می‌کنیم
            combined = self.current_token + char
            if combined in self.symbols['multi']:
                self.emit_token('symbol', combined)
            else:
                # اگر ترکیب به نماد چندکلمه‌ای نرسید، توکن فعلی را تولید کرده و کاراکتر جدید را پردازش می‌کنیم
                self.emit_token('symbol', self.current_token)
                self.reset_and_process(char)

        elif self.state == 'preprocessor':
            # اگر در وضعیت پیش‌پردازنده باشیم و کاراکتر < باشد، وارد وضعیت هدر می‌شویم
            if char == '<':
                self.current_token += char
                self.state = 'header_body'
            # اگر کاراکتر فاصله باشد، توکن پیش‌پردازنده تولید می‌شود
            elif char.isspace():
                self.emit_token('preprocessor')
                self.state = 'start'
            else:
                # در غیر این صورت، کاراکتر را به توکن پیش‌پردازنده اضافه می‌کنیم
                self.current_token += char

        elif self.state == 'header_body':
            # در اینجا هدر را پردازش می‌کنیم و وقتی به > برسیم، توکن هدر تولید می‌شود
            self.current_token += char
            if char == '>':
                self.emit_token('HEADER')
                self.state = 'start'

    def tokenize(self, code):
        # در این متد، کد ورودی را کاراکتر به کاراکتر پردازش کرده و توکن‌ها را برمی‌گرداند
        for char in code:
            self.transition(char)
        return self.tokens

    def begin_token(self, new_state):
        # این متد وضعیت جدیدی برای توکن جاری تعیین می‌کند
        self.state = new_state
        self.current_token = ''

    def emit_token(self, token_type, value=None):
        # این متد توکن جاری را تولید کرده و به لیست توکن‌ها اضافه می‌کند
        value = value or self.current_token
        self.tokens.append((token_type.upper(), value))
        self.reset()

    def check_reserved(self):
        # لیست کلمات رزرو شده
        reserved = {'int', 'float', 'void', 'return', 'if', 'while',
                   'cin', 'cout', 'continue', 'break', 'include',
                   'using', 'iostream', 'namespace', 'std', 'main'}
        # اگر شناسه جاری در کلمات رزرو شده باشد، توکن RESERVEDWORD تولید می‌شود
        if self.current_token in reserved:
            self.emit_token('RESERVEDWORD')
        else:
            # در غیر این صورت، به عنوان شناسه (IDENTIFIER) ثبت می‌شود
            self.emit_token('IDENTIFIER')

    def reset_and_process(self, char):
        # این متد وضعیت را بازنشانی کرده و کاراکتر جدید را پردازش می‌کند
        self.reset()
        self.transition(char)

    def reset(self):
        # وضعیت را به حالت ابتدایی (start) بازنشانی می‌کند
        self.state = 'start'
        # توکن جاری را خالی می‌کند
        self.current_token = ''
