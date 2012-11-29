import gen_lexer

RESERVED = 'RESERVED'
INT      = 'INT'
ID       = 'ID'

token_regex_list = [
    (r'[ \n\t]+', None),
    (r'#[^\n]*', None),
    (r'\:=', RESERVED),
    (r'\(', RESERVED),
    (r'\)', RESERVED),
    (r';', RESERVED),
    (r'\:', RESERVED),
    (r'\+', RESERVED),
    (r'-', RESERVED),
    (r'\*', RESERVED),
    (r'/', RESERVED),
    (r'<=', RESERVED),
    (r'<', RESERVED),
    (r'>=', RESERVED),
    (r'>', RESERVED),
    (r'==', RESERVED),
    (r'=', RESERVED),
    (r'!=', RESERVED),
    (r'and\b', RESERVED),
    (r'or\b', RESERVED),
    (r'not\b', RESERVED),
    (r'if\b', RESERVED),
    (r'then\b', RESERVED),
    (r'else\b', RESERVED),
    (r'while\b', RESERVED),
    (r'do\b', RESERVED),
    (r'end\b', RESERVED),
    (r'[0-9]+', INT),
    (r'[A-Za-z][A-Za-z0-9_]*', ID),
]

def chatlang_lexer(character_stream):
    return gen_lexer.lexer(character_stream, token_regex_list)
