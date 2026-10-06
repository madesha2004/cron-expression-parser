import sys

from parser import parse_cron
from formatter import format_output


def main():
    if len(sys.argv) != 2:
        print(
            'Usage: python3 main.py "<cron expression>"',
            file=sys.stderr
        )
        sys.exit(1)

    try:
        result = parse_cron(sys.argv[1])
        print(format_output(result))

    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()