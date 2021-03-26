from mesa import Model
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.MessageService import MessageService
from communication.preferences.Preferences import Preferences
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

