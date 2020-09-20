from restaurant_assistant.textclass.decision_tree_classifier import DecisionTreeClassifier
from restaurant_assistant.dialog_system.DialogStates import InitState, EndConversation
import pandas as pd

class DialogSystem(object):

    def __init__(self, classifier:DecisionTreeClassifier()):
        self.classifier = classifier
      
        self.stack = pd.DataFrame(dict)
        self.currentState = InitState(self.stack)
    
    def executeState(self):
        # loop = True
        while(True):
            self.currentState = self.currentState.execute(self.classifier)
            self.stack = self.currentState.stack
            print(self.stack)
            if type(self.currentState) is EndConversation:
                break
        return 
