from parser_expr.identifier_node import IdentifierNode
from parser_expr.integer_node import IntegerNode
from parser_expr.real_node import RealNode
from parser_expr.unary_operation_node import UnaryOperationNode
from parser_expr.binary_operation_node import BinaryOperationNode
from parser_expr.syntax_error import SyntaxError

class ParserExpr:
    def __init__(self, lexer):
        self.lexer = lexer
        self.integer = "integer"
        self.real = "real"
        self.identifier = "identifier"

    def parse_expr(self):
        lexem = self.lexer.current()
        if lexem.eof() or lexem.get_value() == ";":
            raise SyntaxError(f"{lexem.get_coord()}        Expected expression")
        left = self.parse_term()
        operation = self.lexer.current()
        while ["+", "-"].count(operation.get_value()):
            self.lexer.next()
            right = self.parse_term()
            left = BinaryOperationNode(operation, left, right)
            operation = self.lexer.current()
        return left


    def parse_term(self):
        left = self.parse_factor()
        operation = self.lexer.current()
        while ["*", "/"].count(operation.get_value()):
            self.lexer.next()
            right = self.parse_factor()
            left = BinaryOperationNode(operation, left, right)
            operation = self.lexer.current()
        return left

    def parse_factor(self):
        lexem = self.lexer.current()
        self.lexer.next()
        if lexem.get_type() == self.integer:
            return IntegerNode(lexem)
        if lexem.get_type() == self.real:
            return RealNode(lexem)
        if lexem.get_type() == self.identifier:
            return IdentifierNode(lexem)
        if ["+", "-"].count(lexem.get_value()):
            operand = self.parse_factor()
            return UnaryOperationNode(lexem, operand)
        if lexem.get_value() == "(":
            left = self.parse_expr()
            lexem = self.lexer.current()
            if lexem.get_value() != ")":
                raise SyntaxError(f"{lexem.get_coord()}        Expected ')'")
            self.lexer.next()
            return left
        raise SyntaxError(f"{lexem.get_coord()}        Unexpected {lexem.get_code()}")