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
        self.falseDict = []

    def check_is_in_knowledge(self, operator):
        # print('--------------------------- operators in check is in knowledge', operator.name)
        for p in range(len(operator.preconditions)):
            # print(operator.preconditions[p].__str__())
            # print('pppppppp',operator.preconditions[p].__str__())
            for k in range(len(self.knowledge)):
                if operator.preconditions[p].name == self.knowledge[k].name and operator.preconditions[p].inputs == \
                        self.knowledge[k].inputs:
                    break
                if k == len(self.knowledge) - 1:
                    return False
        # print('--------------------------')
        return True

    def check_knowledge(self, operator):
        dict = {}
        for p in operator.preconditions:
            # print("ppppp", p.inputs)
            for rule in self.knowledge:
                if p.name == rule.name:
                    operator_inputs_saved = p.inputs
                    for i in range(len(p.inputs)):
                        if p.inputs[i] in operator.inputs and p.inputs[i] not in dict.keys():
                            if operator.name in self.falseDict:
                                if rule.inputs[i] == self.falseDict[operator.name][p.inputs[i]]:
                                    continue
                            dict[p.inputs[i]] = rule.inputs[i]
                            p.inputs[i] = rule.inputs[i]
                        elif p.inputs[i] in operator.inputs and p.inputs[i] in dict.keys():
                            p.inputs[i] = dict[p.inputs[i]]
                    if p.inputs != rule.inputs:
                        p.inputs = operator_inputs_saved

        # here should be fixed
        is_in_knowledge = self.check_is_in_knowledge(operator)
        if is_in_knowledge:
            return True, dict
        else:
            self.falseDict.append({operator.name: dict})
            return False, dict

    def add_knowledge(self, effects, values_given):
        # print("#####inside add knowledge#########")
        # print("############", values_given)
        for e in range(len(effects)):
            for i in range(len(effects[e].inputs)):
                # print("$$$$$$$$$$$$$$$$$", values_given)
                if effects[e].inputs[i] in values_given.keys():
                    effects[e].inputs[i] = values_given[effects[e].inputs[i]]
        # print("$$$$$$$$$$$$$$$$$efects$$$$$$$$$$$$$$$$$$$$$")
        # for e in effects:
        #     print(e.__str__())
        # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        for e in effects:
            if e.delete:
                for rule in self.knowledge:
                    if e.name == rule.name and e.inputs == rule.inputs:
                        self.knowledge.remove(rule)
            else:
                # print('^^^^^^^^^^^^',e.__str__())
                self.knowledge.append(e)
        # print("###############################")

    def check_knowledge_end(self):
        has_goal = []
        for rule in self.knowledge:
            for goal in self.goalStates:
                if rule.name == goal.name and rule.inputs == goal.inputs:
                    has_goal.append(True)
        if len(has_goal) == len(self.goalStates):
            return True
        return False

    def forward_search(self):
        # print("=====================================================================")
        # for k in self.knowledge:
        #     print(k.__str__())
        # print("=====================================================================")
        x = 0
        while True:
            print("__________________________________________________________")
            # self.falseDict = []
            x += 1
            for operator in self.operators:
                o = copy.deepcopy(operator)
                precondition_satisfied, values_given = self.check_knowledge(operator)
                # print(operator.__str__())
                print(operator.name, precondition_satisfied, values_given)
                if precondition_satisfied:
                    self.add_knowledge(operator.effects, values_given)
                if self.check_knowledge_end():
                    return
                operator.preconditions = copy.deepcopy(o.preconditions)
                operator.effects = copy.deepcopy(o.effects)
                print("*********************************** knowledge base")
                for k in self.knowledge:
                    print(k.__str__())
                print('')
            if x == 10:
                break

    def backward_search(self):
        print("backward search => ")
        goal_states = self.goalStates
        dont_add_knowledge = False
        while True:
            print("_______________________________________________________")
            for operator in self.operators:
                o = copy.deepcopy(operator)
                goal_effects = check_satisfy(operator.effects, goal_states)
                if len(goal_effects) > 0:
                    end_search, values = self.check_knowledge(operator)
                    if end_search and self.check_knowledge_end:
                        print(operator.name, values)
                        print("#########", operator.__str__())
                        return
                    else:
                        self.path.append(operator)
                        print(operator.name, values)
                        print("#########", operator.__str__())
                        self.add_knowledge(operator.effects, values)
                        goal_states = operator.preconditions
                operator = o
            dont_add_knowledge = True

    def ignore_preconditions(self):
        pass

    def ignore_delete_lists(self):
        pass
