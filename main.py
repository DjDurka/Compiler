from lexer.lexer import Lexer
from lexer.lex_error import LexError

from parser_expr.parser_expr import ParserExpr
from parser_expr.syntax_error import SyntaxError

import sys
import os

# lexer file "lexer_tests/1 (source).txt"

# lexer dir lexer_tests

# parser_expr file "parser_expr_tests/1 (source).txt"

# parser_expr dir parser_expr_tests

def start_compiler():
    type_work = ""
    type_view = ""
    path = ""
    for command in sys.argv:
        command = command.lower()

        if command == "lexer":
            type_work = "lexer"
        elif command == "parser_expr":
            type_work = "parser_expr"

        if command == "file":
            type_view = "file"
        elif command == "dir":
            type_view = "dir"

        if os.path.isfile(command) or os.path.isdir(command):
            path = command

    if type_work == "lexer":
        lexer(type_view, path)
    elif type_work == "parser_expr":
        parser(type_view, path)


def lexer(type_view, path):
    if type_view == "file":
        lexer_file(path)
    else:
        lexer_dir(path)

def lexer_file(path):
    lexer = Lexer(path)
    try:
        lexem = lexer.next()
        print(lexem.print())
        while not lexem.eof():
            lexem = lexer.next()
            print(lexem.print())
    except LexError as error:
        print(error)

def lexer_dir(path):
    if os.path.isdir(path):
        all = 0
        failed = 0
        for file in os.listdir(path):
            abs_path = os.path.join(path, file)
            if file[len(file) - 12 :] == "(source).txt":
                all += 1
                path_res = file[: len(file) - 13] + ".txt"
                abs_path_res = os.path.join(path, path_res)
                file_res = open(abs_path_res, "r", encoding="utf-8")
                passed = True
                try:
                    lexer = Lexer(abs_path)
                    lexem = lexer.next()
                    correct = file_res.readline().replace("\n", "")
                    passed = passed and lexem.print() == correct
                    while not lexem.eof():
                        lexem = lexer.next()
                        correct = file_res.readline().replace("\n", "")
                        passed = passed and lexem.print() == correct
                except LexError as error:
                    correct = file_res.readline().replace("\n", "")
                    passed = passed and str(error) == correct
                if not passed:
                    failed += 1
                file_res.close()
                print(f"{path_res} - {'OK' if passed else 'WA'}")
        print(f"Всего тестов: {all}")
        print(f"Провалено тестов: {failed}")

def parser(type_view, path):
    if type_view == "file":
        parser_file(path)
    else:
        parser_dir(path)

def parser_file(path):
    lexer = Lexer(path)
    try:
        lexer.next()
        parser = ParserExpr(lexer).parse_expr()
        print(parser.print())
    except SyntaxError as error:
        print(error)

def parser_dir(path):
    if os.path.isdir(path):
        all = 0
        failed = 0
        for file in os.listdir(path):
            abs_path = os.path.join(path, file)
            if file[len(file) - 12 :] == "(source).txt":
                all += 1
                path_res = file[: len(file) - 13] + ".txt"
                abs_path_res = os.path.join(path, path_res)
                file_res = open(abs_path_res, "r", encoding="utf-8")
                try:
                    lexer = Lexer(abs_path)
                    lexer.next()
                    parser = ParserExpr(lexer).parse_expr().print()
                    correct = file_res.read()
                    passed = parser == correct
                except SyntaxError as error:
                    correct = file_res.read()
                    passed = str(error) == correct
                if not passed:
                    failed += 1
                file_res.close()
                print(f"{path_res} - {'OK' if passed else 'WA'}")
        print(f"Всего тестов: {all}")
        print(f"Провалено тестов: {failed}")


if __name__ == '__main__':
    start_compiler()

