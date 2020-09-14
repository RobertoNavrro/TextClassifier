from restaurant_assistant.textclass.utterance_classifier import UtteranceClassifier,\
    UtteranceType


class KeywordClassifier(UtteranceClassifier):

    def __init__(self):
        self.keywords = dict()

    def initialize(self, data):
        self.generate_full_dict()

    def classify(self, utterance):
        """
        search the string with all dictionary words,
        Todo: count how many of each type appear, the one with the highest occurance is the class
        of that sentence. Otherwise we use the first one we identified.
        """
        value = UtteranceType.null
        for key in self.keywords:
            if key in utterance:
                value = self.keywords.get(key, UtteranceType.null)

        return value

    def generate_full_dict(self):
        """
        Method for "filling" in the dictionary with our keywords.
        """
        type_dict = dict()

        type_dict[UtteranceType.ack] = ['okay uhm', 'sure um', 'uhuh', 'alright um', 'aha']

        type_dict[UtteranceType.affirm] = ['sure', 'correct', 'that\'s right', 'yes', 'yes right',
                                           'yeah', 'sounds good']

        type_dict[UtteranceType.bye] = ['goodbye', 'bye', 'see you', 'good bye']

        type_dict[UtteranceType.confirm] = ['is it in', 'are there', 'does it have',
                                            'are you sure', 'where is']

        type_dict[UtteranceType.deny] = ['i dont want', 'not', 'that is not', 'isn\'t right']

        type_dict[UtteranceType.hello] = ['hi', 'hello', 'hey']

        type_dict[UtteranceType.inform] = [
            'looking for', 'want to', 'feeling', 'thinking', 'i feel', 'i want', 'i need',
            'vietnamese', 'chinese', 'greek', 'european', 'mexican', 'turkish', 'south', 'north',
            'east', 'west', 'cheap', 'persian', 'korean', 'japanese', 'oriental', 'fast',
            'portuguese', 'spanish', 'dutch', 'mediterranean', 'italian', 'expensive', 'cozy',
            'fancy', 'casual', 'price', 'moderately', 'cheaply', 'restaurant', 'food']

        type_dict[UtteranceType.negate] = ['no', 'wrong', 'isn\'t', 'not right', 'isn\'t right']

        type_dict[UtteranceType.repeat] = ['repeat', 'again', 'sorry']

        type_dict[UtteranceType.reqalts] = ['anything else', 'anything', 'any other', 'any',
                                            'alternative']

        type_dict[UtteranceType.reqmore] = ['more', 'keep going', 'is there more', 'any more']

        type_dict[UtteranceType.request] = ['what is', 'post code', 'phone', 'address',
                                            'how expensive', 'where is', 'what do', 'can you',
                                            'tell me', 'can i']

        type_dict[UtteranceType.restart] = ['start over', 'forget', 'restart']

        type_dict[UtteranceType.thankyou] = ['thanks', 'appreciate it', 'thank you']

        for key, wordlist in type_dict.items():
            for word in wordlist:
                self.keywords[word] = key
