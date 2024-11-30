class AST:
    def __init__(self):
        pass

    def traverse_print(self, level=0):
        pass

    def traverse_do(self, symbol_table):
        pass

class NoopAST(AST):
    def traverse_print(self, level=0):
        print(" " * level * 2, "noop")

class FactorAST(AST):
    def __init__(self, factor, factor_type):
        self.factor = factor
        self.type = factor_type

    def traverse_print(self, level=0):
        print(" " * level * 2, f"{self.factor}({self.type})", sep='', end='')
        print()

class OperationAST(AST):
    def __init__(self, operand1, operator, operand2):
        self.operand1 = operand1
        self.operator = operator
        self.operand2 = operand2

    def traverse_print(self, level=0):
        self.operand1.traverse_print(level + 1)
        print(" " * level * 2, f" {self.operator} ", sep='')
        self.operand2.traverse_print(level + 1)
        print()

class AssignmentAST(AST):
    def __init__(self, symbol, expression):
        self.symbol = symbol
        self.expression = expression

    def traverse_print(self, level=0):
        print(" " * level * 2, f"{self.symbol}->", sep='')
        self.expression.traverse_print(level + 1)

class IfAST(AST):
    def __init__(self, condition, stmts, elsestmts):
        self.condition = condition
        self.stmts = stmts
        self.elsestmts = elsestmts

    def traverse_print(self, level=0):
        indent = " " * level * 2
        print(f"{indent}IF")
        self.condition.traverse_print(level + 1)
        print(f"{indent}THEN")
        self.stmts.traverse_print(level + 1)
        print(f"{indent}ELSE")
        self.elsestmts.traverse_print(level + 1)
        print(f"{indent}END IF")

class WhileAST(AST):
    def __init__(self, condition, stmts):
        self.condition = condition
        self.stmts = stmts

    def traverse_print(self, level=0):
        indent = " " * level * 2
        print(f"{indent}WHILE")
        self.condition.traverse_print(level + 1)
        print(f"{indent}THEN")
        self.stmts.traverse_print(level + 1)
        print(f"{indent}WEND")

class ForAST(AST):
    def __init__(self, symbol, start, end, step, stmts):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.step = step
        self.stmts = stmts

    def traverse_print(self, level=0):
        indent = " " * level * 2
        print(f"{indent}FOR")
        self.symbol.traverse_print(level + 1)
        print(f"{indent}FROM")
        self.start.traverse_print(level + 1)
        print(f"{indent}TO")
        self.end.traverse_print(level + 1)
        print(f"{indent}STEP")
        self.step.traverse_print(level + 1)
        print(f"{indent}DO")
        self.stmts.traverse_print(level + 1)
        print(f"{indent}NEXT")

class StatementsAST(AST):
    def __init__(self):
        self.stmts = []

    def add_statement(self, stmt):
        self.stmts = [stmt] + self.stmts
        return self

    def traverse_print(self, level=0):
        for stmt in self.stmts:
            if not hasattr(stmt, 'traverse_print'):
                continue
            stmt.traverse_print(level + 1)

class FunctionAST(AST):
    def __init__(self, name, stmts):
        self.name = name
        self.stmts = stmts

    def traverse_print(self, level=0):
        print(" " * level * 2, f"{self.name}", sep='')
        self.stmts.traverse_print()
