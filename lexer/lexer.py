from lexer.lexem import Lexem
from lexer.lex_error import LexError

class Lexer:
    def __init__(self, path):
        self.file = open(path,'r', encoding='utf-8')
        self.symbol = self.file.read(1)
        self.indefinite = 'indefinite'
        self.identifier = 'identifier'
        self.reserved_word = 'reserved_word'
        self.integer = 'integer'
        self.integer2 = 'integer2'
        self.integer8 = 'integer8'
        self.integer16 = 'integer16'
        self.real = "real"
        self.real_e = "real (e)"
        self.real_e_degree = "real (e degree)"
        self.string = "string"
        self.string_literal_sharp = "string literal #"
        self.string_literal_digit = "string literal digit"
        self.operation = "operation"
        self.separator = "separator"
        self.comment = "commentary"
        self.comment_block = "block commentary"
        self.comment_block2 = "block commentary 2"
        self.error = "error"
        self.reserved_list = ["array", "asm", "begin", "case", "const", "constructor", "destructor", "do",
                            "downto", "else", "end", "exports", "file", "for", "function", "goto", "if", "implementation",
                            "in", "inherited", "inline", "interface", "label", "library", "nil", "object",
                             "of", "packed", "procedure", "program", "record", "repeat", "set", "shl", "shr",
                            "string", "then", "to", "type", "unit", "until", "uses", "var", "while", "with", "xor", "abs", "arctan", "boolean", "char", "cos", "dispose", "eof", "eoln", "exp",
                            "false", "get", "input", "integer", "ln", "maxint", "new", "output",
                            "pack", "page", "pred", "put", "read", "readln", "real", "reset", "rewrite",
                            "sin", "sqr", "sqrt", "succ", "text", "true", "unpack", "write", "writeln"]
        self.space_list = [' ', '', '\n', '\t', '\0', '\r']
        self.operation_list = ['+', '-', '*', '/', '**', ':=', '=', '<', '>', '<=', '>=', 'div', 'mod', '-=', '+=', '*=', '/=']
        self.separator_list = [':', ',', ';', '.', '(', ')', '[', ']']
        self.buffer = ''
        self.line = 1
        self.col = 1
        self.coordinates = [self.line, self.col]
        self.state = self.indefinite

    def save_coordinates(self):
        self.coordinates = [self.line, self.col]

    def add_buffer(self, val):
        self.buffer += val

    def clear_buffer(self):
        self.buffer = ''

    def current(self):
        return self.lexem

    def find_code(self, str):
        array = str.split("'")
        result = ""
        buf = ""
        for index, value in enumerate(array):
            if index % 2 == 0:
                for s in value:
                    if s == "#":
                        if buf:
                            result += chr(int(buf))
                            buf = ""
                    else:
                        buf += s
                result += chr(int(buf))
                buf = ""
            else:
                for s in value:
                    result += s
        if buf:
            result += chr(int(buf))
        return result







    def next(self):
        self.clear_buffer()
        while self.symbol or self.buffer:
            if self.state == self.indefinite:
                if self.space_list.count(self.symbol):

                    if self.symbol == '\n':
                        self.line += 1
                        self.col = 0
                    self.get_symbol()

                elif self.symbol.isalpha():
                    self.add_buffer(self.symbol)
                    self.state = self.identifier
                    self.save_coordinates()
                    self.get_symbol()

                elif self.symbol.isdigit():
                    self.add_buffer(self.symbol)
                    self.state = self.integer
                    self.save_coordinates()
                    self.get_symbol()

                elif self.symbol == "#":
                    self.add_buffer(self.symbol)
                    self.state = self.string_literal_sharp
                    self.save_coordinates()
                    self.get_symbol()

                elif self.symbol == "%":
                    self.add_buffer(self.symbol)
                    self.state = self.integer2
                    self.save_coordinates()
                    self.get_symbol()

                elif self.symbol == "&":
                    self.add_buffer(self.symbol)
                    self.state = self.integer8
                    self.save_coordinates()
                    self.get_symbol()

                elif self.symbol == "$":
                    self.add_buffer(self.symbol)
                    self.state = self.integer16
                    self.save_coordinates()
                    self.get_symbol()

                elif self.symbol == "'":
                    self.add_buffer(self.symbol)
                    self.state = self.string
                    self.save_coordinates()
                    self.get_symbol()

                elif self.symbol == "{":
                    self.state = self.comment_block
                    self.get_symbol()

                elif self.operation_list.count(self.symbol):
                    self.add_buffer(self.symbol)
                    self.state = self.operation
                    self.save_coordinates()
                    self.get_symbol()

                elif self.separator_list.count(self.symbol):
                    self.add_buffer(self.symbol)
                    self.state = self.separator
                    self.save_coordinates()
                    self.get_symbol()
                else:
                    self.state = self.error

            elif self.state == self.integer:

                if self.symbol.isdigit():
                    self.add_buffer(self.symbol)
                    self.get_symbol()

                elif self.symbol == '.':
                    self.add_buffer(self.symbol)
                    self.get_symbol()
                    self.state = self.real

                elif self.symbol.isalpha():
                    if self.symbol.lower() == "e":
                        self.add_buffer(self.symbol)
                        self.get_symbol()
                        self.state = self.real_e
                    else:
                        self.state = self.error

                else:
                    self.state = self.indefinite
                    self.lexem = Lexem(self.coordinates, self.integer, self.buffer, int(self.buffer))
                    return self.current()

            elif self.state == self.integer2:
                if "0" <= self.symbol <= "1":
                    self.add_buffer(self.symbol)
                    self.get_symbol()
                elif self.space_list.count(self.symbol):
                    self.state = self.indefinite
                    self.lexem = Lexem(self.coordinates, self.integer2, self.buffer, int(self.buffer[1:], 2))
                    return self.current()
                else:
                    self.state = self.error;

            elif self.state == self.integer8:
                if "0" <= self.symbol <= "7":
                    self.add_buffer(self.symbol)
                    self.get_symbol()
                elif self.space_list.count(self.symbol):
                    self.state = self.indefinite
                    self.lexem = Lexem(self.coordinates, self.integer8, self.buffer, int(self.buffer[1:], 8))
                    return self.current()
                else:
                    self.state = self.error;

            elif self.state == self.integer16:
                if self.symbol.isdigit() or "a" <= self.symbol.lower() <= "f":
                    self.add_buffer(self.symbol)
                    self.get_symbol()
                elif self.space_list.count(self.symbol):
                    self.state = self.indefinite
                    self.lexem = Lexem(self.coordinates, self.integer16, self.buffer, int(self.buffer[1:], 16))
                    return self.current()
                else:
                    self.state = self.error;

            elif self.state == self.real:
                if self.symbol.isdigit():
                    self.add_buffer(self.symbol)
                    self.get_symbol()
                elif self.symbol.isalpha():
                    if self.symbol.lower() == "e" and self.buffer[len(self.buffer) - 1] != ".":
                        self.add_buffer(self.symbol)
                        self.get_symbol()
                        self.state = self.real_e
                    else:
                        self.state = self.error
                else:
                    self.state = self.indefinite
                    self.lexem = Lexem(self.coordinates, self.real, self.buffer, float(self.buffer))
                    return self.current()

            elif self.state == self.real_e:
                if ["+", "-"].count(self.symbol) or self.symbol.isdigit():
                    self.add_buffer(self.symbol)
                    self.get_symbol()
                    self.state = self.real_e_degree
                else:
                    self.state = self.error

            elif self.state == self.real_e_degree:
                if self.symbol.isdigit():
                    self.add_buffer(self.symbol)
                    self.get_symbol()
                else:
                    if self.buffer[-1] == "+" or self.buffer[-1] == "-":
                        raise LexError(f"{self.coordinates}\tUnexpected {self.buffer}")
                    self.state = self.indefinite
                    self.lexem = Lexem(self.coordinates, self.real, self.buffer, float(self.buffer))
                    return self.current()

            elif self.state == self.identifier:
                if self.symbol.isalpha() or self.symbol.isdigit() or self.symbol == '_':
                    self.add_buffer(self.symbol)
                    self.get_symbol()

                else:
                    self.state = self.indefinite
                    if self.reserved_list.count(self.buffer):
                        self.lexem = Lexem(self.coordinates, self.reserved_word, self.buffer, self.buffer.lower())
                        return self.current()

                    elif self.operation_list.count(self.buffer):
                        self.lexem = Lexem(self.coordinates, self.operation, self.buffer, self.buffer.lower())
                        return self.current()
                    else:
                        self.lexem = Lexem(self.coordinates, self.identifier, self.buffer, self.buffer.lower())
                        return self.current()

            elif self.state == self.string:
                if self.symbol == '\n':
                    raise LexError(f"{[self.line, self.col]}\tUnexpected end of line")
                elif self.symbol == '':
                    raise LexError(f"{[self.line, self.col]}\tUnexpected end of file")
                elif self.symbol == "'":
                    self.add_buffer(self.symbol)
                    self.get_symbol()
                    self.state = self.string_literal_sharp if self.symbol == "#" else self.indefinite
                    if self.state == self.indefinite:
                        buffer2 = self.buffer
                        buffer2 = self.find_code(buffer2)
                        self.lexem = Lexem(self.coordinates, self.string, self.buffer, buffer2)
                        return self.current()
                    else:
                        self.add_buffer(self.symbol)
                        self.get_symbol()

                else:
                    self.add_buffer(self.symbol)
                    self.get_symbol()

            elif self.state == self.string_literal_sharp:
                if self.symbol.isdigit():
                    self.add_buffer(self.symbol)
                    self.get_symbol()
                    self.state = self.string_literal_digit
                else:
                    self.state = self.error

            elif self.state == self.string_literal_digit:
                if self.symbol == "'":
                    self.add_buffer(self.symbol)
                    self.get_symbol()
                    self.state = self.string
                elif self.symbol == "#":
                    self.add_buffer(self.symbol)
                    self.get_symbol()
                    self.state = self.string_literal_sharp
                elif self.symbol.isdigit():
                    self.add_buffer(self.symbol)
                    self.get_symbol()
                else:
                    self.state = self.indefinite
                    buffer2 = self.find_code(self.buffer)
                    self.lexem = Lexem(self.coordinates, self.string, self.buffer, buffer2)
                    return self.current()

            elif self.state == self.operation:
                if self.buffer + self.symbol == "//":
                    self.clear_buffer()
                    self.state = self.comment
                    self.get_symbol()
                else:
                    if self.operation_list.count(self.buffer + self.symbol):
                        self.add_buffer(self.symbol)
                        self.get_symbol()
                    self.state = self.indefinite
                    self.lexem = Lexem(self.coordinates, self.operation, self.buffer, self.buffer)
                    return self.current()

            elif self.state == self.separator:
                if self.buffer + self.symbol == "(*":
                        self.clear_buffer()
                        self.state = self.comment_block2
                        self.get_symbol()
                elif self.operation_list.count(self.buffer + self.symbol):
                    self.state = self.operation
                else:
                    self.state = self.indefinite
                    self.lexem = Lexem(self.coordinates, self.separator, self.buffer, self.buffer)
                    return self.current()

            elif self.state == self.comment:
                if self.symbol == "\n":
                    self.state = self.indefinite
                self.get_symbol()

            elif self.state == self.comment_block:
                if self.symbol == "}":
                    self.state = self.indefinite
                current = self.symbol
                self.get_symbol()
                if not self.symbol and current != "}":
                    raise LexError(f"{[self.line, self.col]}" + "\t'}' was expected")

            elif self.state == self.comment_block2:
                current = self.symbol
                self.get_symbol()
                if current + self.symbol == "*)":
                    self.state = self.indefinite
                    self.get_symbol()
                if not self.symbol and current + self.symbol != "*)":
                    raise LexError(f"{[self.line, self.col]}" + "\t'}' was expected")

            elif self.state == self.error:
                if self.space_list.count(self.symbol):
                    raise LexError(f"{self.coordinates}\tUnexpected {self.buffer}")
                self.add_buffer(self.symbol)
                self.get_symbol()

        self.lexem = Lexem([self.line, self.col], "eof", "end of file", "end of file")
        return self.current()

    def get_symbol(self):
        self.symbol = self.file.read(1)
        self.col += 1
