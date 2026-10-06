# Cron Expression Parser

A command-line application that parses a standard five-field cron expression and expands each time field into its corresponding values.

## Supported Fields

| Field | Range |
|---|---|
| Minute | 0-59 |
| Hour | 0-23 |
| Day of month | 1-31 |
| Month | 1-12 |
| Day of week | 0-6 |

## Supported Syntax

- `*` - all values
- `,` - multiple values
- `-` - ranges
- `/` - step values
- Combinations such as `1-10/2`

Special expressions such as `@yearly` are not supported.

## Project Structure

```text
cron-expression-parser/
├── src/
│   ├── parser.py
│   ├── formatter.py
│   └── main.py
├── tests/
│   └── test_parser.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Requirements

- Python 3.10+
- pytest

## Usage

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run:

```bash
python src/main.py "*/15 0 1,15 * 1-5 /usr/bin/find"
```

Example output:

```text
minute        0 15 30 45
hour          0
day of month  1 15
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   1 2 3 4 5
command       /usr/bin/find
```

## Tests

Run the test suite:

```bash
python -m pytest
```

Tests cover wildcards, lists, ranges, steps, invalid input, duplicate values, and the provided sample expression.

## Design Approach

The parser uses generic field-expansion logic with field-specific valid ranges. Parsed values are sorted and duplicates are removed.

- `parser.py` - parsing and validation
- `formatter.py` - output formatting
- `main.py` - command-line interface
- `test_parser.py` - automated tests

## Assumptions and Limitations

- Standard five-field numeric cron syntax is supported.
- Day of week uses `0-6`, where `0` represents Sunday.
- Everything after the five cron fields is treated as the command.
- Special expressions, named months/weekdays, and advanced cron modifiers are not supported.

## Extensibility

Parsing, formatting, and CLI handling are separated so additional cron syntax or output formats can be added without significantly changing the existing code.