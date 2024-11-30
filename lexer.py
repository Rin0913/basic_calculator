from sly import Lexer

class BasicLexer(Lexer):
    tokens = {
        PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN,
        AND, OR, XOR, NOT,
        LT, LE, GT, GE, NE, EQ,
        IF, THEN, ELSEIF, ELSE, END,
        FOR, TO, STEP, NEXT,
        DO, WHILE, WEND,
        PRINT, INPUT, DIM, LET,
        GOTO, MARK, RETURN, REM,
        STOP,
        IDENTIFIER, NUMBER,
    }

    ignore = ' \t'
    ignore_comment = r'\#.*'

    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'

    LT      = r'<'
    LE      = r'<='
    GT      = r'>'
    GE      = r'>='
    EQ      = r'='
    NE      = r'!='

    LPAREN  = r'\('
    RPAREN  = r'\)'

    AND     = r'AND'
    OR      = r'OR'
    XOR     = r'XOR'
    NOT     = r'NOT'
    LET     = r'LET'
    ELSEIF  = r'ELSEIF'
    IF      = r'IF'
    ELSE    = r'ELSE'
    THEN    = r'THEN'
    END     = r'END'
    FOR     = r'FOR'
    TO      = r'TO'
    STEP    = r'STEP'
    NEXT    = r'NEXT'
    DO      = r'DO'
    WHILE   = r'WHILE'
    WEND    = r'WEND'
    PRINT   = r'PRINT'
    INPUT   = r'INPUT'
    DIM     = r'DIM'
    GOTO    = r'GOTO'
    MARK    = r':'
    RETURN  = r'RETURN'
    STOP    = r'STOP'
    REM     = r"(REM[^\n].*)"

    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER = r'\d+'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.line_content = {}

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def tokenize(self, code):
        for lineno, line in enumerate(code.splitlines(), start=1):
            self.line_content[lineno] = line
        return super().tokenize(code)

    def error(self, t):
        print(f"Invalid token: '{t.value[0]}' at line {self.lineno}")
        self.index += 1
