#TOKEN VARIABELS

TT_INT = 'TT_INT'
TT_FLOAT = 'TT_FLOAT'
TT_PLUS = 'TT_PLUS'
TT_MUL  = 'TT_MUL'
TT_MINUS = 'TT_MINUS'
TT_DIV = 'TT_DIV'
TT_LPAREN = 'TT_LPAREN'
TT_RPAREN = 'TT_RPAREN'

# Digits

Digits = '0123456789.'

# creating ERROR

class Error():
    def __init__(self,error_type,details):
        self.error_type = error_type
        self.details = details
    def as_string(self):
        result = (f" {self.error_type} : {self.details} ")
        return result

class IllegalCharError(Error):
    def __init__(self,details):
        super().__init__('Illegal Character',details)

# creating TOKENS

class Tokens():
    def __init__(self,type,value=None):
        self.type = type
        self.value = value
    def __repr__(self):
        if self.value :return f'{self.type}:{self.value}'
        else:return f'{self.type}'

# creating LEXER

class Lexer():
    def __init__ (self, text):
        self.text = text
        self.pos = -1
        self.current_cha = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_cha = self.text[self.pos] if self.pos < (len(self.text)) else None

    def make_tokens(self):
        tokens = []

        while self.current_cha != None :
            if self.current_cha in ' \t':
               pass
            elif self.current_cha == '+':
                tokens.append(Tokens(TT_PLUS))

            elif self.current_cha == '-':
                tokens.append(Tokens(TT_MINUS))
            elif self.current_cha == '*':
                tokens.append(Tokens(TT_MUL))
            elif self.current_cha == '/':
                tokens.append(Tokens(TT_DIV))
            elif self.current_cha == '(':
                tokens.append(Tokens(TT_LPAREN))
            elif self.current_cha == ')':
                tokens.append(Tokens(TT_RPAREN))
            elif self.current_cha in Digits:
                tokens.append(self.make_number())
            else:
                char = self.current_cha
                self.advance()
                return [],IllegalCharError("'"+ char + "'")

            self.advance()

        return tokens, None


    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_cha != None and self.current_cha in Digits:

            if self.current_cha == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'

            else:
                num_str += self.current_cha

            
            self.advance()



        if dot_count == 0:
            return Tokens(TT_INT, int(num_str))
        else:
            return Tokens(TT_FLOAT, float(num_str))

# creating a runner

def Run(text):
    lexer = Lexer(text)
    tokens , error = lexer.make_tokens()
    return tokens, error
