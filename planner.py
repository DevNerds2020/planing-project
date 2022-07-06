import copy
from tabnanny import check

from state import State
from planneroperator import Operator


class Planner:
    def __init__(self, initialStates, goalStates, operators):
        self.initialStates = initialStates
        self.goalStates = goalStates
        self.operators = operators
        self.knowledge = initialStates
        self.path = []
        self.falseDict = []

    def add_my_operators(self):
        x = []
        for operator in self.operators:
            operator_copy = copy.deepcopy(operator)
            for input in operator.inputs:
                for p in operator.preconditions:
                    for i in input:
                        for pi in range(len(p.inputs)):
                            if p.inputs[pi] == i:
                                p.inputs[pi] = input[i]
                for e in operator.effects:
                    for i in input:
                        for ei in range(len(e.inputs)):
                            if e.inputs[ei] == i:
                                e.inputs[ei] = input[i]
                o = copy.deepcopy(operator)
                operator = copy.deepcopy(operator_copy)
                x.append(o)
        # for f in x :
        #     print("============================================")
        #     print("preconditionssssssssssssssss")
        #     f. __preconditions__()
        #     print('effecctssssssssssssssssssss')
        #     f.__effects__()
        self.operators = x

    def print_knowledge(self):
        print("knowledge => ")
        for k in self.knowledge:
            if not k.delete:
                print(k.__str__())

    def print_path(self):
        print("path => ")
        for p in self.path:
            print(p.__str__())

    def forward_search(self):
        x = 0
        self.add_my_operators()
        # return
        while True:
            x += 1
            print("====================================================")
            # for k in self.knowledge:
            #     print(k.__str__())
            for operator in self.operators:
                is_in_knowledge = []
                for p in operator.preconditions:
                    for k in self.knowledge:
                        if p.name == k.name and p.inputs == k.inputs and p.delete == k.delete:
                            is_in_knowledge.append(p)
                if len(is_in_knowledge) >= len(operator.preconditions):
                    print("##############################", operator.name)
                    for e in operator.effects:
                        # if e.delete:
                        #     for k in self.knowledge:
                        #         if e.name == k.name and e.inputs == k.inputs:
                        #             self.knowledge.remove(k)
                        self.knowledge.append(e)

                for k in self.knowledge:
                    # print(k.__str__())
                    for g in self.goalStates:
                        if k.name == g.name and k.inputs == g.inputs and k.delete == g.delete:
                            print(
                                "*************************finished*********************************")
                            self.print_knowledge()
                            return True
            if x == 10:
                break

    def satisfy_all_goals(self, effects, goal_states):
        # print("---------------------------------------")
        # print("goal states => ")
        # for g in goal_states:
        #     print(g.__str__())
        # print("effects => ")
        # for e in effects:
        #     print(e.__str__())
        satisfies = 0
        for g in goal_states:
            for k in self.knowledge:
                if not g.delete:
                    if g.name == k.name and g.inputs == k.inputs and g.delete == k.delete:
                        goal_states.remove(g)
                        break
                else:
                    if self.check_if_not_in_knowledge(g):
                        goal_states.remove(g)
                        break

        for e in effects:
            for g in goal_states:
                if e.name == g.name and e.inputs == g.inputs and e.delete == g.delete:
                    satisfies += 1
                    break
        # print('final goal states => ')
        # for g in goal_states:
        #     print(g.__str__())
        if satisfies > 0:
            return True
        return False

    def check_if_in_knowledge(self, state):
        for k in self.knowledge:
            if k.name == state.name and k.inputs == state.inputs and k.delete == state.delete:
                return True
        return False

    def check_if_not_in_knowledge(self, state):
        for k in self.knowledge:
            if k.name == state.name and k.inputs == state.inputs and k.delete == state.delete:
                return False
        return True
    def check_knowledge_finished(self):
        satisfied = 0
        # for g in self.goalStates:
        #     print("goal state => ", g.__str__())
        for k in self.knowledge:
            for g in self.goalStates:
                if k.name == g.name and k.inputs == g.inputs and k.delete == g.delete:
                    # print(k.name, k.inputs, k.delete)
                    satisfied += 1
        # print("satisfied => ", satisfied, len(self.goalStates))
        if satisfied >= len(self.goalStates):
            return True
        return False
    def backward_search(self):
        print("backward search => ")
        goal_states = self.goalStates
        x = 0
        while True:
            if self.check_knowledge_finished():
                print("********************finished***************************")
                self.print_knowledge()
                return True
            x += 1
            print("_______________________________________________________")
            for operator in self.operators:
                o = copy.deepcopy(operator)
                if self.satisfy_all_goals(operator.effects, goal_states):
                    print("##############################", operator.name)
                    self.path.append(o.name)
                    is_in_knowledge = []
                    for p in operator.preconditions:
                        for k in self.knowledge:
                            if p.name == k.name and p.inputs == k.inputs and p.delete == k.delete:
                                is_in_knowledge.append(p)
                    if len(is_in_knowledge) >= len(operator.preconditions):
                        for e in operator.effects:
                            if e.delete:
                                for k in self.knowledge:
                                    if e.name == k.name and e.inputs == k.inputs:
                                        self.knowledge.remove(k)
                            else:
                                self.knowledge.append(e)
                    else:
                        # print("##############################")
                        print(operator.__str__())
                        # print("##############################")
                        operator.__preconditions__()
                        # print("##############################")
                        operator.__effects__()
                        goal_states = copy.deepcopy(operator.preconditions)
                        # self.goalStates = copy.deepcopy(operator.preconditions)
                        # for g in goal_states:
                        #     print(g.__str__())
                        # print("##############################")
                        # self.print_knowledge()
                        self.path.append(operator)
                        break
            if x == 10:
                break

    def ignore_preconditions(self):
        print("ignore preconditions => ")
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
                operator.preconditions = copy.deepcopy(o.preconditions)
                operator.effects = copy.deepcopy(o.effects)
            dont_add_knowledge = True

    def ignore_delete_lists(self):
        print("ignore delete lists => ")
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
