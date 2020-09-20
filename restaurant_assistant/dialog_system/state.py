from restaurant_assistant.textclass.decision_tree_classifier import DecisionTreeClassifier
import pandas as pd
class State:
    def __init__(self, order):
        self.order = order
        print ('Executing event state:', str(self))
    def execute(self,classifier: DecisionTreeClassifier):
        assert 0, "next not implemented"
    def __str__(self):
        return self.__class__.__name__