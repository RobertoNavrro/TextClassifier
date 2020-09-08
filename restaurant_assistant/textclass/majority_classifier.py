from restaurant_assistant.textclass.utterance_classifier import UtteranceClassifier,\
    UtteranceType
from restaurant_assistant.data_processing.data_loader import Column


class MajorityClassifier(UtteranceClassifier):
    
    def __init__(self):
        self.answer = None

    def initialize(self, data):
        most_used = data[Column.label].value_counts().idxmax()
        self.answer = UtteranceType[most_used]

    def classify(self, utterance):
        return self.answer
