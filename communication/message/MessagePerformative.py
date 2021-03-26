#!/usr/bin/env python3

from enum import Enum


class MessagePerformative(Enum):
    """MessagePerformative enum class.
    Enumeration containing the possible message performative.
    """
    PROPOSE = 101
    ACCEPT = 102
    COMMIT = 103
    ASK_WHY = 104
    ARGUE = 105
    QUERY_REF = 106
    INFORM_REF = 107
    REJECT = 108

    def __str__(self):
        """Returns the name of the enum item.
        """
        return '{0}'.format(self.name)
