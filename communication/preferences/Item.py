#!/usr/bin/env python3


class Item:
    """Item class.
    This class implements the objects about which the argument will be conducted.

    attr:
        name: the name of the item
        description: the description of the item
     """

    def __init__(self, name, description):
        """Creates a new Item.
        """
        self.__name = name
        self.__description = description

    def __str__(self):
        """Returns Item as a String.
        """
        return self.__name + " (" + self.__description + ")"

    def get_name(self):
        """Returns the name of the item.
        """
        return self.__name

    def get_description(self):
        """Returns the description of the item.
        """
        return self.__description

    def get_value(self, preferences, criterion_name):
        """Returns the Value of the Item according to agent preferences.
        """
        return preferences.get_value(self, criterion_name)

    def get_score(self, preferences):
        """Returns the score of the Item according to agent preferences.
        """
        criterion_weight = 100
        sum_result = 0
        for criterion_name in preferences.get_criterion_name_list():
            sum_result = sum_result + criterion_weight * self.get_value(preferences, criterion_name).value
            criterion_weight = criterion_weight / 2
        return sum_result
