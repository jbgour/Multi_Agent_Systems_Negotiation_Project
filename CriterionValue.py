#!/usr/bin/env python3


class CriterionValue:
    """CriterionValue class.
    This class implements the CriterionValue object which associates an item with a CriterionName and a Value.
    """
    def __init__(self, item, criterion_name, value):
        """Creates a new CriterionValue.
        """
        self.__item = item
        self.__criterion_name = criterion_name
        self.__value = value

    def get_item(self):
        """Returns the item.
        """
        return self.__item

    def get_criterion_name(self):
        """Returns the criterion name.
        """
        return self.__criterion_name

    def get_value(self):
        """Returns the value.
        """
        return self.__value
