class AST:
    def __init__(self):
        pass

    def traverse_print(self, level=0):
        pass

    def traverse_do(self, symbol_table):
        pass

    def execute(self, symbol_table):
        return None

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

    def execute(self, symbol_table):
        if self.type == 'symbol':
            return symbol_table[self.factor]
        return self.factor

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

    def execute(self, symbol_table):
        if self.operator == '+':
            return self.operand1.execute(symbol_table) + self.operand2.execute(symbol_table)
        if self.operator == '-':
            return self.operand1.execute(symbol_table) - self.operand2.execute(symbol_table)
        if self.operator == '*':
            return self.operand1.execute(symbol_table) * self.operand2.execute(symbol_table)
        if self.operator == '/':
            return self.operand1.execute(symbol_table) / self.operand2.execute(symbol_table)
        if self.operator == '>=':
            return self.operand1.execute(symbol_table) >= self.operand2.execute(symbol_table)
        if self.operator == '>':
            return self.operand1.execute(symbol_table) > self.operand2.execute(symbol_table)
        if self.operator == '<=':
            return self.operand1.execute(symbol_table) <= self.operand2.execute(symbol_table)
        if self.operator == '<':
            return self.operand1.execute(symbol_table) < self.operand2.execute(symbol_table)
        if self.operator == '==':
            return self.operand1.execute(symbol_table) == self.operand2.execute(symbol_table)
        if self.operator == '!=':
            return self.operand1.execute(symbol_table) != self.operand2.execute(symbol_table)
        if self.operator == 'AND':
            return self.operand1.execute(symbol_table) and self.operand2.execute(symbol_table)
        if self.operator == 'OR':
            return self.operand1.execute(symbol_table) or self.operand2.execute(symbol_table)
        if self.operator == 'XOR':
            return self.operand1.execute(symbol_table) ^ self.operand2.execute(symbol_table)

class AssignmentAST(AST):
    def __init__(self, symbol, expression):
        self.symbol = symbol
        self.expression = expression

    def traverse_print(self, level=0):
        print(" " * level * 2, f"{self.symbol}->", sep='')
        self.expression.traverse_print(level + 1)

    def execute(self, symbol_table):
        if self.symbol.type == 'symbol':
            symbol_table[self.symbol.factor] = self.expression.execute(symbol_table)
        else:
            raise Exception('Constant value could not be assigned.')

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

    def execute(self, symbol_table):
        if self.condition.execute(symbol_table):
            self.stmts.execute(symbol_table)

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

    def execute(self, symbol_table):
        while self.condition.execute(symbol_table):
            self.stmts.execute(symbol_table)

class ForAST(AST):
    def __init__(self, symbol, initial, end, step, stmts):
        self.symbol = symbol
        self.initial = initial
        self.end = end
        self.step = step
        self.stmts = stmts

    def traverse_print(self, level=0):
        indent = " " * level * 2
        print(f"{indent}FOR")
        self.initial.traverse_print(level + 1)
        print(f"{indent}TO")
        self.end.traverse_print(level + 1)
        print(f"{indent}STEP")
        self.step.traverse_print(level + 1)
        print(f"{indent}DO")
        self.stmts.traverse_print(level + 1)
        print(f"{indent}NEXT")
    
    def execute(self, symbol_table):
        self.initial.execute(symbol_table)
        while True:
            if self.step.execute(symbol_table) == 0:
                raise Exception("Step could not be zero.")
            elif self.step.execute(symbol_table) < 0 and self.symbol.execute(symbol_table) < self.end.execute(symbol_table):
                return
            elif self.step.execute(symbol_table) > 0 and self.symbol.execute(symbol_table) > self.end.execute(symbol_table):
                return
            self.stmts.execute(symbol_table)
            AssignmentAST(
                self.symbol,
                OperationAST(self.symbol, '+', self.step)
            ).execute(symbol_table)

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

    def execute(self, symbol_table):
        for stmt in self.stmts:
            val = stmt.execute(symbol_table)
            if val != None:
                print(val)

class FunctionAST(AST):
    def __init__(self, name, stmts):
        self.name = name
        self.stmts = stmts

    def traverse_print(self, level=0):
        print(" " * level * 2, f"{self.name}", sep='')
        self.stmts.traverse_print()

    def execute(self, symbol_table):
        self.stmts.execute(symbol_table)
