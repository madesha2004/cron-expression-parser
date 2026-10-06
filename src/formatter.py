from parser import FIELD_DEFINITIONS


def format_output(result):
    lines = []

    for name, _, _ in FIELD_DEFINITIONS:
        values = " ".join(str(value) for value in result[name])
        lines.append(f"{name:<14}{values}")

    lines.append(f"{'command':<14}{result['command']}")

    return "\n".join(lines)