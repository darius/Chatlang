import sys
from chatlang_lexer import *

if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename) as f:
        characters = f.read()
    tokens = chatlang_lexer(characters)
    for token in tokens:
        print token
