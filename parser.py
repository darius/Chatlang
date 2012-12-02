from chatlang_lexer import *
from ast_ds import *
from combinators import *

num = Process(Tag(INT, True), int)
var = Tag(ID, True)

def chatlang_parse(tokens):
    ast_parser = parser()
    #import pdb; pdb.set_trace();
    ast = ast_parser(list(tokens), 0)
    return ast

def parser():
    return All(statements())

def statements():
    separator = Process(Tag(";"), lambda: CompoundStatement)
    return Chain(single_stmt(), separator)

def single_stmt():
    return Or(assign_statement(), if_statement(), while_statement())

def assign_statement():
    return Process(Sequence(var, Tag(":="), a_exp()),
                   AssignmentStatement)

def if_statement():
    return Process(Sequence(Tag("if"), 
                            b_exp(), 
                            Tag(":"), 
                            Lazy(statements), 
                            Optional(Sequence(Tag("else"),
                                              Tag(":"),
                                              Lazy(statements)))),
                   IfStatement)

def while_statement():
    return Process(Sequence(Tag("while"),
                            b_exp(),
                            Tag("do"),
                            Lazy(statements),
                            Tag("end")),
                   WhileStatement)

#left (op) right

def one_of(ops):
    return reduce(Or, map(lambda op: Tag(op, True), ops))

def a_exp():
    def process(op):
        return lambda left, right: BinopExp(op, left, right)
    def operator_precedence(ops):
        return Process(one_of(ops), process)
    parser = Chain(a_exp_term(), operator_precedence(arithmetic_precedence[0]))
    for precedence_op in arithmetic_precedence[1:]:
        parser = Chain(parser, operator_precedence(precedence_op))
    return parser

arithmetic_precedence = [["*", "/"], ["+", "-"]]

def a_exp_term():
    return Or(a_exp_value(), a_exp_group())

def a_exp_value():
    return Or(Process(num, IntExp),
              Process(var, VarExp))

def a_exp_group():
    return Sequence(Tag("("), Lazy(a_exp), Tag(")"))

def b_exp():
    def process(op):
        if op == "and":
            return AndExp
        elif op == "or":
            return OrExp
        else:
            assert False
    def operator_precedence(ops):
        return Process(one_of(ops), process)
    parser = Chain(b_exp_term(), operator_precedence(boolean_precedence[0]))
    for precedence_op in boolean_precedence[1:]:
        parser = Chain(parser, operator_precedence(precedence_op))
    return parser

boolean_precedence = [["and"], ["or"]]

def b_exp_term():
    return Or(b_exp_not(), b_exp_relop(), b_exp_group())

def b_exp_not():
    return Process(Sequence(Tag('not'), Lazy(b_exp_term)),
                   NotExp)

def b_exp_relop():
    relops = ['<=', '<', '>=', '>', '==', '!=']
    return Process(Sequence(a_exp(), one_of(relops), a_exp()),
                   lambda left, op, right: RelExp(op, left, right))

def b_exp_group():
    return Sequence(Tag('('), Lazy(b_exp), Tag(')'))
