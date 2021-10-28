from parser_expr.node import Node

class IdentifierNode(Node):
    def __init__(self, value):
        self.value = value

    def print(self, p=1):
        return str(self.value.get_value())

    def get_value(self):
        return self.value.get_value()