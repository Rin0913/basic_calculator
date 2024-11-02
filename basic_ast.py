class AST:
    def __init__(self):
        pass

    def traverse_print(self, level=0):
        pass

    def traverse_do(self, symbol_table):
        pass

    def __repr__(self):
        return ""

class FactorAST(AST):
    def __init__(self, factor, factor_type):
        self.factor = factor
        self.type = factor_type

    def traverse_print(self, level=0):
        print(" " * level * 2, f"{self.factor}({self.type})", sep='')

class OperationAST(AST):
    def __init__(self, operand1, operator, operand2):
        self.operand1 = operand1
        self.operator = operator
        self.operand2 = operand2

    def traverse_print(self, level=0):
        self.operand1.traverse_print(level + 1)
        print(" " * level * 2, f"{self.operator}", sep='')
        self.operand2.traverse_print(level + 1)

class AssignmentAST(AST):
    def __init__(self, symbol, expression):
        self.symbol = symbol
        self.expression = expression

    def traverse_print(self, level=0):
        print(" " * level * 2, f"{self.symbol}->", sep='')
        self.expression.traverse_print(level + 1)

class IfAST(AST):
    def __init__(self, condition, stmts):
        self.condition = condition
        self.stmts = stmts

    def traverse_print(self, level=0):
        print(" " * level * 2, f"IF {self.condition} THEN", sep='')
        for stmt in self.stmts:
            if not hasattr(stmt, 'traverse_print'):
                print(stmt)
                continue
            stmt.traverse_print(level + 1)


class FunctionAST(AST):
    def __init__(self, name, stmts):
        self.name = name
        self.stmts = stmts

    def traverse_print(self, level=0):
        print(" " * level * 2, f"{self.name}", sep='')
        for stmt in self.stmts:
            if not hasattr(stmt, 'traverse_print'):
                print(stmt)
                continue
            stmt.traverse_print(level + 1)

