#!/usr/bin/env python3

from mesa import Agent

from communication.mailbox.Mailbox import Mailbox
from communication.message.MessageService import MessageService
from arguments.Argument import Argument


class CommunicatingAgent(Agent):
    """CommunicatingAgent class.
    Class implementing communicating agent in a generalized manner.

    Not intended to be used on its own, but to inherit its methods to multiple
    other agents.

    attr:
        name: The name of the agent (str)
        mailbox: The mailbox of the agent (Mailbox)
        message_service: The message service used to send and receive message (MessageService)
    """

    def __init__(self, unique_id, model, name, item_list):
        """ Create a new communicating agent.
        """
        super().__init__(unique_id, model)
        self.__name = name
        self.__mailbox = Mailbox()
        self.__messages_service = MessageService.get_instance()
        self.__item_list = item_list

    def step(self):
        """ The step methods of the agent called by the scheduler at each time tick.
        """
        super().step()

    def get_name(self):
        """ Return the name of the communicating agent."""
        return self.__name

    def receive_message(self, message):
        """ Receive a message (called by the MessageService object) and store it in the mailbox.
        """
        self.__mailbox.receive_messages(message)

    def send_message(self, message):
        """ Send message through the MessageService object.
        """
        self.__messages_service.send_message(message)

    def get_new_messages(self):
        """ Return all the unread messages.
        """
        return self.__mailbox.get_new_messages()

    def get_messages(self):
        """ Return all the received messages.
        """
        return self.__mailbox.get_messages()

    def get_messages_from_performative(self, performative):
        """ Return a list of messages which have the same performative.
        """
        return self.__mailbox.get_messages_from_performative(performative)

    def get_messages_from_exp(self, exp):
        """ Return a list of messages which have the same sender.
        """
        return self.__mailbox.get_messages_from_exp(exp)

    def get_item_list(self):
        return self.__item_list

    def remove_item(self, item):
        self.__item_list.remove(item)

    def get_preference(self):
        return self.preference

    def List_supporting_proposal(self, item):
        """Generate a list of arguments which can be used to support an item
        :param item: Item - name of the item
        :return: list of all arguments PRO an item (sorted by order of importance based on agent's preferences)
        """
        argument = Argument(boolean_decision=True, item=item)
        pref = self.get_preference()
        criterion_value_list = pref.get_criterion_value_list()
        for elt in criterion_value_list:
            if elt.get_item() == item:
                if elt.get_value().name == 'GOOD' or elt.get_value().name == 'VERY_GOOD':
                    argument.add_premiss_couple_values(elt.get_criterion_name(), elt.get_value())
        return argument.get_couple_values_list()

    def List_attacking_proposal(self, item):
        """Generate a list of arguments which can be used to attack an item
        :param item: Item - name of the item
        :return: list of all arguments CON an item (sorted by order of importance based on preferences)
        """
        argument = Argument(boolean_decision=False, item=item)
        pref = self.get_preference()
        criterion_value_list = pref.get_criterion_value_list()
        for elt in criterion_value_list:
            if elt.get_item() == item:
                if elt.get_value().name == 'BAD' or elt.get_value().name == 'VERY_BAD':
                    argument.add_premiss_couple_values(elt.get_criterion_name(), elt.get_value())
        return argument.get_couple_values_list()

    def support_proposal(self, item):
        """
        Used when the agent recieves "ASK_WHY" after having proposed an item
        :param item: str - name of the item which was proposed
        :return: string - the strongest supportive argument
        """
        possible_proposals = self.List_supporting_proposal(item)
        if len(possible_proposals) == 0:
            return 'No arguments in favor of this item'
        for proposal in possible_proposals:
            if proposal.get_value().name == 'VERY_GOOD':
                return proposal
            else:
                temp_proposal = proposal
        return temp_proposal

    def argument_parsing(self, item):
        """ returns ....
        :param argument:
        :return:
        """
        # To be completed
        proposal = self.support_proposal(item)
        return item.get_name() + " because " + proposal.get_criterion_name() + " is " + proposal.get_value().name
