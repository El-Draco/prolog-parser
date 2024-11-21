from main import Lexer, Parser
import os

def test_file1():
    filename = "files/1.txt"
    assert os.path.isfile(filename)


    with open(filename, 'r') as f:
        code = f.read()

        lexer = Lexer(code)
        parser = Parser(lexer)
        parser.parse()

        assert parser.errors == []

def test_file2():
    filename = "files/2.txt"
    assert os.path.isfile(filename)


    with open(filename, 'r') as f:
        code = f.read()

        lexer = Lexer(code)
        parser = Parser(lexer)
        parser.parse()

        assert parser.errors == []

def test_file3():
    filename = "files/3.txt"
    assert os.path.isfile(filename)


    with open(filename, 'r') as f:
        code = f.read()

        lexer = Lexer(code)
        parser = Parser(lexer)
        parser.parse()

        assert parser.errors == []

def test_file4():
    filename = "files/4.txt"
    assert os.path.isfile(filename)


    with open(filename, 'r') as f:
        code = f.read()

        lexer = Lexer(code)
        parser = Parser(lexer)
        parser.parse()

        assert len(parser.errors) > 0

def test_file5():
    filename = "files/5.txt"
    assert os.path.isfile(filename)


    with open(filename, 'r') as f:
        code = f.read()

        lexer = Lexer(code)
        parser = Parser(lexer)
        parser.parse()

        assert len(parser.errors) > 0


def test_file6():
    filename = "files/6.txt"
    assert os.path.isfile(filename)


    with open(filename, 'r') as f:
        code = f.read()

        lexer = Lexer(code)
        parser = Parser(lexer)
        parser.parse()

        assert len(parser.errors) > 0

