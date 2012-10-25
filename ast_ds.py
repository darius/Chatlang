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
		if self.name in env:
			return env[self.name]
		else
			return 0

class BinopExp(ArithmeticExp):
	def __init__(self, op, left, right):
		self.op = op
		self.left = left
		self.right = right
	
	def eval(self, env):
		left_val = self.left.eval(env)
		right_val = self.right.eval(env)
		if self.op == '+'
			return left_val + right_val
		elif self.op == '-'
			return left_val - right_val
		elif self.op == '*'
			return left_val * right_val
		elif self.op == '/'
			return left_val / right_val
		else
			raise Excpetion('Unknown operator' + self.op)

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
        if self.op == '<'
            return left_val < right_val
        elif self.op == '>'
            return left_val > right_val
        elif self.op == '<='
            return left_val <= right_val
        elif self.op == '>='
            return left_val >= right_val
		elif self.op == '=='
			return left_val == right_val
		elif self.op == '!='
			return left_val != right_val
        else
            raise Excpetion('Unknown operator' + self.op)

class AndExp(BooleanExp):
	def __init__(self, left, right):
		self.left = left
		self.right = right
	
	def eval(self, env):
		left_val = self.left.eval(env)
		right_val = self.right.eval(env)
		return left_val and right_val

class OrExp(BooleanExp):
	def __init__(self, left, right):
		self.left = left
        self.right = right

    def eval(self, env):
        left_val = self.left.eval(env)
        right_val = self.right.eval(env)
        return left_val or right_val

class NotExp(BooleanExp):
	def __init__(self, exp):
        self.exp = exp

    def eval(self, env):
		val = self.exp.eval(env)
        return not val

class Statement:
	pass

class AssignmentStatement(Statement):
	def __init__(self, name, val):
		self.name = name
		self.val = val

	def eval(self, env):
		val = self.val.eval(env)
		env[self.name] = val

class WhileStatement(Statement):
	def __init__(self, condition, body):
		self.condition = condition
		self.body = body

	def eval(self, env):
		eval_cond = self.condition.eval(env)
		while eval_cond:
			self.body.eval(env)
			eval_cond = self.condition.eval(env)

class IfThenElseStatement(Statement):
	def __init__(self, condition, true_body, false_body):
		self.condition = condition
		self.true_body = true_body
		self.false_body = false_body

	def eval(self, env):
		eval_cond = self.condition.eval(env)
		if eval_cond:
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
