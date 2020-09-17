class SystemMachine:
    def __init__(self, initialState):
        self.currentState = initialState
        self.currentState.run()