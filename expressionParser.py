#node recursion parser bc i hate myself

from nodes import *
import re


def tokenize(expr):
    tokens = re.findall(r"[A-Za-z]+|\d+\.\d+|\d+|[\+\-\*/\^\(\)]", expr)
    return tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if(self.pos < len(self.tokens)):
            return self.tokens[self.pos]
        else:
            None

    def eat(self, token=None):
        currentVal = self.peek()
        if currentVal is None:
            raise SyntaxError("Expected more Input")
        if token and currentVal != token:
            raise SyntaxError(f"Expected {token}, got {currentVal}")
        self.pos += 1
        return currentVal
    

    def parse(self):
        return self.parseExpression()
    
    def parseExpression(self):
        node = self.parseTerm()
        while self.peek() in ("+", "-"):
            operator = self.eat()
            right = self.parseTerm()
            if operator == "+":
                node = node + right
            else:
                node = node - right
        return node
    
    def parseTerm(self):
        node = self.parseFactor()
        while self.peek() in ("*", "/"):
            operator = self.eat()
            right = self.parseFactor()
            if operator == "*":
                node = node * right
            else:
                node = node / right
        return node
    
    def parseFactor(self):
        node = self.parsePower()
        while self.peek() == "^":
            self.eat("^")
            right = self.parsePower()
            node = node ** right
        return node
    
    def parsePower(self):
        token = self.peek()

        if token == "(":
            self.eat("(")
            inner = self.parseExpression()
            self.eat(")")
            return inner
        
        if token in ("sin", "cos", "tan", "exp", "ln"):
            function = self.eat()
            self.eat("(")
            argument = self.parseExpression()
            self.eat(")")
            return {"sin": sin, "cos": cos, "tan": tan, "exp": exp, "ln": ln}[function](argument)
        
        if re.match(r"\d", token):
            return ConstantNode(float(self.eat()))
        
        if re.match(r"[A-Za-z]", token):
            return inp(self.eat())
        
        raise SyntaxError(f"Unexpected Phrasing: {token}")
    

def parseExpression(expr: str):
    tokens = tokenize(expr)
    parser = Parser(tokens)
    return parser.parse()




        
