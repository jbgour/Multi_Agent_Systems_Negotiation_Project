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
from arguments.Argument import Argument

import csv
import pandas as pd


def csv_to_dict(csv_path):
    df = pd.read_csv(csv_path)
    return df.to_dict()

class ArgumentAgent(CommunicatingAgent):
    """
    TestAgent which inherit from CommunicatingAgent.
    """

    def __init__(self, unique_id, model, name, item_list):
        super().__init__(unique_id, model, name, item_list)
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
        item_list = self.get_item_list()
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
            a = ArgumentAgent(i, self, "Agent" + str(i), self.list_items)
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

    print("Creating Items...")
    Item1 = Item('Item1', description='first item')
    Item2 = Item('Item2', description='second item')
    item_list = [Item1, Item2]
    item_list2 = [Item1, Item2]

    # To be completed
    print("Creating Agents...")
    Agent1 = ArgumentAgent(1, argument_model, "Agent1", item_list)
    Agent2 = ArgumentAgent(2, argument_model, "Agent2", item_list2)

    print("Generating Preferences...")
    Agent1.generate_preferences(csv_to_dict(preferences_path['Agent1']))
    Agent2.generate_preferences(csv_to_dict(preferences_path['Agent2']))

    print("Starting Communication...")
    acceptance = False
    mailbox = Mailbox()
    m1 = Message("Agent1", "Agent2", MessagePerformative.PROPOSE, Item1)
    print("First message is : " + str(m1))
    item = m1.get_content()
    print(Agent1.get_item_list())
    if Agent2.get_preference().is_item_among_top_10_percent(item, Agent2.get_item_list()):
        m2 = Message("Agent2", "Agent1", MessagePerformative.ACCEPT, item)
        acceptance = False
    else:
        m2 = Message("Agent2", "Agent1", MessagePerformative.ASK_WHY, item)
        acceptance = False
    print("Second message is : " + str(m2))

    print("Items of Agent1 are: "+str([i.get_name() for i in Agent1.get_item_list()]))
    print("Items of Agent2 are: "+str([i.get_name() for i in Agent2.get_item_list()]))

    if acceptance:
        if item.get_name() in [i.get_name() for i in Agent1.get_item_list()] and item.get_name() in [i.get_name() for i in Agent2.get_item_list()]:
            m3 = Message("Agent1", "Agent2", MessagePerformative.COMMIT, item)
            m4 = Message("Agent2", "Agent1", MessagePerformative.COMMIT, item)
            Agent1.remove_item(item)
            print("Items of Agent1 are: " + str([i.get_name() for i in Agent1.get_item_list()]))
            print("Items of Agent2 are: " + str([i.get_name() for i in Agent2.get_item_list()]))
            Agent2.remove_item(item)
            print("Items of Agent1 are: " + str([i.get_name() for i in Agent1.get_item_list()]))
            print("Items of Agent2 are: " + str([i.get_name() for i in Agent2.get_item_list()]))
            print(Agent2.get_item_list())
        else :
            print("Errror : item not in list")
    else:
        #on commence à construire l'argumentation autour de l'item
        argument_Agent1 = Argument(True, item)
        argument_Agent2 = Argument(False, item)
        for elt in Agent1.List_supporting_proposal(item):
            argument_Agent1.add_premiss_couple_values(elt.get_criterion_name(), elt.get_value())
        for elt in Agent2.List_supporting_proposal(item):
            argument_Agent2.add_premiss_couple_values(elt.get_criterion_name(), elt.get_value())

        m3 = Message("Agent1", "Agent2", MessagePerformative.ARGUE, (item.get_name(), Agent1.support_proposal(item)))
        print("Third message is : " + Agent1.argument_parsing(item))
        mailbox.receive_messages(m3)
        can_be_attacked  = Agent2.can_be_attacked(Agent1.support_proposal,item)
        if can_be_attacked:
            #l'autre agent n'est pas d'accord
            m4 = Message("Agent2", "Agent1", MessagePerformative.ARGUE, (item.get_name(), Agent2.support_proposal(item)))
            print("Third message is : " + Agent2.argument_parsing(item))
        else:
            acceptance = True
            m5 = Message("Agent1","Agent2", MessagePerformative.COMMIT, item)
            m6 = Message("Agent2", "Agent1", MessagePerformative.COMMIT, item)
            Agent1.remove_item(item)
            Agent2.remove_item(item)
            
    print("exchange done")

