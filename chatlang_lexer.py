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
    (r':', RESERVED),
    (r'\+', RESERVED),
    (r'-', RESERVED),
    (r'\*', RESERVED),
    (r'/', RESERVED),
    (r'<', RESERVED),
    (r'<=', RESERVED),
    (r'>', RESERVED),
    (r'>=', RESERVED),
	(r'==', RESERVED),
    (r'=', RESERVED),
    (r'!=', RESERVED),
    (r'and', RESERVED),
    (r'or', RESERVED),
    (r'not', RESERVED),
    (r'if', RESERVED),
    (r'then', RESERVED),
    (r'else', RESERVED),
    (r'while', RESERVED),
    (r'do', RESERVED),
    (r'end', RESERVED),
    (r'[0-9]+', INT),
    (r'[A-Za-z][A-Za-z0-9_]*', ID),
]

def chatlang_lexer(character_stream):
    return gen_lexer.lexer(character_stream, token_regex_list)
