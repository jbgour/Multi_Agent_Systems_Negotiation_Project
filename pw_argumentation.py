from mesa import Model
from mesa.time import RandomActivation

from communication.agent.CommunicatingAgent import CommunicatingAgent
from communication.message.MessageService import MessageService
from communication.preferences.Preferences import Preferences



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

    # To be completed
    Agent1 = ArgumentAgent(1, argument_model, "Alice")
    Agent2 = ArgumentAgent(2, argument_model, "Bob")
    preferences = {'PRODUCTION_COST':'VERY_BAD'}
    Agent2.generate_preferences(preferences)
    print('Agent 2 Preferences: {}'.format(Agent2.get_preference().get_criterion_name_list()))
#
# PRODUCTION_COST = 0
#     CONSUMPTION = 1
#     DURABILITY = 2
#     ENVIRONMENT_IMPACT = 3
#     NOISE = 4
#
# VERY_BAD = 0
#     BAD = 1
#     AVERAGE = 2
#     GOOD = 3
#     VERY_GOOD = 4