from mesa import Model
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.MessageService import MessageService
from communication.preferences.Preferences import Preferences
from communication.preferences.Item import Item
from communication.mailbox.Mailbox import Mailbox
from communication.message.MessagePerformative import MessagePerformative
from communication.message.Message import Message
from communication.preferences.Preferences import CriterionValue
from communication.preferences.CriterionName import CriterionName
from communication.preferences.Value import Value

import csv
import pandas as pd


def csv_to_dict(csv_path):
    df = pd.read_csv(csv_path)
    return df.to_dict()

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

    def generate_preferences(self, preferences, item_list):
        """
        Set the preferences of the agent
        preferences : dict type
        """
        # To be completed
        criterion_name_list = list(preferences['CRITERION'].values())
        self.preference = Preferences()
        self.preference.set_criterion_name_list([CriterionName[criterion] for criterion in criterion_name_list])
        for item in item_list:
            i = 0
            for criterion_name in criterion_name_list:
                criterion_value = CriterionValue(item, criterion_name, Value[preferences[item.get_name()][i]])
                self.preference.add_criterion_value(criterion_value)
                i += 1

class ArgumentModel(Model):
    """ ArgumentModel which inherit from Model.
    """

    def __init__(self):
        self.schedule = RandomActivation(self)
        self.__messages_service = MessageService(self.schedule)
        Item1 = Item('Item1', description='first item')
        Item2 = Item('Item2', description='second item')
        self.list_items = [Item1,Item2]
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
    print("Creating Agents...")
    Agent1 = ArgumentAgent(1, argument_model, "Agent1")
    Agent2 = ArgumentAgent(2, argument_model, "Agent2")

    print("Creating Items...")
    Item1 = Item('Item1', description='first item')
    Item2 = Item('Item2', description='second item')
    item_list = [Item1, Item2]

    print("Generating Preferences...")
    Agent1.generate_preferences(csv_to_dict(preferences_path['Agent1']),item_list)
    Agent2.generate_preferences(csv_to_dict(preferences_path['Agent2']),item_list)

    print("Starting Communication...")
    mailbox = Mailbox()
    m1 = Message("Agent1", "Agent2", MessagePerformative.PROPOSE, Item1)
    print("First message is : " + str(m1))
    item = m1.get_content()
    if Agent2.get_preference().is_item_among_top_10_percent(item, item_list):
        m2 = Message("Agent1", "Agent2", MessagePerformative.ACCEPT, item)
    else:
        m2 = Message("Agent1", "Agent2", MessagePerformative.ASK_WHY, item)
    print("Second message is : " + str(m2))


    print("exchange done")
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


