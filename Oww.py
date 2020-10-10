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

class Error:
    def __init__(self, pos_start, pos_end, error_type, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_type = error_type
        self.details = details

    def as_string(self):
        result = f" {self.error_type} : {self.details}\n "
        result += f' File name {self.pos_start.fn}, line {self.pos_start.ln+1}'
        return result

class IllegalCharError(Error):
    def __init__(self,pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


# creating POSITION

class position:
    def __init__(self,idx,ln,col,fn,ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_cha):
        self.idx +=1
        self.col +=1

        if current_cha == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return position(self.idx, self.ln, self.col, self.fn, self.ftxt)

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
    def __init__ (self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = position(-1, 0, -1, fn, text)
        self.current_cha = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_cha)
        self.current_cha = self.text[self.pos.idx] if self.pos.idx < (len(self.text)) else None

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
                pos_start = self.pos.copy()
                char = self.current_cha
                self.advance()
                return [],IllegalCharError(pos_start, self.pos, "'"+ char + "'")

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

def Run(text, fn):
    lexer = Lexer(fn, text)
    tokens , error = lexer.make_tokens()
    return tokens, error
