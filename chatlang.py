import sys
from chatlang_lexer import *
from parser import *

if __name__ == "__main__":
    filename = sys.argv[1]
    code = open(filename).read()
    tokens = chatlang_lexer(code)
    parsed = chatlang_parse(tokens)
    if not parsed:
        sys.stderr.write('Parse error!\n')
        sys.exit(1)
    ast, pos = parsed
    env = {}
    #import pdb;pdb.set_trace();
    ast.eval(env)

    for name in env:
        print name+':', env[name]
