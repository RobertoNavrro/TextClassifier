from restaurant_assistant.textclass.utterance_classifier import UtteranceType

class SystemState:
    def __init__(self,action: UtteranceType, utterance):
        self.action = action
        self.utterance = utterance
    def __str__(self): return self.action
    def __hash__(self):
        return hash(self.action)