from chatlang_lexer import *
from ast_ds import *
from combinators import *

arithmetic_precedence = [["*", "/"], ["+", "-"]]
boolean_precedence = [["and"], ["or"]]

def reserved_word(rw):
    return Reserved(rw, RESERVED)

num = Process(Tag(INT), (lambda (i, _) : int(i)))
id = Tag(ID)

def chatlang_parse(tokens):
    ast_parser = parser()
    #import pdb; pdb.set_trace();
    ast = ast_parser(list(tokens), 0)
    return ast

def parser():
    return All(statements())

def statements():
    separator = Process(reserved_word(";"), (lambda x: lambda f, s: CompoundStatement(f, s)))
    return Exp(single_stmt(), separator)

def single_stmt():
    return Or(assign_statement(), if_statement(), while_statement())

def assign_statement():
    def process(parsed):
        (name, _, exp) = parsed
        return AssignmentStatement(name, exp)
    return Process(Sequence(id, reserved_word(":="), a_exp()), process)

def if_statement():
    def process(parsed):
        (_, condition, _, true_body, false_block) = parsed
        if false_block:
            (_, _, false_body) = false_block
        else:
            false_body = None
        return IfStatement(condition, true_body, false_body)
    return Process(Sequence(
                    reserved_word("if"), 
                    b_exp(), 
                    reserved_word(":"), 
                    Lazy(statements), 
                    Optional(Sequence(
                        reserved_word("else"),
                        reserved_word(":"),
                        Lazy(statements)))), process)

def while_statement():
    def process(parsed):
        (_, condition, _, body, _) = parsed
        return WhileStatement(condition, body)
    return Process(Sequence(
                    reserved_word("while"),
                    b_exp(),
                    reserved_word("do"),
                    Lazy(statements),
                    reserved_word("end")), process)

#left (op) right

def a_exp():
    def process(op):
        return lambda left, right : BinopExp(op, left, right)
    def operator_precedence(ops):
        return Process(reduce(lambda l, r: Or(l, r), [reserved_word(op) for op in ops]), process)
    parser = Exp(a_exp_term(), operator_precedence(arithmetic_precedence[0]))
    for precedence_op in arithmetic_precedence[1:]:
        parser = Exp(parser, operator_precedence(precedence_op))
    return parser

def a_exp_term():
    return Or(a_exp_value(), a_exp_group())

def a_exp_value():
    return Or(Process(num, (lambda i: IntExp(i))), Process(id, (lambda a: VarExp(a))))

def a_exp_group():
    def process(parsed):
        (_, exp, _) = parsed
        return exp
    return Process(Sequence(
                    reserved_word("("),
                    Lazy(a_exp),
                    reserved_word(")")), process)

def b_exp():
    def process((op, _)):
        if op=="and":
            return lambda left, right : AndExp(left, right)
        elif op=="or":
            return lambda left, right : OrExp(left, right)
        else:
            raise RuntimeError('unknown logic operator: ' + op)
    def operator_precedence(ops):
        return Process(reduce(lambda l, r: Or(l, r), [reserved_word(op) for op in ops]), process)
    parser = Exp(b_exp_term(), operator_precedence(boolean_precedence[0]))
    for precedence_op in boolean_precedence[1:]:
        parser = Exp(parser, operator_precedence(precedence_op))
    return parser

def b_exp_term():
    return Or(b_exp_not(), b_exp_relop(), b_exp_group())

def b_exp_not():
    def process(parsed):
        (_, exp) = parsed
        return NotExp(exp)
    return Process(Sequence(reserved_word('not'), Lazy(b_exp_term)), process)

def b_exp_relop():
    def process(parsed):
        (left, op, right) = parsed
        return RelExp(op, left, right)
    relops = ['<=', '<', '>=', '>', '==', '!=']
    return Process(Sequence(a_exp(), 
                    reduce(lambda l, r: Or(l, r), [reserved_word(op) for op in relops]),
                    a_exp()), process)

def b_exp_group():
    def process(parsed):
        (_, exp, _) = parsed
        return exp
    return Process(Sequence(
                    reserved_word('('),
                    Lazy(b_exp),
                    reserved_word(')')), process)
