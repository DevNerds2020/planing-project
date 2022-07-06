from state import State
from planneroperator import Operator
from planner import Planner


def spare_tire():
    planner = Planner(
        initialStates=[
            State('Tire', ['Spare']),
            State('Tire', ['Flat']),
            State('At', ['Flat', 'Axle']),
            State('At', ['Spare', 'Trunk'])
        ],
        goalStates=[
            State('At', ['Spare', 'Axle'])
        ],
        operators=[
            Operator(name='Remove', inputs=['obj', 'loc'],
                     preconditions=[
                         State('At', ['Flat', 'Axle'])
            ],
                effects=[
                         State('At', ['Flat', 'Axle'], delete=True),
                         State('At', ['Flat', 'Ground'])
            ]),
            Operator(name='Remove', inputs=['obj', 'loc'],
                     preconditions=[
                         State('At', ['Flat', 'Trunk'])
            ],
                effects=[
                         State('At', ['Flat', 'Trunk'], delete=True),
                         State('At', ['Flat', 'Ground'])
            ]),
            Operator(name='Remove', inputs=['obj', 'loc'],
                     preconditions=[
                         State('At', ['Spare', 'Trunk'])
            ],
                effects=[
                         State('At', ['Spare', 'Trunk'], delete=True),
                         State('At', ['Spare', 'Ground'])
            ]),

            Operator(name='putOn', inputs=['t'],
                     preconditions=[
                         State('Tire', ['Spare']),
                         State('At', ['Spare', 'Ground']),
                         State('At', ['Flat', 'Axle'], delete=True),
                         State('At', ['Spare', 'Axle'], delete=True)
            ],
                effects=[
                         State('At', ['Spare', 'Ground'], delete=True),
                         State('At', ['Spare', 'Axle'])
            ]),
            Operator(name='putOn', inputs=['t'],
                     preconditions=[
                         State('Tire', ['Flat']),
                         State('At', ['Flat', 'Ground']),
                         State('At', ['Flat', 'Axle'], delete=True),
                         State('At', ['Spare', 'Axle'], delete=True)
            ],
                effects=[
                         State('At', ['Flat', 'Ground'], delete=True),
                         State('At', ['Flat', 'Axle'])
            ]),
            # Operator(name='LeaveOverNight', inputs=['obj', 'loc'],
            #          preconditions=[

            # ],
            #     effects=[
            #              State('At', ['Spare', 'Ground'], delete=True),
            #              State('At', ['Spare', 'Axle'], delete=True),
            #              State('At', ['Spare', 'Trunk'], delete=True),
            #              State('At', ['Flat', 'Ground'], delete=True),
            #              State('At', ['Flat', 'Axle'], delete=True),
            #              State('At', ['Flat', 'Trunk'], delete=True)
            # ]),
        ]
    )
    planner.backward_search()
    # planner.forward_search()


def blocks_world():
    planner = Planner(
        initialStates=[State('On', ['A', 'Table']),
                       State('On', ['B', 'Table']),
                       State('On', ['C', 'A']),
                       State('Block', ['A']),
                       State('Block', ['B']),
                       State('Block', ['C']),
                       State('Clear', ['B']),
                       State('Clear', ['C']),
                       State('Clear', ['Table']),
                       ],
        goalStates=[State('On', ['A', 'B']),
                    State('On', ['B', 'C'])],
        operators=[
            Operator(name='Move', inputs=['b', 'x', 'y'],
                     preconditions=[State('On', ['b', 'x']),
                                    State('Block', ['y']),
                                    State('Block', ['b']),
                                    State('Clear', ['b']),
                                    State('Clear', ['y'])],
                     effects=[State('On', ['b', 'y']),
                              State('Clear', ['x']),
                              State('On', ['b', 'x'], delete=True),
                              State('Clear', ['y'], delete=True)]),
            Operator(name='MoveToTable', inputs=['b', 'x'],
                     preconditions=[State('On', ['b', 'x']),
                                    State('Block', ['x']),
                                    State('Block', ['b']),
                                    State('Clear', ['b']), ],
                     effects=[State('On', ['b', 'Table']),
                              State('Clear', ['x']),
                              State('On', ['b', 'x'], delete=True)])
        ]
    )
    planner.backward_search()
    # planner.forward_search()


def monkey_and_bananas():
    planner = Planner(
        initialStates=[
            State('Notequal', ['A', 'B']),
            State('Notequal', ['A', 'C']),
            State('Notequal', ['B', 'A']),
            State('Notequal', ['B', 'C']),
            State('Notequal', ['C', 'A']),
            State('Notequal', ['C', 'B']),
            State('Pushable', ['Box']),
            State('At', ['Monkey', 'A']),
            State('At', ['Bananas', 'B']),
            State('At', ['Box', 'B']),
            State('Height', ['Monkey', 'Low']),
            State('Height', ['Box', 'Low']),
            State('Height', ['Bananas', 'High']),
            State('Climbable', ['Box']),
            State('Graspable', ['Bananas']),

        ],
        goalStates=[
            State('Have', ['Monkey', 'Bananas'])
        ],
        operators=[
            Operator(name='Go', inputs=[{'x': 'A', 'y': 'A'}, {'x': 'A', 'y': 'B'}, {'x': 'A', 'y': 'C'}, {'x': 'B', 'y': 'A'}, {'x': 'B', 'y': 'B'},
                                        {'x': 'B', 'y': 'C'}, {'x': 'C', 'y': 'A'}, {'x': 'C', 'y': 'B'}, {'x': 'C', 'y': 'C'}],
                     preconditions=[State('At', ['Monkey', 'x']),
                                    State(
                         'Height', ['Monkey', 'Low']),
                State(
                    'Notequal', ['x', 'y']),
            ], effects=[State('At', ['Monkey', 'y']),
                        State(
                'At', ['Monkey', 'x'], True)
            ]
            ),
            Operator(name='Push', inputs=[{'b': 'Box', 'x': 'A', 'y': 'A'}, {'b': 'Box', 'x': 'A', 'y': 'B'},
                                          {'b': 'Box', 'x': 'A', 'y': 'C'}, {
                                              'b': 'Box', 'x': 'B', 'y': 'A'},
                                          {'b': 'Box', 'x': 'B', 'y': 'B'}, {
                                              'b': 'Box', 'x': 'B', 'y': 'C'},
                                          {'b': 'Box', 'x': 'C', 'y': 'A'}, {'b': 'Box', 'x': 'C', 'y': 'B'}, {'b': 'Box', 'x': 'C', 'y': 'C'}, ],
                     preconditions=[State('Notequal', ['x', 'y']), State('At', ['Monkey', 'x']),
                                    State('Height', ['Monkey', 'Low']),
                                    State('At', ['b', 'x']), State('Pushable', [
                                        'b']), State('Height', ['b', 'Low']),
                                    ],
                     effects=[State('At', ['b', 'y']), State('At', ['Monkey', 'y']),
                              State('At', ['b', 'x'], delete=True), State('At', ['Monkey', 'x'], delete=True)]),
            Operator(name='ClimbUp', inputs=[{'x': 'A', 'b': 'Box'}, {'x': 'B', 'b': 'Box'}, {'x': 'C', 'b': 'Box'}],
                     preconditions=[State('At', ['Monkey', 'x']),
                                    State(
                         'Height', ['Monkey', 'Low']),
                State(
                         'At', ['b', 'x']),
                State(
                         'Climbable', ['b']),
                State('Height', ['b', 'Low'])],
                effects=[State("On", ['Monkey', 'b']),
                         State("Height", ["Monkey", "Low"], delete=True),
                         State("Height", ["Monkey", "High"])]),
            Operator(name='Grasp', inputs=[{'x': 'A', 'b': 'Bananas', 'h': 'High'}, {'x': 'A', 'b': 'Bananas', 'h': 'Low'},
                                           {'x': 'B', 'b': 'Bananas', 'h': 'High'},  {
                                               'x': 'B', 'b': 'Bananas', 'h': 'Low'},
                                           {'x': 'C', 'b': 'Bananas', 'h': 'High'}, {
                                               'x': 'C', 'b': 'Bananas', 'h': 'Low'},
                                           {'x': 'A', 'b': 'Box', 'h': 'High'}, {
                                               'x': 'A', 'b': 'Box', 'h': 'Low'},
                                           {'x': 'B', 'b': 'Box', 'h': 'High'}, {
                                               'x': 'B', 'b': 'Box', 'h': 'Low'},
                                           {'x': 'C', 'b': 'Box', 'h': 'High'}, {
                                               'x': 'C', 'b': 'Box', 'h': 'Low'},
                                           ],
                     preconditions=[State('At', ['Monkey', 'x']),
                                    State(
                         'Height', ['Monkey', 'h']),
                State(
                         'At', ['b', 'x']),
                State(
                         'Graspable', ['b']),
                State('Height', ['b', 'h'])],
                effects=[State("Have", ['Monkey', 'b']),
                         State("At", ["b", "x"], delete=True),
                         State("Height", ["Monkey", "High"], delete=True)]),
        ]
    )
    # planner.backward_search()
    planner.forward_search()


def dinner_date():
    pass


def link_repeat():
    pass


if __name__ == '__main__':
    print("choose your domain")
    print("1- monkey and bananas")
    print("2- blocks world")
    print("3- spare tire")
    chosen = int(input())
    if chosen == 1:
        monkey_and_bananas()
    if chosen == 2:
        blocks_world()
    if chosen == 3:
        spare_tire()
