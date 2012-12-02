class ArithmeticExp:
    pass

class IntExp(ArithmeticExp):
    def __init__(self, i):
        self.i = i

    def eval(self, env):
        return self.i

class VarExp(ArithmeticExp):
    def __init__(self, x):
        self.x = x

    def eval(self, env):
        return env.get(self.x, 0)

class BinopExp(ArithmeticExp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
    
    def eval(self, env):
        left_val = self.left.eval(env)
        right_val = self.right.eval(env)
        if self.op == '+':
            return left_val + right_val
        elif self.op == '-':
            return left_val - right_val
        elif self.op == '*':
            return left_val * right_val
        elif self.op == '/':
            return left_val / right_val
        else:
            raise Exception('Unknown operator', self.op)

class BooleanExp:
    pass

class RelExp(BooleanExp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def eval(self, env):
        left_val = self.left.eval(env)
        right_val = self.right.eval(env)
        if self.op == '<':
            return left_val < right_val
        elif self.op == '>':
            return left_val > right_val
        elif self.op == '<=':
            return left_val <= right_val
        elif self.op == '>=':
            return left_val >= right_val
        elif self.op == '==':
            return left_val == right_val
        elif self.op == '!=':
            return left_val != right_val
        else:
            raise Exception('Unknown operator', self.op)

class AndExp(BooleanExp):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def eval(self, env):
        return (self.left.eval(env)
                and self.right.eval(env))

class OrExp(BooleanExp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        return (self.left.eval(env)
                or self.right.eval(env))

class NotExp(BooleanExp):
    def __init__(self, exp):
        self.exp = exp

    def eval(self, env):
        return not self.exp.eval(env)

class Statement:
    pass

class AssignmentStatement(Statement):
    def __init__(self, name, val):
        self.name = name
        self.val = val

    def eval(self, env):
        env[self.name] = self.val.eval(env)

class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def eval(self, env):
        while self.condition.eval(env):
            self.body.eval(env)

class IfStatement(Statement):
    def __init__(self, condition, true_body, false_body):
        self.condition = condition
        self.true_body = true_body
        self.false_body = false_body

    def eval(self, env):
        if self.condition.eval(env):
            self.true_body.eval(env)
        else:
            if self.false_body:
                self.false_body.eval(env)

class CompoundStatement(Statement):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def eval(self, env):
        self.first.eval(env)
        self.second.eval(env)
