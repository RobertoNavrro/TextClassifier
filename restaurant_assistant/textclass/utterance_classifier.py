from abc import ABC, abstractmethod
from enum import Enum, auto
from pandas.core.frame import DataFrame


"""
Enumeration containing all possible types of utterances.
"""
class UtteranceType(Enum):
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
