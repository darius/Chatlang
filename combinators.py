import pdb;

class Parser:
    def __call__(self, tokens, pos):
        """Given a token sequence and an index into it, try to parse a
        subsequence starting there. On failure, return None; on
        success, return (results, new_pos) where results is a tuple of
        parsed values and new_pos points to the remainder after the
        text parsed."""
        abstract

# Just one example of making the code shorter using a higher-order
# function instead of a class.
def Tag(tag, produce=False):
    "Eat one token, that bears the given tag."
    def parse(tokens, pos):
        if pos < len(tokens):
            text, token_tag = tokens[pos]
            if token_tag == tag:
                values = (text,) if produce else ()
                return (values, pos+1)
        return None
    return parse

class Sequence(Parser):
    """Eat what the parsers eat in sequence, each taking up where the
    last left off. Concatenate all their results."""
    def __init__(self, *parsers):
        self.parsers = parsers

    def __call__(self, tokens, pos):
        values = []
        cur_pos = pos
        for parser in self.parsers:
            result = parser(tokens, cur_pos)
            if result:
                asts, cur_pos = result
                values.extend(asts)
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
    "Always succeed, producing (None,) if parser fails."
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result:
            return result
        else:
            return (None,), pos

class Process(Parser):
    "Transform parser's results to (function(*results),)."
    def __init__(self, parser, function):
        self.parser = parser
        self.fn = function

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result:
            asts, pos = result
            new_ast = self.fn(*asts)
            return (new_ast,), pos
        else:
            return None

# And another example, where it's trickier.
def Lazy(parser_function):
    """A parser equivalent to parser_function(), but we call that just
    once, and not until we're first called to parse an input. (Use
    this for recursive grammars.)"""
    def parse(tokens, pos):
        if not parse.parser:
            parse.parser = parser_function()
        return parse.parser(tokens, pos)
    parse.parser = None
    return parse

class All(Parser):
    "Like parser, but succeeding only when it eats all of the input."
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result:
            _, pos = result
            if pos == len(tokens):
                return result
        return None

class Chain(Parser):
    """Eat (parser (separator parser)*). parser should produce a
    single result; separator should produce a function of two
    arguments, like (lambda left, right: left + right). Produce, as
    the overall result, that function folded over all the results from
    parser (associating from left to right)."""
    def __init__(self, parser, separator):
        self.parser = parser
        self.separator = separator
    
    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result:
            (ast,), pos = result
        else:
            return None
        def process_next(sep_func, exp):
            return sep_func(ast, exp)
        next_parser = Process(Sequence(self.separator, self.parser),
                              process_next)

        while True:
            next_result = next_parser(tokens, pos)
            if next_result:
                result = next_result
                (ast,), pos = result
            else:
                return result
