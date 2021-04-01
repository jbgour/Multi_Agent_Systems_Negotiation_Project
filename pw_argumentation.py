from mesa import Model
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.MessageService import MessageService
from communication.preferences.Preferences import Preferences
from communication.preferences.Item import Item
from communication.mailbox.Mailbox import Mailbox
from communication.message.MessagePerformative import MessagePerformative
from communication.message.Message import Message

import csv


def csv_to_dict(csv_path):
    reader = csv.reader(open(csv_path, mode='r', encoding='utf-8-sig'))
    preferences = {}
    for row in reader:
        key = row[0]
        preferences[key] = row[1]
    return preferences


class ArgumentAgent(CommunicatingAgent):
    """
    TestAgent which inherit from CommunicatingAgent.
    """

    def __init__(self, unique_id, model, name):
        super().__init__(unique_id, model, name)
        self.preference = None

    def step(self):
        super().step()

    def get_preference(self):
        return self.preference

    def generate_preferences(self, preferences):
        """
        Set the preferences of the agent
        preferences : dict type
        """
        # To be completed
        criterion_name_list = list(preferences.keys())
        self.preference = Preferences()
        self.preference.set_criterion_name_list(criterion_name_list)
        for criterion_name in criterion_name_list:
            criterion_value = preferences[criterion_name]
            self.preference.add_criterion_value(criterion_value)


class ArgumentModel(Model):
    """ ArgumentModel which inherit from Model.
    """

    def __init__(self):
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)
        Item1 = Item('Item1', description='first item')
        Item2 = Item('Item2', description='second item')
        list_items = [Item1,Item2]
        for i in range(2):
            a = ArgumentAgent(i, self, "Agent" + str(i))
            self.schedule.add(a)
        self.running = True
        # To be completed
        # list_items = [...]
        #
        # a = ArgumentAgent(id, "agent_name")
        # a.generate_preferences(preferences)
        # self.schedule.add(a)
        # ...

        self.running = True

    def step(self):
        self.__messages_service.dispatch_messages()
        self.schedule.step()


if __name__ == "__main__":
    argument_model = ArgumentModel()

    preferences_path = {
        'Agent1': 'agent1.csv',
        'Agent2': 'agent2.csv'
    }

    # To be completed
    Agent1 = ArgumentAgent(1, argument_model, "Agent1")
    Agent2 = ArgumentAgent(2, argument_model, "Agent2")

    Agent1.generate_preferences(csv_to_dict(preferences_path['Agent1']))
    Agent2.generate_preferences(csv_to_dict(preferences_path['Agent2']))

    print('Agent 1 Criterions: {}'.format(Agent1.get_preference().get_criterion_name_list()))
    print('Agent 2 Criterions: {}'.format(Agent2.get_preference().get_criterion_name_list()))

    Item1 = Item('Item1',description='first item')
    Item2 = Item('Item2',description='second item')

    mailbox = Mailbox()
    m1 = Message("Agent1", "Agent2", MessagePerformative.PROPOSE, "Bonjour")
    m2 = Message("Agent1", "Agent2", MessagePerformative.ACCEPT, "Hello")
    m3 = Message("Agent2", "Agent1", MessagePerformative.ARGUE, "Buenos Dias")

    mailbox.receive_messages(m1)
    mailbox.receive_messages(m2)

    assert(len(mailbox.get_new_messages()) == 2)
    print("*     get_new_messages() => OK")
    assert(len(mailbox.get_messages()) == 2)
    print("*     get_messages() => OK")

    mailbox.receive_messages(m3)
    assert(len(mailbox.get_messages()) == 3)
    assert(len(mailbox.get_messages_from_exp("Agent1")) == 2)
    print("*     get_messages_from_exp() => OK")
    assert(len(mailbox.get_messages_from_performative(MessagePerformative.ACCEPT)) == 1)
    assert(len(mailbox.get_messages_from_performative(MessagePerformative.PROPOSE)) == 1)
    assert(len(mailbox.get_messages_from_performative(MessagePerformative.ARGUE)) == 1)
    print("*     get_messages_from_performative() => OK")

    print("* 2) Testing CommunicatingAgent & MessageService")

    communicating_model = ArgumentModel()

    assert(len(communicating_model.schedule.agents) == 2)
    print("*     get the number of CommunicatingAgent => OK")

    agent0 = communicating_model.schedule.agents[0]
    agent1 = communicating_model.schedule.agents[1]

    assert(agent0.get_name() == "Agent0")
    assert(agent1.get_name() == "Agent1")
    print("*     get_name() => OK")

    agent0.send_message(Message("Agent0", "Agent1", MessagePerformative.COMMIT, "Bonjour"))
    agent1.send_message(Message("Agent1", "Agent0", MessagePerformative.COMMIT, "Bonjour"))
    agent0.send_message(Message("Agent0", "Agent1", MessagePerformative.COMMIT, "Comment ça va ?"))

    assert(len(agent0.get_new_messages()) == 1)
    assert(len(agent1.get_new_messages()) == 2)
    assert(len(agent0.get_messages()) == 1)
    assert(len(agent1.get_messages()) == 2)
    print("*     send_message() & dispatch_message (instant delivery) => OK")

    MessageService.get_instance().set_instant_delivery(False)

    agent0.send_message(Message("Agent0", "Agent1", MessagePerformative.COMMIT, "Bonjour"))
    agent1.send_message(Message("Agent1", "Agent0", MessagePerformative.COMMIT, "Bonjour"))
    agent0.send_message(Message("Agent0", "Agent1", MessagePerformative.COMMIT, "Comment ça va ?"))

    assert(len(agent0.get_messages()) == 1)
    assert(len(agent1.get_messages()) == 2)

    communicating_model.step()

    assert(len(agent0.get_new_messages()) == 1)
    assert(len(agent1.get_new_messages()) == 2)
    assert(len(agent0.get_messages()) == 2)
    assert(len(agent1.get_messages()) == 4)
    print("*     send_message() & dispatch_messages => OK")


