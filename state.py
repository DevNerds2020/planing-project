class State:
    def __init__(self, name, inputs, delete=False):
        self.name = name
        self.inputs = inputs
        self.delete = delete

    def __str__(self):
        return (f"""
            name:{self.name}
            inputs:{self.inputs}
            delete: {self.delete}
        """)
