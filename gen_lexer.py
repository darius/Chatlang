import sys
import re

def lexer(character_stream, token_regex_list):
    char_pos = 0
    compiled_regexes = [(re.compile(p), tag) for p, tag in token_regex_list]
    while char_pos < len(character_stream):
        for token_regex in compiled_regexes:
            regex, tag = token_regex
            match = regex.match(character_stream, char_pos)
            if match:
                matched_text = match.group(0)
                if tag:
                    yield (matched_text, tag)
                break
        else:
            raise Exception("Lexical error",
                            character_stream[char_pos:].split()[0])
        char_pos = match.end(0)
