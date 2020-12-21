#!/usr/bin/env python
import sys
from dataclasses import dataclass
from enum import auto, Enum
from typing import Any, Iterable, List, Union


class TokenType(Enum):
    INTEGER = auto()
    PLUS = auto()
    MUL = auto()
    LPAREN = auto()
    RPAREN = auto()
    EOL = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: Union[str, int, None]


class Lexer:
    def __init__(self, text: str) -> None:
        self.text = text
        self.pos = 0
        self.c = self.text[self.pos]

    @classmethod
    def from_file(cls, filename: str) -> 'Lexer':
        with open(filename) as f:
            return cls(f.read())

    def __iter__(self) -> Iterable:
        self.pos = 0
        self.c = self.text[self.pos]
        return self

    def __next__(self) -> Token:
        token = self.get_next_token()
        if token.type is TokenType.EOF:
            raise StopIteration
        return token

    def advance(self) -> None:
        self.pos += 1
        try:
            self.c = self.text[self.pos]
        except IndexError:
            self.c = None

    def integer(self) -> int:
        res = []
        while self.c is not None and self.c.isdigit():
            res += self.c
            self.advance()
        return int(''.join(res))

    def get_next_token(self) -> Token:
        while self.c is not None:
            if self.c == '\n':
                self.advance()
                return Token(TokenType.EOL, '\n')
            elif self.c.isspace():
                while self.c is not None and self.c.isspace():
                    self.advance()
                continue
            elif self.c.isdigit():
                return Token(TokenType.INTEGER, self.integer())
            elif self.c == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')
            elif self.c == '*':
                self.advance()
                return Token(TokenType.MUL, '*')
            elif self.c == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(')
            elif self.c == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')')

            nb = self.text[:self.pos].count('\n')
            line = self.text.splitlines()[nb]
            for p in range(self.pos, -1, -1):
                if self.text[p] == '\n':
                    pos = self.pos - p
                    break
            else:
                pos = self.pos + 1
            raise SyntaxError('invalid syntax', ('', nb + 1, pos, line))

        return Token(TokenType.EOF, None)


class AST:
    pass


class Prog(AST):
    def __init__(self, nodes: List[AST]) -> None:
        self.statements = nodes


class BinOp(AST):
    def __init__(self, left: AST, op: Token, right: AST) -> None:
        self.left = left
        self.token = self.op = op
        self.right = right

    def __str__(self) -> str:
        return f'({self.left} {self.op.value} {self.right})'


class Num(AST):
    def __init__(self, token: Token) -> None:
        self.token = token
        self.value = token.value

    def __str__(self) -> str:
        return str(self.value)


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type: TokenType) -> None:
        if self.current_token.type is token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise SyntaxError

    def prog(self) -> AST:
        nodes = [self.expr()]

        while (self.current_token.type is TokenType.EOL):
            self.eat(TokenType.EOL)
            if self.current_token.type is TokenType.EOF:
                break
            nodes.append(self.expr())

        return Prog(nodes)

    def parse(self) -> AST:
        self.lexer = iter(self.lexer)
        self.current_token = self.lexer.get_next_token()
        return self.prog()


class ParserBasic(Parser):
    """Parse the following grammar.

    prog: expr (EOL expr)*
    expr: term ((PLUS | MUL) term)*
    term: INTEGER | LPARN expr RPAREN
    """

    def term(self) -> AST:
        token = self.current_token
        if token.type is TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)
        elif token.type is TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node

        raise SyntaxError

    def expr(self) -> AST:
        node = self.term()

        while (self.current_token.type is TokenType.PLUS
               or self.current_token.type is TokenType.MUL):
            token = self.current_token
            if token.type is TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type is TokenType.MUL:
                self.eat(TokenType.MUL)

            node = BinOp(node, token, self.term())

        return node


class ParserAdvanced(Parser):
    """Parse the following grammar.

    prog:   expr (EOL expr)*
    expr:   factor (MUL factor)*
    factor: term (PLUS term)*
    term:   INTEGER | LPARN expr RPAREN
    """

    def term(self) -> AST:
        token = self.current_token
        if token.type is TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)
        elif token.type is TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node

        raise SyntaxError

    def factor(self) -> AST:
        node = self.term()

        while self.current_token.type is TokenType.PLUS:
            token = self.current_token
            self.eat(TokenType.PLUS)

            node = BinOp(node, token, self.term())

        return node

    def expr(self) -> AST:
        node = self.factor()

        while self.current_token.type is TokenType.MUL:
            token = self.current_token
            self.eat(TokenType.MUL)

            node = BinOp(node, token, self.factor())

        return node


class Interpreter:
    def __init__(self, ast: AST) -> None:
        self.ast = ast

    def visit(self, node: AST) -> Any:
        return getattr(self, f'visit_{type(node).__name__}')(node)

    def visit_Prog(self, prog: Prog) -> List[Any]:
        return [self.visit(s) for s in prog.statements]

    def visit_BinOp(self, node: BinOp) -> Any:
        if node.op.type is TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type is TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)

    def visit_Num(self, node: Num) -> float:
        return node.value

    def run(self) -> Any:
        return self.visit(self.ast)


def main(filename: str):
    lexer = Lexer.from_file(filename)

    parser = ParserBasic(lexer)
    interpreter = Interpreter(parser.parse())
    res = interpreter.run()
    print(f'Step 1: {sum(res)}')

    parser = ParserAdvanced(lexer)
    interpreter = Interpreter(parser.parse())
    res = interpreter.run()
    print(f'Step 2: {sum(res)}')


if __name__ == '__main__':
    main(sys.argv[1])
