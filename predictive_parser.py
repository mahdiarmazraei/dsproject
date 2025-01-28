class TreeNode:
    """کلاس برای نمایش گره‌های درخت پارس"""

    def __init__(self, value):
        # مقدار (value) گره را تعیین می‌کند و لیستی از فرزندان (children) برای گره ایجاد می‌کند
        self.value = value
        self.children = []

    def __repr__(self, level=0):
        # نمایش گرافیکی گره و فرزندان آن با استفاده از فاصله گذاری
        ret = "  " * level + f"{self.value}\n"  # برای هر سطح فاصله ایجاد می‌کند
        for child in self.children:
            ret += child.__repr__(level + 1)  # بازگشتی برای فرزندان
        return ret


class PredictiveParser:
    def __init__(self, parse_table):
        # ذخیره جدول تجزیه و تنظیم اولیه پشته و بافر ورودی
        self.parse_table = parse_table
        self.stack = ['$', 'Start']  # پشته با نماد شروع 'Start' و نماد پایان '$'
        self.input_buffer = []  # بافر ورودی که توکن‌ها در آن قرار می‌گیرند
        self.productions = []  # ذخیره تولیدات به صورت (غیرپایانه، قاعده تولید)

    def parse(self, tokens):
        # متد برای تجزیه ورودی و استفاده از الگوریتم پارس پیش‌بینی‌کننده
        self.input_buffer = [t[0] for t in tokens] + ['$']  # بافر ورودی که با علامت پایان '$' پر می‌شود
        while self.stack:
            top = self.stack[-1]  # نماد بالای پشته
            current_input = self.input_buffer[0]  # نماد ورودی فعلی

            if top == current_input == '$':
                # اگر هر دو نماد پشته و ورودی برابر '$' باشند، تجزیه موفقیت‌آمیز است
                return True

            if top == current_input:
                # اگر نمادهای پشته و ورودی برابر باشند، آنها را از پشته و بافر ورودی حذف می‌کنیم
                self.stack.pop()
                self.input_buffer.pop(0)
            else:
                if top not in self.parse_table:
                    # اگر نماد بالای پشته در جدول تجزیه وجود نداشته باشد، خطای نحوی پرتاب می‌شود
                    raise SyntaxError(f"خطای نحوی: غیرپایانه ناشناخته {top}")

                production = self.parse_table[top].get(current_input)  # پیدا کردن تولید مربوطه
                if not production:
                    # اگر تولیدی برای نماد ورودی یافت نشد، خطای نحوی با نمادهای مورد انتظار پرتاب می‌شود
                    expected = list(self.parse_table[top].keys())
                    raise SyntaxError(f"خطای نحوی در {current_input}. انتظار می‌رفت: {expected}")

                self.stack.pop()
                if production[0] != 'ε':
                    # اگر تولید 'ε' نباشد، نمادهای تولید معکوس به پشته اضافه می‌شوند
                    for symbol in reversed(production):
                        self.stack.append(symbol)
                self.productions.append((top, production))  # تولید را ذخیره می‌کنیم
        return True


def build_parse_tree(productions, grammar):
    """ساخت درخت پارس از دنباله تولیدات"""
    if not productions:
        # اگر دنباله تولیدات خالی باشد، درختی ساخته نمی‌شود
        return None

    root = TreeNode(grammar.start)  # ریشه درخت با نماد شروع ساخته می‌شود
    stack = [root]  # پشته شامل ریشه است

    for lhs, rhs in productions:
        # برای هر جفت تولید (lhs، rhs) در دنباله تولیدات
        if not stack:
            raise ValueError("خطا در دنباله تولیدات: پشته خالی است")

        current_node = stack.pop()  # گره فعلی از پشته برداشته می‌شود

        if current_node.value != lhs:
            # اگر نماد سمت چپ تولید با مقدار گره فعلی مطابقت نداشته باشد، خطا رخ می‌دهد
            raise ValueError(f"تولید برای {lhs} با گره فعلی {current_node.value} مطابقت ندارد")

        for symbol in reversed(rhs):
            # برای هر نماد در دنباله راست تولید
            if symbol == 'ε':
                continue  # اگر نماد 'ε' باشد، هیچ کاری انجام نمی‌دهیم
            child = TreeNode(symbol)  # یک گره فرزند جدید ساخته می‌شود
            current_node.children.insert(0, child)  # فرزند در ابتدای لیست فرزندان اضافه می‌شود
            if symbol in grammar.non_terminals:
                # اگر نماد یک غیرپایانه باشد، آن را به پشته اضافه می‌کنیم
                stack.append(child)

    return root  # ریشه درخت پارس ساخته شده باز می‌گردد
