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
        return [p[0]] + p[1]

    @_('')
    def stmt_list(self, p):
        return []

    # Statements
    @_('assignment')
    def stmt(self, p):
        return p[0]

    @_('if_stmt')
    def stmt(self, p):
        return p[0]

    @_('while_stmt')
    def stmt(self, p):
        return p[0]

    # While statement
    @_('WHILE expr DO stmt_list WEND')
    def while_stmt(self, p):
        return ('while', p[1], p[3])

    # Assignment
    @_('LET IDENTIFIER EQ expr')
    def assignment(self, p):
        return basic_ast.AssignmentAST(p[1], p[3])

    @_('IDENTIFIER EQ expr')
    def assignment(self, p):
        return basic_ast.AssignmentAST(p[0], p[2])

    # If statement
    @_('IF expr THEN stmt_list END IF')
    def if_stmt(self, p):
        return basic_ast.IfAST(p[1], p[3])

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
        return basic_ast.OperationAST(p[1], 'NOT')

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
        return basic_ast.FactorAST(p[0], 'constant_int')

    @_('IDENTIFIER')
    def factor(self, p):
        return basic_ast.FactorAST(p[0], 'symbol')

    # Error handling
    def error(self, p):
        if p:
            line_content = self.lexer.line_content.get(p.lineno, "Unknown line")
            print(f"Syntax error at line {p.lineno}")
            print(f"{line_content}")
        else:
            print("EOF")

# Testing the parser
if __name__ == '__main__':
    lexer = BasicLexer()
    parser = BasicParser(lexer)

    # Test code
    code = """
    LET x = 10
    LET y = 20
    IF x > 0 THEN
        x = 53
    END IF
    REM WHILE z > 0 DO
    REM     z = z - 1
    REM WEND
    """

    try:
        result = parser.parse(lexer.tokenize(code))
        result.traverse_print()
    except Exception as e:
        print(e)

