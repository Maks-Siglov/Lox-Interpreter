import sys

from parser import Parser
from interpreter import Interpreter
from scanner import Scanner


class Lox:
    had_error = False

    @staticmethod
    def run_file(filepath):
        with open(filepath, "r") as file:
            source = file.read()
            Lox.run(source)

    @staticmethod
    def run_prompt():
        while True:
            try:
                line = input("> ")
                Lox.run(line)

                if Lox.had_error:
                    sys.exit(65)

            except EOFError:
                print("\nExiting...")
                break

    @staticmethod
    def run(source):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        for token in tokens:
            print(token.__dict__)
        if Lox.had_error:
            sys.exit(65)

        parser = Parser(tokens)
        statements = parser.parse()
        print("statements")
        for statement in statements:
            print(statement, statement.__dict__)

        interpreter = Interpreter()
        interpreter.interpret(statements)
        print(interpreter.environment.__dict__)

    @staticmethod
    def read_file(path):
        try:
            with open(path, "rb") as file:
                bytes_content = file.read()
                source = bytes_content.decode("utf-8")
                Lox.run(source)
        except FileNotFoundError:
            print(f"Error: File '{path}' not found.")
            sys.exit(66)
        except IOError as e:
            print(f"Error reading file '{path}': {e}")
            sys.exit(74)

    @staticmethod
    def error(line, message):
        Lox.report(line, "", message)

    @staticmethod
    def report(line, where, message):
        print(f"[line {line}] Error{where}: {message}")
        Lox.had_error = True


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Usage: python lox.py [script]")
        sys.exit(64)
    elif len(sys.argv) == 2:
        Lox.read_file(sys.argv[1])
    else:
        Lox.run_prompt()
