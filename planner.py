import copy

from state import State
from planneroperator import Operator


def check_satisfy(effects, goal_states):
    goal_effects = []

    for goal_state in goal_states:
        for effect in effects:
            if effect.name == goal_state.name and goal_state.delete == effect.delete:
                goal_effects.append(effect)
    return goal_effects


def set_value_to_inputs(goal_effects, goal_states, operator):
    # print("*************", operator.name)
    # print(goal_effects)
    found_the_goal = False
    inputs_dict = {}
    # for i in operator.inputs:
    #     inputs_dict[i] = ''
    for i in goal_effects:
        for j in goal_states:
            if i.name == j.name and i.delete == j.delete:
                for k in range(len(i.inputs)):
                    if i.inputs[k] in operator.inputs:
                        inputs_dict.update({i.inputs[k]: j.inputs[k]})
                        i.inputs[k] = j.inputs[k]
                    # print(i.inputs, j.inputs)
                    if i.inputs == j.inputs:
                        found_the_goal = True

    # print('#', inputs_dict)
    if found_the_goal:
        return inputs_dict
    return None


class Planner:
    def __init__(self, initialStates: [], goalStates: [], operators: []):
        self.initialStates = initialStates
        self.goalStates = goalStates
        self.operators = operators
        self.knowledge = initialStates
        self.path = []

    def check_knowledge(self, operator):
        dict = {}
        is_in_knowledge = []
        for p in operator.preconditions:
            for rule in self.knowledge:
                if p.name == rule.name:
                    operator_inputs_saved = p.inputs
                    for i in range(len(p.inputs)):
                        if p.inputs[i] in operator.inputs and p.inputs[i] not in dict.keys():
                            dict[p.inputs[i]] = rule.inputs[i]
                            p.inputs[i] = rule.inputs[i]
                    if p.inputs != rule.inputs:
                        p.inputs = operator_inputs_saved

        for p in operator.preconditions:
            for rule in self.knowledge:
                if p.inputs == rule.inputs and p.name == rule.name:
                    if p.delete:
                        is_in_knowledge.append(False)
                    else:
                        is_in_knowledge.append(True)
        # if operator.name == 'Go':
        #     print(dict)
        if len(is_in_knowledge) < len(operator.preconditions) or False in is_in_knowledge:
            return False, dict
        else:
            return True, dict

    # def check_goal_in_knowledge(self, effects, values):
    #     for v in values.keys():
    #         for e in range(len(effects)):
    #             for i in range(len(effects[e].inputs)):
    #                 if effects[e].inputs[i] == v:
    #                     effects[e].inputs[i] = values[v]
    #     for e in effects:
    #         print(e.__str__())

    def forward_search(self):
        while True:
            for operator in self.operators:
                for p in operator.preconditions:
                    pass

    def backward_search(self):
        print("backward search => ")
        goal_states = self.goalStates
        while True:
            print("_______________________________________________________")
            for operator in self.operators:
                o = copy.deepcopy(operator)
                goal_effects = check_satisfy(operator.effects, goal_states)
                if len(goal_effects) > 0:
                    # inputs_values = set_value_to_inputs(goal_effects, goal_states, operator)
                    # print("input values => ", inputs_values)
                    # if inputs_values is not None:
                    # for p in operator.preconditions:
                    #     for i in range(len(p.inputs)):
                    #         if p.inputs[i] in inputs_values.keys():
                    #             pass
                    end_search, values = self.check_knowledge(operator)
                    # print(operator.name, values)
                    if end_search:
                        # self.check_goal_in_knowledge(operator.effects, values)
                        # print(len(self.path))
                        # self.path.append(operator)
                        # print("the final answer ")
                        # for a in self.path:
                        #     print(a.__str__())
                        return
                    else:
                        self.path.append(operator)
                        print(operator.name, values)
                        print("#########", operator.__str__())
                        # print(operator.__str__())
                        # print('input values', inputs_values)
                        # for p in operator.preconditions:
                        #     pass
                        #     print(p.__str__())
                        goal_states = operator.preconditions
                operator = o

    def ignore_preconditions(self):
        pass

    def ignore_delete_lists(self):
        pass
