from lexical_analyzer import DFATokenizer
from token_table import TokenTable
from grammar import CPPGrammar
from predictive_parser import PredictiveParser, build_parse_tree

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

    # مرحله ۳: ساخت Parse Table
    grammar = CPPGrammar()
    parse_table = grammar.parse_table
    print("\nParse Table:")
    for nt in grammar.non_terminals:
        print(f"{nt}: {dict(parse_table[nt])}")

    # مرحله ۴: تجزیه نحوی
    parser = PredictiveParser(parse_table)
    # try:
    success = parser.parse(tokens)
    if success:
        print("\nParse Tree Productions:")
        for prod in parser.productions:
            print(f"{prod[0]} -> {' '.join(prod[1])}")

        # ساخت درخت پارس
        parse_tree = build_parse_tree(parser.productions, grammar)

        print("\nParse Tree Structure:")
        print(parse_tree)

    # except SyntaxError as e:
    #     print(f"Parse Error: {e}")