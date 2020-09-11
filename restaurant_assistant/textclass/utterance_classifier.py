from abc import ABC, abstractmethod
from enum import Enum, auto
from pandas.core.frame import DataFrame
from sklearn.metrics._classification import f1_score, accuracy_score

from restaurant_assistant.data_processing.data_loader import Column


class UtteranceType(Enum):
    """
    Enumeration containing all possible types of utterances.
    """
    ack = auto()
    affirm = auto()
    bye = auto()
    confirm = auto()
    deny = auto()
    hello = auto()
    inform = auto()
    negate = auto()
    null = auto()
    repeat = auto()
    reqalts = auto()
    reqmore = auto()
    request = auto()
    restart = auto()
    thankyou = auto()


class UtteranceClassifier(ABC):

    """
    Abstract class for the different types of utterance classifiers. Can process the
    training data and classify given strings.
    """
    def __init__(self):
        pass

    @abstractmethod
    def initialize(self, data: DataFrame):
        """
        Process training data
        """

    @abstractmethod
    def classify(self, utterance: str) -> UtteranceType:
        """
        Classify the utterance as one of the utterance types and return the type.
        """

    def test_performance(self, test_data: DataFrame):
        """
        Test the performance of the classifier on various metrics.
        """
        result = 'result'
        test_data[result] = ''
        for i in test_data.index:
            guess = self.classify(test_data.at[i, Column.utterance])
            test_data.at[i, result] = guess.name

        f1_result = f1_score(test_data[Column.label], test_data[result], average='macro',
                             labels=[x.name for x in UtteranceType], zero_division=1)
        acc_result = accuracy_score(test_data[Column.label], test_data[result])
        return f1_result, acc_result
