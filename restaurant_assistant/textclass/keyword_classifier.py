from restaurant_assistant.textclass.utterance_classifier import UtteranceClassifier


class KeywordClassifier(UtteranceClassifier):
    
    def __init__(self):
        self.keywords = dict()

    def initialize(self, data):
        pass

    def classify(self, utterance):
        pass
