import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

import pytest

import pytest

from src.parser import expand_field, parse_cron


def test_wildcard():
    assert expand_field("*", 0, 5) == [0, 1, 2, 3, 4, 5]


def test_single_value():
    assert expand_field("5", 0, 59) == [5]


def test_list():
    assert expand_field("1,5,10", 0, 59) == [1, 5, 10]


def test_range():
    assert expand_field("1-5", 0, 59) == [1, 2, 3, 4, 5]


def test_step():
    assert expand_field("*/15", 0, 59) == [0, 15, 30, 45]


def test_range_step():
    assert expand_field("1-10/2", 0, 59) == [1, 3, 5, 7, 9]


def test_combined_expression():
    assert expand_field("1,5-7", 0, 59) == [1, 5, 6, 7]


def test_duplicate_values_are_removed():
    assert expand_field("1,1,2", 0, 59) == [1, 2]


def test_invalid_value():
    with pytest.raises(ValueError):
        expand_field("60", 0, 59)


def test_invalid_step():
    with pytest.raises(ValueError):
        expand_field("*/0", 0, 59)


def test_invalid_range():
    with pytest.raises(ValueError):
        expand_field("10-5", 0, 59)


def test_invalid_cron_structure():
    with pytest.raises(ValueError):
        parse_cron("* * *")


def test_sample_cron_expression():
    result = parse_cron(
        "*/15 0 1,15 * 1-5 /usr/bin/find"
    )

    assert result["minute"] == [0, 15, 30, 45]
    assert result["hour"] == [0]
    assert result["day of month"] == [1, 15]
    assert result["month"] == list(range(1, 13))
    assert result["day of week"] == [1, 2, 3, 4, 5]
    assert result["command"] == "/usr/bin/find"