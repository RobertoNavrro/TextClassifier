import pandas as pd
from pathlib import Path
from enum import Enum, auto


class Column(Enum):
    label = auto()
    utterance = auto()


def load_dialog_data():
    tuppled_data = list()
    path = str(Path(__file__).parent.parent.parent.joinpath('data', 'dialogs.dat'))
    with open(path,"r") as raw_dialog_data:
        for line in raw_dialog_data:
            (label,utterance) = line.split(' ',1) #divides the data into two strings
            utterance = utterance[:-1] #removes the \n character
            tuppled_data.append([label, utterance]) #creates a tupple
    return tuppled_data


def generate_dataframe(tuppled_data):
    df = pd.DataFrame.from_records(tuppled_data, columns=[Column.label, Column.utterance])
    return df
