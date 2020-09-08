from restaurant_assistant.textclass.utterance_classifier import UtteranceClassifier,\
    UtteranceType


class KeywordClassifier(UtteranceClassifier):
    
    
    def __init__(self):
        self.keywords = dict()

    def initialize(self, data):
        #acknowledgments 
        self.generate_full_dict()
        pass
    
    def classify(self, utterance):
        
        #search the string with all dictionary words, 
        #Todo: count how many of each type appear, the one with the highest occurance is the class
        #      of that sentence. Otherwise we use the first one we identified.
        value = "\0"
        #go through the dictionary
        for key in self.keywords:
            #check whether the key occurs in the utterance (does it appear as a substring basically)
            if key in utterance:
                value = self.keywords.get(key,"\0")
                break

        if value == "\0":
            answer = UtteranceType["null"] #If we cannot classify make it null (might be incorrect to do so!, ask)
        else:
            answer = UtteranceType[value]
            
        return answer
    
    
    #Methods for filling in the dictionary with our keywords.
    #At the bottom to not cluster the actual class, might be better to have a separate class do it.
    
    def generate_full_dict(self):
        self.generate_ack()
        self.generate_affirm()
        # generate_bye(self)
        # generate_confirm(self)
        # generate_deny(self)
        # generate_hello(self)
        # generate_inform(self)
        # generate_negate(self)
        # generate_null(self)
        # generate_repeat(self)
        # generate_reqalts(self)
        # generate_reqmore(self)
        # generate_request(self)
        # generate_restart(self)
        # generate_thankyou(self)
    
    def generate_ack(self):
        self.keywords["okay um"] = "ack"
        self.keywords["sure um"] = "ack"
        self.keywords["uhuh"] = "ack"
        self.keywords["alright um"] = "ack"
        self.keywords["aha"] = "ack"
        
    def generate_affirm(self):
        self.keywords["sure"] = "affirm"
        self.keywords["correct"] = "affirm"
        self.keywords["that's right"] = "affirm"
        self.keywords["yes"] = "affirm"
        self.keywords["yes right"] = "affirm"
        self.keywords["yeah"] = "affirm"
        self.keywords["sounds good"] = "affirm"
        
    def generate_bye(self):
        self.keywords["goodbye"] = "bye"
        self.keywords[""] = "bye"
        
    def generate_confirm(self):
        self.keywords[""] = ""
        
    def generate_deny(self):
        self.keywords[""] = ""
    
    def generate_hello(self):
        self.keywords[""] = ""
        
    def generate_inform(self):
        self.keywords[""] = ""
        
    def generate_negate(self):
        self.keywords[""] = ""
        
    def generate_null(self):
        self.keywords[""] = ""
        
    def generate_repeat(self):
        self.keywords[""] = ""
        
    def generate_reqalts(self):
        self.keywords[""] = ""
        
    def generate_reqmore(self):
        self.keywords[""] = ""
        
    def generate_request(self):
        self.keywords[""] = ""
        
    def generate_restart(self):
        self.keywords[""] = ""
        
    def generate_thankyou(self):
        self.keywords[""] = ""
    
