#!/usr/bin/env python3

from enum import Enum


class Value(Enum):
    """Value enum class.
    Enumeration containing the possible Value.
    """
    VERY_BAD = 0
    BAD = 1
    AVERAGE = 2
    GOOD = 3
    VERY_GOOD = 4
