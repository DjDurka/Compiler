from parser_expr.node import Node

class UnaryOperationNode(Node):
    def __init__(self, operation, operand):
        self.operation = operation
        self.operand = operand

    def print(self, p=1):
        return f"{self.operation.get_value()}{self.operand.get_value()}"