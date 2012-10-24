import sys
from chatlang_lexer import *

if __name__ == '__main__':
    filename = sys.argv[1]
    file = open(filename)
    characters = file.read()
    file.close()
    tokens = chatlang_lexer(characters)
    for token in tokens:
        print token
