from restaurant_assistant.dialog_system.state import State
from restaurant_assistant.textclass.utterance_classifier import UtteranceType
from restaurant_assistant.textclass.decision_tree_classifier import DecisionTreeClassifier
from restaurant_assistant.dialog_system import order as order

class InitState(State):
    def execute(self, classifier: DecisionTreeClassifier):
        print ('Hello, how can I be of help?')
        return GreetUser(self.stack)


class GreetUser(State):
    def execute(self, classifier: DecisionTreeClassifier):
        answer = input().lower()
        classification = classifier.classify(answer)      
        if classification is UtteranceType.hello:
            return AskPreference(self.stack)
        if classification is UtteranceType.inform:
            # type, keyword = order.identifyKeywords(answer)
            return StackCheck(self.stack)
        else:
            print("Sorry, I did not understand what you said. Could you reword that?")
            return self
        
        
class StackCheck(State):
     def execute(self, classifier: DecisionTreeClassifier):
         if order.stackFull(self.stack) is True:
             return AckOrder(self.stack)
         else:
             return AskPreference(self.stack)
         return self
     
        
class AskPreference(State):
    def execute(self, classifier: DecisionTreeClassifier):
        order.requestType(self.stack)
        answer = input().lower()
        classification = classifier.classify(answer)
        print(f'That utterance is of type {classification.name}')
        if classification is UtteranceType.inform:
            # self.stack.at[0,'food'] = 'spanish'
            # type, keyword = order.identifyKeywords(answer)
            return StackCheck(self.stack)
        if  classification is UtteranceType.bye:
            return EndConversation(self.stack)
        else:
            print("Sorry, I did not understand what you said. Could you reword that?")
            return self


class AckOrder(State):
    def execute(self, classifier: DecisionTreeClassifier):
        order.displayOrder(self.stack)
        print("Is this correct? y/n")
        answer = input().lower()
        if answer == 'y':
            return Suggest(self.stack)
        if answer == 'n':
            return ChangePreference(self.stack)
        pass
    
    
class Suggest(State):
    def execute(self, classifier: DecisionTreeClassifier):
        print("Here is what I found:")
        order.displaySuggestion(self.stack)
        return EndConversation(self.stack)
    
        
class ChangePreference(State):
    def execute(self, classifier: DecisionTreeClassifier):
        print("Please tell us ")
        pass
    
    
class EndConversation(State):
    def execute(self, classifier: DecisionTreeClassifier):
        return EndConversation(self.stack)
