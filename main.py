from lexer import BasicLexer
from parser import BasicParser

def multi_line_input():
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)

if __name__ == '__main__':
    lexer = BasicLexer()
    parser = BasicParser(lexer)
    symbol_table = {}
    while True:
        program = multi_line_input()
        tokens = lexer.tokenize(program)
        result = parser.parse(tokens)
        result.execute(symbol_table)
