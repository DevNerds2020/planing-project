class Operator:
    def __init__(self, name, inputs, preconditions, effects):
        self.name = name
        self.inputs = inputs
        self.preconditions = preconditions
        self.effects = effects

    def __str__(self):
        return (f"""
            operator => 
            name:{self.name}
            inputs:{self.inputs}
        """)
    def __preconditions__(self):
      print(self.name, 'preconditions')
      for p in self.preconditions:
        print(p.__str__())
    
    def __effects__(self):
      print(self.name, 'effects')
      for e in self.effects:
        print(e.__str__())
    # def __addoperators__(self):
    #     for input in operator.inputs:
    #         for p in operator.preconditions:
    #             for i in input:
    #                 for pi in range(len(p.inputs)):
    #                     if p.inputs[pi] == i:
    #                         p.inputs[pi] = input[i]