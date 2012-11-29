import re

def lexer(character_stream, token_specifiers):
    choices = [(re.compile(regex), tag)
               for regex, tag in token_specifiers]
    pos = 0
    while pos < len(character_stream):
        for regex, tag in choices:
            match = regex.match(character_stream, pos)
            if match:
                if tag: yield match.group(0), tag
                pos = match.end(0)
                break
        else:
            raise Exception("Lexical error",
                            character_stream[pos:].split()[0])
