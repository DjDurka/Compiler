from parser_expr.node import Node

class BinaryOperationNode(Node):
    def __init__(self, operation, left, right):
        self.operation = operation
        self.left = left
        self.right = right

    def print(self, p=1):
        operation = self.operation.get_value()
        tab = "\t"
        right = self.right.print(p+1)
        left = self.left.print(p+1)
        return f"{operation}\n" \
               f"{tab*p}{left}\n" \
               f"{tab*p}{right}"
