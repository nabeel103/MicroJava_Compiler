class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

    def __str__(self):
        return f"{self.token_type}: {self.value}"

# defined keywords
keywords = {'if', 'final', 'class', 'void', 'while', 'else', 'program', 'int', 'new', 'while'}

# function to get the next character
def get_next_character(i, word):
    try:
        return word[i]
    except IndexError:
        return False

# function to generate recognized tokens (stateless NFA)
def get_next_token(result):
    tokens = []
    for word in result:
        i = 0
        while True:
            ch = get_next_character(i, word)
            if ch == '<':
                i += 1
                ch = get_next_character(i, word)
                if ch == '=':
                    tokens.append(Token('LE', '<='))
                    break
                elif ch is False:
                    tokens.append(Token('LT', '<'))
                    break
                else:
                    break
            elif ch == '/':
                i += 1
                ch = get_next_character(i, word)
                if ch == '/':
                    # Ignore comments
                    break
                else:
                    tokens.append(Token('OPERATOR', '/'))
                    break
            elif ch == '>':
                i += 1
                ch = get_next_character(i, word)
                if ch == '=':
                    tokens.append(Token('GE', '>='))
                    break
                elif ch is False:
                    tokens.append(Token('GT', '>'))
                    break
                else:
                    break
            elif ch == '!':
                i += 1
                ch = get_next_character(i, word)
                if ch == '=':
                    tokens.append(Token('NE', '!='))
                    break
                else:
                    break
            elif ch == '=':
                i += 1
                ch = get_next_character(i, word)
                if ch == '=':
                    tokens.append(Token('EQ', '=='))
                    break
                else:
                    tokens.append(Token('ASSIGNMENT', '='))
                    break
            elif ch.isalpha():
                identifier = ""
                while i < len(word) and (ch.isalnum() or ch == '_'):
                    identifier += ch
                    i += 1
                    ch = get_next_character(i, word)
                if identifier.lower() in keywords:
                    tokens.append(Token('KEYWORD', identifier))
                else:
                    tokens.append(Token('IDENTIFIER', identifier))
                break
            elif ch.isdigit():
                number = ""
                while i < len(word) and (ch.isdigit() or ch == '.'):
                    number += ch
                    i += 1
                    ch = get_next_character(i, word)
                    if ch == 'e':
                        number += ch
                        i += 1
                        ch = get_next_character(i, word)
                        if ch in {'+', '-'}:
                            number += ch
                            i += 1
                            ch = get_next_character(i, word)
                    elif ch == '.':
                        i += 1
                        ch = get_next_character(i, word)
                        while i < len(word) and ch.isdigit():
                            number += ch
                            i += 1
                            ch = get_next_character(i, word)
                tokens.append(Token('NUMBER', number))
                break
            elif ch == '{' :
                tokens.append(Token('LBRACE', ch))
                i += 1
                break
            elif ch == '}':
                tokens.append(Token('RBRACE', ch))
                i += 1
                break
            elif ch == '[':
                tokens.append(Token('LSQUARE', ch))
                i += 1
                break
            elif ch == ']':
                tokens.append(Token('RSQUARE', ch))
                i += 1
                break
            elif ch == '(':
                tokens.append(Token('LPAREN', ch))
                i += 1
                break
            elif ch == ')':
                tokens.append(Token('RPAREN', ch))
                i += 1
                break
            elif ch == '.':
                tokens.append(Token('PERIOD', ch))
                i += 1
                break
            elif ch == ',':
                tokens.append(Token('COMMA', ch))
                i += 1
                break
            elif ch in {'+', '/', '-', '*', '%'}:
                tokens.append(Token('OPERATOR', ch))
                i += 1
                break
            elif ch == ';':
                tokens.append(Token('SEMICOLON', ch))
                i += 1
                break
            elif ch.isspace():
                i += 1
                continue
            else:
                break
    return tokens

