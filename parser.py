from chatlang.lexer import *
from ast_ds import *
from combinators import *

arithmetic_precedence = [["*", "/"], ["+", "/"]]
boolean_precedence = ["and", "or"]

def reserved_word(rw):
	return Reserved(rw, RESERVED)

num = Process(Tag(INT), (lambda i: int(i))

var = Tag(ID)

def parser(tokens):
	return All(statements())

def statements():
	separator = Process(reserved_word(";"), (lambda x: lambda f, s: CompoundStatement(f, s)))
	return Exp(single_stmt(), separator)

def stmt():
	return Or(if_statement(), while_statement(), assign_statement())

def assign_statement():
	def process(parsed):
		(name, _, exp) = parsed
		return AssignmentStatement(name, exp)
	return Process(Sequence(var, reserved_word(":="), a_exp()), process)

def if_statement():
	def process(parsed):
		(_, condition, _, true_body, _, _, false_body) = parsed
		return IfStatement(condition, true_body, false_body or None)
	return Process(Sequence(
					reserved_word("if"), 
					b_exp(), 
					reserved_word(":"), 
					Lazy(statements()), 
					Optional(
						reserved_word("else"),
						reserved_word(":"),
						Lazy(statements()))), process)

def while_statement():
	def process(parsed):
		(_, condition, _, body, _) = parsed
		return WhileStatement(condition, body)
	return Process(Sequence(
					reserved_word("while"),
					b_exp(),
					reserved_word("do"),
					Lazy(statements()),
					reserved_word("end")), process)

def a_exp():
	def process(op):
		return lambda left, right : BinopExp(op, left, right)
	def operator_precedence(ops):
		return Process(Or([reserved_word(op), op in ops]), process)
	parser = Exp(a_exp_term(), operator_precedence(arithmetic_precedence[0]))
	for precedence_op in arithmetic_precedence[1:]:
		parser = Exp(a_exp_term(), operator_precedence(precedence_op))
	return parser

def a_exp_term():
	return Or(a_exp_value(), a_exp_group())

def a_exp_value():
	return Or(Process(num, (lambda i: IntExp(i)), Process(var, (lambda a: VarExp(a)))

def a_exp_group():
	def process(parsed):
		(_, exp, _) = parsed
		return exp
	return Process(Sequence(
					reserved_word("("),
					Lazy(a_exp),
					reserved_word(")")), process)


