from collections import defaultdict

class TokenTable:
    def __init__(self):
        # ترتیب اولویت توکن‌ها که برای ایجاد جدول از آن استفاده می‌شود
        self.order = ['STRING', 'NUMBER', 'SYMBOL', 'IDENTIFIER', 'RESERVEDWORD']
        # استفاده از defaultdict برای ذخیره لیستی از مقادیر مرتبط با هر نوع توکن
        self.tokens = defaultdict(list)

    def add_token(self, token_type, value):
        # این متد برای اضافه کردن توکن‌ها به لیست مربوط به نوع توکن استفاده می‌شود
        # نوع توکن (token_type) و مقدار آن (value) را دریافت کرده و به لیست آن نوع اضافه می‌کند
        self.tokens[token_type].append(value)

    def _hash(self, value):
        # این متد یک هش ساده برای یک مقدار (مثلاً شناسه یا رشته) ایجاد می‌کند
        # با استفاده از کدهای ASCII کاراکترها و محاسبه مجموع آنها
        return sum(ord(c) for c in value) % 1000  # هش به‌طور تصادفی در بازه [0, 1000] تولید می‌شود

    def generate_table(self):
        # این متد جدول توکن‌ها را به صورت مرتب تولید می‌کند
        sorted_table = []
        # برای هر نوع توکن در ترتیب مشخص شده، توکن‌ها را مرتب می‌کند
        for token_type in self.order:
            if token_type in self.tokens:
                # ابتدا توکن‌ها را از لیست استخراج کرده و از تکرار جلوگیری می‌کنیم (set)
                # سپس بر اساس مقادیرشان به صورت الفبایی مرتب می‌کنیم
                sorted_values = sorted(set(self.tokens[token_type]), key=lambda x: (x, [ord(c) for c in x]))
                # برای هر مقدار مرتب‌شده، هش مربوطه را محاسبه کرده و به جدول اضافه می‌کنیم
                for val in sorted_values:
                    sorted_table.append((token_type, val, self._hash(val)))
        return sorted_table  # جدول مرتب‌شده توکن‌ها را برمی‌گرداند
