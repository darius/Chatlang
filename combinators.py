import pdb;

class Parser:
    def __call__(self, tokens, pos):
        """Given a token sequence and an index into it, try to parse a
        subsequence starting there. On failure, return None; on
        success, return (result, new_pos) where result is the parsed
        value and new_pos points to the remainder after the text
        parsed."""
        abstract

class Tag(Parser):
    "Eat one token, that bears the given tag."
    def __init__(self, tag):
        self.tag = tag

    def __call__(self, tokens, pos):
        if pos < len(tokens):
            token = tokens[pos]
            _, tag = token
            return (token, pos+1) if tag == self.tag else None

class Sequence(Parser):
    """Eat what the parsers eat in sequence, each taking up where the
    last left off. Produce a tuple of all their results."""
    def __init__(self, *parsers):
        self.parsers = parsers

    def __call__(self, tokens, pos):
        values = []
        cur_pos = pos
        for parser in self.parsers:
            result = parser(tokens, cur_pos)
            if result:
                ast, cur_pos = result
                values.append(ast)
            else:
                return None
        return tuple(values), cur_pos

class Or(Parser):
    "Act as the first of the parsers to succeed, trying them in order."
    def __init__(self, *parsers):
        self.parsers = parsers

    def __call__(self, tokens, pos):
        for parser in self.parsers:
            result = parser(tokens, pos)
            if result:
                return result
        return None

class Optional(Parser):
    "Always succeed, producing None if parser fails."
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result:
            return result
        else:
            return None, pos

class Process(Parser):
    "Transform parser's result to function(result)."
    def __init__(self, parser, function):
        self.parser = parser
        self.fn = function

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result:
            ast, pos = result
            new_ast = self.fn(ast)
            result = new_ast, pos
            return result
        else:
            return None

class Lazy(Parser):
    """A parser equivalent to parser_function(), but we call that just
    once, and not until we're first called to parse an input. (Use
    this for recursive grammars.)"""
    def __init__(self, parser_function):
        self.parser = None
        self.fn = parser_function

    def __call__(self, tokens, pos):
        if not self.parser:
            self.parser = self.fn()
        return self.parser(tokens, pos)

class All(Parser):
    "Like parser, but succeeding only when it eats all of the input."
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result:
            ast, pos = result
            if pos == len(tokens):
                return result
        return None

class Chain(Parser):
    """Eat (parser (separator parser)*). separator should produce a
    function like (lambda left, right: left + right). The result
    produced is that function folded over the results from parser
    (associating from left to right)."""
    def __init__(self, parser, separator):
        self.parser = parser
        self.separator = separator
    
    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result:
            ast, pos = result
        else:
            return None
        def process_next(parsed):
            sep_func, exp = parsed
            return sep_func(ast, exp)
        next_parser = Process(Sequence(self.separator, self.parser), process_next)
        next_result = result

        while next_result:
            next_result = next_parser(tokens, pos)
            if next_result:
                result = next_result
                ast, pos = result
        return result
