# Prolog Parser Project

This project implements a **Recursive Descent Parser** for a simplified version of the Prolog programming language, following a given BNF grammar. The parser validates Prolog code by checking its syntax, identifying any errors, and reporting them. 

### Key Features

- **Lexical Analysis**
- **Syntax Analysis**
- **Error Reporting**

## Requirements

- **Python**
- **Dependencies**: Install project dependencies listed in `requirements.txt`.

## Project Structure

- `main.py` - The core parser implementation with lexer, parser, and error handling.
- `test_parser.py` - Unit tests for verifying the parser’s functionality and error handling.
- `Makefile` - Common tasks - running tests, checking code style, and generating coverage reports.

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv env
   source env/bin/activate

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Run Tests**:

    ```bash
    make tests
    ```

5. **To run the linter (ruff)**:

    ```bash
    make codestyle
    ```

## Usage

### Running the Parser

The parser reads Prolog files from the `files` directory in the format `1.txt`, `2.txt`, etc. Modify or add files in this format to test additional cases.

Run the parser:

```bash
python main.py

