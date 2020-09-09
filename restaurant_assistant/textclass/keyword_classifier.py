from restaurant_assistant.textclass.utterance_classifier import UtteranceClassifier,\
    UtteranceType


class KeywordClassifier(UtteranceClassifier):
    
    
    def __init__(self):
        self.keywords = dict()

    def initialize(self, data):
        self.generate_full_dict()
    
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

        if value == "\0": #If we cannot classify make it null (might be incorrect to do so!, ask)
            answer = UtteranceType["null"]
        else:
            answer = UtteranceType[value]
        return answer

    



    #Methods for "filling" in the dictionary with our keywords.
    #At the bottom to not cluster the actual class, might be better to have a separate class do it.
    
    def generate_full_dict(self):
        self.generate_ack()
        self.generate_affirm()
        self.generate_bye()
        self.generate_confirm()
        self.generate_deny()
        self.generate_hello()
        self.generate_inform()
        self.generate_negate()
        self.generate_repeat()
        self.generate_reqalts()
        self.generate_reqmore()
        self.generate_request()
        self.generate_restart()
        self.generate_thankyou()
    
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
        self.keywords["bye"] = "bye"
        self.keywords["see you"] = "bye"
        self.keywords["good bye"] = "bye"
        
    def generate_confirm(self):
        self.keywords["is it in "] = "confirm"
        self.keywords["are there"] = "confirm"
        self.keywords["does it have"] = "confirm"
        self.keywords["are you sure"] = "confirm"
        self.keywords["where is"] = "confirm"
        
    def generate_deny(self):
        self.keywords["i dont want"] = "deny"
        self.keywords["not"] = "deny"
        self.keywords["that is not"] = "deny"
        self.keywords["isn't right"] = "deny"
    
    def generate_hello(self):
        self.keywords["hi"] = "hello"
        self.keywords["hello"] = "hello"
        self.keywords["hey"] = "hello"
        
    def generate_inform(self):
        self.keywords["looking for"] = "inform"
        self.keywords["want to"] = "inform"
        self.keywords["feeling"] = "inform"
        self.keywords["thinking"] = "inform"
        self.keywords["i feel"] = "inform"
        self.keywords["i want"] = "inform"
        self.keywords["i need"] = "inform"
        self.keywords["vietnamese"] = "inform"
        self.keywords["chinese"] = "inform"
        self.keywords["greek"] = "inform"
        self.keywords["european"] = "inform"
        self.keywords["mexican"] = "inform"
        self.keywords["turkish"] = "inform"
        self.keywords["south"] = "inform"
        self.keywords["north"] = "inform"
        self.keywords["east"] = "inform"
        self.keywords["west"] = "inform"
        self.keywords["cheap"] = "inform"
        self.keywords["persian"] = "inform"
        self.keywords["korean"] = "inform"
        self.keywords["japanese"] = "inform"
        self.keywords["oriental"] = "inform"
        self.keywords["fast"] = "inform"
        self.keywords["portuguese"] = "inform"
        self.keywords["spanish"] = "inform"
        self.keywords["dutch"] = "inform"
        self.keywords["mediterranean"] = "inform"
        self.keywords["italian"] = "inform"
        self.keywords["expensive"] = "inform"
        self.keywords["cozy"] = "inform"
        self.keywords["fancy"] = "inform"
        self.keywords["casual"] = "inform"
        self.keywords["price"] = "inform"
        self.keywords["moderately"] = "inform"
        self.keywords["cheaply"] = "inform"
        self.keywords["restaurant"] = "inform"
        self.keywords[" food"] = "inform"
        
    def generate_negate(self):
        self.keywords["no"] = "negate"
        self.keywords["wrong"] = "negate"
        self.keywords["isn't"] = "negate"
        self.keywords["not right"] = "negate"
        self.keywords["isn't right"] = "negate"
        
    def generate_repeat(self):
        self.keywords["repeat"] = "repeat"
        self.keywords["again"] = "repeat"
        self.keywords["sorry"] = "repeat"
        
    def generate_reqalts(self):
        self.keywords["anything else"] = "reqalts"
        self.keywords["anything"] = "reqalts"
        self.keywords["any other"] = "reqalts"
        self.keywords["other"] = "reqalts"
        self.keywords["alternative"] = "reqalts"
        
    def generate_reqmore(self):
        self.keywords["more"] = "reqmore"
        self.keywords["keep going"] = "reqmore"
        self.keywords["is there more"] = "reqmore"
        self.keywords["any more"] = "reqmore"
        
    def generate_request(self):
        self.keywords["what is"] = "request"
        self.keywords["post code"] = "request"
        self.keywords["phone"] = "request"
        self.keywords["address"] = "request"
        self.keywords["how expensive"] = "request"
        self.keywords["where is"] = "request"
        self.keywords["what do"] = "request"
        self.keywords["can you"] = "request"
        self.keywords["tell me"] = "request"
        self.keywords["can i"] = "request"
        
    def generate_restart(self):
        self.keywords["start over"] = "restart"
        self.keywords["forget"] = "restart"
        self.keywords["restart"] = "restart"
        
    def generate_thankyou(self):
        self.keywords["thanks"] = "thankyou"
        self.keywords["appreciate it"] = "thankyou"
        self.keywords["thank you"] = "thankyou"