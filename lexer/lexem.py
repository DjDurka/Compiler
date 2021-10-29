class Lexem:
    def __init__(self,coordinate,type,code,value):
        self.coordinate = coordinate
        self.type = type
        self.code = code
        self.value = value

    def get_coord(self):
        return self.coordinate

    def get_type(self):
        return self.type

    def get_code(self):
        return self.code

    def get_value(self):
        return self.value

    def eof(self):
        return self.type == "eof"

    def print(self):
        if self.eof():
            return ""
        return f'{self.coordinate}\t{self.type}\t{self.code}\t{self.value}'
