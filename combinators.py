class Parser:
	pass

class Reserved(Parser):
	def __init__(self, name, tag):
		self.name = name
		self.tag = tag

	def __call__(self, tokens, pos):
		if pos < len(tokens):
			token = tokens[pos]
			name, tag = token
			if name == self.name and tag == self.tag:
				return (token, pos+1)
			else:
				return None
		else:
			raise Exception("Unexpected eof")

class Tag(Parser):
	def __init__(self, tag):
		self.tag = tag

	def __call__(self, tokens, pos):
		if pos < len(tokens):
			token = tokens[pos]
			_, tag = token
			return (token, pos+1) if tag is self.tag else None
		else:
			raise Exception("Unexpected eof")

class Sequence(Parser):
	def __init__(self, *parsers):
		self.parsers = parsers

	def __call__(self, tokens, pos):
		cur_pos = pos
		values = []
		for parser in self.parsers:
			result = parser(tokens, cur_pos)
			if result:
				ast, cur_pos = result
				values.append(ast)
			else:
				return None
		return tuple(values), pos

class Or(Parser):
	def __init__(self, *parsers):
		self.parsers = parsers

	def __call__(self, tokens, pos):
		for parser in self.parsers:
			result = parser(tokens, pos)
			if result:
				return result
		return None

class Optional(Parser):
	def __init__(self, parser):
		self.parser = parser

	def __call__(self, tokens, pos):
		result = self.parser(tokens, pos)
		if result:
			return result
		else:
			return None, pos

class BinOp(Parser):
	def __init__(self, op, left_op, right_op=None):
		self.sequence = Sequence(op, left_op, right_op or left_op)

	def __call__(self, tokens, pos):
		result = self.sequence(tokens, pos)
		if result:
			(left, op, right), new_pos = result
			return (op, left, right), new_pos
		else:
			return None

class Conditional(Parser):
	def __init__(self):
		exp = Exp()
		self.sequence = Sequence(
							Reserved("if", "RESERVED"),
							Reserved("(", "RESERVED"),
							exp,
							Reserved(")", "RESERVED"),
							Reserved(":", "RESERVED"),
							exp,
							Optional(Sequence(
										Reserved("else", "RESERVED"),
										Reserved(":", "RESERVED"),
										exp)))
	
if __name__ == "__main__":
	b = Reserved("if", "RESERVED")
	print b([("if", "RESERVED")], 1)
	print b([("foo", "RESERVED")], 0)
