from restaurant_assistant.dialog_system.state import State
from restaurant_assistant.textclass.utterance_classifier import UtteranceType
from restaurant_assistant.textclass.decision_tree_classifier import DecisionTreeClassifier
import pandas as pd

class InitState(State):
    def execute(self, classifier: DecisionTreeClassifier):
        return GreetUser(self.stack)

class GreetUser(State):
    def execute(self, classifier: DecisionTreeClassifier):
        print ('Hello, how can I be of help?')
        answer = input().lower()
        if classifier.classify(answer) is UtteranceType.hello:
            return AskPreference(self.stack)
        if classifier.classify(answer) is UtteranceType.inform:
            return AskPreference(self.stack)
        else:
            print("Sorry, I did not understand what you said. Could you reword that?")
            return self
        
class AskPreference(State):
    def execute(self, classifier: DecisionTreeClassifier):
        answer = input().lower()
        classification = classifier.classify(answer)
        print(f'That utterance is of type {classification.name}')
        if classifier.classify(answer) is UtteranceType.inform:
            print('KNOWLEDGE!')
            self.stack = self.stack.at(0,'food') = 'spanish'
            return AskPreference(self.stack)
        if  classifier.classify(answer) is UtteranceType.bye:
            return EndConversation(self.stack)
        else:
            print("Sorry, I did not understand what you said. Could you reword that?")
            return self
 
class EndConversation(State):
    def execute(self, classifier: DecisionTreeClassifier):
        return EndConversation(self.stack)
