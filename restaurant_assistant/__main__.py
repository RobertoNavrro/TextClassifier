from restaurant_assistant.data_processing import data_loader
from restaurant_assistant.textclass.decision_tree_classifier import DecisionTreeClassifier
from restaurant_assistant.dialog_system.DialogSystem import DialogSystem
from restaurant_assistant.dialog_system.DialogStates import *
from restaurant_assistant.dialog_system.order import UserOrder

def main():
    data = data_loader.load_dialog_data()
    train_data, test_data = data_loader.generate_dataframes(data)
    classifier = DecisionTreeClassifier()
    classifier.initialize(train_data)
    
    print('Do you want to test the performance of the classifier? y/n')
    answer = input().lower()
    if answer == 'y':
        print('Testing performance.')
        f1_result, acc_result = classifier.test_performance(test_data)
        print(f'F1 score: {f1_result}')
        print(f'Accuracy: {acc_result}')

    print('Welcome to the text classifier.')

    order = UserOrder()
    current = InitState(order)
    
    res_data = data_loader.load_restaurant_dataset()
    while(True):
        answer = input().lower()
        utterance_type = classifier.classify(answer)
        current = current.execute(answer,utterance_type)
        if type(current) is type(EndConversation):
            break

if __name__ == "__main__":
    main()
