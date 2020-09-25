import numpy
from pathlib import Path
from typing import List
from pandas.core.frame import DataFrame
from sklearn.utils import compute_class_weight
from tensorflow import config
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.initializers import TruncatedNormal

from restaurant_assistant.textclass.utterance_classifier import UtteranceClassifier, UtteranceType
from restaurant_assistant.data_processing.data_loader import Column

config.set_visible_devices([], 'GPU')
CONVERTED = 'converted'
NR_LABEL = 'nr_label'
WEIGHTS_LOCATION = Path(__file__).parent.parent.parent.joinpath('data', 'network_weights.h5')


class NeuralNetworkClassifier(UtteranceClassifier):

    def __init__(self):
        self.network = None
        self.words = list()

    def initialize(self, data: DataFrame):
        self.process_data(data)
        self.network = self.build_model(len(self.words))
        class_weights = compute_class_weight(class_weight='balanced',
                                             classes=[x.name for x in UtteranceType],
                                             y=data[Column.label])
        class_weights = {num: value for num, value in enumerate(class_weights)}

        print('Do you want to load a model from a previous run? Enter y/n')
        answer = input().lower()

        if answer == 'y':
            self.network.load_weights(WEIGHTS_LOCATION)
            print('Model loaded.')
        else:
            history = self.network.fit(
                x=numpy.array(data[CONVERTED].to_list()),
                y=numpy.array(data[NR_LABEL].to_list()),
                epochs=10,
                verbose=2,
                validation_split=0.1,
                batch_size=32,
                class_weight=class_weights)

            print('Done training. Do you want to save the model? y/n')
            answer = input().lower()
            if answer == 'y':
                self.network.save_weights(WEIGHTS_LOCATION)
                print(f'Network weights saved to {WEIGHTS_LOCATION}.')

    def classify(self, utterance):
        converted = self.convert_utterance(utterance)
        output = list(self.network.predict([converted])[0])
        max_index = output.index(max(output))
        return UtteranceType(max_index + 1)

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
        all_words = sorted(list(set([y for x in data[Column.utterance]
                                     for y in x.lower().split()])))
        all_words.insert(0, None)
        self.words = all_words

        data[CONVERTED] = [self.convert_utterance(x) for x in data[Column.utterance]]
        data[NR_LABEL] = [[0 if y != UtteranceType[x] else 1
                           for y in UtteranceType]
                          for x in data[Column.label]]

    @staticmethod
    def build_model(input_size: int) -> Sequential:
        """
        Builds a neural network.

        :param input_size: how many words are in the input layer
        :return: a compiled neural network
        """
        input_size = [input_size]
        model = Sequential()
        model.add(Dense(128, activation='relu', input_shape=input_size,
                        kernel_initializer=TruncatedNormal(mean=0.0, stddev=0.05, seed=None),
                        bias_initializer='zeros'))
        model.add(Dense(len(UtteranceType), activation='softmax',
                        kernel_initializer=TruncatedNormal(mean=0.0, stddev=0.05, seed=None),
                        bias_initializer='zeros'))

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model
