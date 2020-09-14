import pandas as pd
from pathlib import Path
from enum import Enum, auto
from typing import Tuple
import numpy
from sklearn.feature_extraction.text import CountVectorizer

class Column(Enum):
    label = auto()
    utterance = auto()


def load_dialog_data():
    tuppled_data = list()
    path = str(Path(__file__).parent.parent.parent.joinpath('data', 'dialogs.dat'))
    with open(path, "r") as raw_dialog_data:
        for line in raw_dialog_data:
            (label, utterance) = line.split(' ', 1)  # divides the data into two strings
            utterance = utterance[:-1]  # removes the \n character
            tuppled_data.append([label, utterance])  # creates a tupple
    return tuppled_data


def tokenize_utterance(string):
    tokens = list()
    tokens = string.split()
    return tokens

def convert_to_bow(data):
    vectorizer = CountVectorizer()
    bow = vectorizer.fit_transform(data[Column.utterance])
    bow = bow.toarray()
    return bow

def generate_dataframes(tuppled_data) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.DataFrame.from_records(tuppled_data, columns=[Column.label, Column.utterance])
    train_data, test_data = numpy.split(df, [int(0.8*len(df))])
    return train_data, test_data


if __name__ == "__main__":
    data = load_dialog_data()
    train , test = generate_dataframes(data)
