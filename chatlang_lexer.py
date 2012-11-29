import gen_lexer

RESERVED = 'RESERVED'
INT      = 'INT'
ID       = 'ID'

reserved = (r'\:= \( \) ; \: \+ - \* / <= < >= > == = != '
            + r'and\b or\b not\b if\b then\b else\b while\b do\b end\b')

token_regex_list = (  [(r'[ \n\t]+', None),
                       (r'#[^\n]*', None)]
                    + [(s, RESERVED) for s in reserved.split()]
                    + [(r'[0-9]+', INT),
                       (r'[A-Za-z][A-Za-z0-9_]*', ID)])

def chatlang_lexer(character_stream):
    return gen_lexer.lexer(character_stream, token_regex_list)
