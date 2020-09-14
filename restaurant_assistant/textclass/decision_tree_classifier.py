import numpy
from pathlib import Path
from typing import List
from pandas.core.frame import DataFrame
import pickle
from restaurant_assistant.textclass.utterance_classifier import UtteranceClassifier,UtteranceType
from sklearn import tree
from restaurant_assistant.data_processing.data_loader import Column



CONVERTED = 'converted'
NR_LABEL = 'nr_label'
MODEL_LOCATION = Path(__file__).parent.parent.parent.joinpath('data', 'tree_model.trm')

class DecisionTreeClassifier(UtteranceClassifier):
    
    def __init__(self):
        self.words = list()
        self.model = None
        
       
    def initialize(self, data):
        
        self.process_data(data)  
        self.model = tree.DecisionTreeClassifier()
        
        print('Do you want to load a model from a previous run? Enter y/n')
        answer = input().lower()
        
        if answer == 'y':
            self.model = pickle.load(open(MODEL_LOCATION,'rb'))
            print('Model loaded.')
        else:
            self.model = self.model.fit(X=numpy.array(data[CONVERTED].to_list()),
                y=numpy.array(data[NR_LABEL].to_list()))
            print('Done training. Do you want to save the model? y/n')
            answer = input().lower()
            if answer == 'y':
                pickle.dump(self.model, open(MODEL_LOCATION,'wb'))
                print(f'Network weights saved to {MODEL_LOCATION}.')
                

    def classify(self, utterance):
        sample = self.convert_utterance(utterance)
        output = list(self.model.predict([sample])[0])
        max_index = output.index(max(output))
        return UtteranceType(max_index + 1)
    
    def evaluate(self, data):
        data[CONVERTED] = [self.convert_utterance(x) for x in data[Column.utterance]]
        data[NR_LABEL] = [[0 if y != UtteranceType[x] else 1
                           for y in UtteranceType]
                          for x in data[Column.label]]
        
        score = self.model.score(X=numpy.array(data[CONVERTED].to_list()),
                y=numpy.array(data[NR_LABEL].to_list()))
        
        print(f'Model achieved {score} accuracy.')        
        
    def convert_utterance(self, utterance: str) -> List[int]:
        """
        Converts the utterance into a list corresponding to self.words, where words that occur
        in the utterance are marked with 1, and the rest as 0.
        :param utterance: string to be converted
        :return: the created list
        """
        converted = [0 for _ in self.words]
        for word in utterance.lower().split():
            try:
                index = self.words.index(word)
            except Exception:  # word not in known list of words
                index = 0
            converted[index] = 1
        return converted
    

    def process_data(self, data: DataFrame) -> None:
        """
        Creates a list of all words in the training data and saves them to self.words.
        Adds columns to the data for converted utterances and the label in one-hot coding format.
        :param data: training data. Not yet separated from validation data
        """
        all_words = list(set([y for x in data[Column.utterance] for y in x.lower().split()]))
        all_words.insert(0, None)
        self.words = all_words

        data[CONVERTED] = [self.convert_utterance(x) for x in data[Column.utterance]]
        data[NR_LABEL] = [[0 if y != UtteranceType[x] else 1
                           for y in UtteranceType]
                          for x in data[Column.label]]

