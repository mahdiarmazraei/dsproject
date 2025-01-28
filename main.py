from lexical_analyzer import DFATokenizer
from token_table import TokenTable
from grammar import CPPGrammar

if __name__ == "__main__":
    # مثال ورودی
    code = """
    #include <iostream>
    using namespace std;
    int main(){
        int x;
        int s=0, t=10;
        while (t >= 0){
            cin >> x;
            t = t - 1;
            s = s + x;
        }
        cout << "sum=" << s;
        return 0;
    }
    """

    # مرحله ۱: توکنایز کردن
    tokenizer = DFATokenizer()
    tokens = tokenizer.tokenize(code)
    print("Generated Tokens:")
    for token in tokens:
        print(token)

    # مرحله ۲: ساخت Token Table
    token_table = TokenTable()
    for ttype, value in tokens:
        token_table.add_token(ttype, value)

    print("\nToken Table:")
    table = token_table.generate_table()
    print("{:<10} {:<15} {:<10}".format("Type", "Value", "Hash"))
    for entry in table:
        print("{:<10} {:<15} {:<10}".format(entry[0], entry[1], entry[2]))

