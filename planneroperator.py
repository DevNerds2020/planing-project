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
