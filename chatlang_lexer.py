import re
import gen_lexer

INT      = 'INT'
ID       = 'ID'

punctuation = ':= ( ) ; : + - * / <= < >= > == = !='
keywords = 'and or not if then else while do end'

token_regex_list = (  [(r'\s+', None),
                       (r'#[^\n]*', None)]
                    + [(re.escape(s), s) for s in punctuation.split()]
                    + [(s+r'\b', s) for s in keywords.split()]
                    + [(r'\d+', INT),
                       (r'[A-Za-z][A-Za-z0-9_]*', ID)])

def chatlang_lexer(character_stream):
    return gen_lexer.lexer(character_stream, token_regex_list)
