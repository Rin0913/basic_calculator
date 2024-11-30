from sly import Parser
from lexer import BasicLexer
import basic_ast

class BasicParser(Parser):
    tokens = BasicLexer.tokens

    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'NOT'),
        ('nonassoc', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
    )

    def __init__(self, lexer):
        super().__init__()
        self.lexer = lexer

    # Program entry
    @_('stmt_list')
    def program(self, p):
        return basic_ast.FunctionAST('main', p[0])

    # Statement list
    @_('stmt stmt_list')
    def stmt_list(self, p):
        p[1].add_statement(p[0])
        return p[1]

    @_('')
    def stmt_list(self, p):
        return basic_ast.StatementsAST()

    # Statements
    @_('REM')
    def stmt(self, p):
        return basic_ast.NoopAST()

    @_('assignment')
    def stmt(self, p):
        return p[0]

    @_('if_stmt')
    def stmt(self, p):
        return p[0]

    @_('while_stmt')
    def stmt(self, p):
        return p[0]

    @_('for_stmt')
    def stmt(self, p):
        return p[0]

    @_('expr')
    def stmt(self, p):
        return p[0]

    # For Statement

    @_('FOR IDENTIFIER EQ expr TO expr step stmt_list NEXT')
    def for_stmt(self, p):
        symbol = basic_ast.FactorAST(p[1], 'symbol')
        return basic_ast.ForAST(
                symbol,
                basic_ast.AssignmentAST(symbol, p[3]),
                p[5], p[6], p[7])

    @_('STEP expr')
    def step(self, p):
        return p[1]

    @_('')
    def step(self, p):
        return basic_ast.FactorAST(1, 'constant_int')

    # While statement
    @_('WHILE expr stmt_list WEND')
    def while_stmt(self, p):
        return basic_ast.WhileAST(p[1], p[2])

    # Assignment
    @_('LET IDENTIFIER EQ expr')
    def assignment(self, p):
        return basic_ast.AssignmentAST(
                basic_ast.FactorAST(p[1], 'symbol'),
                p[3])

    @_('IDENTIFIER EQ expr')
    def assignment(self, p):
        return basic_ast.AssignmentAST(
                basic_ast.FactorAST(p[0], 'symbol'),
                p[2])

    # If statements
    @_('IF expr THEN stmt_list else_stmts END IF')
    def if_stmt(self, p):
        return basic_ast.IfAST(p[1], p[3], p[4])

    @_('ELSEIF expr THEN stmt_list else_stmts')
    def else_stmts(self, p):
        return basic_ast.IfAST(p[1], p[3], p[4])

    @_('ELSE stmt_list')
    def else_stmts(self, p):
        return p[1]

    @_('')
    def else_stmts(self, p):
        return basic_ast.NoopAST()


    # Expression rules with comparison operators
    @_('expr LE expr')
    def expr(self, p):
        return basic_ast.OperationAST(p[0], '<=', p[2])

    @_('expr GE expr')
    def expr(self, p):
        return basic_ast.OperationAST(p[0], '>=', p[2])

    @_('expr LT expr')
    def expr(self, p):
        return basic_ast.OperationAST(p[0], '<', p[2])

    @_('expr GT expr')
    def expr(self, p):
        return basic_ast.OperationAST(p[0], '>', p[2])

    @_('expr EQ expr')
    def expr(self, p):
        return basic_ast.OperationAST(p[0], '==', p[2])

    @_('expr NE expr')
    def expr(self, p):
        return basic_ast.OperationAST(p[0], '!=', p[2])

    # Logical expressions
    @_('expr AND expr')
    def expr(self, p):
        return basic_ast.OperationAST(p[0], 'AND', p[2])

    @_('expr OR expr')
    def expr(self, p):
        return basic_ast.OperationAST(p[0], 'OR', p[2])

    @_('NOT expr')
    def expr(self, p):
        return basic_ast.OperationAST(p[1], 'XOR', 
                                      basic_ast.FactorAST(0, 'constant_int'))

    # Arithmetic expressions
    @_('term')
    def expr(self, p):
        return p[0]

    @_('expr PLUS expr')
    def expr(self, p):
        return basic_ast.OperationAST(p[0], '+', p[2])

    @_('expr MINUS expr')
    def expr(self, p):
        return basic_ast.OperationAST(p[0], '-', p[2])

    @_('term TIMES expr')
    def term(self, p):
        return basic_ast.OperationAST(p[0], '*', p[2])

    @_('term DIVIDE expr')
    def term(self, p):
        return basic_ast.OperationAST(p[0], '/', p[2])

    # Basic definitions
    @_('factor')
    def term(self, p):
        return p[0]

    @_('LPAREN expr RPAREN')
    def factor(self, p):
        return p[1]

    @_('NUMBER')
    def factor(self, p):
        return basic_ast.FactorAST(int(p[0]), 'constant_int')

    @_('IDENTIFIER')
    def factor(self, p):
        return basic_ast.FactorAST(p[0], 'symbol')

    # Error handling
    def error(self, p):
        if p:
            line_content = self.lexer.line_content.get(p.lineno, "Unknown line")
            print(f"Syntax error at line {p.lineno}")
            print(f"{line_content}")
            exit(1)
        else:
            print("EOF")

# Testing the parser
if __name__ == '__main__':
    lexer = BasicLexer()
    parser = BasicParser(lexer)

    # Test code
    code = """
    LET x = 10
    LET y = 20 + 30
    IF x > 0 THEN
        x = 53
    ELSEIF x > 0 THEN
        x = 52
    ELSEIF x > 0 THEN
        x = 51
    END IF
    FOR i = 0 TO 100 STEP 3
        z = 100
        WHILE z > 0 DO
           z = z - 1
        WEND
    NEXT
    """

    try:
        tokens = lexer.tokenize(code)
        result = parser.parse(tokens)
        result.traverse_print()
    except Exception as e:
        print(e)

