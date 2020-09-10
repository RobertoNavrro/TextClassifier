from restaurant_assistant.textclass.utterance_classifier import UtteranceClassifier
from sklearn import tree
from restaurant_assistant.data_processing import data_loader as dl

class DecisionTreeClassifier(UtteranceClassifier):
    
    def __init__(self):
        self.tree_cf = tree.DecisionTreeClassifier()

    def initialize(self, data):
        # data is train_data, convert the entire training set
        # into a bag of words matrix: 694 (unique words) in 20400 
        # utterances
        x = dl.convert_to_bow(data)
        
        #convert the dataframe back into an array for the classifier tree to use
        y = data[dl.Column.label].to_numpy()
        
        # train model
        self.tree_cf = self.tree_cf.fit(x, y)

        

    def classify(self, utterance):
        #this sample =  actually doesnt work (still got to figure out what to do about this)
        sample = dl.convert_to_bow(utterance)
        answer = self.tree_cf.predict(sample)
        print ("Classification is:" + answer)
        return answer
