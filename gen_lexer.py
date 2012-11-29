import sys
import re

def lexer (character_stream, token_regex_list):
    tokens = []
    char_pos = 0
    compiled_regexes = [ (re.compile(p), tag) for p, tag in token_regex_list ]
    while char_pos < len(character_stream):
        match = None
        for token_regex in compiled_regexes:
            regex, tag =  token_regex
            #regex = re.compile(pattern)
            match = regex.match(character_stream, char_pos)
            if match:
                matched_text = match.group(0)
                if tag:
                    token = (matched_text, tag)
                    tokens.append(token)
                break
        if not match:
            sys.stderr.write('Error! Invalid character: %s ' % characters[pos])
            sys.exit(1)
        else:
            char_pos = match.end(0)
    return tokens
