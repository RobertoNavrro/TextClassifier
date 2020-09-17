from restaurant_assistant.textclass.decision_tree_classifier import DecisionTreeClassifier
from restaurant_assistant.textclass.utterance_classifier import UtteranceType
import pandas as pd

class DialogSystem():

    def __init__(self):
        self.state = None
        self.classifier = None
        self.stack = pd.DataFrame(columns = ['food','price','area'],index = ['0'])

    def initialize(self, classifier: DecisionTreeClassifier):
        self.classifier = classifier
        # self.stack.reindex(columns = [*self.stack.columns.tolist(),*columns])
        print('Hello! Welcome to the X Restaurant Assistant, How may we be of help?')
    
    def classify_user_input(self, utterance):
        utype  = self.classifier.classify(utterance)
        return utype
    
    def state_controller(self, utype: UtteranceType):
        if self.state is None:
            if utype is UtteranceType.inform:
                print ('Gotta obtain the information')
                self.state = 'Ask_Pref'
            if utype is UtteranceType.hello:
                self.state = 'Ask_Pref'
                print ('oh hi')
            else: # here maybe create a function for handling unlikely responses HandleUnknown
                print('Sorry I did not quite understand you. Could you reword that?')
        if self.state is 'Ask_Pref'
            if utype is 'inform':
                
                
    
    def execute_loop(self):
        while(True):
            utterance = input().lower()
            utype = self.classify_user_input(utterance)
            self.state_controller(utype)


