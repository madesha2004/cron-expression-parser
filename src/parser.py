FIELD_DEFINITIONS = [
    ("minute", 0, 59),
    ("hour", 0, 23),
    ("day of month", 1, 31),
    ("month", 1, 12),
    ("day of week", 0, 6),
]


def parse_integer(value):
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"Invalid numeric value: '{value}'")


def validate_value(value, minimum, maximum):
    if value < minimum or value > maximum:
        raise ValueError(
            f"Value {value} is outside the allowed range "
            f"{minimum}-{maximum}"
        )


def expand_single_value(expression, minimum, maximum):
    if "/" in expression:
        if expression.count("/") != 1:
            raise ValueError(f"Invalid step expression: '{expression}'")

        base, step_text = expression.split("/")

        step = parse_integer(step_text)

        if step <= 0:
            raise ValueError("Step value must be greater than zero.")

        if base == "*":
            start = minimum
            end = maximum

        elif "-" in base:
            if base.count("-") != 1:
                raise ValueError(f"Invalid range: '{base}'")

            start_text, end_text = base.split("-")

            start = parse_integer(start_text)
            end = parse_integer(end_text)

            validate_value(start, minimum, maximum)
            validate_value(end, minimum, maximum)

            if start > end:
                raise ValueError(
                    f"Range start {start} cannot be greater than end {end}."
                )

        else:
            raise ValueError(
                f"Invalid step expression: '{expression}'"
            )

        return list(range(start, end + 1, step))

    if expression == "*":
        return list(range(minimum, maximum + 1))

    if "-" in expression:
        if expression.count("-") != 1:
            raise ValueError(f"Invalid range: '{expression}'")

        start_text, end_text = expression.split("-")

        start = parse_integer(start_text)
        end = parse_integer(end_text)

        validate_value(start, minimum, maximum)
        validate_value(end, minimum, maximum)

        if start > end:
            raise ValueError(
                f"Range start {start} cannot be greater than end {end}."
            )

        return list(range(start, end + 1))

    value = parse_integer(expression)

    validate_value(value, minimum, maximum)

    return [value]


def expand_field(expression, minimum, maximum):
    if not expression:
        raise ValueError("Cron field cannot be empty.")

    values = set()

    for part in expression.split(","):
        if not part:
            raise ValueError(
                f"Invalid list expression: '{expression}'"
            )

        values.update(
            expand_single_value(part, minimum, maximum)
        )

    return sorted(values)


def parse_cron(expression):
    parts = expression.split(maxsplit=5)

    if len(parts) != 6:
        raise ValueError(
            "Cron expression must contain five time fields "
            "and a command."
        )

    cron_fields = parts[:5]
    command = parts[5]

    result = {}

    for (name, minimum, maximum), field_expression in zip(
        FIELD_DEFINITIONS,
        cron_fields
    ):
        result[name] = expand_field(
            field_expression,
            minimum,
            maximum
        )

    result["command"] = command

    return result