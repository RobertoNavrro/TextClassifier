from restaurant_assistant.dialog_system.state import State
from restaurant_assistant.textclass.utterance_classifier import UtteranceType
from restaurant_assistant.textclass.decision_tree_classifier import DecisionTreeClassifier
from restaurant_assistant.dialog_system import order as order

class InitState(State):
    def execute(self, utterance: str, type : UtteranceType):
        print ('Hello, how can I be of help?')
        return GreetUser(self.order)
    

class GreetUser(State):
    def execute(self, utterance: str, type : UtteranceType):
        if type is UtteranceType.hello:
            return AskPreference(self.order)
        if type is UtteranceType.inform:
            # type, keyword = order.identifyKeywords(answer)
            if self.order.stackFull() is True:
                return AckOrder(self.order)
            else:
                self.order.findMissingType()
            return AskPreference(self.order)
        else:
            print("Sorry, I did not understand what you said. Could you reword that?")
            return self
        
        
class StackCheck(State):
     def execute(self, utterance: str, type : UtteranceType):
         if self.order.stackFull() is True:
             return AckOrder(self.order)
         else:
             self.order.findMissingType()
             return AskPreference(self.order)
         return self
     
        
class AskPreference(State):
    def execute(self, utterance: str, type : UtteranceType):
        if type is UtteranceType.inform:
            self.order.identifyKeywords(utterance)
            if(self.order.preferences)
            self.order.findMissingType()
            if self.order.stackFull() is True:
                return AckOrder(self.order)
            else:
                self.order.findMissingType()
                return self
        
        if  type is UtteranceType.bye:
            return EndConversation(self.order)
        else:
            print("Sorry, I did not understand what you said, please try again.")
            return self


class AckOrder(State):
    def execute(self, utterance: str, type : UtteranceType):
        self.order.displayOrder(self.order)
        print("Is this correct? y/n")
        answer = input().lower()
        if answer == 'y':
            return Suggest(self.order)
        if answer == 'n':
            print("Please indicate what you want, either food, price or area.")
            return ChangePreference(self.order)
        else:
            print("Sorry I did not understand what you said, please try again.")
            return self
    
    
class Suggest(State):
    def execute(self, utterance: str, type : UtteranceType):
        print("Here is what I found:")
        self.order.displaySuggestion()
        return EndConversation(self.order)
    
        
class ChangePreference(State):
    def execute(self, utterance: str, type : UtteranceType):
        return AskPreference
    
    
class EndConversation(State):
    def execute(self, utterance: str, type : UtteranceType):
        return None
