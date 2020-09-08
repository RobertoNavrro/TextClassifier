from textclass.Utterance import Utterance

def load_dialog_data():
    dialog_list = list()
    with open("D:\\Documents\\University\\UU\\MAIR\\Projects\\Text_Classifier\\data\\dialogs.dat","r") as raw_dialog_data:
        for line in raw_dialog_data:
            dialog_list.append(line)
    return dialog_list


def generate_Classes(dialog_list):
   for dialog in dialog_list:
       


if __name__ == "__main__":
    dialog_list = load_dialog_data()
    generate_Classes(dialog_list)
    
