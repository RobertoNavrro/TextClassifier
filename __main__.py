import pandas as pd
import numpy as np
import os

def load_dialog_data():
    tuppled_data = list()
    with open("data\\dialogs.dat","r") as raw_dialog_data:
        for line in raw_dialog_data:
          
            (label,utterance) = line.split(' ',1) #divides the data into two strings
            utterance = utterance[:-1] #removes the \n character
            tuppled_data.append([label, utterance]) #creates a tupple
    return tuppled_data


def generate_dataframe(tuppled_data):
    df = pd.DataFrame.from_records(tuppled_data, columns=['label','utterance'])
    
    return df
       


if __name__ == "__main__":
    
    #print(os.getcwd())
    data = load_dialog_data()
    df = generate_dataframe(data)