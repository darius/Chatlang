import pdb;

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

class Tag(Parser):
    def __init__(self, tag):
        self.tag = tag

    def __call__(self, tokens, pos):
        if pos < len(tokens):
            token = tokens[pos]
            _, tag = token
            return (token, pos+1) if tag is self.tag else None

class Sequence(Parser):
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

class Process(Parser):
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
    def __init__(self, parser_function):
        self.parser = None
        self.fn = parser_function

    def __call__(self, tokens, pos):
        if not self.parser:
            self.parser = self.fn()
        return self.parser(tokens, pos)

class All(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        result = self.parser(tokens,pos)
        ast, pos = result
        if result and pos == len(tokens):
            return result
        else:
            return None

class Exp(Parser):
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
    
if __name__ == "__main__":
    b = Reserved("if", "RESERVED")
    print b([("if", "RESERVED")], 0)
    print b([("foo", "RESERVED")], 0)
